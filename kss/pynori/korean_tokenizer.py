import gc
import os
import sys
import unicodedata

from kss.pynori.char_unicode import (
    SPACE_SEPARATOR,
    NON_SPACING_MARK,
    LINE_SEPARATOR,
    PARAGRAPH_SEPARATOR,
    CONTROL,
    FORMAT,
    DASH_PUNCTUATION,
    START_PUNCTUATION,
    END_PUNCTUATION,
    CONNECTOR_PUNCTUATION,
    OTHER_PUNCTUATION,
    MATH_SYMBOL,
    CURRENCY_SYMBOL,
    MODIFIER_SYMBOL,
    OTHER_SYMBOL,
    INITIAL_QUOTE_PUNCTUATION,
    FINAL_QUOTE_PUNCTUATION,
)
from kss.pynori.dict.connection_costs import ConnectionCosts
from kss.pynori.dict.user_dictionary import UserDictionary
from kss.pynori.dict.known_dictionary import KnownDictionary
from kss.pynori.dict.unknown_dictionary import UnknownDictionary
from kss.pynori.dict.character_definition import (
    CharacterDefinition,
    character_category_map,
)
from kss.pynori.dictionary_token import DictionaryToken
from kss.pynori.decompound_token import DecompoundToken
from kss.pynori.pos import POS
from kss.pynori.token_attribute import TokenAttribute

PATH_CUR = os.path.dirname(__file__)


class Type(object):
    """Token type reflecting the original source of this token"""

    KNOWN = "KN"
    UNKNOWN = "UKN"
    USER = "US"


class DcpdMode(object):
    """Decompound mode: this determines how the tokenizer handles"""

    NONE = "NONE"
    DISCARD = "DISCARD"
    MIXED = "MIXED"


class KoreanTokenizer(object):
    """Tokenizer for Korean text.

    KoreanTokenizer - Split input string into several tokens.

    Parameters
    ----------
    decompound_mode : {'NONE', 'DISCARD', 'MIXED'}
            this determines how the tokenizer handles common compound words, remaining the root(original) word or not.

    infl_decompound_mode : {'NONE', 'DISCARD', 'MIXED'}
            this determines how the tokenizer handles inflect compound words, remaining the root(original) word or not.

    output_unknown_unigrams : {'True', 'False'}
            true if outputs unigrams for unknown words.

    discard_punctuation : {'True', 'False'}
            true if punctuation tokens should be dropped from the output.

    Notes
    -----
    This tokenizer uses a rolling viterbi search to find
    the least cost segmentation (path) of the incoming characters.

    """

    MAX_UNKNOWN_WORD_LENGTH = 1024
    MAX_BACKTRACE_GAP = 1024

    def __init__(
        self,
        path_userdict,
        decompound_mode,
        infl_decompound_mode,
        output_unknown_unigrams,
        discard_punctuation,
    ):
        self.mode = decompound_mode
        self.infl_mode = infl_decompound_mode
        self.output_unknown_unigrams = output_unknown_unigrams
        self.discard_punctuation = discard_punctuation

        gc.disable()
        self.buffer = KoreanTokenizer.Buffer()
        self.character_definition = CharacterDefinition()
        self.user_dict = UserDictionary.open(PATH_CUR + path_userdict)
        self.unk_dict = UnknownDictionary.open(
            PATH_CUR + "/resources/mecab-ko-dic-2.1.1-20180720/unk.def"
        )
        self.kn_dict = KnownDictionary.open(
            PATH_CUR + "/resources/pkl_mecab_csv/mecab_csv.pkl"
        )
        self.conn_costs = ConnectionCosts.open(
            PATH_CUR + "/resources/pkl_mecab_matrix/matrix_def.pkl"
        )
        self.reset_state()
        gc.enable()

    @staticmethod
    def open(dicts):
        return dicts[0].open(dicts[1])

    def reset_state(self):
        self.pos = 0
        self.end = False
        self.last_backtrace_pos = 0
        self.positions = KoreanTokenizer.WrappedPositionArray()
        self.tkn_attr_obj = TokenAttribute()
        self.pending = []
        self.positions.get(0).add(0, 0, -1, -1, -1, -1, Type.KNOWN, None, None, None)

    def set_input(self, in_string, preprocessed: bool = False):
        """Load input korean string to buffer."""
        if not preprocessed:
            new_string = ""
            for ch in in_string:
                if character_category_map(ch) is None:
                    new_string += " "
                else:
                    new_string += ch
        else:
            new_string = in_string

        self.buffer.set(new_string)
        self.reset_state()

    class Buffer(object):
        """Bring the input korean text."""

        def set(self, in_string):
            self.in_string = in_string

        def get(self, pos):
            if 0 <= pos <= len(self.in_string) - 1:
                result = self.in_string[pos]
            else:
                result = -1
            return result

        def slice_get(self, start_pos, end_pos_plus1):
            return self.in_string[start_pos:end_pos_plus1]

    class Position(object):
        """Holds all back pointers arriving to this position."""

        def __init__(self):
            self.pos = 0
            self.count = 0
            self.costs = []
            self.lastRightID = []
            self.backPos = []
            self.backWordPos = []
            self.backIndex = []
            self.backID = []
            self.backDictType = []
            self.backPosType = []
            self.morphemes = []
            self.backPosTag = []

        def add(
            self,
            cost,
            lastRightID,
            backPos,
            backRPos,
            backIndex,
            backID,
            backDictType,
            backPosType,
            morphemes,
            backPosTag,
        ):
            """
            NOTE: this isn't quite a true Viterbi search,
            because we should check if lastRightID is
            already present here, and only update if the new
            cost is less than the current cost, instead of
            simply appending.  However, that will likely hurt
            performance (usually we add a lastRightID only once),
            and it means we actually create the full graph
            intersection instead of a "normal" Viterbi lattice:
            """
            self.costs.append(cost)
            self.lastRightID.append(lastRightID)
            self.backPos.append(backPos)
            self.backWordPos.append(backRPos)
            self.backIndex.append(backIndex)
            self.backID.append(backID)
            self.backDictType.append(backDictType)
            self.count += 1
            self.backPosType.append(backPosType)
            self.morphemes.append(morphemes)
            self.backPosTag.append(backPosTag)

        def reset(self):
            self.count = 0

    class WrappedPositionArray(object):
        def __init__(self):
            self.positions = []
            for _ in range(0, 4):
                self.positions.append(KoreanTokenizer.Position())

            self.nextWrite = 0
            self.nextPos = 0
            self.count = 0

        def reset(self):
            self.nextWrite -= 1
            while self.count > 0:
                if self.nextWrite == -1:
                    self.nextWrite = len(self.positions) - 1

                self.positions[self.nextWrite].reset()
                self.nextWrite -= 1
                self.count -= 1

            self.nextWrite = 0
            self.nextPos = 0
            self.count = 0

        def get(self, pos):
            while pos >= self.nextPos:
                if self.count == len(self.positions):
                    self.newPositions = []
                    for _ in range(0, 1 + self.count):
                        self.newPositions.append(KoreanTokenizer.Position())

                    self.newPositions[
                        : len(self.positions) - self.nextWrite
                    ] = self.positions[
                        self.nextWrite : len(self.positions) - self.nextWrite
                    ]
                    self.newPositions[
                        len(self.positions) - self.nextWrite : self.nextWrite
                    ] = self.positions[: self.nextWrite]
                    self.positions = self.newPositions[:]

                if self.nextWrite == len(self.positions):
                    self.nextWrite = 0

                assert self.positions[self.nextWrite].count == 0

                self.positions[self.nextWrite].pos = self.nextPos
                self.nextWrite += 1
                self.nextPos += 1
                self.count += 1

            assert self.in_bounds(pos)
            index = self.get_index(pos)
            assert self.positions[index].pos == pos

            return self.positions[index]

        def get_nextpos(self):
            return self.nextPos

        def in_bounds(self, pos):
            return self.nextPos > pos >= self.nextPos - self.count

        def get_index(self, pos):
            index = self.nextWrite - (self.nextPos - pos)
            if index < 0:
                index += len(self.positions)
            return index

    @staticmethod
    def compute_space_penalty(leftPOS, numSpaces):
        """Returns the space penalty associated with the provided POS.Tag.

        Arguments:
        ----------
        leftPOS
                the left part of speech of the current token.

        numSpaces
                the number of spaces before the current token.
        """
        spacePenalty = 0
        if numSpaces > 0:
            if leftPOS in ["JKS", "JKC", "JKG", "JKO", "JKB", "JKV", "JKQ", "JX", "JC"]:
                spacePenalty = 6000
            elif leftPOS == ["E", "J", "VCP", "XSA", "XSN", "XSV"]:
                spacePenalty = 3000
        return spacePenalty

    def add(self, trie_dict, fromPosData, wordPos, endPos, wordID, type_, dict=None):
        """Add the optimal token info to each position."""
        leftPOS = trie_dict["POS"]
        wordCost = trie_dict["word_cost"]
        leftID = trie_dict["left_id"]
        rightID = trie_dict["right_id"]
        wordID = trie_dict["surface"]
        backPosType = trie_dict["POS_type"]
        morphemes = trie_dict["morphemes"]

        leastCost = sys.maxsize
        leastIDX = -1
        assert fromPosData.count > 0

        for idx in range(0, fromPosData.count):
            numSpaces = wordPos - fromPosData.pos
            cost = (
                fromPosData.costs[idx]
                + self.conn_costs.get(fromPosData.lastRightID[idx], leftID)
                + self.compute_space_penalty(leftPOS, numSpaces)
            )

            if cost < leastCost:
                leastCost = cost
                leastIDX = idx

        leastCost += wordCost
        self.positions.get(endPos).add(
            cost=leastCost,
            lastRightID=rightID,
            backPos=fromPosData.pos,
            backRPos=wordPos,
            backIndex=leastIDX,
            backID=wordID,
            backDictType=type_,
            backPosType=backPosType,
            morphemes=morphemes,
            backPosTag=leftPOS,
        )

    def increment_token(self):
        """Excute parse() and save token info. until at the end of string.

        parse() is able to return w/o producing any new tokens,
        when the tokens it had produced were entirely punctuation.
        So we loop here until we get a real token or we end:
        """

        while len(self.pending) == 0:

            if self.end:
                return False

            self.parse()

        token = self.pending.pop()
        length = token.getLength()
        assert length > 0

        self.tkn_attr_obj.termAtt.append(token.getSurfaceFormString())
        self.tkn_attr_obj.offsetAtt.append(
            (token.getStartOffset(), token.getEndOffset())
        )
        self.tkn_attr_obj.posLengthAtt.append(token.getPositionLength())
        self.tkn_attr_obj.posTypeAtt.append(token.getPOSType())
        self.tkn_attr_obj.posTagAtt.append(token.getPOSTag())
        self.tkn_attr_obj.dictTypeAtt.append(token.getDictType())
        return True

    def parse(self):
        """While move from start to end of input string in character unit, find the optimal path.

            Incrementally parse some more characters.  This runs
        the viterbi search forwards "enough" so that we
        generate some more tokens.  How much forward depends on
        the chars coming in, since some chars could cause
        longer-lasting ambiguity in the parsing.  Once the
        ambiguity is resolved, then we back trace, produce
        the pending tokens, and return
        """

        unknownWordEndIndex = -1
        userWordMaxPosAhead = -1
        while True:
            if self.buffer.get(self.pos) == -1:
                break

            posData = self.positions.get(self.pos)
            isFrontier = self.positions.get_nextpos() == self.pos + 1

            if posData.count == 0:
                self.pos += 1
                continue

            if self.pos > self.last_backtrace_pos and posData.count == 1 and isFrontier:
                self.backtrace(posData, 0)

                posData.costs[0] = 0
                if len(self.pending) > 0:
                    return

            if ord(self.buffer.get(self.pos)) in SPACE_SEPARATOR:
                self.pos += 1
                nextChar = self.buffer.get(self.pos)

                while nextChar != -1 and ord(nextChar) in SPACE_SEPARATOR:
                    self.pos += 1
                    nextChar = self.buffer.get(self.pos)

            if self.buffer.get(self.pos) == -1:
                self.pos = posData.pos

            anyMatches = False

            if self.user_dict is not None:
                maxPosAhead = 0
                posAhead = self.pos

                while True:
                    ch = self.buffer.get(posAhead)
                    if ch == -1:
                        break
                    userIdRef = self.user_dict.userTrie[
                        self.buffer.slice_get(self.pos, posAhead + 1)
                    ]
                    if userIdRef is not None:
                        maxPosAhead = posAhead
                        lastResult = userIdRef.result[0]
                        anyMatches = True
                    posAhead += 1

                if anyMatches and maxPosAhead > userWordMaxPosAhead:
                    self.add(
                        lastResult, posData, self.pos, maxPosAhead + 1, None, Type.USER
                    )
                    userWordMaxPosAhead = max(userWordMaxPosAhead, maxPosAhead)

            if not anyMatches:
                posAhead = self.pos

                a = 1
                while True:
                    ch = self.buffer.get(posAhead)
                    if ch == -1:
                        break
                    a += 1
                    wordIdRef = self.kn_dict.sysTrie[
                        self.buffer.slice_get(self.pos, posAhead + 1)
                    ]

                    if wordIdRef is not None:
                        for each in wordIdRef.result:
                            self.add(
                                each, posData, self.pos, posAhead + 1, None, Type.KNOWN
                            )
                            anyMatches = True

                    posAhead += 1
            if unknownWordEndIndex > posData.pos:
                self.pos += 1
                continue

            firstCharacter = self.buffer.get(self.pos)
            if anyMatches is False or self.character_definition.isInvoke(
                firstCharacter
            ):
                characterId = self.character_definition.getCharacterClass(
                    firstCharacter
                )
                if self.character_definition.isGroup(firstCharacter) is False:
                    unknownWordLength = 1
                else:
                    unknownWordLength = 1
                    scriptCode = unicodedata.category(firstCharacter)
                    isPunct = self.is_punctuation(firstCharacter)
                    posAhead = self.pos + 1

                    while True:
                        next_ch = self.buffer.get(posAhead)

                        if next_ch == -1:
                            break

                        next_hex_ch = ord(next_ch)
                        next_scriptCode = unicodedata.category(next_ch)

                        if unknownWordLength == self.MAX_UNKNOWN_WORD_LENGTH:
                            break

                        sameScript = (scriptCode == next_scriptCode) or (
                            next_hex_ch in NON_SPACING_MARK
                        )
                        if (
                            sameScript
                            and isPunct == self.is_punctuation(next_ch)
                            and self.character_definition.isGroup(next_ch)
                        ):
                            unknownWordLength += 1
                        else:
                            break

                        posAhead += 1

                wordIdRef = self.unk_dict.unkTrie[characterId]
                wordIdRef = wordIdRef.result[0]
                self.add(
                    wordIdRef,
                    posData,
                    self.pos,
                    self.pos + unknownWordLength,
                    None,
                    Type.UNKNOWN,
                )

            self.pos += 1
        self.end = True

        if self.pos > 0:
            endPosData = self.positions.get(self.pos)
            leastCost = sys.maxsize
            leastIDX = -1

            for idx in range(0, endPosData.count):
                cost = endPosData.costs[idx] + self.conn_costs.get(
                    endPosData.lastRightID[idx], 0
                )

                if cost < leastCost:
                    leastCost = cost
                    leastIDX = idx

            self.backtrace(endPosData, leastIDX)

    def backtrace(self, endPosData, fromIDX):
        """Add tokens in the optimal path to the pending list while backtrace positions of input string.

        the pending list.  The pending list is then in-reverse
        (last token should be returned first).
        """

        endPos = endPosData.pos
        pos = endPos
        bestIDX = fromIDX

        while pos > self.last_backtrace_pos:

            posData = self.positions.get(pos)
            assert bestIDX < posData.count

            backPos = posData.backPos[bestIDX]
            backWordPos = posData.backWordPos[bestIDX]
            assert backPos >= self.last_backtrace_pos

            length = pos - backWordPos
            backDictType = posData.backDictType[bestIDX]
            nextBestIDX = posData.backIndex[bestIDX]

            fragment = self.buffer.slice_get(backWordPos, backWordPos + length)
            backPosType = posData.backPosType[bestIDX]
            morphemes = posData.morphemes[bestIDX]
            backPosTag = posData.backPosTag[bestIDX]

            fragmentOffset = backWordPos - self.last_backtrace_pos
            assert fragmentOffset >= 0

            if self.output_unknown_unigrams and backDictType == Type.UNKNOWN:
                for i in range(length - 1, -1, -1):
                    charLen = 1
                    token = DictionaryToken(
                        dictType=Type.UNKNOWN,
                        dictionary=None,
                        wordId=None,
                        surfaceForm=fragment[i],
                        offset=fragmentOffset + i,
                        length=charLen,
                        startOffset=backWordPos + i,
                        endOffset=backWordPos + i + charLen,
                        posType=backPosType,
                        morphemes=morphemes,
                        posTag=backPosTag,
                    )
                    self.pending.append(token)
            else:
                token = DictionaryToken(
                    dictType=backDictType,
                    dictionary=None,
                    wordId=None,
                    surfaceForm=fragment,
                    offset=fragmentOffset,
                    length=length,
                    startOffset=backWordPos,
                    endOffset=backWordPos + length,
                    posType=backPosType,
                    morphemes=morphemes,
                    posTag=backPosTag,
                )

                if (
                    token.getPOSType() == POS.Type.MORPHEME
                    or (
                        token.getPOSType() != POS.Type.INFLECT
                        and self.mode == DcpdMode.NONE
                    )
                    or (
                        token.getPOSType() == POS.Type.INFLECT
                        and self.infl_mode == DcpdMode.NONE
                    )
                ):

                    if not self.should_filter_token(token):
                        self.pending.append(token)

                if (
                    token.getPOSType() != POS.Type.MORPHEME
                    and (
                        token.getPOSType() != POS.Type.INFLECT
                        and self.mode != DcpdMode.NONE
                    )
                    or (
                        token.getPOSType() == POS.Type.INFLECT
                        and self.infl_mode != DcpdMode.NONE
                    )
                ):

                    morphemes = token.getMorphemes()
                    if morphemes is None:
                        self.pending.append(token)

                    else:
                        endOffset = backWordPos + length
                        posLen = 0

                        for i in range(len(morphemes) - 1, -1, -1):
                            morpheme = morphemes[i]

                            if token.getPOSType() == POS.Type.COMPOUND:
                                assert endOffset - len(morpheme.surfaceForm) >= 0
                                compoundToken = DecompoundToken(
                                    posTag=morpheme.posTag,
                                    surfaceForm=morpheme.surfaceForm,
                                    startOffset=endOffset - len(morpheme.surfaceForm),
                                    endOffset=endOffset,
                                    posType=POS.Type.MORPHEME,
                                    dictType=backDictType,
                                )
                            else:
                                compoundToken = DecompoundToken(
                                    posTag=morpheme.posTag,
                                    surfaceForm=morpheme.surfaceForm,
                                    startOffset=token.getStartOffset(),
                                    endOffset=token.getEndOffset(),
                                    posType=POS.Type.MORPHEME,
                                    dictType=backDictType,
                                )

                            if i == 0 and (
                                self.mode == DcpdMode.MIXED
                                or self.infl_mode == DcpdMode.MIXED
                            ):
                                compoundToken.setPositionIncrement(0)

                            posLen += 1
                            endOffset -= len(morpheme.surfaceForm)
                            self.pending.append(compoundToken)

                        if (
                            token.getPOSType() != POS.Type.INFLECT
                            and self.mode == DcpdMode.MIXED
                        ) or (
                            token.getPOSType() == POS.Type.INFLECT
                            and self.infl_mode == DcpdMode.MIXED
                        ):
                            token.setPositionLength(max(1, posLen))
                            self.pending.append(token)

            if self.discard_punctuation is False and backWordPos != backPos:
                offset = backPos - self.last_backtrace_pos
                len_ = backWordPos - backPos
                wordIdRef = self.unk_dict.unkTrie["SPACE"]
                wordIdRef = wordIdRef.result[0]
                spaceToken = DictionaryToken(
                    dictType=Type.UNKNOWN,
                    dictionary=None,
                    wordId=None,
                    surfaceForm=" ",
                    offset=offset,
                    length=len_,
                    startOffset=backPos,
                    endOffset=backPos + len_,
                    posType=POS.Type.MORPHEME,
                    morphemes=None,
                    posTag=wordIdRef["POS"],
                )
                self.pending.append(spaceToken)

            pos = backPos
            bestIDX = nextBestIDX

        self.last_backtrace_pos = endPos

    def get_dict(self, type):
        if type == Type.USER:
            return self.user_dict
        elif type == Type.KNOWN:
            return self.kn_dict
        elif type == Type.UNKNOWN:
            return self.unk_dict

    def should_filter_token(self, token):
        """Delete token, where the characters are 'all' punctuation."""
        is_punct = True
        for ch in token.getSurfaceForm():
            if not self.is_punctuation(ch):
                is_punct = False
                return self.discard_punctuation and is_punct
        return self.discard_punctuation and is_punct

    def is_punctuation(self, ch):
        hex_ch = ord(ch)
        if hex_ch == 0x318D:  # 'ㆍ'
            return True
        if (
            hex_ch in SPACE_SEPARATOR
            or hex_ch in LINE_SEPARATOR
            or hex_ch in PARAGRAPH_SEPARATOR
            or hex_ch in CONTROL
            or hex_ch in FORMAT
            or hex_ch in DASH_PUNCTUATION
            or hex_ch in START_PUNCTUATION
            or hex_ch in END_PUNCTUATION
            or hex_ch in CONNECTOR_PUNCTUATION
            or hex_ch in OTHER_PUNCTUATION
            or hex_ch in MATH_SYMBOL
            or hex_ch in CURRENCY_SYMBOL
            or hex_ch in MODIFIER_SYMBOL
            or hex_ch in OTHER_SYMBOL
            or hex_ch in INITIAL_QUOTE_PUNCTUATION
            or hex_ch in FINAL_QUOTE_PUNCTUATION
        ):
            return True
        return False

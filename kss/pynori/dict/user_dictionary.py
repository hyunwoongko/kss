from kss.pynori.dict.dictionary import Dictionary
from kss.pynori.dict.character_definition import CharacterDefinition
from kss.pynori.dict.trie import Trie
from kss.pynori.pos import POS


class UserDictionary(Dictionary):
    """Build User Dictionary"""

    WORD_COST = -100000
    LEFT_ID = 1781  # NNG left
    RIGHT_ID = 3533  # NNG right
    RIGHT_ID_T = 3535  # NNG right with hangul and a coda on the last char
    RIGHT_ID_F = 3534  # NNG right with hangul and no coda on the last char
    USER_POS = "NNG"

    @staticmethod
    def open(USER_PATH):
        entries = []
        with open(USER_PATH, "r", encoding="UTF8") as rf:
            for line in rf:
                line = line.strip()
                if len(line) == 0:
                    continue
                if line[:2] == "# ":  # 주석 line (#+공백)
                    continue
                entries.append(line)
        if len(entries) == 0:
            return None
        else:
            return UserDictionary(entries)

    def __init__(self, entries):
        char_def = CharacterDefinition()
        entries = sorted(entries, reverse=True)
        self.userTrie = Trie()
        last_token = ""

        for entry in entries:
            splits = entry.split()
            token = splits[0]

            if token == last_token:
                continue

            last_char = list(entry)[0]
            if char_def.isHangul(last_char):
                if char_def.hasCoda(last_char):
                    right_id = self.RIGHT_ID_T
                else:
                    right_id = self.RIGHT_ID_F
            else:
                right_id = self.RIGHT_ID
            if len(splits) == 1:
                pass
            else:
                length = []
                offset = 0
                for i in range(1, len(splits)):
                    length.append(len(splits[i]))
                    offset += len(splits[i])
                if offset > len(token):
                    raise Exception(
                        f"Illegal user dictionary entry '{entry}' - the segmentation is bigger than the surface form ({token}) "
                    )
            # add mapping to Trie (similar to FST)
            morph_inf = dict()
            morph_inf["surface"] = token
            morph_inf["left_id"] = self.LEFT_ID
            morph_inf["right_id"] = right_id
            morph_inf["word_cost"] = int(self.WORD_COST)
            morph_inf["POS"] = self.USER_POS

            if len(splits) == 1:
                morph_inf["POS_type"] = POS.Type.MORPHEME
                morph_inf["morphemes"] = None
                self.userTrie[token] = morph_inf
            else:
                morph_inf["POS_type"] = POS.Type.COMPOUND
                morphemes_list = []
                for subword in splits[1:]:
                    morphemes_list.append(
                        Dictionary.Morpheme(posTag=self.USER_POS, surfaceForm=subword)
                    )
                morph_inf["morphemes"] = morphemes_list
                self.userTrie[token] = morph_inf

            last_token = token

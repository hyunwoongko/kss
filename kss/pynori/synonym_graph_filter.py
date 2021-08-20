import os
from kss.pynori.dict.trie import Trie
from kss.pynori.token_attribute import TokenAttribute

PATH_CUR = os.path.dirname(__file__)


class SynMode(object):
    """Synonym mode to select synonyms"""

    NORM = "NORM"  # select representative synonym token
    EXT = "EXTENSION"  # select all synonym tokens


class SynonymGraphFilter(object):
    """Synonym Text Processing

    Add synonym words to token stream / or Norm synonmy words
    keeping token offsets.

    Parameters
    ----------
    kor_tokenizer

    mode_synonym : {'EXTENSION', 'NORM'}

    동의어 필터링 특징
     - Decompound 모드(MIXED, DISCARD, NONE)에 상관없이 동작

    """

    def __init__(self, kor_tokenizer, mode_synonym):
        self.SEP_CHAR = "_"  # separate charcter in token
        self.kor_tokenizer = (
            kor_tokenizer  # korean_analyzer.py 에서 decompound mode가 이미 결정
        )
        self.mode_synonym = mode_synonym
        self.syn_trie = None
        self.synonym_build(PATH_CUR + "/resources/synonyms.txt")
        pass

    def _simple_tokenizer(self, in_string):
        # Tokenizing
        self.kor_tokenizer.set_input(in_string)
        while self.kor_tokenizer.increment_token():
            pass
        return self.kor_tokenizer.tkn_attr_obj

    def synonym_build(self, path_syn_file):
        entries = []
        with open(path_syn_file, "r", encoding="utf-8") as rf:
            for line in rf:
                line = line.strip()
                if len(line) == 0:
                    continue
                if line[:2] == "# ":
                    continue
                entries.append(line)

        self.syn_trie = Trie()
        for line in entries:
            tkn_attr_obj_list = []
            for token in line.split(","):
                tkn_attr_obj_list.append(self._simple_tokenizer(token))

            if self.mode_synonym == SynMode.EXT:
                trie_result = tkn_attr_obj_list
            elif self.mode_synonym == SynMode.NORM:
                trie_result = [tkn_attr_obj_list[0]]

            for tkn_attr_obj in tkn_attr_obj_list:
                self.syn_trie[self.SEP_CHAR.join(tkn_attr_obj.termAtt)] = trie_result

    def _set_token_attribute(self, source, target, idx):
        for name, _ in target.__dict__.items():
            target.__dict__[name].append(source.__dict__[name][idx])
        return target

    def do_filter(self, tkn_attrs):
        new_tkn_attrs = TokenAttribute()
        token_list = tkn_attrs.termAtt
        step = 0

        for m, _ in enumerate(token_list):
            if m < step:
                continue

            token = token_list[step]
            for n in range(m, len(token_list)):
                node = self.syn_trie[token]
                tkn = node is None

                if tkn is False and node is None:  # [A]
                    if len(token.split(self.SEP_CHAR)) == 1:
                        new_tkn_attrs = self._set_token_attribute(
                            tkn_attrs, new_tkn_attrs, n
                        )
                        step = n + 1
                        break
                    else:
                        new_tkn_attrs = self._set_token_attribute(
                            tkn_attrs, new_tkn_attrs, n - 1
                        )
                        step = n
                        break

                if tkn is True and node is None:  # [B]
                    if n == len(token_list) - 1:
                        new_tkn_attrs = self._set_token_attribute(
                            tkn_attrs, new_tkn_attrs, n
                        )
                    else:
                        token += self.SEP_CHAR
                        token += token_list[n + 1]
                        continue

                if tkn is True and node is not None:
                    for trie_tkn_attrs in node.result[0]:
                        for k, _ in enumerate(trie_tkn_attrs.termAtt):
                            new_tkn_attrs = self._set_token_attribute(
                                trie_tkn_attrs, new_tkn_attrs, k
                            )
                    step = n + 1
                    break

        return new_tkn_attrs

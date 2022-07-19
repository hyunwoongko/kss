from kss.pynori.dict.dictionary import Dictionary
from kss.pynori.dict.trie import Trie
from kss.pynori.pos import POS


class UnknownDictionary(Dictionary):
    """Build Unknown Dictionary

    Loaded words will be used as unknown tokens.
    """

    @staticmethod
    def open(UNK_PATH):
        entries = []
        with open(UNK_PATH, "r", encoding="UTF8") as rf:
            for line in rf:
                line = line.strip()
                if len(line) == 0:
                    continue
                entries.append(line)
        if len(entries) == 0:
            return None
        else:
            return UnknownDictionary(entries)

    def __init__(self, entries):
        super().__init__()
        entries = sorted(entries)
        self.unkTrie = Trie()

        for entry in entries:
            splits = entry.split(",")
            morph_inf = dict()
            morph_inf["surface"] = splits[0]
            morph_inf["left_id"] = splits[1]
            morph_inf["right_id"] = splits[2]
            morph_inf["word_cost"] = int(splits[3])
            morph_inf["POS"] = splits[4]
            morph_inf["POS_type"] = POS.Type.MORPHEME
            morph_inf["morphemes"] = None
            self.unkTrie[splits[0]] = morph_inf

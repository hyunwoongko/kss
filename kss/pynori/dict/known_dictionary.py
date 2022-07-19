import gzip
import pickle

from kss.pynori.dict.trie import Trie

from kss.pynori.dict.dictionary import Dictionary


class KnownDictionary(Dictionary):
    """Buid Known Dictionary (or System Dictionary)

    Load korean words from mecab-ko-dic
    Loaded words will be used as system words
    """

    @staticmethod
    def open(KNOWN_PATH):
        with gzip.open(KNOWN_PATH, "rb") as rf:
            entries = pickle.load(rf)

        if len(entries) == 0:
            return None
        else:
            return KnownDictionary(entries)

    def __init__(self, entries):
        super().__init__()
        self.sysTrie = Trie()

        for token, morph_inf in entries:
            if morph_inf["morphemes"] is not None:
                morphemes_list = []
                for subpos, subword in morph_inf["morphemes"]:
                    morphemes_list.append(
                        Dictionary.Morpheme(
                            posTag=subpos,
                            surfaceForm=subword,
                        )
                    )
                morph_inf["morphemes"] = morphemes_list
            self.sysTrie[token] = morph_inf

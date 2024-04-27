# This was copied from KoEDA [https://github.com/toriving/KoEDA]
# And modified by Hyunwoong Ko [https://github.com/hyunwoongko]

import random
from itertools import repeat, chain
from typing import Union, List

from kss._modules.morphemes.split_morphemes import split_morphemes
from kss._modules.augmentation.utils import get_synonyms
from kss._modules.augmentation.distance import hangul_levenshtein


class SynonymReplacement:
    def __init__(self, backend):
        self.backend = backend

    def __call__(self, *args, **kwargs):
        return self.synonym_replacement(*args, **kwargs)

    def synonym_replacement(
        self, data: Union[List[str], str], p: float = 0.1, repetition: int = 1, verbose: bool = False
    ) -> Union[List[str], str]:
        if isinstance(data, str):
            if repetition <= 1:
                return self._replacement(data, p, verbose)
            else:
                return list(
                    map(
                        self._replacement,
                        repeat(data, repetition),
                        repeat(p, repetition),
                        repeat(verbose, repetition),
                    )
                )
        elif isinstance(data, list):
            if repetition <= 1:
                return list(map(self._replacement, data, repeat(p, len(data)), repeat(verbose, len(data))))
            else:
                return list(
                    map(
                        self._replacement,
                        chain.from_iterable(repeat(x, repetition) for x in data),
                        repeat(p, len(data) * repetition),
                        repeat(verbose, len(data) * repetition),
                    )
                )
        else:
            raise TypeError(f"Does not support the data type : {type(data)}")

    def _replacement(self, data: str, p: float = 0.1, verbose: bool=False) -> str:
        words = split_morphemes(data, backend=self.backend, drop_space=False)
        n = max(0, int(len(words) * p))

        random_word_list = list(set([
            word for word, pos in words
            if pos.startswith("N") and len(word) > 1
        ]))

        random.shuffle(random_word_list)
        num_replaced = 0
        old2new = {}
        for random_word in random_word_list:
            synonyms = get_synonyms(random_word, min_length=2)

            if len(synonyms) >= 1:
                synonym2distance = {}
                for synonym in synonyms:
                    distance = hangul_levenshtein(synonym, random_word)
                    synonym2distance[synonym] = distance

                closet_synonym = min(synonym2distance, key=synonym2distance.get)
                closet_synonym_distance = synonym2distance[closet_synonym]
                if closet_synonym_distance > 0.5:
                    continue
                for word, pos in words:
                    if word == random_word:
                        old2new[word] = closet_synonym
                        break
                num_replaced += 1
            if num_replaced >= n:
                break

        finalized_words = []
        verbose_dict = {}

        for i, (word, pos) in enumerate(words):
            if word in old2new and pos.startswith("N"):
                finalized_words.append(old2new[word])
                verbose_dict[word] = old2new[word]
            else:
                finalized_words.append(word)

        if verbose:
            for word, replaced_word in verbose_dict.items():
                print(f"{word} -> {replaced_word}")

        return "".join(finalized_words)

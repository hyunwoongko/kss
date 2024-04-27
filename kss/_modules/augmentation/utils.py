# This was copied from KoEDA [https://github.com/toriving/KoEDA]
# And modified by Hyunwoong Ko [https://github.com/hyunwoongko]

import json
import os

from kss._modules.morphemes.split_morphemes import split_morphemes
from kss._modules.josa.josa import select_josa

WORDNET_JSON_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets/wordnet.json"
)

with open(WORDNET_JSON_PATH, "r", encoding="utf-8") as f:
    WORDNET = json.load(f)


def get_synonyms(word, min_length=None):
    synonyms = set()
    synsets = WORDNET["lemmas"].get(word, None)

    if synsets is None:
        return []

    for syn in synsets:
        synonym = WORDNET["synsets"][syn]["lemmas"]
        if min_length is not None:
            synonym = [s for s in synonym if len(s) >= min_length]
        synonyms.update(synonym)

    if word in synonyms:
        synonyms.remove(word)

    return list(synonyms)


def correct_josa(text: str):
    morphemes = split_morphemes(text, drop_space=False)
    outputs = []
    previous = None
    for i, (word, pos) in enumerate(morphemes):
        if pos.startswith("J") and previous is not None:
            if not previous[1].startswith("S"):
                outputs.append(select_josa(previous[0], word))
            else:
                outputs.append(word)
        else:
            outputs.append(word)
        previous = (word, pos)
    return "".join(outputs)

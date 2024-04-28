# Copyright (C) 2021 Hyunwoong Ko <kevin.brain@kakaobrain.com> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.

from kss._modules.augmentation.augment import augment
from kss._modules.collocation.collocate import collocate
from kss._modules.g2p.g2p import g2p
from kss._modules.hangulization.hangulization import hangulize
from kss._modules.hanja._hanja import split_hanja, is_hanja, hanja2hangul
from kss._modules.jamo._jamo import h2j, h2hcj, j2h, j2hcj, hcj2h, hcj2j, is_jamo, is_jamo_modern, is_hcj, \
    is_hcj_modern, is_hangul_char
from kss._modules.josa.josa import select_josa, combine_josa
from kss._modules.keywords.extract_keywords import extract_keywords
from kss._modules.morphemes.split_morphemes import split_morphemes
from kss._modules.paradigm.paradigm import paradigm
from kss._modules.preprocessing.anonymize import anonymize
from kss._modules.preprocessing.clean_news import clean_news
from kss._modules.preprocessing.completed_form import is_completed_form, get_all_completed_form_hangul_chars, \
    get_all_incompleted_form_hangul_chars
from kss._modules.preprocessing.filter_out import filter_out
from kss._modules.preprocessing.half2full import half2full
from kss._modules.preprocessing.normalize import normalize
from kss._modules.preprocessing.preprocess import preprocess
from kss._modules.preprocessing.reduce_repeats import reduce_char_repeats, reduce_emoticon_repeats
from kss._modules.preprocessing.remove_invisible_chars import remove_invisible_chars
from kss._modules.qwerty.qwerty import qwerty
from kss._modules.romanization.romanize import romanize
from kss._modules.safety.check_safety import is_unsafe
from kss._modules.sentences.split_sentences import split_sentences
from kss._modules.spacing.correct_spacing import correct_spacing
from kss._modules.summarization.summarize_sentences import summarize_sentences

supported_modules = {
    "augment": augment,
    "collocate": collocate,
    "g2p": g2p,
    "hangulize": hangulize,
    "split_hanja": split_hanja,
    "is_hanja": is_hanja,
    "hanja2hangul": hanja2hangul,
    "h2j": h2j,
    "h2hcj": h2hcj,
    "j2h": j2h,
    "j2hcj": j2hcj,
    "hcj2h": hcj2h,
    "hcj2j": hcj2j,
    "is_jamo": is_jamo,
    "is_jamo_modern": is_jamo_modern,
    "is_hcj": is_hcj,
    "is_hcj_modern": is_hcj_modern,
    "is_hangul_char": is_hangul_char,
    "select_josa": select_josa,
    "combine_josa": combine_josa,
    "extract_keywords": extract_keywords,
    "split_morphemes": split_morphemes,
    "paradigm": paradigm,
    "anonymize": anonymize,
    "clean_news": clean_news,
    "is_completed_form": is_completed_form,
    "get_all_completed_form_hangul_chars": get_all_completed_form_hangul_chars,
    "get_all_incompleted_form_hangul_chars": get_all_incompleted_form_hangul_chars,
    "filter_out": filter_out,
    "half2full": half2full,
    "reduce_char_repeats": reduce_char_repeats,
    "reduce_emoticon_repeats": reduce_emoticon_repeats,
    "remove_invisible_chars": remove_invisible_chars,
    "normalize": normalize,
    "preprocess": preprocess,
    "qwerty": qwerty,
    "romanize": romanize,
    "is_unsafe": is_unsafe,
    "split_sentences": split_sentences,
    "correct_spacing": correct_spacing,
    "summarize_sentences": summarize_sentences,
}

alias = {
    "aug": "augment",
    "augmentation": "augment",
    "collocation": "collocate",
    "hangulization": "hangulize",
    "hangulisation": "hangulize",
    "hangulise": "hangulize",
    "hanja": "hanja2hangul",
    "hangul2jamo": "h2j",
    "hangul2hcj": "h2hcj",
    "jamo2hangul": "j2h",
    "jamo2hcj": "j2hcj",
    "hcj2hangul": "hcj2h",
    "hcj2jamo": "hcj2j",
    "josa": "select_josa",
    "keyword": "extract_keywords",
    "keywords": "extract_keywords",
    "morpheme": "split_morphemes",
    "morphemes": "split_morphemes",
    "annonymization": "anonymize",
    "news_cleaning": "clean_news",
    "news": "clean_news",
    "completed_form": "is_completed_form",
    "completed": "is_completed_form",
    "filter": "filter_out",
    "reduce_repeats": "reduce_char_repeats",
    "reduce_char": "reduce_char_repeats",
    "reduce_emoticon": "reduce_emoticon_repeats",
    "remove_invisible": "remove_invisible_chars",
    "invisible": "remove_invisible_chars",
    "normalization": "normalize",
    "normalisation": "normalize",
    "normalise": "normalize",
    "preprocessing": "preprocess",
    "prep": "preprocess",
    "romanization": "romanize",
    "romanisation": "romanize",
    "romanise": "romanize",
    "safety": "is_unsafe",
    "check_safety": "is_unsafe",
    "sentence": "split_sentences",
    "sentences": "split_sentences",
    "sent_split": "split_sentences",
    "sent_splits": "split_sentences",
    "spacing": "correct_spacing",
    "space": "correct_spacing",
    "spaces": "correct_spacing",
    "summarization": "summarize_sentences",
    "summarize": "summarize_sentences",
    "summ": "summarize_sentences",
}


class Kss(object):
    def __init__(self, module: str):
        self.module = self._check_module(module, supported_modules, alias)

    def __call__(self, *args, **kwargs):
        return self.module(*args, **kwargs)

    def help(self):
        print(self.module.__doc__.strip())

    @staticmethod
    def available():
        return list(supported_modules.keys())

    def _check_module(self, module: str, supported_modules, alias):
        from kss._utils.sanity_checks import _check_type

        module = module.lower()
        module = _check_type(module, "module", str)

        if module in supported_modules:
            return supported_modules[module]

        elif module in alias:
            return supported_modules[alias[module]]

        else:
            error_message = f"'{module}' is not supported module." \
                            f"\nSupported modules are the following:" \
                            f"\n{list(supported_modules.keys())}"
            closest_module = self._find_closest_module(module)
            if closest_module:
                if closest_module in alias:
                    closest_module = alias[closest_module]
                error_message += f"\n\nDid you mean '{closest_module}'?"
            raise ValueError(error_message)

    @staticmethod
    def _find_closest_module(module, min_distance=0.5):
        import distance
        current_min_distance = 99
        closest_module = None
        for supported_module in list(supported_modules.keys()) + list(alias.keys()):
            dist = distance.nlevenshtein(module, supported_module)
            if dist < current_min_distance and dist <= min_distance:
                current_min_distance = dist
                closest_module = supported_module

        if closest_module is None:
            return None
        else:
            return closest_module


__ALL__ = list(supported_modules.keys()) + ["Kss"]
__version__ = "6.0.1"

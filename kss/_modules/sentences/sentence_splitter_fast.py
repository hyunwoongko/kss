# Copyright (C) 2021 Hyunwoong Ko <kevin.brain@kakaobrain.com> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.

from collections import defaultdict

from kss._modules.morphemes.analyzers import Analyzer, CharacterAnalyzer
from kss._modules.sentences.sentence_postprocessor import SentencePostprocessor
from kss._modules.sentences.sentence_preprocessor import SentencePreprocessor
from kss._utils import const


class ID(object):
    NONE: int = 0
    PREV: int = 1 << 0
    CONT: int = 1 << 1
    NEXT: int = 1 << 2
    NEXT1: int = 1 << 3
    NEXT2: int = 1 << 4


class Stats(object):
    DEFAULT: int = 0
    DA: int = 1
    YO: int = 2
    JYO: int = 3
    SB: int = 4
    COMMON: int = 5


def create_dict(d, default=0):
    return defaultdict(lambda: default, d)


Table = create_dict(
    {
        Stats.DA: create_dict(
            {
                "갔": ID.PREV,
                "간": ID.PREV,
                "겠": ID.PREV,
                "겼": ID.PREV,
                "같": ID.PREV,
                "놨": ID.PREV,
                "녔": ID.PREV,
                "니": ID.PREV,
                "논": ID.PREV,
                "낸": ID.PREV,
                "냈": ID.PREV,
                "뒀": ID.PREV,
                "때": ID.PREV,
                "랐": ID.PREV,
                "럽": ID.PREV,
                "렵": ID.PREV,
                "렸": ID.PREV,
                "뤘": ID.PREV,
                "린": ID.PREV,
                "몄": ID.PREV,
                "밌": ID.PREV,
                "볐": ID.PREV,
                "볍": ID.PREV,
                "봤": ID.PREV,
                "섰": ID.PREV,
                "샜": ID.PREV,
                "셨": ID.PREV,
                "싼": ID.PREV,
                "싸": ID.PREV,
                "않": ID.PREV,
                "았": ID.PREV,
                "없": ID.PREV,
                "었": ID.PREV,
                "였": ID.PREV,
                "온": ID.PREV,
                "웠": ID.PREV,
                "이": ID.PREV,
                "인": ID.PREV,
                "있": ID.PREV,
                "진": ID.PREV,
                "졌": ID.PREV,
                "쳤": ID.PREV,
                "췄": ID.PREV,
                "챘": ID.PREV,
                "켰": ID.PREV,
                "켠": ID.PREV,
                "캔": ID.PREV,
                "팠": ID.PREV,
                "펐": ID.PREV,
                "폈": ID.PREV,
                "했": ID.PREV,
                "혔": ID.PREV,
                "한": ID.NEXT,
                "가": ID.NEXT,
                "고": ID.NEXT | ID.NEXT2,
                "는": ID.NEXT | ID.NEXT2,
                "라": ID.NEXT,
                "시": ID.NEXT,
                "던": ID.NEXT,
                "든": ID.NEXT,
                "지": ID.NEXT2,
                "를": ID.NEXT,
                "운": ID.NEXT,  # ~ 다운
                "만": ID.NEXT,  # ~ 하다만
                "며": ID.NEXT | ID.NEXT2,
                "면": ID.NEXT | ID.NEXT1 | ID.NEXT2,
                "서": ID.PREV | ID.NEXT2,
                "싶": ID.PREV | ID.NEXT,
                "죠": ID.NEXT,
                "죵": ID.NEXT,
                "쥬": ID.NEXT,
                "하": ID.NEXT1,
                "해": ID.NEXT1,
                "도": ID.NEXT2,
                "": ID.NONE,
            }
        ),
        Stats.YO: create_dict(
            {
                "겨": ID.PREV,
                "거": ID.PREV,
                "구": ID.PREV,
                "군": ID.PREV,
                "걸": ID.PREV,
                "까": ID.PREV,
                "께": ID.PREV,
                "껴": ID.PREV,
                "네": ID.PREV,
                "나": ID.PREV,
                "니": ID.PREV,
                "데": ID.PREV,
                "든": ID.PREV,
                "려": ID.PREV,
                "서": ID.PREV,
                "세": ID.PREV,
                "아": ID.PREV,
                "어": ID.PREV,
                "워": ID.PREV,
                "에": ID.PREV,
                "예": ID.PREV,
                "을": ID.PREV,
                "져": ID.PREV,
                "줘": ID.PREV,
                "지": ID.PREV,
                "춰": ID.PREV,
                "해": ID.PREV,
                "먼": ID.PREV,
                "만": ID.PREV,
                "고": ID.NEXT2,
                "는": ID.NEXT,
                "라": ID.NEXT1,
                "를": ID.NEXT,
                "즘": ID.NEXT,
                "소": ID.NEXT,
                "며": ID.NEXT2,
                "면": ID.PREV | ID.NEXT2,
                "하": ID.NEXT1,
                "": ID.NONE,
            }
        ),
        Stats.JYO: create_dict(
            {
                "거": ID.PREV,
                "가": ID.PREV,
                "갔": ID.PREV,
                "겠": ID.PREV,
                "같": ID.PREV,
                "놨": ID.PREV,
                "녔": ID.PREV,
                "냈": ID.PREV,
                "니": ID.PREV,
                "뒀": ID.PREV,
                "르": ID.PREV,
                "랐": ID.PREV,
                "럽": ID.PREV,
                "렵": ID.PREV,
                "렸": ID.PREV,
                "맞": ID.PREV,
                "몄": ID.PREV,
                "밌": ID.PREV,
                "볐": ID.PREV,
                "볍": ID.PREV,
                "봤": ID.PREV,
                "서": ID.PREV,
                "섰": ID.PREV,
                "셨": ID.PREV,
                "샜": ID.PREV,
                "았": ID.PREV,
                "않": ID.PREV,
                "없": ID.PREV,
                "었": ID.PREV,
                "였": ID.PREV,
                "이": ID.PREV,
                "졌": ID.PREV,
                "쳤": ID.PREV,
                "챘": ID.PREV,
                "켰": ID.PREV,
                "팠": ID.PREV,
                "폈": ID.PREV,
                "펐": ID.PREV,
                "하": ID.PREV,
                "했": ID.PREV,
                "혔": ID.PREV,
                "고": ID.PREV | ID.NEXT2,
                "는": ID.NEXT,
                "라": ID.NEXT1,
                "를": ID.NEXT,
                "며": ID.NEXT2,
                "면": ID.PREV | ID.NEXT2,
                "": ID.NONE,
            }
        ),
        Stats.SB: create_dict(
            {
                "것": ID.PREV,
                "거": ID.PREV,
                "가": ID.PREV,
                "까": ID.PREV,
                "걸": ID.PREV,
                "껄": ID.PREV,
                "나": ID.PREV,
                "니": ID.PREV,
                "네": ID.PREV,
                "다": ID.PREV,
                "도": ID.PREV,
                "쎄": ID.PREV,
                "래": ID.PREV,
                "데": ID.PREV,
                "지": ID.PREV,
                "든": ID.PREV,
                "덩": ID.PREV,
                "등": ID.PREV,
                "랴": ID.PREV,
                "마": ID.PREV,
                "봐": ID.PREV,
                "서": ID.PREV,
                "셈": ID.PREV,  # ~하셈 (신조어)
                "아": ID.PREV,
                "어": ID.PREV,
                "오": ID.PREV,
                "요": ID.PREV,
                "용": ID.PREV,
                "을": ID.PREV,
                "자": ID.PREV,
                "죠": ID.PREV,
                "쥬": ID.PREV,  # ~했쥬 (사투리)
                "죵": ID.PREV,  # ~했죵 (신조어)
                "고": ID.PREV | ID.NEXT2,
                "는": ID.NEXT,
                "라": ID.PREV | ID.NEXT,
                "며": ID.NEXT2,
                "면": ID.NEXT2,
                "하": ID.NEXT1,
                "": ID.NONE,
            }
        ),
        Stats.COMMON: create_dict(
            {
                "ㄱ": ID.CONT,
                "ㄴ": ID.CONT,
                "ㄷ": ID.CONT,
                "ㄹ": ID.CONT,
                "ㅁ": ID.CONT,
                "ㅂ": ID.CONT,
                "ㅅ": ID.CONT,
                "ㅇ": ID.CONT,
                "ㅈ": ID.CONT,
                "ㅊ": ID.CONT,
                "ㅋ": ID.CONT,
                "ㅌ": ID.CONT,
                "ㅍ": ID.CONT,
                "ㅎ": ID.CONT,
                "ㅏ": ID.CONT,
                "ㅑ": ID.CONT,
                "ㅓ": ID.CONT,
                "ㅕ": ID.CONT,
                "ㅗ": ID.CONT,
                "ㅛ": ID.CONT,
                "ㅜ": ID.CONT,
                "ㅠ": ID.CONT,
                "ㅡ": ID.CONT,
                "ㅣ": ID.CONT,
                "^": ID.CONT,
                ";": ID.CONT,
                ".": ID.CONT,
                "?": ID.CONT,
                "!": ID.CONT,
                "~": ID.CONT,
                "…": ID.CONT,
                "": ID.NONE,
            }
        ),
    },
    default=create_dict({}),
)


def _split_sentences_fast(
    text: str,
    backend: Analyzer,
    strip: bool,
    preprocessor: SentencePreprocessor,
    postprocessor: SentencePostprocessor,
):
    backup_sentence = preprocessor.backup(text)
    syllables = backend.pos(backup_sentence, drop_space=False)
    syllables = preprocessor.preprocess(syllables)

    output_sentences = []
    current_sentence = []
    current_stat = Stats.DEFAULT

    for i, syllable in enumerate(syllables):
        if current_stat == Stats.DEFAULT:
            if syllable.text in [".", "!", "?", "…", "~"]:
                if Table[Stats.SB][syllable.prev.text] & ID.PREV:
                    current_stat = Stats.SB

            if syllable.text in ["다"]:
                if Table[Stats.DA][syllable.prev.text] & ID.PREV:
                    current_stat = Stats.DA

            if syllable.text in ["요"]:
                if Table[Stats.YO][syllable.prev.text] & ID.PREV:
                    current_stat = Stats.YO

            if syllable.text in ["죠", "죵"]:
                if Table[Stats.JYO][syllable.prev.text] & ID.PREV:
                    current_stat = Stats.JYO

        else:
            endif = False

            if not endif:
                if syllable.text == " " or Table[Stats.COMMON][syllable.text] & ID.CONT or syllable.pos == "EMOJI":
                    if Table[current_stat][syllable.prev.text] & ID.NEXT1:
                        output_sentences.append(current_sentence)
                        current_sentence = [syllable.prev]
                        current_stat = Stats.DEFAULT
                    endif = True

            if not endif:
                if Table[current_stat][syllable.text] & ID.NEXT:
                    if Table[current_stat][syllable.prev.text] & ID.NEXT1:
                        current_sentence.append(syllable.prev)

                    elif syllable.prev_skip("SP").text in Table[Stats.COMMON]:
                        # NEW RULE for KSS 3 to fix following issue.
                        # https://github.com/hyunwoongko/kss/issues/7
                        output_sentences.append(current_sentence)
                        current_sentence = []

                    current_stat = Stats.DEFAULT
                    endif = True

            if not endif:
                if Table[current_stat][syllable.text] & ID.NEXT1:
                    if Table[current_stat][syllable.prev.text] & ID.NEXT1:
                        output_sentences.append(current_sentence)
                        current_sentence = [syllable.prev]
                        current_stat = Stats.DEFAULT
                    endif = True

            if not endif:
                if Table[current_stat][syllable.text] & ID.NEXT2:
                    if Table[current_stat][syllable.prev.text] & ID.NEXT1:
                        current_sentence.append(syllable.prev)

                    else:
                        # NEW RULE for KSS 3 to fix following issue.
                        # https://github.com/hyunwoongko/kss/issues/7
                        output_sentences.append(current_sentence)
                        current_sentence = []

                    current_stat = Stats.DEFAULT
                    endif = True

            if not endif:
                if (
                    not Table[current_stat][syllable.text]
                    or Table[current_stat][syllable.text] & ID.PREV
                ):

                    if syllable.text not in const.not_endpoint:
                        output_sentences.append(current_sentence)
                        current_sentence = []
                        if Table[current_stat][syllable.prev.text] & ID.NEXT1:
                            current_sentence.append(syllable.prev)

                    current_stat = Stats.DEFAULT

        if current_stat == Stats.DEFAULT or not (Table[current_stat][syllable.text] & ID.NEXT1):
            current_sentence.append(syllable)

    if len(current_sentence) != 0:
        output_sentences.append(current_sentence)
        current_sentence = []

    if Table[current_stat][syllable.prev.text] & ID.NEXT1:
        current_sentence.append(syllable.prev)
        output_sentences.append(current_sentence)

    output_sentences = postprocessor.postprocess(output_sentences, strip)
    output_sentences = [postprocessor.restore(s, text) for s in output_sentences]
    return output_sentences

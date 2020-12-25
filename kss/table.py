from collections import defaultdict
from typing import Any

from kss.base import Stats, ID, Const


def create_dict(d, default: Any = 0):
    return defaultdict(lambda: default, d)


# Pattern Mapping Table for Sentence Splitter
Table = create_dict({
    Stats.DA:
        create_dict({
            "갔": ID.PREV,
            "간": ID.PREV,
            "겠": ID.PREV,
            "겼": ID.PREV,
            "같": ID.PREV,
            "놨": ID.PREV,
            "녔": ID.PREV,
            "니": ID.PREV,
            "낸": ID.PREV,
            "냈": ID.PREV,
            "뒀": ID.PREV,
            "때": ID.PREV,
            "랐": ID.PREV,
            "럽": ID.PREV,
            "르": ID.PREV,
            "렵": ID.PREV,
            "렸": ID.PREV,
            "린": ID.PREV,
            "뤘": ID.PREV,
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
            "챘": ID.PREV,
            "켰": ID.PREV,
            "켜": ID.PREV,
            "켠": ID.PREV,
            "팠": ID.PREV,
            "펐": ID.PREV,
            "폈": ID.PREV,
            "했": ID.PREV,
            "혔": ID.PREV,
            "가": ID.NEXT,
            "고": ID.NEXT | ID.NEXT2,
            "는": ID.NEXT | ID.NEXT2,
            "라": ID.NEXT,
            "를": ID.NEXT,
            "만": ID.NEXT,
            "며": ID.NEXT | ID.NEXT2,
            "면": ID.NEXT | ID.NEXT1 | ID.NEXT2,
            "서": ID.PREV | ID.NEXT2,
            "싶": ID.PREV | ID.NEXT,
            "죠": ID.NEXT,
            "죵": ID.NEXT,
            "쥬": ID.NEXT,
            "하": ID.PREV | ID.NEXT1,
            "한": ID.PREV,
            "해": ID.NEXT1,
            "도": ID.NEXT2,
            "": ID.NONE
        }),
    Stats.YO:
        create_dict({
            "가": ID.PREV,
            "겨": ID.PREV,
            # "거": ID.PREV,  # 이거요새유명하나? -> [이거요, 새유명하나?]
            "구": ID.PREV,
            "군": ID.PREV,
            "걸": ID.PREV,
            "까": ID.PREV,
            "께": ID.PREV,
            "껴": ID.PREV,
            "네": ID.PREV,
            "나": ID.PREV,
            # "니": ID.PREV,  # 아니요즘에누가그래 -> [아니요, 즘에누가그래]
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
            "고": ID.PREV | ID.NEXT2,
            "는": ID.NEXT,
            "라": ID.NEXT1,
            "를": ID.NEXT,
            "며": ID.NEXT2,
            "면": ID.PREV | ID.NEXT2,
            "하": ID.NEXT1,
            "": ID.NONE
        }),
    Stats.JYO:
        create_dict({
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
            "았": ID.PREV,
            "럽": ID.PREV,
            "렵": ID.PREV,
            "렸": ID.PREV,
            "몄": ID.PREV,
            "밌": ID.PREV,
            "볐": ID.PREV,
            "볍": ID.PREV,
            "봤": ID.PREV,
            "서": ID.PREV,
            "섰": ID.PREV,
            "셨": ID.PREV,
            "샜": ID.PREV,
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
            "하": ID.PREV,
            "했": ID.PREV,
            "혔": ID.PREV,
            "": ID.NONE
        }),
    Stats.SB:
        create_dict({
            "것": ID.PREV,
            "가": ID.PREV,
            "까": ID.PREV,
            "거": ID.PREV,
            "걸": ID.PREV,
            "껄": ID.PREV,
            "나": ID.PREV,
            "니": ID.PREV,
            "다": ID.PREV,
            "도": ID.PREV,
            "든": ID.PREV,
            "랴": ID.PREV,
            "래": ID.PREV,
            "마": ID.PREV,
            "봐": ID.PREV,
            "서": ID.PREV,
            "아": ID.PREV,
            "어": ID.PREV,
            "오": ID.PREV,
            "요": ID.PREV,
            "을": ID.PREV,
            "자": ID.PREV,
            "지": ID.PREV,
            "죠": ID.PREV,
            "고": ID.PREV | ID.NEXT2,
            "는": ID.NEXT,
            "라": ID.PREV | ID.NEXT,
            "며": ID.NEXT2,
            "면": ID.NEXT2,
            "하": ID.NEXT1,
            "": ID.NONE
        }),
    Stats.COMMON:
        create_dict({
            "ㄱ": ID.CONT,  # ㄱㄱ
            "ㄴ": ID.CONT,  # ㄴㄴ
            "ㄷ": ID.CONT,  # ㄷㄷ, ㅎㄷㄷ
            "ㄹ": ID.CONT,  # ㄹㄹ, ㅈㄹ
            # "ㅁ": ID.CONT,  # ㅁㅁ는 잘 안씀
            "ㅂ": ID.CONT,  # ㅂㅂ, ㅅㅂ
            "ㅅ": ID.CONT,  # ㅅㅅ, ㄳ, ㅄ
            "ㅇ": ID.CONT,  # ㅇㅇ
            "ㅈ": ID.CONT,  # ㅈㅈ
            "ㅊ": ID.CONT,  # ㅊㅊ
            "ㅋ": ID.CONT,  # ㅋㅋ, ㅋㅋㅋ, ㅋㅋㅋㅋ...
            "ㅌ": ID.CONT,  # ㅌㅌ, ㅎㅌㅌ
            # "ㅍ": ID.CONT,  # ㅍㅍ는 잘 안씀
            "ㅎ": ID.CONT,  # ㅇㅎ, ㅎㅎ, ㅎㅎㅎ, ㅎㅎㅎㅎ...
            "ㅠ": ID.CONT,  # ㅜㅠ, ㅠㅠ
            "ㅜ": ID.CONT,  # ㅜㅜ
            "ㅡ": ID.CONT,  # ㅡㅡ
            "ㅗ": ID.CONT,  # ㅗㅗ
            "^": ID.CONT,
            ";": ID.CONT,
            ".": ID.CONT,
            "?": ID.CONT,
            "!": ID.CONT,
            ")": ID.CONT,
            "）": ID.CONT,
            "〉": ID.CONT,
            ">": ID.CONT,
            "》": ID.CONT,
            "]": ID.CONT,
            "］": ID.CONT,
            "〕": ID.CONT,
            "】": ID.CONT,
            "}": ID.CONT,
            "｝": ID.CONT,
            "』": ID.CONT,
            "」": ID.CONT,
            "~": ID.CONT,
            "…": ID.CONT,
            ",": ID.CONT,
            "": ID.NONE,
        })
},
    default=create_dict({})
)
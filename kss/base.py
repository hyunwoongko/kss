#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Korean Sentence Splitter
# Split Korean text into sentences using heuristic algorithm.
#
# Copyright (C) 2021 Hyun-Woong Ko <kevin.ko@tunib.ai> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

from collections import namedtuple
from typing import List

SentenceIndex = namedtuple("SentenceIndex", ["start", "end"])
ChunkWithIndex = namedtuple("ChunkWithIndex", ["start", "text"])


class Stats(object):
    DEFAULT: int = 0
    DA: int = 1
    YO: int = 2
    JYO: int = 3
    HAM: int = 4
    UM: int = 5
    SB: int = 6
    COMMON: int = 7


class ID(object):
    NONE: int = 0
    PREV: int = 1 << 0
    CONT: int = 1 << 1
    NEXT: int = 1 << 2
    NEXT1: int = 1 << 3
    NEXT2: int = 1 << 4


class Const:
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    lower_alphabets = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]
    upper_alphabets = [_.upper() for _ in lower_alphabets]

    # <와 >는 수학기호나 화살표(<-, ->)로 쓰이는 경우가 잦아서 제외 함
    bracket = [
        ")",
        "）",
        "〉",
        "》",
        "]",
        "］",
        "〕",
        "】",
        "}",
        "｝",
        "』",
        "」",
        "(",
        "（",
        "〈",
        "《",
        "[",
        "［",
        "〔",
        "【",
        "{",
        "｛",
        "「",
        "『",
    ]

    bracket_open_to_close = {
        "(": ")",
        "（": "）",
        "〈": "〉",
        "《": "》",
        "[": "]",
        "［": "］",
        "〔": "〕",
        "【": "】",
        "{": "}",
        "｛": "｝",
        "「": "」",
        "『": "』",
    }

    bracket_close_to_open = {v: k for k, v in bracket_open_to_close.items()}

    double_quotes = ['"', "“", "”"]
    single_quotes = ["'", "‘", "’"]
    double_quotes_open_to_close = {"“": "”", '"': '"'}
    single_quotes_open_to_close = {"‘": "’", "'": "'"}
    double_quotes_close_to_open = {v: k for k, v in double_quotes_open_to_close.items()}
    single_quotes_close_to_open = {v: k for k, v in single_quotes_open_to_close.items()}

    punctuation = [";", ".", ":", "?", "!", ",", "·"]
    special = punctuation + bracket


class BackupManager:
    def __init__(self):
        self.backup_dict = {k: str(abs(hash(k))) for k in self._get_data()}

    @staticmethod
    def _get_data():
        faces = [":)", ":(", ":'(", "O:)", "&)", ">:(", "3:)", '<(")', ":-)", ":-("]
        low_upper_num = Const.lower_alphabets + Const.upper_alphabets

        apostrophe = []
        for i in low_upper_num:
            for j in low_upper_num:
                apostrophe.append(f"{i}'{j}")

        year_s = []
        for i in Const.numbers:
            year_s.append(f"{i}'s")
            year_s.append(f"{i}'S")

        EC_cases = [
            "쌓이다",
            "보이다",
            "먹이다",
            "죽이다",
            "끼이다",
            "트이다",
            "까이다",
            "꼬이다",
            "데이다",
            "치이다",
            "쬐이다",
            "꺾이다",
            "낚이다",
            "녹이다",
            "벌이다",
            "다 적발",
            "다 말하",
            "다 말한",
            "다 말했",
            "다 밝혀",
            "다 밝혔",
            "다 밝히",
            "다 밝힌",
            "다 주장",
            "요 라고",
            "요. 라고",
            "죠 라고",
            "죠. 라고",
            "다 라고",
            "다. 라고",
            "다 하여",
            "다 거나",
            "다. 거나",
            "다 시피",
            "다. 시피",
            "다 응답",
            "다 로 응답",
            "다. 로 응답",
            "요 로 응답",
            "요. 로 응답",
            "죠 로 응답",
            "죠. 로 응답",
            "다 에서" "다. 에서" "요 에서" "요. 에서" "죠 에서" "죠. 에서" "타다 금지법",
            "다 온 사실",
            "다 온 것",
            "다 온 사람",
            "다 왔다",
            "다 왔더",
            "다 와보",
        ]

        Exceptions = [
            "초.중.고.",
            "우간다",
            "사이다",
        ]

        return faces + apostrophe + year_s + EC_cases + Exceptions

    def _process(self, text: str, purpose_dict: dict):
        for k, v in purpose_dict.items():
            text = text.replace(k, v)

        return text.strip()

    def add_item_to_dict(self, key, val):
        self.backup_dict[key] = val

    def backup(self, text: str):
        return self._process(text=text, purpose_dict=self.backup_dict)

    def restore(self, text: str):
        return self._process(
            text=text,
            purpose_dict={v: k for k, v in self.backup_dict.items()},
        )


def empty(obj) -> bool:
    return len(obj) == 0


def top(stack: List[str], symbol: str) -> bool:
    return stack[len(stack) - 1] == symbol


def do_push_pop_symbol(stack: List[str], symbol: str, current_ch):
    # call by assignment
    if empty(stack):
        stack.append(symbol)

    else:
        if top(stack, current_ch):
            return stack.pop()
        else:
            stack.append(symbol)

    return current_ch


def do_trim_sent_push_results(cur_sentence, results):
    # call by assignment
    results.append(cur_sentence.strip())
    cur_sentence = ""
    return cur_sentence


class QuoteException:
    def process(
        self,
        cur_chr,
        prev_1,
        prev_2,
        prev_3,
        prev_4,
        single_stack,
        double_stack,
    ):
        # for time (5'40) : ['5', '\u', {'}, '\u', '4']
        if cur_chr in Const.numbers:
            if prev_1 == "\u200b":
                if prev_2 in Const.single_quotes:
                    if prev_3 == "\u200b":
                        if prev_4 in Const.numbers + Const.special:
                            do_push_pop_symbol(single_stack, "'")

        # for inch (2.5") : ['.', '5', '\u', {"}, '\u']
        if cur_chr == "\u200b":
            if prev_1 in Const.double_quotes:
                if prev_2 == "\u200b":
                    if prev_3 in Const.numbers:
                        if prev_4 in Const.numbers + Const.special:
                            do_push_pop_symbol(double_stack, '"')

        # for SOMETHING's : ['G', '\u', {'}, '\u', 's']
        if cur_chr in ["s", "S"]:
            if prev_1 == "\u200b":
                if prev_2 in Const.single_quotes:
                    if prev_3 == "\u200b":
                        if prev_4 != " ":
                            do_push_pop_symbol(single_stack, "'")

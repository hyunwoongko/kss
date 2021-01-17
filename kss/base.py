#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Korean Sentence Splitter
# Split Korean text into sentences using heuristic algorithm.
#
# Copyright (C) 2019 Sang-Kil Park <skpark1224@hyundai.com> and Hyun-woong Ko <kevin.woong@kakaobrain.com>
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.
from collections import namedtuple
from typing import List

SentenceIndex = namedtuple('SentenceIndex', ['start', 'end'])
ChunkWithIndex = namedtuple('ChunkWithIndex', ['start', 'text'])


class Stats(object):
    DEFAULT: int = 0
    DA: int = 1
    YO: int = 2
    JYO: int = 3
    SB: int = 4
    COMMON: int = 5


class ID(object):
    NONE: int = 0
    PREV: int = 1 << 0
    CONT: int = 1 << 1
    NEXT: int = 1 << 2
    NEXT1: int = 1 << 3
    NEXT2: int = 1 << 4


class Const:
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    # <와 >는 수학기호나 화살표(<-, ->)로 쓰이는 경우가 잦아서 제외 함
    bracket = [")", "）", "〉", "》", "]", "］", "〕", "】", "}", "｝", "』", "」",
               "(", "（", "〈", "《", "[", "［", "〔", "【", "{", "｛", "「", "『"]
    punctuation = [";", ".", ":", "?", "!", ',']
    double_quotes = ["\"", "“", "”", "″"]
    single_quotes = ["'", "`", "‘", "’"]

    lower_alphabets = alphabets
    upper_alphabets = [_.upper() for _ in alphabets]
    special = punctuation + bracket


class BackupManager:

    def __init__(self):
        self.backup_dict = {k: str(abs(hash(k))) for k in self._get_data()}
        self.restore_dict = {v: k for k, v in self.backup_dict.items()}

    @staticmethod
    def _get_data():
        faces = [':)', ':(', ":'(", "O:)", "&)", ">:(", "3:)", '<(")']
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
            '쌓',  # 동사 (쌓이다가)
            '보',  # 동사 (보이다가)
            '먹',  # 동사 (먹이다가)
            '죽',  # 동사 (죽이다가)
            "끼",  # 동사 (끼이다가)
            '트',  # 동사 (트이다가)
            '까',  # 동사 (까이다가)
            '꼬',  # 동사 (꼬이다가)
            '데',  # 동사 (데이다가)
            '치',  # 동사 (치이다가)
            '쬐',  # 동사 (쬐이다가)
            '꺾',  # 동사 (꺾이다가)
            '낚',  # 동사 (낚이다가)
            '녹',  # 동사 (녹이다가)
            '벌',  # 동사 (벌이다가)
            '사',  # 사이다
            # '파',  # 형용사
        ]

        EC_cases = [_ + "이다" for _ in EC_cases]

        Excepted_cases = [
            '손자',
            '요원',
            '어린다',
            '다이빙',
            '우간다',
            '초.중.고.',
            "다적발",
            "다 적발",
            '다말하',
            '다 말하',
            '다말한',
            '다 말한',
            '다말했',
            '다 말했',
            '다밝혔',
            '다 밝혔',
            '다밝히',
            '다 밝히',
            '다밝힌',
            '다 밝힌',
            '다주장',
            '다 주장',
            '요라고',
            '요 라고',
            '요. 라고',
            '죠라고',
            '죠 라고',
            '죠. 라고',
            '다라고',
            '다 라고',
            '다. 라고',
            '다하여',
            '다 하여',
            "다거나",
            "다 거나",
            "다. 거나",
            '다시피',
            "다 시피",
            "다. 시피",
            '다응답',
            "다 응답",
            '다로 응답',
            "다 로 응답",
            "다. 로 응답",
            '요로 응답',
            "요 로 응답",
            "요. 로 응답",
            '죠로 응답',
            "죠 로 응답",
            "죠. 로 응답",
            "다에서"
            "다 에서"
            "다. 에서"
            "요에서"
            "요 에서"
            "요. 에서"
            "죠에서"
            "죠 에서"
            "죠. 에서"
            '요소',
            '타다 금지법',
            '요법',
            '요인',
            '다리',
            '다>',
            '다스',
            '다던',
            '다습',
            '다든',
            '요금',
            '다음',
            '다거나',
            '다식',
            '초.중.고.',
            "갔다온 사실",
            "갔다 온 사실",
            "갔다온 것",
            "갔다 온 것",
            "갔다 왔다",
            "갔다왔다",
            "하다 왔다",
            "하다왔다",
        ]

        return faces + apostrophe + year_s + EC_cases + Excepted_cases

    def _process(self, text: str, purpose_dict: dict):
        for k, v in purpose_dict.items():
            text = text.replace(k, v)

        return text.strip()

    def backup(self, text: str):
        return self._process(text, self.backup_dict)

    def restore(self, text: str):
        return self._process(text, self.restore_dict)


def empty(obj) -> bool:
    return len(obj) == 0


def top(stack: List[str], symbol: str) -> bool:
    return stack[len(stack) - 1] == symbol


def do_push_pop_symbol(stack: List[str], symbol: str):
    # call by assignment
    if empty(stack):
        stack.append(symbol)

    else:
        if top(stack, symbol):
            stack.pop()
        else:
            stack.append(symbol)


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
            if prev_1 in "\u200b":
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
                            do_push_pop_symbol(double_stack, "\"")

        # for SOMETHING's : ['G', '\u', {'}, '\u', 's']
        if cur_chr in ["s", "S"]:
            if prev_1 == "\u200b":
                if prev_2 in Const.single_quotes:
                    if prev_3 == "\u200b":
                        if prev_4 != " ":
                            do_push_pop_symbol(single_stack, "'")

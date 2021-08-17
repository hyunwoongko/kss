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

import logging
from copy import deepcopy

from kss.morph import MorphExtractor

logger = logging.getLogger("Korean Sentence Splitter")
logger.warning("[KSS]: Initializing Kss...")


class Stats(object):
    DEFAULT: int = 0
    DA_EOJEOL: int = 1
    DA_MORPH: int = 2
    YO: int = 3
    JYO: int = 4
    SB: int = 5
    COMMON: int = 6
    EOMI: int = 7


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
    brackets = [
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

    double_quotes = ['"', "“", "”", "″"]
    single_quotes = ["'", "‘", "’", "`"]
    double_quotes_open_to_close = {
        "“": "”",
        '"': '"',
        "″": "″",
    }
    single_quotes_open_to_close = {
        "‘": "’",
        "'": "'",
        "`": "`",
    }
    double_quotes_close_to_open = {v: k for k, v in double_quotes_open_to_close.items()}
    single_quotes_close_to_open = {v: k for k, v in single_quotes_open_to_close.items()}

    punctuation = [";", ".", ":", "?", "!", ",", "·"]
    special = punctuation + brackets
    quotes_or_brackets = single_quotes + double_quotes + brackets
    endpoint = quotes_or_brackets + punctuation + [" "]

    @staticmethod
    def exceptions():
        faces = [":)", ":(", ":'(", "O:)", "&)", ">:(", "3:)", '<(")', ":-)", ":-("]
        low_upper = Const.lower_alphabets + Const.upper_alphabets

        apostrophe = []
        for i in low_upper:
            for j in low_upper:
                for k in Const.single_quotes:
                    apostrophe.append(f"{i}{k}{j}")

        year_s = []
        for i in Const.numbers:
            for j in Const.single_quotes:
                year_s.append(f"{i}{j}s")
                year_s.append(f"{i}{j}S")

        time = []
        for i in Const.numbers:
            for j in Const.numbers:
                for k in Const.single_quotes:
                    time.append(f"{i}{k}{j}")
                    time.append(f"{i}{k}{j}")
                    time.append(f"{i}{k}{j}")

        inch = []
        for i in Const.numbers + ["."]:
            for j in Const.numbers:
                for k in Const.double_quotes:
                    inch.append(f"{i}{j}{k}")

        return faces + apostrophe + year_s + time + inch

    @staticmethod
    def ec_cases():
        return [
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
            "다 에서",
            "다. 에서",
            "요 에서",
            "요. 에서",
            "죠 에서",
            "죠. 에서",
            "타다 금지법",
            "다 온 사실",
            "다 온 것",
            "다 온 사람",
            "다 왔다",
            "다 왔더",
            "다 와보",
            "우간다",
            "사이다",
        ]


class Eojeol:
    eojeol: str
    pos: str

    def __init__(self, eojeol: str, pos: str):
        self.eojeol = eojeol
        self.pos = pos

    def __str__(self):
        return f"({self.eojeol}, {self.pos})"

    def __repr__(self):
        return f"('{self.eojeol}', {self.pos})"


class Preprocessor:
    def __init__(self, use_morpheme: bool):
        global _exceptions
        exceptions = deepcopy(_exceptions)

        # drop ec cases if morpheme features are not available
        if not use_morpheme:
            exceptions += Const.ec_cases()

        self.backup_dict = {k: str(abs(hash(k))) for k in exceptions}

    @staticmethod
    def tostring(eojeols):
        return ["".join([j.eojeol for j in i]) for i in eojeols]

    @staticmethod
    def remove_zwsp(text):
        return text.replace("\u200b", "")

    @staticmethod
    def remove_useless_space(text):
        while "  " in text:
            text = text.replace("  ", " ")

        return text

    @staticmethod
    def _replace(text: str, purpose_dict: dict):
        for k, v in purpose_dict.items():
            text = text.replace(k, v)

        return text

    def backup(self, text: str):
        return self._replace(text=text, purpose_dict=self.backup_dict)

    def restore(self, text: str):
        return self._replace(
            text=text,
            purpose_dict={v: k for k, v in self.backup_dict.items()},
        )

    def add_item_to_dict(self, key: str, val: str):
        self.backup_dict[key] = val

    def add_ec_cases_to_dict(self, text):
        for i in range(0, len(text)):
            cond1 = text[i] in ["다", "요", "죠"]
            cond2 = i != len(text) - 1
            if cond1 and cond2:
                if text[i + 1] not in Const.endpoint:
                    target_to_backup = text[i] + text[i + 1]
                    self.add_item_to_dict(
                        key=target_to_backup,
                        val=str(abs(hash(target_to_backup))),
                    )

        return text


class Postprocessor(object):
    @staticmethod
    def _contains(src, tgt):
        for s in src:
            for p in [" ", "?", ".", "!"]:
                if f"{s}{p}" in tgt:
                    return True
        return False

    @staticmethod
    def _lindex_split(some_list, *args):
        args = (0,) + tuple(data + 1 for data in args) + (len(some_list) + 1,)
        return [some_list[start:end] for start, end in zip(args, args[1:])]

    @staticmethod
    def _find_all(a_str, sub):
        start = 0
        while True:
            start = a_str.find(sub, start)
            if start == -1:
                return
            yield start + len(sub) - 1
            start += len(sub)

    @staticmethod
    def nt_post_process(results, prep):
        n_outputs = []
        for s in results:
            s = prep.restore(s).replace("\u200b", "")
            if "\n" in s:
                segmented = s.split("\n")
                for _s in segmented:
                    n_outputs.append(_s)
            else:
                n_outputs.append(s)

        t_outputs = []
        for s in n_outputs:
            if "\t" in s:
                segmented = s.split("\t")
                for _s in segmented:
                    t_outputs.append(_s)
            else:
                t_outputs.append(s)
        return t_outputs

    def _heuristic(self, results, post_processing_list):
        final_results = []
        for res in results:
            split_idx = []

            find_quotes = False
            for qt in Const.quotes_or_brackets:
                if qt in res:
                    find_quotes = True
                    break

            if not find_quotes:
                for post in post_processing_list:
                    if post in res:
                        split_idx += list(self._find_all(res, post))

            split_idx = sorted(split_idx)
            final_results += self._lindex_split(res, *split_idx)

        return final_results

    def apply_heuristic(self, text, results, use_morpheme):
        from kss.rule import (
            post_processing_da,
            post_processing_jyo,
            post_processing_yo,
        )

        if self._contains(["요"], text):
            results = self._heuristic(results, post_processing_yo)
        if self._contains(["죠"], text):
            results = self._heuristic(results, post_processing_jyo)
        if not use_morpheme and self._contains(["다"], text):
            results = self._heuristic(results, post_processing_da)

        return results


_morph = MorphExtractor()
_exceptions = Const.exceptions()

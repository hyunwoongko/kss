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
import functools
import re
import logging
from typing import List

from kss.morph import MorphExtractor
from kss.pynori.dict.character_definition import (
    get_emoji,
    categories,
)
from kss.rule import Table, Stats, unicodes

logging.basicConfig(
    format="[Korean Sentence Splitter]: %(message)s", level=logging.WARNING
)


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

    punctuation = [";", ".", "?", "!", "~", "…"]
    special = punctuation + brackets
    quotes_or_brackets = single_quotes + double_quotes + brackets
    endpoint = (
        quotes_or_brackets + punctuation + [" "] + list(Table[Stats.COMMON].keys())
    )
    not_endpoint = [",", ":", "\u200b"] + quotes_or_brackets + ["<", ">"]

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

        return faces + apostrophe + year_s

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
            "우간다",
            "사이다",
        ]

    pattern_space = re.compile(r"\s+")


class Eojeol:
    eojeol: str
    pos: str

    def __init__(self, eojeol: str = "", pos: str = "TEMP"):
        self.eojeol = eojeol
        self.pos = pos

    def __str__(self):
        return f"({self.eojeol}, {self.pos})"

    def __repr__(self):
        return f"('{self.eojeol}', {self.pos})"


@functools.lru_cache(maxsize=2)
def get_exceptions(use_morpheme):
    _exceptions = Const.exceptions()
    if not use_morpheme:
        _exceptions += Const.ec_cases()

    return _exceptions


@functools.lru_cache(maxsize=2)
def get_default_backup_dict(use_morpheme):
    return {k: str(abs(hash(k))) for k in get_exceptions(use_morpheme)}


class Preprocessor:
    def __init__(self, use_morpheme: bool):
        self.backup_dict = get_default_backup_dict(use_morpheme)

    @staticmethod
    def tostring(eojeols):
        return ["".join([j.eojeol for j in i]) for i in eojeols]

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

    def _add_item_to_dict(self, key: str, val: str):
        self.backup_dict[key] = val

    def add_ec_cases_to_dict(self, text):
        for i in range(0, len(text)):
            cond1 = text[i] in ["다", "요", "죠"]
            cond2 = i != len(text) - 1
            if cond1 and cond2:
                if text[i + 1] not in Const.endpoint:
                    target_to_backup = text[i] + text[i + 1]
                    self._add_item_to_dict(
                        key=target_to_backup,
                        val=str(abs(hash(target_to_backup))),
                    )

        return text

    def add_emojis_to_dict(self, text):
        emoji_dict = {e: str(abs(hash(e))) for e in get_emoji(text)}
        unicode_dict = {u: str(abs(hash(u))) for u in unicodes}
        self.backup_dict.update(emoji_dict)
        self.backup_dict.update(unicode_dict)
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


def empty(obj, dim=1) -> bool:
    assert dim in [1, 2], "only 1 or 2 dimension iterable is supported."

    if dim == 1:
        return len(obj) == 0
    else:
        return all([empty(o) for o in obj])


def top(stack: List[str], symbol: str) -> bool:
    return stack[len(stack) - 1] == symbol


def do_push_pop_symbol(stack: List[str], symbol: str, current_ch: str):
    # call by assignment
    if empty(stack):
        stack.append(symbol)

    else:
        if top(stack, current_ch):
            return stack.pop()
        else:
            stack.append(symbol)

    return current_ch


def check_pos(pos, pos_list):
    for target in pos_list:
        if target in pos.pos:
            return True
    return False


def replace_quotes_or_brackets_to_zwsp(eojeols):
    results = []
    for eojeol in eojeols:
        item = [eojeol]

        for s in Const.quotes_or_brackets:
            if eojeol.eojeol == s:
                item = [
                    Eojeol("\u200b", "TEMP"),
                    eojeol,
                    Eojeol("\u200b", "TEMP"),
                ]

        results += item

    return results


def length_constraints(
    text,
    max_recover_length,
    max_recover_step,
):
    if len(text) > max_recover_length:
        logging.warning("Too long text! turn off quotes calibration!")
        max_recover_step = 0

    return max_recover_step


def build_preprocessed_list(text):
    input_texts = []
    split_texts = text.split("\n")

    for t in split_texts:
        t = t.split("\t")
        for s in t:
            s = s.strip()
            if len(s) > 0:
                s = preprocess_text(s)
                input_texts.append(s)

    return input_texts


def clear_list_to_sentences(results):
    total_result = []
    for result in results:
        temp = []
        for sent in result:
            sent = sent.strip()
            if len(sent) > 0:
                temp.append(sent)
        total_result.append(temp)

    return total_result


def get_num_workers(num_workers):
    if num_workers < 0:
        num_workers = None

    if num_workers == 0:
        num_workers = 1

    return num_workers


def remove_useless_space(text):
    return Const.pattern_space.sub(" ", text.replace("\n", ""))


def get_chunk_with_index(text, span):
    text = remove_useless_space(text)

    if len(span) == 0:
        return None
    else:
        start = span[0][0]
        end = span[-1][1]
        return text[start:end]


def preprocess_text(text):
    total_text = "".join(
        [c for c in text if c in _posix or len(get_emoji(c)) != 0 or c in unicodes]
    )

    return Const.pattern_space.sub(" ", total_text)


_posix = list(chr(x) for x in categories.keys())
_morph = MorphExtractor()

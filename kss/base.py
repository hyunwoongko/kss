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

from typing import List


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


class SentenceIndex:
    def __init__(self, start, end):
        self.start = start
        self.end = end


class ChunkWithIndex:
    def __init__(self, start, text):
        self.start = start
        self.text = text


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

        return faces + apostrophe + year_s

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
                        if prev_4 in [] + Const.numbers + Const.special:
                            do_push_pop_symbol(single_stack, "'")

        # for inch (2.5") : ['.', '5', '\u', {"}, '\u']
        if cur_chr == "\u200b":
            if prev_1 in Const.double_quotes:
                if prev_2 == "\u200b":
                    if prev_3 in Const.numbers:
                        if prev_4 in [] + Const.numbers + Const.special:
                            do_push_pop_symbol(double_stack, "\"")

        # for SOMETHING's : ['G', '\u', {'}, '\u', 's']
        if cur_chr in ["s", "S"]:
            if prev_1 == "\u200b":
                if prev_2 in Const.single_quotes:
                    if prev_3 == "\u200b":
                        if prev_4 != " ":
                            do_push_pop_symbol(single_stack, "'")


class Safe(object):
    LOW: int = 0
    MID: int = 1
    HIGH: int = 2

    def __init__(self, safe: int=0):
        level = int(safe)
        # if safe:
        #     self.level = Level.MID
        # else:
        if level > Safe.HIGH:
            self.level = Safe.HIGH
        elif level < Safe.LOW:
            self.level = Safe.LOW
        else:
            self.level = level
    def get_level(self):
        return self.level

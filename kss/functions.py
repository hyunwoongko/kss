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

from typing import List
from kss.classes import Const, Eojeol, logger


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
        logger.warning("[KSS]: Too long text ! turn off quotes calibration !")
        max_recover_step = 0

    return max_recover_step


def split_input_texts(text):
    input_texts = []
    split_texts = text.split("\n")

    for t in split_texts:
        t = t.split("\t")
        for s in t:
            s = s.strip()
            if len(s) > 0:
                input_texts.append(s)

    return input_texts


def get_input_texts(text):
    input_texts = []

    if isinstance(text, str):
        input_texts.append(split_input_texts(text))

    elif isinstance(text, list) or isinstance(text, tuple):
        for txt in text:
            if not isinstance(txt, str):
                raise TypeError(
                    "param `text` must be one of type [str, List[str], Tuple[str]]`. "
                    f"but you inputted {type(text)}."
                )

            input_texts.append(split_input_texts(txt))
    else:
        raise TypeError("param `text` must be one of type [str, List[str], Tuple[str]]")

    return input_texts


def clear_list_to_sentences(results):
    return [
        [sentence.strip() for sentence in result if len(sentence.strip()) > 0]
        for result in results
    ]


def get_num_workers(num_workers):
    if num_workers < 0:
        num_workers = None

    if num_workers == 0:
        num_workers = 1

    return num_workers


def remove_useless_space(text):
    text = text.replace("\n", "")
    while "  " in text:
        text = text.replace("  ", " ")

    return text


def get_chunk_with_index(text, span):
    text = remove_useless_space(text)
    start = span[0][0]
    end = span[-1][1]
    return text[start:end]

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

import math
import re
from typing import List

# classes
from kss.base import (
    ID,
    Stats,
    Const,
    BackupManager,
    QuoteException,
    ChunkWithIndex,
    SentenceIndex,
)

# functions
from kss.base import (
    empty,
    do_trim_sent_push_results,
    do_push_pop_symbol,
)

# mapping table
from kss.korean import post_processing_da, post_processing_jyo, post_processing_yo
from kss.table import Table


# TODO (bug) : 책을 봤다. 고구려에 관한
def realign_by_quote(text, last_quote_pos, quote_type):
    before_quote = split_sentences(text[:last_quote_pos])
    before_last = before_quote[-1] if len(before_quote) > 0 else ""
    before_quote = [] if len(before_quote) == 1 else before_quote[: -1]

    after_quote = split_sentences(text[last_quote_pos + 1:])
    after_first = after_quote[0] if len(after_quote) > 0 else ""
    after_quote = [] if len(after_quote) == 1 else after_quote[1:]

    middle_quote = [before_last + quote_type + after_first]
    return before_quote + middle_quote + after_quote


def lindexsplit(some_list, *args):
    args = (0,) + tuple(data + 1 for data in args) + (len(some_list) + 1,)
    return [some_list[start:end].strip() for start, end in zip(args, args[1:])]


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start + len(sub) - 1
        start += len(sub)


def post_processing(results, post_processing_list):
    final_results = []
    for res in results:
        split_idx = []
        quotes = []

        for qt in Const.single_quotes + Const.double_quotes + Const.bracket:
            if qt in res:
                quotes += list(find_all(res, qt))

        if len(quotes) % 2 == 0:
            for post in post_processing_list:
                if post in res:
                    split_idx += list(find_all(res, post))

        split_idx = sorted(split_idx)
        final_results += lindexsplit(res, *split_idx)

    return final_results


def split_sentences(text: str, safe=False):
    backup_manager = BackupManager()
    quote_exception = QuoteException()
    text = backup_manager.backup(text)

    for s in Const.single_quotes + Const.double_quotes + Const.bracket:
        text = text.replace(s, f"\u200b{s}\u200b")

    prev_1: str = ""
    prev_2: str = ""
    prev_3: str = ""
    prev_4: str = ""

    cur_sentence: str = ""
    results: List[str] = []
    cur_stat: int = Stats.DEFAULT

    single_quote_stack: List[str] = []
    double_quote_stack: List[str] = []
    bracket_stack: List[str] = []

    last_single_quote_pos = 0
    last_double_quote_pos = 0
    last_bracket_pos = 0

    for i, chr_string in enumerate(text):
        if cur_stat == Stats.DEFAULT:
            if chr_string in Const.double_quotes:
                do_push_pop_symbol(double_quote_stack, "\"")
                last_double_quote_pos = i

            elif chr_string in Const.single_quotes:
                do_push_pop_symbol(single_quote_stack, "'")
                last_single_quote_pos = i

            elif chr_string in Const.bracket:
                do_push_pop_symbol(bracket_stack, "B")
                last_bracket_pos = i

            elif chr_string == "다":
                if empty(double_quote_stack) and empty(single_quote_stack) and empty(bracket_stack) and (
                        Table[Stats.DA][prev_1] & ID.PREV):
                    cur_stat = Stats.DA
            elif chr_string == "요":
                if empty(double_quote_stack) and empty(single_quote_stack) and empty(bracket_stack) and (
                        Table[Stats.YO][prev_1] & ID.PREV):
                    cur_stat = Stats.YO
            elif chr_string == "죠":
                if empty(double_quote_stack) and empty(single_quote_stack) and empty(bracket_stack) and (
                        Table[Stats.JYO][prev_1] & ID.PREV):
                    cur_stat = Stats.JYO
            elif chr_string in [".", "!", "?"]:
                if empty(double_quote_stack) and empty(single_quote_stack) and empty(bracket_stack) and (
                        Table[Stats.SB][prev_1] & ID.PREV):
                    cur_stat = Stats.SB

            quote_exception.process(
                chr_string,
                prev_1,
                prev_2,
                prev_3,
                prev_4,
                single_quote_stack,
                double_quote_stack,
            )

        else:
            if chr_string in Const.double_quotes:
                last_double_quote_pos = i

            elif chr_string in Const.single_quotes:
                last_single_quote_pos = i

            elif chr_string in Const.bracket:
                last_bracket_pos = i

            endif = False
            if not endif:
                # Space
                if chr_string == " " or \
                        Table[Stats.COMMON][chr_string] & ID.CONT:
                    if Table[cur_stat][prev_1] & ID.NEXT1:
                        cur_sentence = do_trim_sent_push_results(
                            cur_sentence,
                            results,
                        )
                        cur_sentence += prev_1
                        cur_stat = Stats.DEFAULT

                    endif = True

            if not endif:
                if Table[cur_stat][chr_string] & ID.NEXT:
                    if Table[cur_stat][prev_1] & ID.NEXT1:
                        # NEXT1 + NEXT => 자르지 않는다.
                        cur_sentence += prev_1
                    cur_stat = Stats.DEFAULT
                    endif = True

            if not endif:
                if Table[cur_stat][chr_string] & ID.NEXT1:
                    if Table[cur_stat][prev_1] & ID.NEXT1:
                        # NEXT1 + NEXT1 => 자른다.
                        cur_sentence = do_trim_sent_push_results(
                            cur_sentence,
                            results,
                        )
                        cur_sentence += prev_1
                        cur_stat = Stats.DEFAULT
                    endif = True

            if not endif:
                if Table[cur_stat][chr_string] & ID.NEXT2:
                    if Table[cur_stat][prev_1] & ID.NEXT1:
                        # NEXT1 + NEXT2 => 자르지 않는다.
                        cur_sentence += prev_1
                    else:
                        # NOT(NEXT1) + NEXT2 => 자른다.
                        cur_sentence = do_trim_sent_push_results(
                            cur_sentence, results)
                    cur_stat = Stats.DEFAULT
                    endif = True

            if not endif:
                if not Table[cur_stat][chr_string] or \
                        Table[cur_stat][chr_string] & ID.PREV:  # NOT exists

                    cur_sentence = do_trim_sent_push_results(
                        cur_sentence, results)
                    if Table[cur_stat][prev_1] & ID.NEXT1:
                        cur_sentence += prev_1
                    cur_stat = Stats.DEFAULT

                    # It's not a good design we suppose, but it's the best unless we change the whole structure.
                    if chr_string in Const.bracket:
                        do_push_pop_symbol(bracket_stack, "B")
                    elif chr_string in Const.double_quotes:
                        do_push_pop_symbol(double_quote_stack, "\"")
                    elif chr_string in Const.single_quotes:
                        do_push_pop_symbol(single_quote_stack, "'")

                    endif = True

        # endif:
        if cur_stat == Stats.DEFAULT or \
                not (Table[cur_stat][chr_string] & ID.NEXT1):
            cur_sentence += chr_string

        prev_4 = prev_3
        prev_3 = prev_2
        prev_2 = prev_1
        prev_1 = chr_string

    if not empty(cur_sentence):
        cur_sentence = do_trim_sent_push_results(cur_sentence, results)

    if Table[cur_stat][prev_1] & ID.NEXT1:
        cur_sentence += prev_1
        do_trim_sent_push_results(cur_sentence, results)

    if len(single_quote_stack) != 0:
        results = realign_by_quote(text, last_single_quote_pos, "'")

    if len(double_quote_stack) != 0:
        results = realign_by_quote(text, last_double_quote_pos, "\"")

    if len(bracket_stack) != 0:
        results = realign_by_quote(text, last_bracket_pos, " ")

    results = [backup_manager.restore(s).replace("\u200b", "") for s in results]

    if not safe:
        # 조사/대명사 + 다 or 요 or 죠 분절 기능
        if "다 " in text:
            results = post_processing(results, post_processing_da)

        if "요 " in text:
            results = post_processing(results, post_processing_yo)

        if "죠 " in text:
            results = post_processing(results, post_processing_jyo)

    return results


def split_sentences_index(text) -> List[SentenceIndex]:
    sentences = split_sentences(text)
    sentence_indexes = []
    offset = 0

    for sentence in sentences:
        sentence_indexes.append(
            SentenceIndex(offset + text.index(sentence), offset + text.index(sentence) + len(sentence)))
        offset += text.index(sentence) + len(sentence)
        text = text[text.index(sentence) + len(sentence):]
    return sentence_indexes


def split_chunks(text: str, max_length=128, overlap=False, indexes=None) -> List[ChunkWithIndex]:
    def get_chunk_with_index():
        start = span[0].start
        end = span[-1].end
        return ChunkWithIndex(span[0].start, text[start:end])

    if indexes is None:
        indexes = split_sentences_index(text)

    span = []
    chunks = []
    for index in indexes:
        if len(span) > 0:
            if index.end - span[0].start > max_length:  # len = last_end - first_start
                chunks.append(get_chunk_with_index())
                if overlap:
                    span = span[math.trunc(len(span) / 2):]  # cut half
                else:
                    span = []
        span.append(index)
    chunks.append(get_chunk_with_index())
    return chunks

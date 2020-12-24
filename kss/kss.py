# Korean Sentence Splitter
# Split Korean text into sentences using heuristic algorithm.
#
# Copyright (C) 2019 Sang-Kil Park <skpark1224@hyundai.com> and Hyun-woong Ko <kevin.woong@kakaobrain.com>
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import math
from typing import List, Any
from collections import defaultdict, namedtuple

SentenceIndex = namedtuple('SentenceIndex', ['start', 'end'])
ChunkWithIndex = namedtuple('ChunkWithIndex', ['start', 'text'])
lower_alphabets = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
]

upper_alphabets = [_.upper() for _ in lower_alphabets]

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


class Stats(object):
    DEFAULT: int = 0
    DA: int = 1
    YO: int = 2
    JYO: int = 3
    SB: int = 4
    COMMON: int = 5


class ID(object):
    NONE: int = 0  # 0000 0000
    PREV: int = 1 << 0  # 0000 0001
    CONT: int = 1 << 1  # 0000 0010
    NEXT: int = 1 << 2  # 0000 0100
    NEXT1: int = 1 << 3  # 0000 1000
    NEXT2: int = 1 << 4  # 0001 0000


def create_dict(d, default: Any = 0):
    return defaultdict(lambda: default, d)


# Pattern Mapping Table for Sentence Splitter
_map = create_dict(
    {
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
                "졌": ID.PREV,
                "쳤": ID.PREV,
                "챘": ID.PREV,
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
                "해": ID.NEXT1,
                "도": ID.NEXT2,
                "": ID.NONE
            }),
        Stats.YO:
            create_dict({
                "가": ID.PREV,
                "구": ID.PREV,
                "군": ID.PREV,
                "걸": ID.PREV,
                "까": ID.PREV,
                "께": ID.PREV,
                "껴": ID.PREV,
                "네": ID.PREV,
                "나": ID.PREV,
                "데": ID.PREV,
                "든": ID.PREV,
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
                "팠": ID.PREV,
                "폈": ID.PREV,
                "하": ID.PREV,
                "했": ID.PREV,
                "혔": ID.PREV,
                "": ID.NONE
            }),
        Stats.SB:
            create_dict({
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
                "ㅋ": ID.CONT,
                "ㅅ": ID.CONT,
                "ㅎ": ID.CONT,
                "ㅠ": ID.CONT,
                "ㅜ": ID.CONT,
                "^": ID.CONT,
                ";": ID.CONT,
                ".": ID.CONT,
                "?": ID.CONT,
                "!": ID.CONT,
                ")": ID.CONT,
                "~": ID.CONT,
                "…": ID.CONT,
                ",": ID.CONT,
                "": ID.NONE
            })
    },
    default=create_dict({}))


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


def realign_by_quote(text, last_quote_pos, quote_type):
    before_quote = split_sentences(text[:last_quote_pos])
    before_last = before_quote[-1] if len(before_quote) > 0 else ""
    before_quote = [] if len(before_quote) == 1 else before_quote[:-1]

    after_quote = split_sentences(text[last_quote_pos + 1:])
    after_first = after_quote[0] if len(after_quote) > 0 else ""
    after_quote = [] if len(after_quote) == 1 else after_quote[1:]

    middle_quote = [before_last + quote_type + after_first]
    return before_quote + middle_quote + after_quote


def quote_exception(
    cur_chr,
    prev_chr,
    prev_prev_chr,
    prev_prev_prev_chr,
    single_stack,
    double_stack,
):
    if cur_chr in ["'", "’"]:
        # expt [1900's, 5'30]
        if prev_chr in numbers:
            do_push_pop_symbol(single_stack, "'")

    if cur_chr in ["\"", "”"]:
        # expt [60" inch]
        if prev_chr in numbers:
            do_push_pop_symbol(double_stack, '"')

    if cur_chr == "s":
        # expt [He's, Jimmy's, KAKAO's]
        if prev_chr in ["'", "`", "‘", "’"]:
            if prev_prev_chr == lower_alphabets + upper_alphabets:
                do_push_pop_symbol(single_stack, "'")

    if prev_prev_chr + prev_chr + cur_chr in [
            "n't",
            "n’t",  # don't, doesn't, can't
            "I'm",
            "I’m",
            "I'd",
            "I’d",
    ]:
        do_push_pop_symbol(single_stack, "'")

    if prev_prev_prev_chr + prev_prev_chr + prev_chr + cur_chr in [
            "I've",
            "I’ve",  # I've
            "u've",
            "u’ve",  # you've
            "e've",
            "e’ve",  # he've, she've, we've
            "y've",
            "y’ve",  # they've
            "ou'd",
            "ou’d",  # you'd
            "ey'd",
            "ey’d",  # they'd
            "he'd",
            "he’d",  # he'd, she'd
            "we'd",
            "we’d",
            "u're",
            "u’re",  # you're
            "y're",
            "y’re",  # they're
            "I'll",
            "I’ll",
            "u'll",
            "u’ll",  # you'll
            "e'll",
            "e’ll",  # He'll
            "y'll",
            "y’ll",  # they'll
            "o'cl",
            "o’cl",  # 10 o'clock
            "O'cl",
            "O’cl",  # 10 O'clock
            "O'Cl",
            "O’Cl",  # 10 O'Clock
    ]:
        do_push_pop_symbol(single_stack, "'")


def split_sentences(text: str):
    prev_chr: str = ""
    prev_prev_chr: str = ""
    prev_prev_prev_chr: str = ""

    cur_sentence: str = ""
    results: List[str] = []
    cur_stat: int = Stats.DEFAULT

    single_quote_stack: List[str] = []
    double_quote_stack: List[str] = []
    last_single_quote_pos = 0
    last_double_quote_pos = 0

    for i, chr_string in enumerate(text):
        if cur_stat == Stats.DEFAULT:
            if chr_string in ["\"", "“", "”"]:
                # Double Quotes
                do_push_pop_symbol(double_quote_stack, "\"")
                last_double_quote_pos = i
            elif chr_string in ["'", "`", "‘", "’"]:
                # Single Quotes
                do_push_pop_symbol(single_quote_stack, "'")
                last_single_quote_pos = i
            elif chr_string == "다":
                if empty(double_quote_stack) and empty(single_quote_stack) and (
                        _map[Stats.DA][prev_chr] & ID.PREV):
                    cur_stat = Stats.DA
            elif chr_string == "요":
                if empty(double_quote_stack) and empty(single_quote_stack) and (
                        _map[Stats.YO][prev_chr] & ID.PREV):
                    cur_stat = Stats.YO
            elif chr_string == "죠":
                if empty(double_quote_stack) and empty(single_quote_stack) and (
                        _map[Stats.JYO][prev_chr] & ID.PREV):
                    cur_stat = Stats.JYO
            elif chr_string in [".", "!", "?"]:
                if empty(double_quote_stack) and empty(single_quote_stack) and (
                        _map[Stats.SB][prev_chr] & ID.PREV):
                    cur_stat = Stats.SB

            quote_exception(
                chr_string,
                prev_chr,
                prev_prev_chr,
                prev_prev_prev_chr,
                single_quote_stack,
                double_quote_stack,
            )

        else:
            endif = False
            # work like 'goto'

            if not endif:
                # Space
                if chr_string == " " or \
                        _map[Stats.COMMON][chr_string] & ID.CONT:

                    if _map[cur_stat][prev_chr] & ID.NEXT1:
                        cur_sentence = do_trim_sent_push_results(
                            cur_sentence,
                            results,
                        )
                        cur_sentence += prev_chr
                        cur_stat = Stats.DEFAULT

                    endif = True

            if not endif:
                if _map[cur_stat][chr_string] & ID.NEXT:
                    if _map[cur_stat][prev_chr] & ID.NEXT1:
                        cur_sentence += prev_chr
                    cur_stat = Stats.DEFAULT
                    endif = True

            if not endif:
                if _map[cur_stat][chr_string] & ID.NEXT1:
                    if _map[cur_stat][prev_chr] & ID.NEXT1:
                        cur_sentence = do_trim_sent_push_results(
                            cur_sentence,
                            results,
                        )
                        cur_sentence += prev_chr
                        cur_stat = Stats.DEFAULT
                    endif = True

            if not endif:
                if _map[cur_stat][chr_string] & ID.NEXT2:
                    if _map[cur_stat][prev_chr] & ID.NEXT1:
                        cur_sentence += prev_chr
                    else:
                        cur_sentence = do_trim_sent_push_results(
                            cur_sentence, results)
                    cur_stat = Stats.DEFAULT
                    endif = True

            if not endif:
                if not _map[cur_stat][chr_string] or \
                        _map[cur_stat][chr_string] & ID.PREV:  # NOT exists

                    cur_sentence = do_trim_sent_push_results(
                        cur_sentence, results)
                    if _map[cur_stat][prev_chr] & ID.NEXT1:
                        cur_sentence += prev_chr
                    cur_stat = Stats.DEFAULT

                    # It's not a good design we suppose, but it's the best unless we change the whole structure.
                    if chr_string in ["\"", "“", "”"]:
                        do_push_pop_symbol(double_quote_stack, "\"")
                    elif chr_string in ["'", "`", "‘", "’"]:
                        do_push_pop_symbol(single_quote_stack, "'")

                    endif = True

        # endif:
        if cur_stat == Stats.DEFAULT or not (_map[cur_stat][chr_string] &
                                             ID.NEXT1):
            cur_sentence += chr_string

        prev_prev_prev_chr = prev_prev_chr
        prev_prev_chr = prev_chr
        prev_chr = chr_string

    if not empty(cur_sentence):
        cur_sentence = do_trim_sent_push_results(cur_sentence, results)

    if _map[cur_stat][prev_chr] & ID.NEXT1:
        cur_sentence += prev_chr
        cur_sentence = do_trim_sent_push_results(cur_sentence, results)

    if len(single_quote_stack) != 0:
        results = realign_by_quote(text, last_single_quote_pos, "'")

    if len(double_quote_stack) != 0:
        results = realign_by_quote(text, last_double_quote_pos, "\"")

    return results


def split_sentences_index(text) -> List[SentenceIndex]:
    sentences = split_sentences(text)
    sentence_indexes = []
    offset = 0
    for sentence in sentences:
        sentence_indexes.append(
            SentenceIndex(offset + text.index(sentence),
                          offset + text.index(sentence) + len(sentence)))
        offset += text.index(sentence) + len(sentence)
        text = text[text.index(sentence) + len(sentence):]
    return sentence_indexes


def split_chunks(
    text: str,
    max_length=128,
    overlap=False,
    indexes=None,
) -> List[ChunkWithIndex]:

    def get_chunk_with_index():
        start = span[0].start
        end = span[-1].end
        return ChunkWithIndex(span[0].start, text[start:end])

    if (indexes is None):
        indexes = split_sentences_index(text)
    span = []
    chunks = []
    for index in indexes:
        if (len(span) > 0):
            if (index.end - span[0].start >
                    max_length):  # len = last_end - first_start
                chunks.append(get_chunk_with_index())
                if (overlap):
                    span = span[math.trunc(len(span) / 2):]  # cut half
                else:
                    span = []
        span.append(index)
    chunks.append(get_chunk_with_index())
    return chunks

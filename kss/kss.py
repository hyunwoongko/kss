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

import math
from typing import List

# functions
# classes
from kss.base import (
    ID,
    BackupManager,
    ChunkWithIndex,
    Const,
    QuoteException,
    SentenceIndex,
    Stats,
    do_push_pop_symbol,
    do_trim_sent_push_results,
    empty,
)

# postprocessing methods
# mapping table
from kss.rule import (
    Table,
    post_processing_da,
    post_processing_ham,
    post_processing_jyo,
    post_processing_um,
    post_processing_yo,
)


# TODO (bug) : 책을 봤다. 고구려에 관한
def realign_by_quote(
    text,
    last_quote_pos,
    quote_type,
    use_heuristic,
    max_recover_step,
    max_recover_length,
    ignore_quotes_or_brackets,
    recover_step,
):
    before_quote = _split_sentences(
        text[:last_quote_pos],
        use_heuristic=use_heuristic,
        max_recover_step=max_recover_step,
        max_recover_length=max_recover_length,
        ignore_quotes_or_brackets=ignore_quotes_or_brackets,
        recover_step=recover_step,
    )

    before_last = before_quote[-1] if len(before_quote) > 0 else ""
    before_quote = [] if len(before_quote) == 1 else before_quote[:-1]

    after_quote = _split_sentences(
        text[last_quote_pos + 1 :],
        use_heuristic=use_heuristic,
        max_recover_step=max_recover_step,
        max_recover_length=max_recover_length,
        ignore_quotes_or_brackets=ignore_quotes_or_brackets,
        recover_step=recover_step,
    )

    after_first = after_quote[0] if len(after_quote) > 0 else ""
    after_quote = [] if len(after_quote) == 1 else after_quote[1:]

    middle_quote = [before_last] + [quote_type + after_first]
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

        find_quotes = False
        for qt in Const.single_quotes + Const.double_quotes + Const.bracket:
            if qt in res:
                find_quotes = True
                break

        if not find_quotes:
            for post in post_processing_list:
                if post in res:
                    split_idx += list(find_all(res, post))

        split_idx = sorted(split_idx)
        final_results += lindexsplit(res, *split_idx)

    return final_results


quote_exception = QuoteException()

endpoint = (
    Const.single_quotes
    + Const.double_quotes
    + Const.bracket
    + Const.punctuation
    + [" ", ""]
)

need_to_replace_zwsp = Const.single_quotes + Const.double_quotes + Const.bracket


def split_sentences(
    text: str,
    use_heuristic: bool = True,
    max_recover_step: int = 5,
    max_recover_length: int = 30000,
    ignore_quotes_or_brackets=False,
):
    """
    split document to sentence

    Args:
        text (str):
            input text
        use_heuristic (bool):
            use heuristic algorithms or not
        max_recover_step (int):
            maximum step for quote and bracket misalignment recovering
        max_recover_length (int):
            maximum text length to recover when quote and bracket misaligned
        ignore_quotes_or_brackets (bool):
            ignore quotes or bracket processing

    Returns:
        (List[str]): list of sentences
    """
    return _split_sentences(
        text,
        use_heuristic,
        max_recover_step,
        max_recover_length,
        ignore_quotes_or_brackets,
    )


def _split_sentences(
    text: str,
    use_heuristic: bool,
    max_recover_step: int,
    max_recover_length: int,
    ignore_quotes_or_brackets: bool,
    recover_step: int = 0,
):
    if len(text) > max_recover_length:
        max_recover_step = 0

    text = text.replace("\u200b", "")
    backup_manager = BackupManager()

    double_quote_stack = []
    single_quote_stack = []
    bracket_stack = []

    for i in range(0, len(text)):
        if text[i] in ["다", "요", "죠", "함", "음"]:
            if i != len(text) - 1:
                if text[i + 1] not in endpoint:
                    target_to_backup = text[i] + text[i + 1]
                    backup_manager.add_item_to_dict(
                        key=target_to_backup, val=str(abs(hash(target_to_backup)))
                    )

    text = backup_manager.backup(text)
    for s in need_to_replace_zwsp:
        text = text.replace(s, f"\u200b{s}\u200b")

    prev_1: str = ""
    prev_2: str = ""
    prev_3: str = ""
    prev_4: str = ""

    cur_sentence: str = ""
    results: List[str] = []
    cur_stat: int = Stats.DEFAULT

    last_single_quote_pos = 0
    last_double_quote_pos = 0
    last_bracket_pos = 0

    single_quote_pop = "'"
    double_quote_pop = '"'
    bracket_pop = " "

    for i, ch in enumerate(text):
        if cur_stat == Stats.DEFAULT:
            if ch in Const.double_quotes:
                if not ignore_quotes_or_brackets:
                    if ch in Const.double_quotes_open_to_close.keys():
                        double_quote_pop = do_push_pop_symbol(
                            double_quote_stack,
                            Const.double_quotes_open_to_close[ch],
                            ch,
                        )
                    else:
                        double_quote_pop = do_push_pop_symbol(
                            double_quote_stack,
                            Const.double_quotes_close_to_open[ch],
                            ch,
                        )
                    last_double_quote_pos = i

            elif ch in Const.single_quotes:
                if not ignore_quotes_or_brackets:
                    if ch in Const.single_quotes_open_to_close.keys():
                        single_quote_pop = do_push_pop_symbol(
                            single_quote_stack,
                            Const.single_quotes_open_to_close[ch],
                            ch,
                        )
                    else:
                        single_quote_pop = do_push_pop_symbol(
                            single_quote_stack,
                            Const.single_quotes_close_to_open[ch],
                            ch,
                        )
                    last_single_quote_pos = i

            elif ch in Const.bracket:
                if not ignore_quotes_or_brackets:
                    if ch in Const.bracket_open_to_close.keys():
                        bracket_pop = do_push_pop_symbol(
                            bracket_stack,
                            Const.bracket_open_to_close[ch],
                            ch,
                        )
                    else:
                        bracket_pop = do_push_pop_symbol(
                            bracket_stack,
                            Const.bracket_close_to_open[ch],
                            ch,
                        )
                    last_bracket_pos = i

            elif ch in [".", "!", "?"]:
                if (
                    empty(double_quote_stack)
                    and empty(single_quote_stack)
                    and empty(bracket_stack)
                    and (Table[Stats.SB][prev_1] & ID.PREV)
                ):
                    cur_stat = Stats.SB

            if use_heuristic is True:
                if ch == "다":
                    if (
                        empty(double_quote_stack)
                        and empty(single_quote_stack)
                        and empty(bracket_stack)
                        and (Table[Stats.DA][prev_1] & ID.PREV)
                    ):
                        cur_stat = Stats.DA
                elif ch == "요":
                    if (
                        empty(double_quote_stack)
                        and empty(single_quote_stack)
                        and empty(bracket_stack)
                        and (Table[Stats.YO][prev_1] & ID.PREV)
                    ):
                        cur_stat = Stats.YO
                elif ch == "죠":
                    if (
                        empty(double_quote_stack)
                        and empty(single_quote_stack)
                        and empty(bracket_stack)
                        and (Table[Stats.JYO][prev_1] & ID.PREV)
                    ):
                        cur_stat = Stats.JYO
                elif ch == "함":
                    if (
                        empty(double_quote_stack)
                        and empty(single_quote_stack)
                        and empty(bracket_stack)
                        and (Table[Stats.HAM][prev_1] & ID.PREV)
                    ):
                        cur_stat = Stats.HAM
                elif ch == "음":
                    if (
                        empty(double_quote_stack)
                        and empty(single_quote_stack)
                        and empty(bracket_stack)
                        and (Table[Stats.UM][prev_1] & ID.PREV)
                    ):
                        cur_stat = Stats.UM

            if not ignore_quotes_or_brackets:
                quote_exception.process(
                    ch,
                    prev_1,
                    prev_2,
                    prev_3,
                    prev_4,
                    single_quote_stack,
                    double_quote_stack,
                )

        else:
            if ch in Const.double_quotes:
                last_double_quote_pos = i

            elif ch in Const.single_quotes:
                last_single_quote_pos = i

            elif ch in Const.bracket:
                last_bracket_pos = i

            endif = False
            if not endif:
                # Space
                if ch == " " or Table[Stats.COMMON][ch] & ID.CONT:
                    if Table[cur_stat][prev_1] & ID.NEXT1:
                        cur_sentence = do_trim_sent_push_results(
                            cur_sentence,
                            results,
                        )
                        cur_sentence += prev_1
                        cur_stat = Stats.DEFAULT

                    endif = True

            if not endif:
                if Table[cur_stat][ch] & ID.NEXT:
                    if Table[cur_stat][prev_1] & ID.NEXT1:
                        # NEXT1 + NEXT => 자르지 않는다.
                        cur_sentence += prev_1
                    cur_stat = Stats.DEFAULT
                    endif = True

            if not endif:
                if Table[cur_stat][ch] & ID.NEXT1:
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
                if Table[cur_stat][ch] & ID.NEXT2:
                    if Table[cur_stat][prev_1] & ID.NEXT1:
                        # NEXT1 + NEXT2 => 자르지 않는다.
                        cur_sentence += prev_1
                    else:
                        # NOT(NEXT1) + NEXT2 => 자른다.
                        cur_sentence = do_trim_sent_push_results(cur_sentence, results)
                    cur_stat = Stats.DEFAULT
                    endif = True

            if not endif:
                if (
                    not Table[cur_stat][ch] or Table[cur_stat][ch] & ID.PREV
                ):  # NOT exists

                    cur_sentence = do_trim_sent_push_results(cur_sentence, results)
                    if Table[cur_stat][prev_1] & ID.NEXT1:
                        cur_sentence += prev_1
                    cur_stat = Stats.DEFAULT

                    # It's not a good design we suppose, but it's the best unless we change the whole structure.
                    if ch in Const.double_quotes:
                        if not ignore_quotes_or_brackets:
                            if ch in Const.double_quotes_open_to_close.keys():
                                double_quote_pop = do_push_pop_symbol(
                                    double_quote_stack,
                                    Const.double_quotes_open_to_close[ch],
                                    ch,
                                )
                            else:
                                double_quote_pop = do_push_pop_symbol(
                                    double_quote_stack,
                                    Const.double_quotes_close_to_open[ch],
                                    ch,
                                )
                            last_double_quote_pos = i

                    elif ch in Const.single_quotes:
                        if not ignore_quotes_or_brackets:
                            if ch in Const.single_quotes_open_to_close.keys():
                                single_quote_pop = do_push_pop_symbol(
                                    single_quote_stack,
                                    Const.single_quotes_open_to_close[ch],
                                    ch,
                                )
                            else:
                                single_quote_pop = do_push_pop_symbol(
                                    single_quote_stack,
                                    Const.single_quotes_close_to_open[ch],
                                    ch,
                                )
                            last_single_quote_pos = i

                    elif ch in Const.bracket:
                        if not ignore_quotes_or_brackets:
                            if ch in Const.bracket_open_to_close.keys():
                                bracket_pop = do_push_pop_symbol(
                                    bracket_stack,
                                    Const.bracket_open_to_close[ch],
                                    ch,
                                )
                            else:
                                bracket_pop = do_push_pop_symbol(
                                    bracket_stack,
                                    Const.bracket_close_to_open[ch],
                                    ch,
                                )
                            last_bracket_pos = i
                    endif = True

        # endif:
        if cur_stat == Stats.DEFAULT or not (Table[cur_stat][ch] & ID.NEXT1):
            cur_sentence += ch

        prev_4 = prev_3
        prev_3 = prev_2
        prev_2 = prev_1
        prev_1 = ch

    if not empty(cur_sentence):
        cur_sentence = do_trim_sent_push_results(cur_sentence, results)

    if Table[cur_stat][prev_1] & ID.NEXT1:
        cur_sentence += prev_1
        do_trim_sent_push_results(cur_sentence, results)

    if use_heuristic is True:
        if "다 " in text:
            results = post_processing(results, post_processing_da)

        if "요 " in text:
            results = post_processing(results, post_processing_yo)

        if "죠 " in text:
            results = post_processing(results, post_processing_jyo)

        if "함 " in text:
            results = post_processing(results, post_processing_ham)

        if "음 " in text:
            results = post_processing(results, post_processing_um)

    if len(single_quote_stack) != 0 and recover_step < max_recover_step:
        results = realign_by_quote(
            text,
            last_single_quote_pos,
            single_quote_pop,
            use_heuristic,
            max_recover_step,
            max_recover_length,
            ignore_quotes_or_brackets,
            recover_step + 1,
        )

    if len(double_quote_stack) != 0 and recover_step < max_recover_step:
        results = realign_by_quote(
            text,
            last_double_quote_pos,
            double_quote_pop,
            use_heuristic,
            max_recover_step,
            max_recover_length,
            ignore_quotes_or_brackets,
            recover_step + 1,
        )

    if len(bracket_stack) != 0 and recover_step < max_recover_step:
        results = realign_by_quote(
            text,
            last_bracket_pos,
            bracket_pop,
            use_heuristic,
            max_recover_step,
            max_recover_length,
            ignore_quotes_or_brackets,
            recover_step + 1,
        )

    results = [backup_manager.restore(s).replace("\u200b", "").strip() for s in results]

    return results


def split_sentences_index(text, **kwargs) -> List[SentenceIndex]:
    sentences = split_sentences(text, **kwargs)
    sentence_indexes = []
    offset = 0

    for sentence in sentences:
        sentence_indexes.append(
            SentenceIndex(
                offset + text.index(sentence),
                offset + text.index(sentence) + len(sentence),
            )
        )
        offset += text.index(sentence) + len(sentence)
        text = text[text.index(sentence) + len(sentence) :]
    return sentence_indexes


def split_chunks(
    text: str,
    max_length=128,
    overlap=False,
    indexes=None,
    **kwargs,
) -> List[ChunkWithIndex]:
    def get_chunk_with_index():
        start = span[0].start
        end = span[-1].end
        return ChunkWithIndex(
            span[0].start,
            text[start:end],
        )

    if indexes is None:
        indexes = split_sentences_index(text, **kwargs)

    span = []
    chunks = []
    for index in indexes:
        if len(span) > 0:
            if index.end - span[0].start > max_length:  # len = last_end - first_start
                chunks.append(get_chunk_with_index())
                if overlap:
                    span = span[math.trunc(len(span) / 2) :]  # cut half
                else:
                    span = []
        span.append(index)
    chunks.append(get_chunk_with_index())
    return chunks

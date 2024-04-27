# This code is copied from soynlp [https://github.com/lovit/soynlp]
# And modified by Hyunwoong Ko [https://github.com/hyuwoongko]

import re
import sys
from functools import partial
from typing import Union, Tuple, Dict, Any, List

from kss._modules.preprocessing.completed_form import _incompleted_form_ratio
from kss._utils.multiprocessing import _run_job
from kss._utils.sanity_checks import _check_type, _check_num_workers, _check_text

hangul_pattern = re.compile(r'[ㄱ-ㅎㅏ-ㅣ가-힣]')
symbols_pattern = re.compile("#+")
punctuations = {'.', '!', '?', '。'}
parenthesis = {'(', ')', '[', ']', '{', '}', '<', '>'}
ellipsis_marks = {"...", "[...]", "(...)", "…", "[…]"}


def _get_ngrams(input_list, n):
    # Fast function to return n-grams from a list of tokens.
    return [item for item in zip(*[input_list[i:] for i in range(n)])]


def _repeating_top_ngram_score(text, n):
    split_text = text.strip().split()
    ngrams = _get_ngrams(split_text, n)
    unique_ngrams = set(ngrams)

    # Find the most frequent ngram in the zipped ngram list
    counts = {
        ngram: {"freq": 0, "num_chars": sum(len(word) for word in ngram)}
        for ngram in unique_ngrams
    }

    for ngram in ngrams:
        counts[ngram]["freq"] += 1
    most_frqnt_ngram = " ".join(max(counts, key=lambda x: counts[x]["freq"]))

    # Find the number of characters the most frequent ngram
    # contributes to the document
    nchar = len(text)
    len_diff = nchar - len(text.replace(most_frqnt_ngram, ""))
    if nchar > 0:
        score = len_diff / nchar
    else:
        # Remove if the document is empty
        score = 1.0
    return score


def _repeating_duplicated_ngrams_score(text, n):
    split_text = text.strip().split()
    ngrams = _get_ngrams(split_text, n)

    counts = {}
    duplicated_nchar = 0
    overlapping_ngrams = 0

    for ngram in ngrams:
        counts[ngram] = counts.get(ngram, 0) + 1
        if counts[ngram] > 1:
            # Count the number of characters in this ngram that haven't been counted already
            duplicated_ngrams = sum(
                len(gram) for gram in ngram[overlapping_ngrams:]
            )
            # Count the spaces between the ngrams
            nspaces = min(n - overlapping_ngrams, n - 1)
            duplicated_nchar += duplicated_ngrams + nspaces
            overlapping_ngrams = n
        overlapping_ngrams = max(overlapping_ngrams - 1, 0)

    nchar = len(text)
    if nchar > 0:
        score = duplicated_nchar / nchar
    else:
        # Remove if the document is empty
        score = 1.0
    return score


def _num_line_by_repeats(text, split_delimiter='\n'):
    split_lines_by_char = [l.strip() for l in text.split(split_delimiter) if len(l.strip()) > 0]
    counter_dict = {}
    for c in split_lines_by_char:
        counter_dict[c] = counter_dict.get(c, 0) + 1

    return max(counter_dict.values())


def _num_line_by_char_repeats(text, split_delimiter='\n'):
    split_lines_by_char = [l.strip()[0] for l in text.split(split_delimiter) if len(l.strip()) > 0]
    counter_dict = {}
    for c in split_lines_by_char:
        counter_dict[c] = counter_dict.get(c, 0) + 1
    return max(counter_dict.values())


def _lines_started_with_bullets_ratio(text):
    lines = [x.strip() for x in text.split('\n') if len(x.strip()) > 0]
    calculated_ratio = sum([x[0] in "•‣⁃⁌⁍∙○●◘◦⦾⦿" for x in lines])
    return calculated_ratio / len(lines)


def _lines_ends_with_ellipsis_ratio(text):
    lines = [x.strip() for x in text.split('\n') if len(x.strip()) > 0]
    num_lines_ends_with_ellipsis = 0
    for line in lines:
        is_lines_ends_with_ellipsis = any([line.endswith(e) for e in ellipsis_marks])
        if is_lines_ends_with_ellipsis:
            num_lines_ends_with_ellipsis += 1
    return num_lines_ends_with_ellipsis / len(lines)


def _symbols_to_word_ratio(text):
    num_symbol_words = 0
    words = text.strip().split()
    for word in words:
        word = word.strip()
        symbol_ratio = len(symbols_pattern.findall(word)) / len(word)
        if word in ellipsis_marks or symbol_ratio > 0.5:
            num_symbol_words += 1
    return num_symbol_words / len(words)


def filter_out(
    text: Union[str, List[str], Tuple[str]],
    min_length: int = 0,
    max_length: int = sys.maxsize,
    min_mean_words_length: int = 0,
    max_mean_words_length: int = sys.maxsize,
    min_words: int = 0,
    max_words: int = sys.maxsize,
    min_lines: int = 0,
    max_lines: int = sys.maxsize,
    min_paragraphs: int = 0,
    max_paragraphs: int = sys.maxsize,
    min_alphabet_ratio: float = 0,
    max_alphabet_ratio: float = 1,
    min_alphanumeric_ratio: float = 0,
    max_alphanumeric_ratio: float = 1,
    min_number_ratio: float = 0,
    max_number_ratio: float = 1,
    min_punctuation_ratio: float = 0,
    max_punctuation_ratio: float = 1,
    min_symbols_to_words_ratio: float = 0,
    max_symbols_to_words_ratio: float = 1,
    min_lines_started_with_bullets_ratio: float = 0,
    max_lines_started_with_bullets_ratio: float = 1,
    min_whitespace_ratio: float = 0,
    max_whitespace_ratio: float = 1,
    min_parenthesis_ratio: float = 0,
    max_parenthesis_ratio: float = 1,
    min_ellipsis_ratio: float = 0,
    max_ellipsis_ratio: float = 1,
    min_hangul_ratio: float = 0,
    max_hangul_ratio: float = 1,
    max_words_length: int = sys.maxsize,
    max_line_repeats: int = sys.maxsize,
    max_line_by_char_repeats: int = sys.maxsize,
    max_paragraph_repeats: int = sys.maxsize,
    max_paragraph_by_char_repeats: int = sys.maxsize,
    max_repeating_top_ngram_repeats_score: float = sys.maxsize,
    max_repeating_duplicate_ngrams_score: float = sys.maxsize,
    ngram_size_for_repeating_top_ngram_repeats: int = 3,
    ngram_size_for_repeating_duplicate_ngrams: int = 3,
    max_hangul_incompleted_form_ratio: float = 1,
    num_workers: Union[int, str] = "auto",
) -> Union[Tuple[bool, Dict[str, Any]], List[Tuple[bool, Dict[str, Any]]]]:
    """
    This filters out bad text based on various conditions.

    Args:
        text (Union[str, List[str], Tuple[str]]): single text or list of texts
        min_length (int): minimum length of text
        max_length (int): maximum length of text
        min_mean_words_length (int): minimum mean words length
        max_mean_words_length (int): maximum mean words length
        min_words (int): minimum number of words
        max_words (int): maximum number of words
        min_lines (int): minimum number of lines
        max_lines (int): maximum number of lines
        min_paragraphs (int): minimum number of paragraphs
        max_paragraphs (int): maximum number of paragraphs
        min_alphabet_ratio (float): minimum alphabet ratio
        max_alphabet_ratio (float): maximum alphabet ratio
        min_alphanumeric_ratio (float): minimum alphanumeric ratio
        max_alphanumeric_ratio (float): maximum alphanumeric ratio
        min_number_ratio (float): minimum number ratio
        max_number_ratio (float): maximum number ratio
        min_punctuation_ratio (float): minimum punctuation ratio
        max_punctuation_ratio (float): maximum punctuation ratio
        min_symbols_to_words_ratio (float): minimum symbols to words ratio
        max_symbols_to_words_ratio (float): maximum symbols to words ratio
        min_lines_started_with_bullets_ratio (float): minimum lines started with bullets ratio
        max_lines_started_with_bullets_ratio (float): maximum lines started with bullets ratio
        min_whitespace_ratio (float): minimum whitespace ratio
        max_whitespace_ratio (float): maximum whitespace ratio
        min_parenthesis_ratio (float): minimum parenthesis ratio
        max_parenthesis_ratio (float): maximum parenthesis ratio
        min_ellipsis_ratio (float): minimum ellipsis ratio
        max_ellipsis_ratio (float): maximum ellipsis ratio
        min_hangul_ratio (float): minimum hangul ratio
        max_hangul_ratio (float): maximum hangul ratio
        max_words_length (int): maximum words length
        max_line_repeats (int): maximum line repeats
        max_line_by_char_repeats (int): maximum line by char repeats
        max_paragraph_repeats (int): maximum paragraph repeats
        max_paragraph_by_char_repeats (int): maximum paragraph by char repeats
        max_repeating_top_ngram_repeats_score (float): maximum repeating top ngram repeats score
        max_repeating_duplicate_ngrams_score (float): maximum repeating duplicate ngrams score
        ngram_size_for_repeating_top_ngram_repeats (int): ngram size for repeating top ngram repeats
        ngram_size_for_repeating_duplicate_ngrams (int): ngram size for repeating duplicate ngrams
        max_hangul_incompleted_form_ratio (float): maximum hangul non completed form ratio
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[Tuple[bool, Dict[str, Any]], List[Tuple[bool, Dict[str, Any]]]]: filtered out text or list of filtered out texts

    Examples:
        >>> from kss import Kss
        >>> filter_out = Kss("filter_out")
        >>> text = "▲ 12월 17일 (목)=============================================================================시간 경기내용 방송사=============================================================================[축구] 프랑스 리그 103:00 (AS모나코-스타드 렌) SBS스포츠[축구] 09-10 UEFA 유로파리그04:00 (스파르타프라하-FC코펜하겐) MBC-ESPN[축구] 09-10 프리미어리그05:00 (토트넘-맨체스터시티) SBS스포츠-----------------------------------------------------------------------------[농구] 2009-10 NBA10:00 (LA레이커스-밀워키) SBS스포츠[농구] 2009-10 신한은행 여자농구17:00 (삼성생명-금호생명) SBS스포츠[농구] 2009-10 KCC 프로농구19:00 (KCC-KT) MBC-ESPN19:00 (LG-SK) SBS스포츠-----------------------------------------------------------------------------[배구] 2009-10 NH농협 V리그17:00 (흥국생명-현대건설)19:00 (대한항공-신협상무) KBS N 스포츠-----------------------------------------------------------------------------19:20 [핸드볼] 2009 세계여자선수권대회-----------------------------------------------------------------------------19:00 [배드민턴] 한국 최강전=============================================================================※ 상기 경기일정 및 방송 편성정보는 사정에 따라 변동될 수 있습니다< pre >/한국아이닷컴 뉴스부 한국아이닷컴 뉴스부 '스타화보 VM' 무료다운받기 [**8253+NATE 또는 통화] [ⓒ 인터넷한국일보(www.hankooki.com), 무단 전재 및 재배포 금지]"
        >>> output = filter_out(text, min_mean_words_length=2, max_mean_words_length=10)
        >>> print(output)
        (True, {'reason': 'mean_words_length', 'value': 13.025316455696203})
    """
    text, finish = _check_text(text)

    if finish:
        return True, {"reason": "unsupported_text_type", "value": text}

    min_length = _check_type(min_length, "min_length", int)
    max_length = _check_type(max_length, "max_length", int)
    min_mean_words_length = _check_type(min_mean_words_length, "min_mean_words_length", int)
    max_mean_words_length = _check_type(max_mean_words_length, "max_mean_words_length", int)
    min_words = _check_type(min_words, "min_words", int)
    max_words = _check_type(max_words, "max_words", int)
    min_lines = _check_type(min_lines, "min_lines", int)
    max_lines = _check_type(max_lines, "max_lines", int)
    min_paragraphs = _check_type(min_paragraphs, "min_paragraphs", int)
    max_paragraphs = _check_type(max_paragraphs, "max_paragraphs", int)
    min_alphabet_ratio = _check_type(min_alphabet_ratio, "min_alphabet_ratio", float)
    max_alphabet_ratio = _check_type(max_alphabet_ratio, "max_alphabet_ratio", float)
    min_alphanumeric_ratio = _check_type(min_alphanumeric_ratio, "min_alphanumeric_ratio", float)
    max_alphanumeric_ratio = _check_type(max_alphanumeric_ratio, "max_alphanumeric_ratio", float)
    min_number_ratio = _check_type(min_number_ratio, "min_number_ratio", float)
    max_number_ratio = _check_type(max_number_ratio, "max_number_ratio", float)
    min_punctuation_ratio = _check_type(min_punctuation_ratio, "min_punctuation_ratio", float)
    max_punctuation_ratio = _check_type(max_punctuation_ratio, "max_punctuation_ratio", float)
    min_symbols_to_words_ratio = _check_type(min_symbols_to_words_ratio, "min_symbols_to_words_ratio", float)
    max_symbols_to_words_ratio = _check_type(max_symbols_to_words_ratio, "max_symbols_to_words_ratio", float)
    min_lines_started_with_bullets_ratio = _check_type(min_lines_started_with_bullets_ratio,
                                                       "min_lines_started_with_bullets_ratio", float)
    max_lines_started_with_bullets_ratio = _check_type(max_lines_started_with_bullets_ratio,
                                                       "max_lines_started_with_bullets_ratio", float)
    min_whitespace_ratio = _check_type(min_whitespace_ratio, "min_whitespace_ratio", float)
    max_whitespace_ratio = _check_type(max_whitespace_ratio, "max_whitespace_ratio", float)
    min_parenthesis_ratio = _check_type(min_parenthesis_ratio, "min_parenthesis_ratio", float)
    max_parenthesis_ratio = _check_type(max_parenthesis_ratio, "max_parenthesis_ratio", float)
    min_ellipsis_ratio = _check_type(min_ellipsis_ratio, "min_ellipsis_ratio", float)
    max_ellipsis_ratio = _check_type(max_ellipsis_ratio, "max_ellipsis_ratio", float)
    min_hangul_ratio = _check_type(min_hangul_ratio, "min_hangul_ratio", float)
    max_hangul_ratio = _check_type(max_hangul_ratio, "max_hangul_ratio", float)
    max_words_length = _check_type(max_words_length, "max_words_length", int)
    max_line_repeats = _check_type(max_line_repeats, "max_line_repeats", int)
    max_line_by_char_repeats = _check_type(max_line_by_char_repeats, "max_line_by_char_repeats", int)
    max_paragraph_repeats = _check_type(max_paragraph_repeats, "max_paragraph_repeats", int)
    max_paragraph_by_char_repeats = _check_type(max_paragraph_by_char_repeats, "max_paragraph_by_char_repeats", int)
    max_repeating_top_ngram_repeats_score = _check_type(max_repeating_top_ngram_repeats_score,
                                                        "max_repeating_top_ngram_repeats_score", int)
    max_repeating_duplicate_ngrams_score = _check_type(max_repeating_duplicate_ngrams_score,
                                                       "max_repeating_duplicate_ngrams_score", int)
    ngram_size_for_repeating_top_ngram_repeats = _check_type(ngram_size_for_repeating_top_ngram_repeats,
                                                             "ngram_size_for_repeating_top_ngram_repeats", int)
    ngram_size_for_repeating_duplicate_ngrams = _check_type(ngram_size_for_repeating_duplicate_ngrams,
                                                            "ngram_size_for_repeating_duplicate_ngrams", int)
    max_hangul_incompleted_form_ratio = _check_type(max_hangul_incompleted_form_ratio,
                                                      "max_hangul_incompleted_form_ratio", float)
    num_workers = _check_num_workers(text, num_workers)

    return _run_job(
        func=partial(
            _filter_out,
            min_length=min_length,
            max_length=max_length,
            min_mean_words_length=min_mean_words_length,
            max_mean_words_length=max_mean_words_length,
            min_words=min_words,
            max_words=max_words,
            min_lines=min_lines,
            max_lines=max_lines,
            min_paragraphs=min_paragraphs,
            max_paragraphs=max_paragraphs,
            min_alphabet_ratio=min_alphabet_ratio,
            max_alphabet_ratio=max_alphabet_ratio,
            min_alphanumeric_ratio=min_alphanumeric_ratio,
            max_alphanumeric_ratio=max_alphanumeric_ratio,
            min_number_ratio=min_number_ratio,
            max_number_ratio=max_number_ratio,
            min_punctuation_ratio=min_punctuation_ratio,
            max_punctuation_ratio=max_punctuation_ratio,
            min_symbols_to_words_ratio=min_symbols_to_words_ratio,
            max_symbols_to_words_ratio=max_symbols_to_words_ratio,
            min_lines_started_with_bullets_ratio=min_lines_started_with_bullets_ratio,
            max_lines_started_with_bullets_ratio=max_lines_started_with_bullets_ratio,
            min_whitespace_ratio=min_whitespace_ratio,
            max_whitespace_ratio=max_whitespace_ratio,
            min_parenthesis_ratio=min_parenthesis_ratio,
            max_parenthesis_ratio=max_parenthesis_ratio,
            min_ellipsis_ratio=min_ellipsis_ratio,
            max_ellipsis_ratio=max_ellipsis_ratio,
            min_hangul_ratio=min_hangul_ratio,
            max_hangul_ratio=max_hangul_ratio,
            max_words_length=max_words_length,
            max_line_repeats=max_line_repeats,
            max_line_by_char_repeats=max_line_by_char_repeats,
            max_paragraph_repeats=max_paragraph_repeats,
            max_paragraph_by_char_repeats=max_paragraph_by_char_repeats,
            max_repeating_top_ngram_repeats_score=max_repeating_top_ngram_repeats_score,
            max_repeating_duplicate_ngrams_score=max_repeating_duplicate_ngrams_score,
            ngram_size_for_repeating_top_ngram_repeats=ngram_size_for_repeating_top_ngram_repeats,
            ngram_size_for_repeating_duplicate_ngrams=ngram_size_for_repeating_duplicate_ngrams,
            max_hangul_incompleted_form_ratio=max_hangul_incompleted_form_ratio,
        ),
        inputs=text,
        num_workers=num_workers,
    )


def _filter_out(
    text,
    min_length=0,
    max_length=sys.maxsize,
    min_mean_words_length=0,
    max_mean_words_length=sys.maxsize,
    min_words=0,
    max_words=sys.maxsize,
    min_lines=0,
    max_lines=sys.maxsize,
    min_paragraphs=0,
    max_paragraphs=sys.maxsize,
    min_alphabet_ratio=0,
    max_alphabet_ratio=1,
    min_alphanumeric_ratio=0,
    max_alphanumeric_ratio=1,
    min_number_ratio=0,
    max_number_ratio=1,
    min_punctuation_ratio=0,
    max_punctuation_ratio=1,
    min_symbols_to_words_ratio=0,
    max_symbols_to_words_ratio=1,
    min_lines_started_with_bullets_ratio=0,
    max_lines_started_with_bullets_ratio=1,
    min_whitespace_ratio=0,
    max_whitespace_ratio=1,
    min_parenthesis_ratio=0,
    max_parenthesis_ratio=1,
    min_ellipsis_ratio=0,
    max_ellipsis_ratio=1,
    min_hangul_ratio=0,
    max_hangul_ratio=1,
    max_words_length=sys.maxsize,
    max_line_repeats=sys.maxsize,
    max_line_by_char_repeats=sys.maxsize,
    max_paragraph_repeats=sys.maxsize,
    max_paragraph_by_char_repeats=sys.maxsize,
    max_repeating_top_ngram_repeats_score=sys.maxsize,
    max_repeating_duplicate_ngrams_score=sys.maxsize,
    ngram_size_for_repeating_top_ngram_repeats=3,
    ngram_size_for_repeating_duplicate_ngrams=3,
    max_hangul_incompleted_form_ratio=1,
):
    words = text.split()
    lines = [x.strip() for x in text.split('\n') if len(x.strip()) > 0]
    paragraphs = [x.strip() for x in text.split('\n\n') if len(x.strip()) > 0]
    eps = 1e-6

    # min/max
    len_text = len(text)
    if not min_length <= len_text <= max_length:
        return True, {"reason": "length", "value": len_text}

    len_text += eps
    mean_words_length = sum(len(w) for w in words) / len(words)
    if not min_mean_words_length <= mean_words_length <= max_mean_words_length:
        return True, {"reason": "mean_words_length", "value": mean_words_length}

    len_words = len(words)
    if not min_words <= len_words <= max_words:
        return True, {"reason": "num_words", "value": len_words}

    len_lines = len(lines)
    if not min_lines <= len_lines <= max_lines:
        return True, {"reason": "num_lines", "value": len_lines}

    len_paragraphs = len(paragraphs)
    if not min_paragraphs <= len_paragraphs <= max_paragraphs:
        return True, {"reason": "num_paragraphs", "value": len_paragraphs}

    alphabet_ratio = sum(c.isalpha() for c in text) / len_text
    if not min_alphabet_ratio <= alphabet_ratio <= max_alphabet_ratio:
        return True, {"reason": "alphabet_ratio", "value": alphabet_ratio}

    alphanumeric_ratio = sum(c.isalnum() for c in text) / len_text
    if not min_alphanumeric_ratio <= alphanumeric_ratio <= max_alphanumeric_ratio:
        return True, {"reason": "alphanumeric_ratio", "value": alphanumeric_ratio}

    digits_ratio = sum(c.isdigit() for c in text) / len_text
    if not min_number_ratio <= digits_ratio <= max_number_ratio:
        return True, {"reason": "number_ratio", "value": digits_ratio}

    punctuation_ratio = sum(c in punctuations for c in text) / len_text
    if not min_punctuation_ratio <= punctuation_ratio <= max_punctuation_ratio:
        return True, {"reason": "punctuation_ratio", "value": punctuation_ratio}

    symbols_to_word_ratio = _symbols_to_word_ratio(text)
    if not min_symbols_to_words_ratio <= symbols_to_word_ratio <= max_symbols_to_words_ratio:
        return True, {"reason": "symbols_to_words_ratio", "value": symbols_to_word_ratio}

    lines_started_with_bullets_ratio = _lines_started_with_bullets_ratio(text)
    if not min_lines_started_with_bullets_ratio <= lines_started_with_bullets_ratio <= max_lines_started_with_bullets_ratio:
        return True, {"reason": "lines_started_with_bullets_ratio", "value": lines_started_with_bullets_ratio}

    whitespace_ratio = sum(c.isspace() for c in text) / len_text
    if not min_whitespace_ratio <= whitespace_ratio <= max_whitespace_ratio:
        return True, {"reason": "whitespace_ratio", "value": whitespace_ratio}

    parenthesis_ratio = sum(c in parenthesis for c in text) / len_text
    if not min_parenthesis_ratio <= parenthesis_ratio <= max_parenthesis_ratio:
        return True, {"reason": "parenthesis_ratio", "value": parenthesis_ratio}

    ellipsis_ratio = _lines_ends_with_ellipsis_ratio(text)
    if not min_ellipsis_ratio <= ellipsis_ratio <= max_ellipsis_ratio:
        return True, {"reason": "ellipsis_ratio", "value": ellipsis_ratio}

    hangul_ratio = len(hangul_pattern.findall(text)) / len_text
    if not min_hangul_ratio <= hangul_ratio <= max_hangul_ratio:
        return True, {"reason": "hangul_ratio", "value": hangul_ratio}

    _max_words_length = max(len(w) for w in words)
    if max_words_length <= _max_words_length:
        return True, {"reason": "max_words_length", "value": _max_words_length}

    _max_line_repeats = _num_line_by_repeats(text)
    if max_line_repeats <= _max_line_repeats:
        return True, {"reason": "line_repeats", "value": _max_line_repeats}

    _max_line_by_char_repeats = _num_line_by_char_repeats(text)
    if max_line_by_char_repeats <= _max_line_by_char_repeats:
        return True, {"reason": "line_by_char_repeats", "value": _max_line_by_char_repeats}

    _max_paragraph_repeats = _num_line_by_char_repeats(text, split_delimiter='\n\n')
    if max_paragraph_repeats <= _max_paragraph_repeats:
        return True, {"reason": "paragraph_repeats", "value": _max_paragraph_repeats}

    _max_paragraph_by_char_repeats = _num_line_by_char_repeats(text, split_delimiter='\n\n')
    if max_paragraph_by_char_repeats <= _max_paragraph_by_char_repeats:
        return True, {"reason": "paragraph_by_char_repeats", "value": _max_paragraph_by_char_repeats}

    _max_repeating_top_ngram_repeats_score = _repeating_top_ngram_score(text,
                                                                        ngram_size_for_repeating_top_ngram_repeats)
    if max_repeating_top_ngram_repeats_score <= _max_repeating_top_ngram_repeats_score:
        return True, {"reason": "repeating_top_ngram_repeats_score", "value": _max_repeating_top_ngram_repeats_score}

    _max_repeating_duplicate_ngrams_score = _repeating_duplicated_ngrams_score(text,
                                                                               ngram_size_for_repeating_duplicate_ngrams)
    if max_repeating_duplicate_ngrams_score <= _max_repeating_duplicate_ngrams_score:
        return True, {"reason": "repeating_duplicate_ngrams_score", "value": _max_repeating_duplicate_ngrams_score}

    _hangul_incompleted_form_ratio = _incompleted_form_ratio(text)
    if max_hangul_incompleted_form_ratio <= _hangul_incompleted_form_ratio:
        return True, {"reason": "hangul_incompleted_form_ratio", "value": _hangul_incompleted_form_ratio}

    return False, {"reason": "pass", "value": None}

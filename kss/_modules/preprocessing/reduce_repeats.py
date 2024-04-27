# This code was copied from [soynlp](https://github.com/lovit/soynlp)
# And modified by Hyunwoong Ko [https://github.com/hyunwoongko]

import re
from functools import partial
from typing import List, Tuple, Union

from kss._utils.multiprocessing import _run_job
from kss._utils.sanity_checks import _check_num_workers, _check_text, _check_type

kor_begin = 44032
kor_end = 55203
chosung_base = 588
jungsung_base = 28
jaum_begin = 12593
jaum_end = 12622
moum_begin = 12623
moum_end = 12643

chosung_list = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ',
                'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
jungsung_list = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ',
                 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ',
                 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ',
                 'ㅡ', 'ㅢ', 'ㅣ']
jongsung_list = [
    ' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ',
    'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ',
    'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ',
    'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
jaum_list = ['ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄸ', 'ㄹ',
             'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ',
             'ㅃ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
moum_list = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ',
             'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']

repeatchars_pattern = re.compile('(\w)\\1{2,}')


def _compose(chosung, jungsung, jongsung):
    return chr(kor_begin + chosung_base * chosung_list.index(chosung) + jungsung_base * jungsung_list.index(
        jungsung) + jongsung_list.index(jongsung))


def _decompose(c):
    if not _is_hangul(c):
        return None
    i = _to_base(c)
    if jaum_begin <= i <= jaum_end:
        return c, ' ', ' '
    if moum_begin <= i <= moum_end:
        return ' ', c, ' '
    i -= kor_begin
    cho = i // chosung_base
    jung = (i - cho * chosung_base) // jungsung_base
    jong = (i - cho * chosung_base - jung * jungsung_base)
    return chosung_list[cho], jungsung_list[jung], jongsung_list[jong]


def _is_hangul(c):
    i = _to_base(c)
    return (kor_begin <= i <= kor_end) or (jaum_begin <= i <= jaum_end) or (moum_begin <= i <= moum_end)


def _is_composed_hangul(c):
    return kor_begin <= _to_base(c) <= kor_end


def _is_consonant(c):
    return jaum_begin <= _to_base(c) <= jaum_end


def _is_vowel(c):
    return moum_begin <= _to_base(c) <= moum_end


def _to_base(c):
    if type(c) == str or type(c) == int:
        return ord(c)
    else:
        raise TypeError


def _character_is_number(i):
    i = _to_base(i)
    return 48 <= i <= 57


def _character_is_english(i):
    i = _to_base(i)
    return (97 <= i <= 122) or (65 <= i <= 90)


def _character_is_punctuation(i):
    i = _to_base(i)
    return i == 33 or i == 34 or i == 39 or i == 44 or i == 46 or i == 63 or i == 96


def reduce_char_repeats(
    text: Union[str, List[str], Tuple[str]],
    num_repeats: int = 2,
    num_workers: Union[int, str] = "auto",
) -> Union[str, List[str]]:
    """
    This reduces character repeats in text.

    Args:
        text (Union[str, List[str], Tuple[str]]): single text or list of texts
        num_repeats (int): the number of character that can be repeated
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[str, List[str]]: text with reduced character repeats or list of texts with reduced character repeats

    Examples:
        >>> from kss import Kss
        >>> reduce_char_repeats = Kss("reduce_char_repeats")
        >>> text = "고고고고고고고"
        >>> output = reduce_char_repeats(text)
        >>> print(output)
        '고고'

    References:
        This was copied from [soynlp](https://github.com/lovit/soynlp) and modified by Kss
    """

    text, finish = _check_text(text)

    if finish:
        return text

    num_repeats = _check_type(num_repeats, "num_repeats", int)
    num_workers = _check_num_workers(text, num_workers)

    return _run_job(
        func=partial(_reduce_char_repeats, num_repeats=num_repeats),
        inputs=text,
        num_workers=num_workers,
    )


def reduce_emoticon_repeats(
    text: Union[str, List[str], Tuple[str]],
    num_repeats: int = 2,
    num_workers: Union[int, str] = "auto",
) -> Union[str, List[str]]:
    """
    This reduces emoticon repeats in text.

    Args:
        text (Union[str, List[str], Tuple[str]]): single text or list of texts
        num_repeats (int): the number of emoticon that can be repeated
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[str, List[str]]: text with reduced emoticon repeats or list of texts with reduced emoticon repeats

    Examples:
        >>> from kss import Kss
        >>> reduce_emoticon_repeats = Kss("reduce_emoticon_repeats")
        >>> text = "앜ㅋㅋㅋㅋㅋㅋ"
        >>> output = reduce_emoticon_repeats(text)
        >>> print(output)
        '아ㅋㅋ'

    References:
        This was copied from [soynlp](https://github.com/lovit/soynlp) and modified by Kss
    """

    text, finish = _check_text(text)

    if finish:
        return text

    num_repeats = _check_type(num_repeats, "num_repeats", int)
    num_workers = _check_num_workers(text, num_workers)

    return _run_job(
        func=partial(_reduce_emoticon_repeats, num_repeats=num_repeats),
        inputs=text,
        num_workers=num_workers,
    )


def _reduce_char_repeats(sent, num_repeats=2):
    if num_repeats > 0:
        sent = repeatchars_pattern.sub('\\1' * num_repeats, sent)
    return sent


def _reduce_emoticon_repeats(sent, num_repeats=2):
    if not sent:
        return sent

    # Pattern matching ㅋ쿠ㅜ
    def pattern(idx):
        # Jaum: 0, Moum: 1, Complete: 2, else -1
        if 12593 <= idx <= 12622:
            return 0
        elif 12623 <= idx <= 12643:
            return 1
        elif 44032 <= idx <= 55203:
            return 2
        else:
            return -1

    idxs = [pattern(ord(c)) for c in sent]
    sent_ = []
    last_idx = len(idxs) - 1
    for i, (idx, c) in enumerate(zip(idxs, sent)):
        if (0 < i < last_idx) and (idxs[i - 1] == 0 and idx == 2 and idxs[i + 1] == 1):
            cho, jung, jong = _decompose(c)
            if (cho == sent[i - 1]) and (jung == sent[i + 1]) and (jong == ' '):
                sent_.append(cho)
                sent_.append(jung)
            else:
                sent_.append(c)
        elif (i < last_idx) and (idx == 2) and (idxs[i + 1] == 0):
            cho, jung, jong = _decompose(c)
            if jong == sent[i + 1]:
                sent_.append(_compose(cho, jung, ' '))
                sent_.append(jong)
        elif (i > 0) and (idx == 2 and idxs[i - 1] == 0):
            cho, jung, jong = _decompose(c)
            if cho == sent[i - 1]:
                sent_.append(cho)
                sent_.append(jung)
        else:
            sent_.append(c)
    return reduce_char_repeats(''.join(sent_), num_repeats)

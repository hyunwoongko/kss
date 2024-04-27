from functools import partial, lru_cache
from typing import Union, List, Tuple

from kss._modules.qwerty.utils import (
    HANGUL,
    HANGUL_FIRST,
    HANGUL_LAST,
    ENGLISH,
    LEADS,
    VOWELS,
    TAILS,
    CONSONANT_FIRST,
    VOWEL_LAST,
    CONNECTABLE_CONSONANTS,
    CONNECTABLE_VOWELS,
    ENGLISH_INDEX,
    separate_hangul,
    generate_hangul,
    index_of,
    is_vowel,
)
from kss._utils.multiprocessing import _run_job
from kss._utils.sanity_checks import _check_text, _check_type, _check_num_workers


def qwerty(
    text: Union[str, List[str], Tuple[str]],
    src: str,
    tgt: str,
    num_workers: Union[int, str] = "auto",
) -> Union[str, List[str]]:
    """
    This converts text from one language to another using QWERTY keyboard layout.

    Args:
        text (Union[str, List[str], Tuple[str]]): single text or list of texts
        src (str): source language
        tgt (str): target language
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[str, List[str]]: converted text or list of converted texts

    Examples:
        >>> from kss import Kss
        >>> qwerty = Kss("qwerty")
        >>> text = "dkssudgktpdy"
        >>> qwerty(text, src="en", tgt="ko")
        '안녕하세요'
        >>> text = "안녕하세요"
        >>> qwerty(text, src="ko", tgt="en")
        'dkssudgktpdy'

    References:
        This was copied from [inko.py](https://github.com/738/inko.py) and modified by Kss
    """
    text, finish = _check_text(text)

    if finish:
        return text

    src = _check_type(src, "src", str)
    tgt = _check_type(tgt, "tgt", str)
    num_workers = _check_num_workers(text, num_workers)

    if src not in ["en", "ko"] or tgt not in ["en", "ko"]:
        raise ValueError("`src` and `tgt` must be one of 'en', 'ko'")

    return _run_job(
        func=partial(_qwerty, src=src, tgt=tgt),
        inputs=text,
        num_workers=num_workers,
    )


@lru_cache(maxsize=500)
def _qwerty(text, src, tgt):
    if src == tgt:
        return text

    if src == "en" and tgt == "ko":
        return _qwerty_en2ko(text)
    elif src == "ko" and tgt == "en":
        return _qwerty_ko2en(text)
    else:
        return text


def _qwerty_en2ko(text, allow_double_consonant=True):
    state_length = [0, 1, 1, 2, 2, 2, 3, 3, 4, 4, 5]
    transitions = [
        [1, 1, 2, 2],  # 0, EMPTY
        [3, 1, 4, 4],  # 1, 자
        [1, 1, 5, 2],  # 2, 모
        [3, 1, 4, -1],  # 3, 자자
        [6, 1, 7, 2],  # 4, 자모
        [1, 1, 2, 2],  # 5, 모모
        [9, 1, 4, 4],  # 6, 자모자
        [9, 1, 2, 2],  # 7, 자모모
        [1, 1, 4, 4],  # 8, 자모자자
        [10, 1, 4, 4],  # 9, 자모모자
        [1, 1, 4, 4],  # 10, 자모모자자
    ]

    def last(_list):
        return _list[len(_list) - 1]

    def combine(arr):
        group = []
        for i in range(len(arr)):
            h = HANGUL[arr[i]]
            if i == 0 or is_vowel(last(group)[0]) != is_vowel(h):
                group.append([])
            last(group).append(h)

        def connect(e):
            w = "".join(e)
            if w in CONNECTABLE_CONSONANTS:
                return CONNECTABLE_CONSONANTS[w]
            elif w in CONNECTABLE_VOWELS:
                return CONNECTABLE_VOWELS[w]
            else:
                return w

        group = [connect(e) for e in group]

        if len(group) == 1:
            return group[0]

        char_set = [LEADS, VOWELS, TAILS]

        code = []
        try:
            code = [index_of(w, char_set[i]) for i, w in enumerate(group)]
        except IndexError:
            pass

        if len(code) < 3:
            code.append(-1)

        return generate_hangul(code)

    def finalize():
        length = len(text)
        last = -1
        result = []
        state = 0
        temp_dict = {
            "tmp": []
        }

        def flush():
            if len(temp_dict["tmp"]) > 0:
                result.append(combine(temp_dict["tmp"]))
            temp_dict["tmp"] = []

        for i in range(length):
            char = text[i]
            if char not in ENGLISH_INDEX:
                state = 0
                flush()
                result.append(char)
            else:
                curr = ENGLISH_INDEX[char]

                def transition():
                    c = (HANGUL[last] if last > -1 else "") + HANGUL[curr]
                    last_is_vowel = is_vowel(HANGUL[last])
                    curr_is_vowel = is_vowel(HANGUL[curr])
                    if not curr_is_vowel:
                        if last_is_vowel:
                            return 0 if index_of("ㄸㅃㅉ", HANGUL[curr]) == -1 else 1
                        if state == 1 and not allow_double_consonant:
                            return 1
                        return 0 if c in CONNECTABLE_CONSONANTS else 1
                    elif last_is_vowel:
                        return 2 if c in CONNECTABLE_VOWELS else 3

                    return 2

                _transition = transition()
                next_state = transitions[state][_transition]
                temp_dict["tmp"].append(curr)
                diff = len(temp_dict["tmp"]) - state_length[next_state]

                if diff > 0:
                    result.append(combine(temp_dict["tmp"][0:diff]))
                    temp_dict["tmp"] = temp_dict["tmp"][diff:]
                state = next_state
                last = curr

        flush()
        return "".join(result)

    return finalize()


def _qwerty_ko2en(text):
    result = ""
    if text == "" or text is None:
        return result
    _seperated = [-1, -1, -1, -1, -1]

    for i in range(len(text)):
        _hangul_text = text[i]
        _code = ord(_hangul_text)

        if (HANGUL_FIRST <= _code <= HANGUL_LAST) or (CONSONANT_FIRST <= _code <= VOWEL_LAST):
            # 가 ~ 힣 사이에 있는 한글일 때
            _seperated = separate_hangul(_hangul_text)
        else:
            # 한글이 아닐 때
            result += _hangul_text
            _seperated = [-1, -1, -1, -1, -1]

        for j in range(len(_seperated)):
            if _seperated[j] != -1:
                result += ENGLISH[_seperated[j]]

    return result

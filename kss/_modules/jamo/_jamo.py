from functools import partial
from typing import Union, List, Tuple

import hangul_jamo
import jamo

from kss._modules.jamo.utils import _j2h
from kss._utils.multiprocessing import _run_job
from kss._utils.sanity_checks import _check_num_workers, _check_text, _check_type, _check_char


def h2j(
    text: Union[str, List[str], Tuple[str]],
    num_workers: Union[int, str] = "auto",
) -> Union[str, List[str]]:
    """
    This converts a string of Hangul to jamo.

    Args:
        text (Union[str, List[str], Tuple[str]): single text or list of texts
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[str, List[str]]: jamo string of the given text

    Examples:
        >>> from kss import Kss
        >>> h2j = Kss("h2j")
        >>> text = "안녕하세요"
        >>> output = h2j(text)
        >>> print(output)
        '안녕하세요'

    References:
        This was copied from [jamo](https://github.com/JDongian/python-jamo) and modified by Kss
    """

    text, finish = _check_text(text)

    if finish:
        return text

    num_workers = _check_num_workers(text, num_workers)

    return _run_job(
        func=jamo.h2j,
        inputs=text,
        num_workers=num_workers,
    )


def h2hcj(
    text: Union[str, List[str], Tuple[str]],
    num_workers: Union[int, str] = "auto",
) -> Union[str, List[str]]:
    """
    This converts a string of Hangul to Hangul Compatibility Jamo.

    Args:
        text (Union[str, List[str], Tuple[str]): single text or list of texts
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[str, List[str]]: Hangul Compatibility Jamo string of the given text

    Examples:
        >>> from kss import Kss
        >>> h2hcj = Kss("h2hcj")
        >>> text = "안녕하세요"
        >>> output = h2hcj(text)
        >>> print(output)
        'ㅇㅏㄴㄴㅕㅇㅎㅏㅅㅔㅇㅛ'

    References:
        This was copied from [hangul-jamo](https://github.com/jonghwanhyeon/hangul-jamo) and modified by Kss
    """

    text, finish = _check_text(text)

    if finish:
        return text

    num_workers = _check_num_workers(text, num_workers)

    return _run_job(
        func=hangul_jamo.decompose,
        inputs=text,
        num_workers=num_workers,
    )


def j2h(
    text: Union[str, List[str], Tuple[str]],
    add_placeholder_for_leading_vowels: bool = False,
    num_workers: Union[int, str] = "auto",
) -> Union[str, List[str]]:
    """
    This converts a string of jamo to Hangul.

    Args:
        text (Union[str, List[str], Tuple[str]): single text or list of texts
        add_placeholder_for_leading_vowels (bool): add 'ㅇ' for leading vowels (e.g. 'ㅐ플' -> '애플')
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[str, List[str]]: Hangul string of the given text

    Examples:
        >>> from kss import Kss
        >>> j2h = Kss("j2h")
        >>> text = '안녕하세요'
        >>> output = j2h(text)
        >>> print(output)
        '안녕하세요'

    References:
        This was copied from [jamo](https://github.com/JDongian/python-jamo) and modified by Kss
    """

    text, finish = _check_text(text)

    if finish:
        return text

    num_workers = _check_num_workers(text, num_workers)
    add_placeholder_for_leading_vowels = _check_type(
        add_placeholder_for_leading_vowels, "add_placeholder_for_leading_vowels", bool
    )

    return _run_job(
        func=partial(_j2h, add_placeholder_for_leading_vowels=add_placeholder_for_leading_vowels),
        inputs=text,
        num_workers=num_workers,
    )


def j2hcj(
    text: Union[str, List[str], Tuple[str]],
    num_workers: Union[int, str] = "auto",
) -> Union[str, List[str]]:
    """
    This converts a string of jamo to Hangul Compatibility Jamo.

    Args:
        text (Union[str, List[str], Tuple[str]): single text or list of texts
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[str, List[str]]: Hangul Compatibility Jamo string of the given text

    Examples:
        >>> from kss import Kss
        >>> j2hcj = Kss("j2hcj")
        >>> text = '안녕하세요'
        >>> output = j2hcj(text)
        >>> print(output)
        'ㅇㅏㄴㄴㅕㅇㅎㅏㅅㅔㅇㅛ'

    References:
        This was copied from [jamo](https://github.com/JDongian/python-jamo) and modified by Kss
    """
    text, finish = _check_text(text)

    if finish:
        return text

    num_workers = _check_num_workers(text, num_workers)

    return _run_job(
        func=jamo.j2hcj,
        inputs=text,
        num_workers=num_workers,
    )


def hcj2h(
    text: Union[str, List[str], Tuple[str]],
    num_workers: Union[int, str] = "auto",
) -> Union[str, List[str]]:
    """
    This converts a string of Hangul Compatibility Jamo to Hangul.

    Args:
        text (Union[str, List[str], Tuple[str]): single text or list of texts
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[str, List[str]]: Hangul string of the given text

    Examples:
        >>> from kss import Kss
        >>> hcj2h = Kss("hcj2h")
        >>> text = 'ㅇㅏㄴㄴㅕㅇㅎㅏㅅㅔㅇㅛ'
        >>> output = hcj2h(text)
        >>> print(output)
        '안녕하세요'

    References:
        This was copied from [hangul-jamo](https://github.com/jonghwanhyeon/hangul-jamo) and modified by Kss
    """

    text, finish = _check_text(text)

    if finish:
        return text

    num_workers = _check_num_workers(text, num_workers)

    return _run_job(
        func=hangul_jamo.compose,
        inputs=text,
        num_workers=num_workers,
    )


def hcj2j(
    text: Union[str, List[str], Tuple[str]],
    position: str = "vowel",
    num_workers: Union[int, str] = "auto",
) -> Union[str, List[str]]:
    """
    This converts a string of Hangul Compatibility Jamo to jamo.

    Args:
        text (Union[str, List[str], Tuple[str]): single text or list of texts
        position (str): the position of the HCJ character to convert to jamo character, one of 'lead', 'vowel', 'tail'
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[str, List[str]]: jamo string of the given text

    Examples:
        >>> from kss import Kss
        >>> hcj2j = Kss("hcj2j")
        >>> text = 'ㅇ'
        >>> output = hcj2j(text)
        >>> print(output)
        'ᄋ'

    References:
        This was copied from [jamo](https://github.com/JDongian/python-jamo) and modified by Kss
    """

    text, finish = _check_text(text)

    if finish:
        return text

    text = _check_char(text)
    num_workers = _check_num_workers(text, num_workers)
    position = _check_type(position, "position", str).lower()

    if position not in ["lead", "vowel", "tail"]:
        raise ValueError("position should be one of 'lead', 'vowel', 'tail'")

    return _run_job(
        func=partial(jamo.hcj2j, position=position),
        inputs=text,
        num_workers=num_workers,
    )


def is_jamo(
    text: Union[str, List[str], Tuple[str]],
    num_workers: Union[int, str] = "auto",
) -> Union[bool, List[bool]]:
    """
    This checks if a character is a jamo character.

    Args:
        text (Union[str, List[str], Tuple[str]): single text or list of texts
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[bool, List[bool]]: whether the given character is a jamo character or not

    Examples:
        >>> from kss import Kss
        >>> is_jamo = Kss("is_jamo")
        >>> text = 'ᄋ'
        >>> output = is_jamo(text)
        >>> print(output)
        True

    References:
        This was copied from [jamo](https://github.com/JDongian/python-jamo) and modified by Kss
    """

    text, finish = _check_text(text)

    if finish:
        return False

    text = _check_char(text)
    num_workers = _check_num_workers(text, num_workers)

    return _run_job(
        func=jamo.is_jamo,
        inputs=text,
        num_workers=num_workers,
    )


def is_jamo_modern(
    text: Union[str, List[str], Tuple[str]],
    num_workers: Union[int, str] = "auto",
) -> Union[bool, List[bool]]:
    """
    This checks if a character is a modern jamo character.

    Args:
        text (Union[str, List[str], Tuple[str]): single text or list of texts
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[bool, List[bool]]: whether the given character is a modern jamo character or not

    Examples:
        >>> from kss import Kss
        >>> is_jamo_modern = Kss("is_jamo_modern")
        >>> text = 'ᄋ'
        >>> output = is_jamo_modern(text)
        >>> print(output)
        True

    References:
        This was copied from [jamo](https://github.com/JDongian/python-jamo) and modified by Kss
    """

    text, finish = _check_text(text)

    if finish:
        return False

    text = _check_char(text)
    num_workers = _check_num_workers(text, num_workers)

    return _run_job(
        func=jamo.is_jamo_modern,
        inputs=text,
        num_workers=num_workers,
    )


def is_hcj(
    text: Union[str, List[str], Tuple[str]],
    num_workers: Union[int, str] = "auto",
) -> Union[bool, List[bool]]:
    """
    This checks if a character is a Hangul Compatibility Jamo character.

    Args:
        text (Union[str, List[str], Tuple[str]): single text or list of texts
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[bool, List[bool]]: whether the given character is a Hangul Compatibility Jamo character or not

    Examples:
        >>> from kss import Kss
        >>> is_hcj = Kss("is_hcj")
        >>> text = 'ㅇ'
        >>> output = is_hcj(text)
        >>> print(output)
        True

    References:
        This was copied from [jamo](https://github.com/JDongian/python-jamo) and modified by Kss
    """

    text, finish = _check_text(text)

    if finish:
        return False

    text = _check_char(text)
    num_workers = _check_num_workers(text, num_workers)

    return _run_job(
        func=jamo.is_hcj,
        inputs=text,
        num_workers=num_workers,
    )


def is_hcj_modern(
    text: Union[str, List[str], Tuple[str]],
    num_workers: Union[int, str] = "auto",
) -> Union[bool, List[bool]]:
    """
    This checks if a character is a modern Hangul Compatibility Jamo character.

    Args:
        text (Union[str, List[str], Tuple[str]): single text or list of texts
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[bool, List[bool]]: whether the given character is a modern Hangul Compatibility Jamo character or not

    Examples:
        >>> from kss import Kss
        >>> is_hcj_modern = Kss("is_hcj_modern")
        >>> text = 'ㅇ'
        >>> output = is_hcj_modern(text)
        >>> print(output)
        True

    References:
        This was copied from [jamo](https://github.com/JDongian/python-jamo) and modified by Kss
    """

    text, finish = _check_text(text)

    if finish:
        return False

    text = _check_char(text)
    num_workers = _check_num_workers(text, num_workers)

    return _run_job(
        func=jamo.is_hcj_modern,
        inputs=text,
        num_workers=num_workers,
    )


def is_hangul_char(
    text: Union[str, List[str], Tuple[str]],
    num_workers: Union[int, str] = "auto",
) -> Union[bool, List[bool]]:
    """
    This checks if a character is a Hangul character.

    Args:
        text (Union[str, List[str], Tuple[str]): single text or list of texts
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[bool, List[bool]]: whether the given character is a Hangul character or not

    Examples:
        >>> from kss import Kss
        >>> is_hangul_char = Kss("is_hangul_char")
        >>> text = '안'
        >>> output = is_hangul_char(text)
        >>> print(output)
        True

    References:
        This was copied from [jamo](https://github.com/JDongian/python-jamo) and modified by Kss
    """

    text, finish = _check_text(text)

    if finish:
        return False

    text = _check_char(text)
    num_workers = _check_num_workers(text, num_workers)

    return _run_job(
        func=jamo.is_hangul_char,
        inputs=text,
        num_workers=num_workers,
    )

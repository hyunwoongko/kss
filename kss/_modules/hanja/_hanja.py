from functools import partial
from typing import List, Union, Tuple

from kss._modules.hanja.utils import _split_hanja, _is_hanja, _hanja2hangul
from kss._utils.multiprocessing import _run_job
from kss._utils.sanity_checks import _check_text, _check_num_workers, _check_char, _check_type


def split_hanja(
    text: Union[str, List[str], Tuple[str]],
    num_workers: Union[int, str] = "auto",
) -> Union[List[str], List[List[str]]]:
    """
    This splits the given text into hanja string and non-hanja string.

    Args:
        text (Union[str, List[str], Tuple[str]): single text or list of texts
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[str, List[str]]: hanja string and non-hanja string of the given text

    Examples:
        >>> from kss import Kss
        >>> split_hanja = Kss("split_hanja")
        >>> text = "大韓民國은 民主共和國이다."
        >>> output = split_hanja(text)
        >>> print(output)
        ["大韓民國", "은 ", "民主共和國", "이다."]

    References:
        This was copied from [hanja](https://github.com/suminb/hanja) and modified by Kss
    """
    text, finish = _check_text(text)

    if finish:
        return text

    num_workers = _check_num_workers(text, num_workers)

    return _run_job(
        func=_split_hanja,
        inputs=text,
        num_workers=num_workers,
    )


def is_hanja(
    text: Union[str, List[str], Tuple[str]],
    num_workers: Union[int, str] = "auto",
) -> Union[bool, List[bool]]:
    """
    This checks if the given character is a hanja character.

    Args:
        text (Union[str, List[str], Tuple[str]): single character or list of characters
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[bool, List[bool]]: whether the given character is a hanja character or not

    Examples:
        >>> from kss import Kss
        >>> is_hanja = Kss("is_hanja")
        >>> text = "大"
        >>> output = is_hanja(text)
        >>> print(output)
        True
        >>> text = "대"
        >>> output = is_hanja(text)
        >>> print(output)
        False

    References:
        This was copied from [hanja](https://github.com/suminb/hanja) and modified by Kss
    """

    text, finish = _check_text(text)

    if finish:
        return False

    text = _check_char(text)
    num_workers = _check_num_workers(text, num_workers)

    return _run_job(
        func=_is_hanja,
        inputs=text,
        num_workers=num_workers,
    )


def hanja2hangul(
    text: Union[str, List[str], Tuple[str]],
    combination: bool = False,
    reverse: bool = False,
    html: bool = False,
    num_workers: Union[int, str] = "auto",
) -> Union[str, List[str]]:
    """
    This converts hanja to hangul.

    Args:
        text (Union[str, List[str], Tuple[str]): single text or list of texts
        combination (bool): whether to return hanja and hangul together or not
        reverse (bool): whether to reverse the order of hanja and hangul or not
        html (bool): whether to return html format or not
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[str, List[str]]: hanja to hangul converted text or list of texts

    Examples:
        >>> from kss import Kss
        >>> hanja2hangul = Kss("hanja2hangul")
        >>> text = "大韓民國은 民主共和國이다."
        >>> output = hanja2hangul(text)
        >>> print(output)
        "대한민국은 민주공화국이다."

    References:
        This was copied from [hanja](https://github.com/suminb/hanja) and modified by Kss
    """
    text, finish = _check_text(text)

    if finish:
        return text

    num_workers = _check_num_workers(text, num_workers)
    combination = _check_type(combination, "combination", bool)
    reverse = _check_type(reverse, "reverse", bool)
    html = _check_type(html, "html", bool)

    if combination is False and reverse is True:
        raise ValueError("`reverse` is only available when `combination` is True")
    if combination is False and html is True:
        raise ValueError("`html` is only available when `combination` is True")

    return _run_job(
        func=partial(
            _hanja2hangul,
            combination=combination,
            reverse=reverse,
            html=html,
        ),
        inputs=text,
        num_workers=num_workers,
    )

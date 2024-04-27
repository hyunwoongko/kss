from typing import Union, List, Tuple

from kss._utils.multiprocessing import _run_job
from kss._utils.sanity_checks import _check_num_workers, _check_text


replace_map = {
    "ﾡ": "ㄱ",
    "ﾢ": "ㄲ",
    "ﾣ": "ㄳ",
    "ﾤ": "ㄴ",
    "ﾥ": "ㄵ",
    "ﾦ": "ㄶ",
    "ﾧ": "ㄷ",
    "ﾨ": "ㄸ",
    "ﾩ": "ㄹ",
    "ﾪ": "ㄺ",
    "ﾫ": "ㄻ",
    "ﾬ": "ㄼ",
    "ﾭ": "ㄽ",
    "ﾮ": "ㄾ",
    "ﾯ": "ㄿ",
    "ﾱ": "ㅁ",
    "ﾲ": "ㅂ",
    "ﾳ": "ㅃ",
    "ﾴ": "ㅄ",
    "ﾵ": "ㅅ",
    "ﾶ": "ㅆ",
    "･": "ㆍ",
    "ﾷ": "ㅇ",
    "ﾸ": "ㅈ",
    "ﾹ": "ㅉ",
    "ﾺ": "ㅊ",
    "ﾻ": "ㅋ",
    "ﾼ": "ㅌ",
    "ﾽ": "ㅍ",
    "ﾾ": "ㅎ",
    "ￂ": "ㅏ",
    "ￃ": "ㅐ",
    "ￄ": "ㅑ",
    "ￆ": "ㅓ",
    "ￇ": "ㅔ",
    "ￊ": "ㅕ",
    "ￌ": "ㅗ",
    "ￏ": "ㅚ",
    "ￒ": "ㅛ",
    "ￓ": "ㅜ",
    "ￖ": "ㅟ",
    "ￗ": "ㅠ",
    "ￚ": "ㅡ",
    "ￜ": "ㅣ",
    "ￍ": "ㅘ",
    "ￔ": "ㅝ",
    "ￎ": "ㅙ",
    "ￕ": "ㅞ",
}


def half2full(
    text: Union[str, List[str], Tuple[str]],
    num_workers: Union[int, str] = "auto",
) -> Union[str, List[str]]:
    """
    This converts half-width characters to full-width characters.

    Args:
        text (Union[str, List[str], Tuple[str]]): single text or list of texts
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[str, List[str]]: converted text or list of converted texts

    Examples:
        >>> from kss import Kss
        >>> half2full = Kss("half2full")
        >>> text = "ﾻﾻﾻﾻﾻﾻ"
        >>> half2full(text)
        'ㅋㅋㅋㅋㅋㅋ'
    """
    text, finish = _check_text(text)

    if finish:
        return text

    num_workers = _check_num_workers(text, num_workers)

    return _run_job(
        func=_half2full,
        inputs=text,
        num_workers=num_workers,
    )


def _half2full(text: str):
    fullwidth_text = ""

    for char in text:
        fullwidth_text += replace_map.get(char, char)

    return fullwidth_text

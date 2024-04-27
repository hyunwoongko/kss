from functools import partial
from typing import Union, List, Tuple

import distance
from kss._modules.hangulization.hangulize import hangulize as _hangulize
from kss._utils.multiprocessing import _run_job
from kss._utils.sanity_checks import _check_text, _check_type, _check_num_workers

supported_langs = languages = {
    "lat": "라틴어",
    "deu": "독일어",
    "rus": "러시아어",
    "ell": "현대 그리스어",
    "grc": "고대 그리스어",
    "ita": "이탈리아어",
    "spa": "스페인어",
    "jpn": "일본어",
    "pol": "폴란드어",
    "ces": "체코어",
    "hbs": "세르보크로아트어",
    "ron": "루마니아어",
    "hun": "헝가리어",
    "vie": "베트남어",
    "swe": "스웨덴어",
    "nld": "네덜란드어",
    "por": "포르투갈어",
    "por.br": "브라질 포르투갈어",
    "cym": "웨일스어",
    "wlm": "중세 웨일스어",
    "bul": "불가리아어",
    "kat": "조지아어 간략전사",
    "kat.narrow": "조지아어 정밀전사",
    "fin": "핀란드어",
    "est": "에스토니아어",
    "lav": "라트비아어",
    "lit": "리투아니아어",
    "isl": "아이슬란드어",
    "cat": "카탈루냐어",
    "slk": "슬로바키아어",
    "slv": "슬로베니아어",
    "sqi": "알바니아어",
    "epo": "에스페란토",
    "ukr": "우크라이나어",
    "bel": "벨라루스어",
    "mkd": "마케도니아어",
    "tur": "터키어",
    "aze": "아제르바이잔어"
}


def hangulize(
    text: Union[str, List[str], Tuple[str]],
    lang: str,
    num_workers: Union[int, str] = "auto",
) -> Union[str, List[str]]:
    """
    This converts the given text to Hangul pronunciation.

    Args:
        text (Union[str, List[str], Tuple[str]): single text or list of texts
        lang (str): source language code
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[str, List[str]]: Hangul pronunciation of the given text

    Examples:
        >>> from kss import Kss
        >>> hangulize = Kss("hangulize")
        >>> text = "Giro d'Italia"
        >>> output = hangulize(text, lang="ita")
        >>> print(output)
        "지로 디탈리아"

    References:
        This was copied from [hangulize](https://github.com/sublee/hangulize) and modified by Kss
    """
    text, finish = _check_text(text)

    if finish:
        return text

    lang = _check_lang(lang)
    num_workers = _check_num_workers(text, num_workers)

    return _run_job(
        func=partial(_hangulize, code=lang),
        inputs=text,
        num_workers=num_workers,
    )


def _check_lang(lang: str):
    lang = lang.lower()
    lang = _check_type(lang, "lang", str)

    if lang not in supported_langs:
        error_message = f"'{lang}' is not supported language code." \
                        f"\nSupported language codes are the following:\n{list(supported_langs.items())}"
        closest_lang = _find_closest_lang(lang)
        if closest_lang:
            error_message += f"\n\nDid you mean '{closest_lang}'?"
        raise ValueError(error_message)

    return lang


def _find_closest_lang(lang, min_distance=0.5):
    current_min_distance = 99
    closest_lang = None
    for supported_lang in supported_langs:
        dist = distance.nlevenshtein(lang, supported_lang)
        if dist < current_min_distance and dist <= min_distance:
            current_min_distance = dist
            closest_lang = supported_lang

    if closest_lang is None:
        return None
    else:
        return closest_lang, supported_langs[closest_lang]

# Copyright (C) 2021 Hyunwoong Ko <kevin.brain@kakaobrain.com> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.

from functools import partial
from typing import List, Union, Tuple

from kss._utils.multiprocessing import _run_job
from kss._utils.sanity_checks import (
    _check_text,
    _check_analyzer_backend,
    _check_num_workers,
    _check_type,
)


def split_morphemes(
    text: Union[str, List[str], Tuple[str]],
    backend: str = "auto",
    num_workers: Union[int, str] = "auto",
    drop_space: bool = True,
) -> Union[List[Tuple[str, str]], List[List[Tuple[str, str]]], Union[List, Tuple]]:
    """
    This splits texts into morphemes.

    Args:
        text (Union[str, List[str], Tuple[str]]): single text or list/tuple of texts
        backend (str): morpheme analyzer backend. 'mecab', 'pecab' are supported.
        num_workers (Union[int, str])): the number of multiprocessing workers
        drop_space (bool): drop all spaces in output or not

    Returns:
        Union[List[Tuple[str, str]], List[List[Tuple[str, str]]], Union[List, Tuple]]:
            outputs of morpheme analysis.

    Examples:
        >>> from kss import Kss
        >>> split_morphemes = Kss("split_morphemes")
        >>> text = "아버지가방에들어오시다."
        >>> output = split_morphemes(text)
        >>> print(output)
        [('아버지', 'NNG'), ('가', 'JKS'), ('방', 'NNG'), ('에', 'JKB'), ('들어오', 'VV'), ('시', 'EP'), ('다', 'EF'), ('.', 'SF')]
    """
    text, finish = _check_text(text)
    drop_space = _check_type(drop_space, "drop_space", bool)

    if finish:
        return text

    num_workers = _check_num_workers(text, num_workers)
    backend = _check_analyzer_backend(backend)
    result = _run_job(partial(backend.pos, drop_space=drop_space), text, num_workers)
    return result

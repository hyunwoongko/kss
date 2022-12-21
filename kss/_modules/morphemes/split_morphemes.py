# Copyright (C) 2021 Hyunwoong Ko <kevin.ko@tunib.ai> and Sang-Kil Park <skpark1224@hyundai.com>
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
    Split texts into morphemes.

    Args:
        text (Union[str, List[str], Tuple[str]]): single text or list/tuple of texts
        backend (str): morpheme analyzer backend. 'mecab', 'pecab' are supported.
        num_workers (Union[int, str])): the number of multiprocessing workers
        drop_space (bool): drop all spaces in output or not

    Returns:
        Union[List[Tuple[str, str]], List[List[Tuple[str, str]]], Union[List, Tuple]]:
            outputs of morpheme analysis.
    """
    text, finish = _check_text(text)
    drop_space = _check_type(drop_space, "drop_space", bool)

    if finish:
        return text

    num_workers = _check_num_workers(text, num_workers)
    backend = _check_analyzer_backend(backend)
    return _run_job(partial(backend.pos, drop_space=drop_space), text, num_workers)

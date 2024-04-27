from functools import partial
from typing import Union, List, Tuple

from kss._modules.augmentation.replacement import SynonymReplacement
from kss._modules.augmentation.utils import correct_josa
from kss._utils.logger import highlight_diffs, logger
from kss._utils.multiprocessing import _run_job
from kss._utils.sanity_checks import _check_text, _check_type, _check_num_workers, _check_backend_mecab_pecab_only


def augment(
    text: Union[str, List[str], Tuple[str]],
    replacement_ratio: float = 0.3,
    josa_correction: bool = True,
    num_workers: Union[int, str] = "auto",
    backend: str = "auto",
    verbose: bool = False,
) -> Union[str, List[str]]:
    """
    Augments text with synonym replacement method and, 
    optionally it postprocesses the text by correcting josa.
    For this, Kss uses the Korean wordnet from KAIST.

    Args:
        text (Union[str, List[str], Tuple[str]]): single text or list of texts
        replacement_ratio (float): ratio of words to be replaced
        josa_correction (bool): whether to normalize josa or not
        num_workers (Union[int, str]): the number of multiprocessing workers
        backend (str): morpheme analyzer backend. 'mecab', 'pecab' are supported
        verbose (bool): whether to print verbose outputs or not

    Returns:
        Union[str, List[str]]: augmented text or list of augmented texts

    Examples:
        >>> from kss import Kss
        >>> augment = Kss("augment")
        >>> text = "앞서 지난해 11월, 보이저 1호는 명령을 수신하고 수행하는 데엔 문제가 없었지만 통신 장치에 문제가 생겨 과학·엔지니어링 데이터가 지구로 전송되지 않았던 바 있다. 당시 그들은 컴퓨터 시스템을 재시작하고 문제의 근본적인 원인을 파악하기 위해 명령을 보내려고 시도했고, 이달 1일 '포크'라는 명령을 보냈다."
        >>> output = augment(text)
        >>> print(output)
        "앞서 지난해 11월, 보이저 1호는 명령을 수신하고 시행하는 데엔 문제가 없었지만 송신 장비에 문제가 생겨 과학·엔지니어링 데이터가 지구로 전송되지 않았던 바 있다. 당시 그들은 컴퓨터 시스템을 재시작하고 문제의 근본적인 원인을 파악하기 위해 명령을 보내려고 시도했고, 이달 1일 '포크'라는 명령을 보냈다."

    References:
        This was copied from [KoEDA](https://github.com/toriving/KoEDA) and modified by Kss
    """
    text, finish = _check_text(text)

    if finish:
        return text

    replacement_ratio = _check_type(replacement_ratio, "replacement_ratio", float)
    josa_correction = _check_type(josa_correction, "josa_correction", bool)
    verbose = _check_type(verbose, "verbose", bool)
    num_workers = _check_num_workers(text, num_workers)
    _check_backend_mecab_pecab_only(backend)

    if num_workers is not False and verbose:
        verbose = False
        logger.warn(
            "Verbose mode is not supported for multiprocessing. "
            "It will be turned off automatically."
        )

    return _run_job(
        func=partial(
            _augment,
            replacement_ratio=replacement_ratio,
            josa_correction=josa_correction,
            backend=backend,
            verbose=verbose,
        ),
        inputs=text,
        num_workers=num_workers,
    )


def _augment(
    text: str,
    replacement_ratio: float = 0.3,
    josa_correction: bool = True,
    backend: str = "auto",
    verbose: bool = False,
):
    orig_text = text
    replacement = SynonymReplacement(backend=backend)  # I want WSD...
    text = replacement(text, p=replacement_ratio, verbose=verbose)

    if josa_correction:
        text = correct_josa(text)

    if verbose:
        print()
        print(highlight_diffs(orig_text, text).replace("\n", "\\n"))

    return text

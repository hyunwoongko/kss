from typing import Union, List

from kss._modules.josa.utils import _check_text, _check_num_workers, _combine_josa, _run_job, _select_josa


def select_josa(
    prefix: Union[str, List[str]],
    josa: Union[str, List[str]],
    num_workers: Union[int, str] = "auto",
) -> Union[str, List[str]]:
    """
    This selects the correct josa for the given prefix.

    Args:
        prefix (Union[str, List[str]): single prefix or list of prefixes
        josa (Union[str, List[str]): single josa or list of josas
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[str, List[str]]: the correct josa for the given prefix

    Examples:
        >>> from kss import Kss
        >>> select_josa = Kss("select_josa")
        >>> prefix = "철수"
        >>> josa = "은"
        >>> output = select_josa(prefix, josa)
        >>> print(output)
        "는"

    References:
        This was copied from [tossi](https://github.com/what-studio/tossi) and modified by Kss
    """
    prefix, josa = _check_text(prefix, josa, "prefix", "josa")
    num_workers = _check_num_workers(prefix, josa, "prefix", "josa", num_workers)

    return _run_job(
        func=_select_josa,
        input_1=prefix,
        input_2=josa,
        input_1_name="prefix",
        input_2_name="josa",
        num_workers=num_workers,
    )


def combine_josa(
    prefix: Union[str, List[str]],
    josa: Union[str, List[str]],
    num_workers: Union[int, str] = "auto",
) -> Union[str, List[str]]:
    """
    This combines the given prefix and josa.

    Args:
        prefix (Union[str, List[str]): single prefix or list of prefixes
        josa (Union[str, List[str]): single josa or list of josas
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[str, List[str]]: the combined prefix and josa

    Examples:
        >>> from kss import Kss
        >>> combine_josa = Kss("combine_josa")
        >>> prefix = "철수"
        >>> josa = "은"
        >>> output = combine_josa(prefix, josa)
        >>> print(output)
        "철수는"

    References:
        This was copied from [tossi](https://github.com/what-studio/tossi) and modified by Kss
    """
    prefix, josa = _check_text(prefix, josa, "prefix", "josa")
    num_workers = _check_num_workers(prefix, josa, "prefix", "josa", num_workers)

    return _run_job(
        func=_combine_josa,
        input_1=prefix,
        input_2=josa,
        input_1_name="prefix",
        input_2_name="josa",
        num_workers=num_workers,
    )

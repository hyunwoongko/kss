import multiprocessing as mp
from typing import Callable, Any, Optional, Union, List, Tuple

import tossi

from kss._modules.morphemes.split_morphemes import split_morphemes


def _check_text(
    param_1: Union[str, List[str]],
    param_2: Union[str, List[str]],
    param_1_name: str,
    param_2_name: str
) -> Tuple[Union[str, List[str]], Union[str, List[str]]]:
    if isinstance(param_1, str) and isinstance(param_2, str):
        if len(param_1) == 0:
            raise ValueError(f"`{param_1_name}` must not be empty")
        if len(param_2) == 0:
            raise ValueError(f"`{param_2_name}` must not be empty")
        return [param_1], [param_2]

    elif isinstance(param_1, (list, tuple)) and isinstance(param_2, (list, tuple)):
        if len(param_1) != len(param_2):
            raise ValueError(
                f"`{param_1_name}` and `{param_2_name}` must have the same length when both are lists or tuples")
        if any(len(p) == 0 for p in param_1):
            raise ValueError(f"`{param_1_name}` must not contain an empty string")
        if any(len(j) == 0 for j in param_2):
            raise ValueError(f"`{param_2_name}` must not contain an empty string")
        return param_1, param_2

    elif isinstance(param_1, (list, tuple)) and isinstance(param_2, str):
        if any(len(p) == 0 for p in param_1):
            raise ValueError(f"`{param_1_name}` must not contain an empty string")
        if len(param_2) == 0:
            raise ValueError(f"`{param_2_name}` must not be empty")
        return param_1, [param_2] * len(param_1)

    elif isinstance(param_1, str) and isinstance(param_2, (list, tuple)):
        if len(param_1) == 0:
            raise ValueError(f"`{param_1_name}` must not be empty")
        if any(len(j) == 0 for j in param_2):
            raise ValueError(f"`{param_2_name}` must not contain an empty string")
        return [param_1] * len(param_2), param_2

    else:
        raise ValueError(f"`{param_1_name}` and `{param_2_name}` must be strings or lists/tuples of strings")


def _run_job(
    func: Callable,
    input_1: List[str],
    input_2: List[str],
    input_1_name: str,
    input_2_name: str,
    num_workers: Optional[Union[int, bool]] = None,
) -> Union[Any, List[Any]]:
    """
    Run job with or without multiprocessing.

    Args:
        func (Callable): function to run
        input_1 (List[str]): input data
        input_2 (List[str]): input data
        input_1_name (str): input data name
        input_2_name (str): input data name
        num_workers (Optional[Union[int, bool]]): the number of multiprocessing workers.
    """
    if num_workers is False:
        if len(input_1) == 1 and len(input_2) == 1:
            return func(input_1[0], input_2[0])
        elif len(input_1) == 1 and len(input_2) > 1:
            return [func(input_1[0], j) for j in input_2]
        elif len(input_1) > 1 and len(input_2) == 1:
            return [func(i, input_2[0]) for i in input_1]
        else:
            return [func(i, j) for i, j in zip(input_1, input_2)]
    else:
        with mp.Pool(num_workers) as pool:
            if len(input_1) == 1 and len(input_2) == 1:
                raise ValueError(
                    f"Oops! `{input_1_name}` or `{input_2_name}` "
                    f"must have at least 2 elements when using multiprocessing."
                )
            elif len(input_1) == 1 and len(input_2) > 1:
                output = pool.starmap(func, [(input_1[0], j) for j in input_2])
            elif len(input_1) > 1 and len(input_2) == 1:
                output = pool.starmap(func, [(i, input_2[0]) for i in input_1])
            else:
                output = pool.starmap(func, list(zip(input_1, input_2)))

            pool.close()
            pool.join()
            return output


def _check_num_workers(
    param_1: List[str],
    param_2: List[str],
    param_1_name: str,
    param_2_name: str,
    num_workers: Union[int, str],
) -> Optional[Union[int, bool]]:
    if isinstance(num_workers, float):
        num_workers = int(num_workers)
    elif isinstance(num_workers, str):
        num_workers = num_workers.lower()

    if not isinstance(num_workers, int) and num_workers != "auto":
        raise TypeError(
            f"Oops! '{num_workers}' is not supported value for `num_workers`.\n"
            f"Currently kss only supports [int, 'auto'] for this.\n"
            f"Please check `num_workers` parameter again ;)"
        )
    elif isinstance(num_workers, int) and num_workers < 1:
        raise ValueError(
            f"Oops! `num_workers` must be same or greater than 1, but you input {num_workers}.\n"
            "- You can input 1 for no multiprocessing.\n"
            "- You can input 2 ~ n for multiprocessing.\n"
            "- You can input 'auto' for using maximum workers.\n"
            "Please check `num_workers` parameter again ;)"
        )

    if len(param_1) == 1 and len(param_2) == 1:
        return False
        # no multiprocessing worker

    elif num_workers == "auto":
        num_workers = None
        # maximum multiprocessing workers

    return num_workers


def _preprocess_josa(prefix, josa):
    if "도록" in josa or "토록" in josa:
        # 공부하다와 같은 동사(v)의 경우, '~도록'을 사용합니다.
        # 평생, 영원과 같은 명사(n)의 경우, '~토록'을 사용합니다.
        # https://www.italki.com/ko/post/question-468087
        return "토록" if split_morphemes(prefix)[-1][1].startswith("N") else "도록"

    elif "던" in josa and (prefix.endswith("어쨋") or prefix.endswith("어쨌") or prefix.endswith("어쩌")):
        # '어쨌든'은 앞의 상황과는 관계 없이란 뜻으로 '어찌하였든'이 줄어진 말입니다.
        # 이때 '-든'을 '-던'으로 쓰는 것은 잘못입니다. '-던'의 '-더-'는 회상을 나타내는 말이므로 과거의 일을 이야기할 때 가능합니다.
        # 그런데 '어쨌든'은 과거의 일을 이야기하지 않는 것이므로 '-던'으로 쓸 이유가 없는 것입니다.
        # https://m.cafe.daum.net/bareunNGO/5Dfn/55
        return "든"

    elif "에게" in josa and (prefix.endswith("것") or prefix.endswith("곳") or prefix.endswith("거")):
        # ‘에’와 ‘에게’를 쓸 때는 그 조사 앞에 오는 말이 ‘유정 명사’냐 아니냐에 따라 달라집니다. ‘유정 명사’라는 것은 사람이나 동물을 가리키는 명사를 말합니다.
        # 모든 유정/무정 명사를 가릴 수 없으니 대표적인 '것', '곳', '거'만 처리.
        # https://world.kbs.co.kr/service/contents_view.htm?lang=k&menu_cate=learnkorean&id=&board_seq=228909&page=249
        return josa.replace("에게", "에")

    return josa


def _select_josa(prefix, josa):
    prefix = prefix.strip()
    josa = josa.strip()

    josa = _preprocess_josa(prefix, josa)
    return tossi.pick(prefix, josa)


def _combine_josa(prefix, josa):
    return prefix + _select_josa(prefix, josa)

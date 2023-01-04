# Copyright (C) 2021 Hyunwoong Ko <kevin.ko@tunib.ai> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.

import multiprocessing as mp
from typing import Union, Any, List, Optional, Callable


def _run_job(
    func: Callable,
    inputs: Any,
    num_workers: Optional[Union[int, bool]] = None,
) -> Union[Any, List[Any]]:
    """
    Run job with or without multiprocessing.

    Args:
        func (Callable): function to run
        inputs (Any): input data
        num_workers (Optional[Union[int, bool]]): the number of multiprocessing workers.

    Returns:
        Union[Any, List[Any]]: output of the job.
    """
    if num_workers is False:
        if isinstance(inputs, str):
            output = func(inputs)
        else:
            output = [func(i) for i in inputs]
        return output
    else:
        with mp.Pool(num_workers) as pool:
            output = pool.map(func, inputs)
            return output

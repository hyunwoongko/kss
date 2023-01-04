# This code was copied from Text Rank KR [https://github.com/theeluwin/textrankr]
# And modified by Hyunwoong Ko [https://github.com/hyunwoongko]

from functools import partial
from typing import List, Dict, Union, Tuple

from networkx import Graph, pagerank

from kss._modules.summarization.sentence import Sentence
from kss._modules.summarization.utils import (
    _parse_text_into_sentences,
    _build_sentence_graph,
)
from kss._utils.multiprocessing import _run_job
from kss._utils.sanity_checks import (
    _check_text,
    _check_num_workers,
    _check_analyzer_backend,
    _check_type,
    _check_value,
)


def summarize_sentences(
    text: Union[str, List[str], Tuple[str]],
    backend: str = "auto",
    num_workers: Union[str, int] = "auto",
    max_sentences: int = 3,
    tolerance: Union[float] = 0.05,
) -> Union[List[str], List[List[str]]]:
    """
    Summarizes the given text, using TextRank algorithm.

    Args:
        text (Union[str, List[str], Tuple[str]]): single text or list/tuple of texts
        backend (str): morpheme analyzer backend. 'mecab', 'pecab' are supported.
        num_workers (Union[int, str])): the number of multiprocessing workers
        max_sentences (int): the max number of sentences in a summarization result.
        tolerance (float): a threshold for omitting edge weights.

    Returns:
        Union[List[str], List[List[str]]]: outputs of text summarization
    """
    text, finish = _check_text(text)

    if finish:
        return text

    _check_analyzer_backend(backend)
    num_workers = _check_num_workers(text, num_workers)
    max_sentences = _check_type(max_sentences, "max_sentences", int)
    max_sentences = _check_value(
        max_sentences, "max_sentences", lambda x: x > 0, "integer value in 1~N"
    )
    tolerance = _check_type(tolerance, "tolerance", float)

    return _run_job(
        func=partial(
            _summarize_sentences,
            backend=backend,
            max_sentences=max_sentences,
            tolerance=tolerance,
        ),
        inputs=text,
        num_workers=num_workers,
    )


def _summarize_sentences(
    text: str,
    backend: str = "auto",
    max_sentences: int = 3,
    tolerance: float = 0.05,
) -> List[str]:
    """
    Summarizes the given text, using TextRank algorithm.

    Args:
        text (str): a single text to be summarized.
        backend (str): morpheme analyzer backend. 'mecab', 'pecab' are supported.
        max_sentences (int): the max number of sentences in a summarization result.
        tolerance (float): a threshold for omitting edge weights.

    Returns:
        List[str]: summarized sentences
    """

    # parse text
    sentences: List[Sentence] = _parse_text_into_sentences(text, backend)

    # build graph
    graph: Graph = _build_sentence_graph(sentences, tolerance=tolerance)

    # run pagerank
    pageranks: Dict[Sentence, float] = pagerank(graph, weight="weight")

    # get top-k sentences
    sentences = sorted(pageranks, key=pageranks.get, reverse=True)
    sentences = sentences[:max_sentences]
    sentences = sorted(sentences, key=lambda sentence: sentence.index)

    # output summaries
    return [sentence.text for sentence in sentences]

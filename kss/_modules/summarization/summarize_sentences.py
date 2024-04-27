# This code was copied from Text Rank KR [https://github.com/theeluwin/textrankr]
# And modified by Hyunwoong Ko [https://github.com/hyunwoongko]

from functools import partial
from typing import List, Dict, Union, Tuple

from kss._modules.summarization.utils import (
    _parse_text_into_sentences,
    _build_sentence_graph,
    Sentence,
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
    strip: bool = True,
    ignores: List[str] = None,
) -> Union[List[str], List[List[str]]]:
    """
    This summarizes the given text, using TextRank algorithm.

    Args:
        text (Union[str, List[str], Tuple[str]]): single text or list/tuple of texts
        backend (str): morpheme analyzer backend. 'mecab', 'pecab' are supported.
        num_workers (Union[int, str])): the number of multiprocessing workers
        max_sentences (int): the max number of sentences in a summarization result.
        tolerance (float): a threshold for omitting edge weights.
        strip (bool): strip all sentences or not
        ignores (List[str]): list of strings to ignore

    Returns:
        Union[List[str], List[List[str]]]: outputs of text summarization

    Examples:
        >>> from kss import Kss
        >>> summarize_sentences = Kss("summarize_sentences")
        >>> text = "개그맨 겸 가수 ‘개가수’ UV 유세윤이 신곡 발매 이후 많은 남편들의 응원을 받고 있다. 유세윤은 지난 3일 오후 6시 새 싱글 ‘마더 사커(Mother Soccer)(Feat. 수퍼비)’를 발매했다. ‘마더 사커’는 아내에 대한 서운한 마음을 위트 있고 강한 어조로 디스 하는 남편 유세윤의 마음을 담은 곡이다. 발매 후 소셜 미디어 상에서 화제를 모으고 있는 가운데, 가수 하동균은 “유세유니 괜찮겠어”라는 반응을 보이기도 했다. 누리꾼들은 ‘두 분의 원만한 합의가 있기를 바랍니다’, ‘집에는 들어갈 수 있겠나’ 등 유세윤의 귀가를 걱정하는 모습을 보였다. 유세윤은 점입가경으로 ‘마더 사커’ 챌린지를 시작, 자신의 SNS를 통해 “부부 싸움이 좀 커졌네요”라며 배우 송진우와 함께 촬영한 영상을 게재했다. 해당 영상에서는 양말을 신고 침대에 들어간 뒤 환호를 지르거나 화장실 불을 끄지 않고 도망가는 등 아내의 잔소리 유발 포인트를 살려 재치 있는 영상을 완성했다. 유세윤은 ‘마더 사커’를 통해 남편들의 마음을 대변해 주고 있는 한편 아내의 반응은 어떨지 궁금증을 모은다."
        >>> summarize_sentences(text)
        ['개그맨 겸 가수 ‘개가수’ UV 유세윤이 신곡 발매 이후 많은 남편들의 응원을 받고 있다.', '‘마더 사커’는 아내에 대한 서운한 마음을 위트 있고 강한 어조로 디스 하는 남편 유세윤의 마음을 담은 곡이다.', '유세윤은 ‘마더 사커’를 통해 남편들의 마음을 대변해 주고 있는 한편 아내의 반응은 어떨지 궁금증을 모은다.']

    References:
        This was copied from [textrankr](https://https://github.com/theeluwin/textrankr) and modified by Kss
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
            strip=strip,
            ignores=ignores,
        ),
        inputs=text,
        num_workers=num_workers,
    )


def _summarize_sentences(
    text: str,
    backend: str = "auto",
    max_sentences: int = 3,
    tolerance: float = 0.05,
    strip: bool = True,
    ignores: List[str] = None,
) -> List[str]:
    """
    Summarizes the given text, using TextRank algorithm.

    Args:
        text (str): a single text to be summarized.
        backend (str): morpheme analyzer backend. 'mecab', 'pecab' are supported.
        max_sentences (int): the max number of sentences in a summarization result.
        tolerance (float): a threshold for omitting edge weights.
        strip (bool): strip all sentences or not
        ignores (List[str]): list of strings to ignore

    Returns:
        List[str]: summarized sentences
    """
    from networkx import pagerank

    # parse text
    sentences: List[Sentence] = _parse_text_into_sentences(text, backend, strip, ignores)

    # build graph
    graph = _build_sentence_graph(sentences, tolerance=tolerance)

    # run pagerank
    pageranks: Dict[Sentence, float] = pagerank(graph, weight="weight")

    # get top-k sentences
    sentences = sorted(pageranks, key=pageranks.get, reverse=True)
    sentences = sentences[:max_sentences]
    sentences = sorted(sentences, key=lambda sentence: sentence.index)

    # output summaries
    return [sentence.text for sentence in sentences]

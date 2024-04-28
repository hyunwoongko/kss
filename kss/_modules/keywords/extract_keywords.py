# This code was copied from KR-WordRank [https://github.com/lovit/KR-WordRank]
# And modified by Hyunwoong Ko [https://github.com/hyuwoongko]
from typing import List, Union, Tuple

from kss._modules.keywords.utils import KRWordRank
from kss._utils.sanity_checks import _check_text, _check_type, _check_backend_mecab_pecab_only


def extract_keywords(
    text: Union[str, List[str]],
    num_keywords: int = 5,
    min_word_count: int = 1,
    max_word_length: int = 10,
    return_scores: bool = False,
    backend: str = "auto",
    noun_only: bool = True,
    num_workers: Union[int, str] = "auto",
) -> Union[List[str], List[Tuple[str, float]]]:
    """
    This extracts keywords from the given text.
    This uses TextRank algorithm to extract keywords.

    Args:
        text (Union[str, List[str]): single text or list of texts
        num_keywords (int): the number of keywords to extract
        min_word_count (int): the minimum count of words
        max_word_length (int): the maximum length of words
        return_scores (bool): whether to return scores or not
        backend (str): morpheme analyzer backend. 'mecab', 'pecab' are supported
        noun_only (bool): whether to extract only nouns or not
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[List[str], List[Tuple[str, float]]]: list of keywords or list of tuples of keywords and scores

    Examples:
        >>> from kss import Kss
        >>> extract_keywords = Kss("extract_keywords")
        >>> text = ['여운이 크게남는영화 엠마스톤 너무 사랑스럽고 라이언고슬링 남자가봐도 정말 매력적인 배우인듯 영상미 음악 연기 구성 전부 좋았고 마지막 엔딩까지 신선하면서 애틋하구요 30중반에 감정이 많이 메말라있었는데 오랜만에 가슴이 촉촉해지네요',
        ...         '영상미도 너무 아름답고 신나는 음악도 좋았다 마지막 세바스찬과 미아의 눈빛교환은 정말 마음 아팠음 영화관에 고딩들이 엄청 많던데 고딩들은 영화 내용 이해를 못하더라ㅡㅡ사랑을 깊게 해본 사람이라면 누구나 느껴볼수있는 먹먹함이 있다',
        ...         '정말 영상미랑 음악은 최고였다 그리고 신선했다 음악이 너무 멋있어서 연기를 봐야 할지 노래를 들어야 할지 모를 정도로 그리고 보고 나서 생각 좀 많아진 영화 정말 이 연말에 보기 좋은 영화 인 것 같다',
        ...         '무언의 마지막 피아노연주 완전 슬픔ㅠ보는이들에게 꿈을 상기시켜줄듯 또 보고 싶은 내생에 최고의 뮤지컬영화였음 단순할수 있는 내용에 뮤지컬을 가미시켜째즈음악과 춤으로 지루할틈없이 빠져서봄 ost너무좋았음',
        ...         '처음엔 초딩들 보는 그냥 그런영화인줄 알았는데 정말로 눈과 귀가 즐거운 영화였습니다 어찌보면 뻔한 스토리일지 몰라도 그냥 보고 듣는게 즐거운 그러다가 정말 마지막엔 너무 아름답고 슬픈 음악이 되어버린',
        ...         '정말 멋진 노래와 음악과 영상미까지 정말 너무 멋있는 영화 눈물을 흘리면서 봤습니다 영화가 끝난 순간 감탄과 동시에 여운이 길게 남아 또 눈물을 흘렸던내 인생 최고의 뮤지컬 영화',
        ...         '평소 뮤지컬 영화 좋아하는 편인데도 평점에 비해 너무나 별로였던 영화 재즈음악이나 영상미 같은 건 좋았지만 줄거리도 글쎄 결말은 정말 별로 6 7점 정도 주는게 맞다고 생각하지만 개인적으로 후반부가 너무 별로여서',
        ...         '오랜만에 좋은 영화봤다는 생각들었구요 음악도 영상도 스토리도 너무나좋았고 무엇보다 진한 여운이 남는 영화는 정말 오랜만이었어요 연인끼리 가서 보기 정말 좋은영화 너뮤너뮤너뮤 재밌게 잘 봤습니다',
        ...         '음악 미술 연기 등 모든 것이 좋았지만 마지막 결말이 너무 현실에 뒤떨어진 꿈만 같다 꿈을 이야기하는 영화지만 과정과 결과에 있어 예술가들의 현실을 너무 반영하지 못한 것이 아닌가하는 생각이든다 그래서 보고 난 뒤 나는 꿈을 꿔야하는데 허탈했다',
        ...         '마지막 회상씬의 감동이 잊혀지질않는다마지막 십분만으로 티켓값이 아깝지않은 영화 음악들도 너무 아름다웠다옛날 뮤지컬 같은 빈티지영상미도 최고']
        >>> output = extract_keywords(text, noun_only=True)
        >>> print(output)
        ['마지막', '영화', '음악', '라이언고슬링', '뮤지컬']
        >>> output = extract_keywords(text, noun_only=False)
        >>> print(output)
        ['너무', '정말', '마지막', '영화', '음악']

    References:
        This was copied from [KR-WordRank](https://github.com/lovit/KR-WordRank) and modified by Kss
    """

    text, finish = _check_text(text)

    if finish:
        return []

    num_keywords = _check_type(num_keywords, "num_keywords", int)
    min_word_count = _check_type(min_word_count, "min_word_count", int)
    max_word_length = _check_type(max_word_length, "max_word_length", int)
    return_scores = _check_type(return_scores, "return_scores", bool)
    noun_only = _check_type(noun_only, "noun_only", bool)
    _check_backend_mecab_pecab_only(backend)

    if num_workers != "auto":
        raise ValueError("`extract_keywords` does not support `num_workers` argument")

    return _extract_keywords(
        text=text,
        num_keywords=num_keywords,
        min_word_count=min_word_count,
        max_word_length=max_word_length,
        return_scores=return_scores,
        noun_only=noun_only,
        backend=backend,
    )


def _extract_keywords(
    text: Union[str, List[str]],
    num_keywords: int = 5,
    min_word_count: int = 1,
    max_word_length: int = 10,
    return_scores: bool = False,
    backend: str = "auto",
    noun_only: bool = True,
):
    if isinstance(text, str):
        text = [text]

    wordrank_extractor = KRWordRank(
        min_count=min_word_count,
        max_length=max_word_length,
        backend=backend,
        noun_only=noun_only,
    )
    keywords = wordrank_extractor.extract(
        text, num_keywords=num_keywords
    )[0]

    if return_scores:
        return keywords
    else:
        return list(keywords.keys())

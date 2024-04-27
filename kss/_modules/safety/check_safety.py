from functools import partial
from typing import Union, List, Tuple

from kss._modules.safety.utils import bad_words, exceptions, pattern
from kss._utils.multiprocessing import _run_job
from kss._utils.sanity_checks import _check_text, _check_num_workers, _check_type


def is_unsafe(
    text: Union[str, List[str], Tuple[str]],
    return_matches: bool = False,
    num_workers: Union[int, str] = "auto",
) -> Union[bool, List[bool], List[bool], List[List[str]]]:
    """
    This checks if the text is unsafe or not.

    Args:
        text (Union[str, List[str], Tuple[str]]): single text or list of texts
        return_matches (bool): whether to return matches or not
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[bool, List[bool], List[bool], List[List[str]]]:
            whether the text is unsafe or not
            or list of whether the texts are unsafe or not
            or list of matched bad words in the texts

    Examples:
        >>> from kss import Kss
        >>> is_unsafe = Kss("is_unsafe")
        >>> text = "안녕하세요"
        >>> is_unsafe(text)
        False
        >>> text = "안녕하세요. 씨발"
        >>> is_unsafe(text)
        True
        >>> text = ["안녕하세요", "안녕하세요. 씨발"]
        >>> is_unsafe(text)
        [False, True]
        >>> text = "안녕하세요. 씨발"
        >>> is_unsafe(text, return_matches=True)
        ['씨발']
        >>> text = ["안녕하세요", "안녕하세요. 씨발"]
        >>> is_unsafe(text, return_matches=True)
        [[], ['씨발']]
    """
    text, finish = _check_text(text)
    return_matches = _check_type(return_matches, "return_matches", bool)
    num_workers = _check_num_workers(text, num_workers)

    if finish:
        return [] if return_matches else False

    return _run_job(
        func=partial(_is_unsafe, return_matches=return_matches),
        inputs=text,
        num_workers=num_workers,
    )


def _is_unsafe(text: str, return_matches: bool = False):
    if return_matches:
        matches = _is_unsafe_regex(text, return_matches=True) + _is_unsafe_dict(text, return_matches=True)
        deduplicated_matches = []
        for match in matches:
            if match not in deduplicated_matches:
                deduplicated_matches.append(match)
        return deduplicated_matches
    else:
        return _is_unsafe_regex(text, return_matches=False) or _is_unsafe_dict(text, return_matches=False)


def _is_unsafe_regex(text: str, return_matches: bool = False):
    longest_matches = []
    for match in pattern.findall(text):
        longest = ""
        for m in match:
            if len(m) > len(longest):
                longest = m
        if len(longest) > 0:
            longest_matches.append(longest)

    if return_matches:
        return longest_matches
    else:
        return len(longest_matches) > 0


def _is_unsafe_dict(text: str, return_matches: bool = False):
    matches = []
    for word in bad_words:
        if word in text:
            found_bad_words = True
            if word in exceptions:
                for exception in exceptions[word]:
                    if exception in text:
                        found_bad_words = False
                        break
            if found_bad_words:
                if return_matches:
                    matches.append(word)
                else:
                    return True
    if return_matches:
        return matches
    else:
        return False

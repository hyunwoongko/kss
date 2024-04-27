# Core algorithm was copied from Kiwi (https://github.com/bab2min/kiwipiepy).
# And modified by Hyunwoong Ko [https://github.com/hyunwoongko]
import re
from functools import partial
from typing import Union, List, Tuple

from kss._elements.subclasses import Token
from kss._modules.morphemes.analyzers import Analyzer
from kss._modules.morphemes.split_morphemes import split_morphemes
from kss._modules.morphemes.utils import _reset_spaces
from kss._modules.sentences.split_sentences import _split_sentences
from kss._modules.spacing.utils import postprocess, postprocess_heuristic
from kss._utils.multiprocessing import _run_job
from kss._utils.sanity_checks import _check_text, _check_backend_mecab_pecab_only, _check_num_workers

any_ws = re.compile(r"\s+")
space_insertable = r"(([^SUWX]|X[RS]|S[EH]).* ([NMI]|V[VAX]|VCN|XR|XPN|S[WLHN]))|(SN ([MI]|N[PR]|NN[GP]|V[VAX]|VCN|XR|XPN|S[WHN]))|((S[FPL]).* ([NMI]|V[VAX]|VCN|XR|XPN|S[WHN]))"
space_insertable = re.compile(space_insertable)

backup_dict = {
    "ㆍ": "/ㆍ/",
    "\n": "\u2424",  # Symbol for newline
    "\t": "\u2409",  # Symbol for horizontal tab
    "\r": "\u240D",  # Symbol for carriage return
    "\f": "\u240C",  # Symbol for form feed
    "\v": "\u240B",  # Symbol for vertical tab
}
restore_dict = {
    v: k for k, v in backup_dict.items()
}


def correct_spacing(
    text: Union[str, List[str], Tuple[str]],
    backend: str = "auto",
    num_workers: Union[int, str] = "auto",
    reset_whitespaces: bool = False,
    return_morphemes: bool = False,
) -> Union[str, List[str]]:
    """
    This corrects the spacing of the text.

    Args:
        text (Union[str, List[str], Tuple[str]]): single text or list/tuple of texts
        backend (str): morpheme analyzer backend. 'mecab', 'pecab', 'punct' are supported
        num_workers (Union[int, str])): the number of multiprocessing workers
        reset_whitespaces (bool): reset whitespaces or not
        return_morphemes (bool): whether to return morphemes or not

    Returns:
        Union[str, List[str]]: corrected text or list of corrected texts

    Examples:
        >>> from kss import Kss
        >>> correct_spacing = Kss("correct_spacing")
        >>> text = "아버지가방에들어가시다"
        >>> correct_spacing(text)
        '아버지가 방에 들어가시다'

    References:
        This was copied from [Kiwi](https://github.com/bab2min/kiwipiepy) and [ko-prfrdr](https://github.com/ychoi-kr/ko-prfrdr)
        and modified by Kss
    """
    text, finish = _check_text(text)

    if finish:
        return text

    backend_string = backend
    backend = _check_backend_mecab_pecab_only(backend)
    _num_workers = _check_num_workers(text, num_workers)

    return _run_job(
        func=partial(_correct_spacing,
                     backend=backend,
                     backend_string=backend_string,
                     reset_whitespaces=reset_whitespaces,
                     return_morphemes=return_morphemes),
        inputs=text,
        num_workers=_num_workers,
    )


def _correct_spacing(
    text: str,
    backend: Analyzer,
    backend_string: str,
    reset_whitespaces: bool = False,
    return_morphemes: bool = False,
) -> Union[str, Tuple[str, List[Tuple[str, str]]]]:
    if reset_whitespaces:
        text = text.replace(" ", "")

    for k, v in backup_dict.items():
        text = text.replace(k, v)

    tokens = []
    chunks = []
    char_length = 0
    last_position = 0
    prev_token = None

    morphs = split_morphemes(
        text,
        backend=backend_string,
        drop_space=False
    )

    for i, (word, pos) in enumerate(morphs):
        token = Token(
            text=word,
            pos=pos.split("+")[0],
            idx=i,
            start=char_length,
            end=char_length + len(word),
        )
        char_length += len(word)
        tokens.append(token)

    for t in tokens:
        if last_position < t.start:
            if (t.pos.startswith("E") or t.pos.startswith("J") or t.pos.startswith("XS")
                or t.pos == "VX" and t.text in "하지"
            ):
                s = any_ws.sub("", text[last_position:t.start])
            else:
                s = text[last_position:t.start]
            if s:
                chunks.append(s)
            last_position = t.start

        if prev_token and space_insertable.match(prev_token.pos + " " + t.pos):
            if t.pos == "VX" and t.text in "하지":
                pass
            elif len(chunks) != 0 and not chunks[-1][-1].isspace():
                chunks.append(" ")

        if last_position < t.end:
            s = any_ws.sub("", text[last_position:t.end])
            if s:
                chunks.append(s)

        last_position = t.end
        prev_token = t

    if last_position < len(text):
        chunks.append(text[last_position:])

    output_text = "".join(chunks)
    sents, morphs = _split_sentences(
        output_text,
        backend=backend,
        recursion=99,
        strip=True,
        return_morphemes=True
    )

    output_text = " ".join(sents)
    morphs_with_spaces = _reset_spaces(output_text, morphs)

    output_text = postprocess(output_text, morphs_with_spaces)
    output_text = postprocess_heuristic(output_text)

    for k, v in restore_dict.items():
        output_text = output_text.replace(k, v)

    if return_morphemes:
        morphs_with_spaces = _reset_spaces(output_text, morphs_with_spaces)
        return output_text, morphs_with_spaces
    else:
        return output_text

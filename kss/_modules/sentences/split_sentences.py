# Copyright (C) 2021 Hyunwoong Ko <kevin.brain@kakaobrain.com> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.

from functools import partial, lru_cache
from typing import List, Union, Tuple, Any

from kss._modules.morphemes.utils import _reset_spaces

from kss._elements.subclasses import Syllable
from kss._modules.morphemes.analyzers import Analyzer
from kss._modules.sentences.embracing_processor import EmbracingProcessor
from kss._modules.sentences.sentence_postprocessor import SentencePostprocessor
from kss._modules.sentences.sentence_preprocessor import SentencePreprocessor
from kss._modules.sentences.sentence_splitter import SentenceSplitter
from kss._utils.multiprocessing import _run_job
from kss._utils.sanity_checks import (
    _check_num_workers,
    _check_text,
    _check_analyzer_backend,
    _check_type,
    _check_iterable_type,
)

preprocessors = {(): SentencePreprocessor()}
postprocessors = {(): SentencePostprocessor()}


def split_sentences(
    text: Union[str, List[str], Tuple[str]],
    backend: str = "auto",
    num_workers: Union[int, str] = "auto",
    strip: bool = True,
    return_morphemes: bool = False,
    ignores: List[str] = None,
) -> Union[List[str], List[List[str]]]:
    """
    This splits texts into sentences.

    Args:
        text (Union[str, List[str], Tuple[str]]): single text or list/tuple of texts
        backend (str): morpheme analyzer backend. 'mecab', 'pecab', 'punct' are supported
        num_workers (Union[int, str])): the number of multiprocessing workers
        strip (bool): strip all sentences or not
        return_morphemes (bool): whether to return morphemes or not
        ignores (List[str]): list of strings to ignore

    Returns:
        Union[List[str], List[List[str]]]: outputs of sentence splitting

    Examples:
        >>> from kss import Kss
        >>> split_sentences = Kss("split_sentences")
        >>> text = "회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요 다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다 강남역 맛집 토끼정의 외부 모습."
        >>> split_sentences(text)
        ['회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요', '다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다', '강남역 맛집 토끼정의 외부 모습.']
    """
    if ignores is None:
        ignores = []

    text, finish = _check_text(text)
    strip = _check_type(strip, "strip", bool)
    return_morphemes = _check_type(return_morphemes, "return_morphemes", bool)
    ignores = _check_iterable_type(ignores, "ignores", list, str)

    if finish:
        return text

    backend_analyzer = _check_analyzer_backend(backend)
    num_workers = _check_num_workers(text, num_workers)

    ignores_tuple = tuple(ignores)
    if ignores_tuple not in preprocessors:
        preprocessors[ignores_tuple] = SentencePreprocessor(ignores)
        postprocessors[ignores_tuple] = SentencePostprocessor(ignores)
    _preprocessor = preprocessors[ignores_tuple]
    _postprocessor = postprocessors[ignores_tuple]

    if backend_analyzer._backend == "fast":
        try:
            from kss_cython import split_sentences_fast as _split_sentences_fast
        except ImportError:
            from kss._modules.sentences.sentence_splitter_fast import _split_sentences_fast

        split_fn = _split_sentences_fast
    else:
        split_fn = _split_sentences

    return _run_job(
        func=partial(
            split_fn,
            backend=backend_analyzer,
            strip=strip,
            return_morphemes=return_morphemes,
            preprocessor=_preprocessor,
            postprocessor=_postprocessor,
        ),
        inputs=text,
        num_workers=num_workers,
    )


@lru_cache(maxsize=500)
def _split_sentences(
    text: Union[str, Tuple[Syllable]],
    backend: Analyzer,
    strip: bool,
    postprocess: bool = True,
    recursion: int = 0,
    return_morphemes: bool = False,
    preprocessor: SentencePreprocessor = preprocessors[()],
    postprocessor: SentencePostprocessor = postprocessors[()],
):
    """
    Split texts into sentences.

    Args:
        text (Union[str, List[Syllable]]): single text
        backend (str): morpheme analyzer backend
        strip (bool): strip all sentences or not
        postprocess (bool): whether it uses postprocessing or not
        recursion (int): recursion times
        return_morphemes (bool): whether to return morphemes or not
        preprocessor (SentencePreprocessor): sentence preprocessor
        postprocessor (SentencePostprocessor): sentence postprocessor

    Returns:
        List[str]: outputs of sentence splitting.
    """

    embracing = EmbracingProcessor()

    # 1. analyze morphemes
    if isinstance(text, str):
        backup_sentence = preprocessor.backup(text)
        morphemes = backend.pos(backup_sentence, drop_space=False)
        syllables = preprocessor.preprocess(morphemes)
    elif isinstance(text, tuple) and len(text) > 0 and isinstance(text[0], Syllable):
        syllables = text
    elif isinstance(text, tuple) and len(text) == 0:
        syllables = tuple()
    else:
        raise ValueError("Wrong data type input for `_split_sentences`.")

    # 2. define variables used for splitting
    output_sentences = []
    current_sentence_syllables = []
    prev_embracing_mode = False
    split_mode = False

    # 3. split sentences
    for idx, syllable in enumerate(syllables):
        sent_idx = len(output_sentences)
        splitter = SentenceSplitter(syllable)
        syllable_added = False
        embracing.process(idx, sent_idx, syllable)
        current_embracing_mode = not embracing.empty()

        if split_mode is False:
            if splitter.check_split_right_now():
                output_sentences.append(current_sentence_syllables)
                current_sentence_syllables = [syllable]
                syllable_added = True

            else:
                if backend._backend == "character":
                    split_mode = splitter._sf()
                else:
                    split_mode = splitter.check_split_start()

        else:
            end_split, end_split_exception = splitter.check_split_end()
            embracing.update_index(idx, sent_idx, syllable)

            if end_split is True:
                split_mode = False

                if current_embracing_mode is False and prev_embracing_mode is True:
                    current_sentence_syllables.append(syllable)
                    output_sentences.append(current_sentence_syllables)
                    current_sentence_syllables = []
                    syllable_added = True

                else:
                    if prev_embracing_mode is False:
                        output_sentences.append(current_sentence_syllables)
                        current_sentence_syllables = []
                    else:
                        split_mode = end_split_exception

        if not syllable_added:
            current_sentence_syllables.append(syllable)

        prev_embracing_mode = current_embracing_mode

    if len(current_sentence_syllables) != 0:
        output_sentences.append(current_sentence_syllables)

    # 4. realign wrong quotes and brackets
    if recursion < 10:
        output_sentences = embracing.realign(
            input_sentences=syllables,
            output_sentences=output_sentences,
            func=partial(
                _split_sentences,
                backend=backend,
                strip=strip,
                return_morphemes=False,
                postprocess=False,
                recursion=recursion + 1,
            ),
        )

    # 5. postprocess
    if postprocess is True:
        output_sentences = postprocessor.postprocess(output_sentences, strip)
        output_sentences = [postprocessor.restore(s, text) for s in output_sentences]

    if return_morphemes and isinstance(text, str):
        morphs_with_spaces = _reset_spaces(" ".join(output_sentences), morphemes)
        return output_sentences, morphs_with_spaces
    else:
        return output_sentences

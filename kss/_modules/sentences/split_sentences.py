# Copyright (C) 2021 Hyunwoong Ko <kevin.ko@tunib.ai> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.

from functools import partial, lru_cache
from typing import List, Union, Tuple

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
)

preprocessor = SentencePreprocessor()
postprocessor = SentencePostprocessor()


def split_sentences(
    text: Union[str, List[str], Tuple[str]],
    backend: str = "auto",
    num_workers: Union[int, str] = "auto",
    strip: bool = True,
) -> Union[List[str], List[List[str]]]:
    """
    Split texts into sentences.

    Args:
        text (Union[str, List[str], Tuple[str]]): single text or list/tuple of texts
        backend (str): morpheme analyzer backend. 'mecab', 'pecab', 'punkt' are supported.
        num_workers (Union[int, str])): the number of multiprocessing workers
        strip (bool): strip all sentences or not

    Returns:
        Union[List[str], List[List[str]]]: outputs of sentence splitting.
    """
    text, finish = _check_text(text)
    strip = _check_type(strip, "strip", bool)

    if finish:
        return text

    backend = _check_analyzer_backend(backend)
    num_workers = _check_num_workers(text, num_workers)

    return _run_job(
        func=partial(_split_sentences, backend=backend, strip=strip),
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
) -> List[str]:
    """
    Split texts into sentences.

    Args:
        text (Union[str, List[Syllable]]): single text
        backend (str): morpheme analyzer backend
        strip (bool): strip all sentences or not
        postprocess (bool): whether it uses postprocessing or not
        recursion (int): recursion times

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
                postprocess=False,
                recursion=recursion + 1,
            ),
        )

    # 5. postprocess
    if postprocess is True:
        output_sentences = postprocessor.postprocess(output_sentences, strip)
        output_sentences = [postprocessor.restore(s, text) for s in output_sentences]

    return output_sentences

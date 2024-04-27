# This code was copied from g2pk [https://github.com/kyubyong/g2pK]
# And modified by Hyunwoong Ko [https://github.com/hyunwoongko]

import re
from functools import partial
from typing import Union, List, Tuple

from kss._modules.g2p.english import convert_eng
from kss._modules.g2p.numerals import convert_num
from kss._modules.g2p.regular import link1, link2, link3, link4
from kss._modules.g2p.special import (
    jyeo,
    ye,
    consonant_ui,
    josa_ui,
    vowel_ui,
    jamo,
    rieulgiyeok,
    rieulbieub,
    verb_nieun,
    balb,
    palatalize,
    modifying_rieul
)
from kss._modules.g2p.utils import (
    rule_id2text,
    annotate,
    gloss,
    group,
    table,
    convert_idioms,
)
from kss._modules.jamo._jamo import h2j, j2h
from kss._utils.multiprocessing import _run_job
from kss._utils.sanity_checks import _check_text, _check_num_workers, _check_type, _check_backend_mecab_pecab_only


def g2p(
    text: Union[str, List[str], Tuple[str]],
    descriptive: bool = False,
    group_vowels: bool = False,
    to_syllable: bool = True,
    convert_english_to_hangul_phonemes: bool = True,
    convert_numbers_to_hangul_phonemes: bool = True,
    num_workers: Union[int, str] = "auto",
    backend: str = "auto",
    verbose: bool = False,
) -> Union[str, List[str]]:
    """
    This function provides a way to convert Korean graphemes to phonemes.
    The 'grapheme' means a letter or a character, and the 'phoneme' means a sound.

    Args:
        text (Union[str, List[str], Tuple[str]]): single text or list of texts
        descriptive (bool): return descriptive pronunciation, the 'descriptive' means a real-life pronunciation
        group_vowels (bool): If True, the vowels of the identical sound are normalized. (e.g. ㅒ -> ㅖ)
        to_syllable: If True, hangul letters or jamo are assembled to form syllables.
        convert_english_to_hangul_phonemes (bool): If True, convert English to Hangul phonemes
        convert_numbers_to_hangul_phonemes (bool): If True, convert numbers to Hangul phonemes
        num_workers (Union[int, str]): the number of multiprocessing workers
        backend (str): morpheme analyzer backend. 'mecab', 'pecab' are supported
        verbose (bool): whether to print verbose outputs or not

    Returns:
        Union[str, List[str]]: phoneme string or list of phoneme strings from the given text

    Examples:
        >>> from kss import Kss
        >>> g2p = Kss("g2p")
        >>> text = "어제는 맑았는데 오늘은 흐리다."
        >>> output = g2p(text)
        >>> print(output)
        "어제는 말간는데 오느른 흐리다."

    References:
        This was copied from [g2pk](https://github.com/Kyubyong/g2pk) and modified by Kss
    """
    text, finish = _check_text(text)

    if finish:
        return text

    descriptive = _check_type(descriptive, "descriptive", bool)
    group_vowels = _check_type(group_vowels, "group_vowels", bool)
    to_syllable = _check_type(to_syllable, "to_syllable", bool)
    convert_english_to_hangul_phonemes = _check_type(convert_english_to_hangul_phonemes,
                                                     "convert_english_to_hangul_phonemes", bool)
    convert_numbers_to_hangul_phonemes = _check_type(convert_numbers_to_hangul_phonemes,
                                                     "convert_numbers_to_hangul_phonemes", bool)
    verbose = _check_type(verbose, "verbose", bool)
    num_workers = _check_num_workers(text, num_workers)
    _check_backend_mecab_pecab_only(backend)

    return _run_job(
        func=partial(
            _g2p,
            descriptive=descriptive,
            group_vowels=group_vowels,
            to_syllable=to_syllable,
            convert_english_to_hangul_phonemes=convert_english_to_hangul_phonemes,
            convert_numbers_to_hangul_phonemes=convert_numbers_to_hangul_phonemes,
            backend=backend,
            verbose=verbose,
        ),
        inputs=text,
        num_workers=num_workers,
    )


def _g2p(
    text: str,
    descriptive: bool = False,
    group_vowels: bool = False,
    to_syllable: bool = True,
    convert_english_to_hangul_phonemes: bool = True,
    convert_numbers_to_hangul_phonemes: bool = True,
    backend: str = "auto",
    verbose: bool = False,
):
    """
    Main function

    Args:
        text: input text
        descriptive: boolean.
        group_vowels: boolean. If True, the vowels of the identical sound are normalized.
        to_syllable: boolean. If True, hangul letters or jamo are assembled to form syllables.
        convert_english_to_hangul_phonemes: boolean. If True, convert English to Hangul phonemes.
        convert_numbers_to_hangul_phonemes: boolean. If True, convert numbers to Hangul phonemes.
        backend: str
        verbose: boolean

    Notes:
        For example, given an input string "나의 친구가 mp3 file 3개를 다운받고 있다",
        STEP 1. idioms
        -> 나의 친구가 엠피쓰리 file 3개를 다운받고 있다

        STEP 2. English to Hangul
        -> 나의 친구가 엠피쓰리 파일 3개를 다운받고 있다

        STEP 3. annotate
        -> 나의/J 친구가 엠피쓰리 파일 3개/B를 다운받고 있다

        STEP 4. Spell out arabic numbers
        -> 나의/J 친구가 엠피쓰리 파일 세개/B를 다운받고 있다

        STEP 5. decompose
        -> 나의/J 친구가 엠피쓰리 파일 세개/B를 다운받고 있다

        STEP 6-9. Hangul
        -> 나의 친구가 엠피쓰리 파일 세개를 다운받꼬 읻따

    Returns:
        str: Phoneme string
    """
    # 1. idioms
    text = convert_idioms(
        text=text,
        descriptive=descriptive,
        convert_english_to_hangul_phonemes=convert_english_to_hangul_phonemes,
        convert_numbers_to_hangul_phonemes=convert_numbers_to_hangul_phonemes,
        verbose=verbose,
    )

    # 2 English to Hangul
    if convert_english_to_hangul_phonemes:
        text = convert_eng(text)

    # 3. annotate
    text = annotate(text, backend=backend)

    # 4. Spell out arabic numbers
    if convert_numbers_to_hangul_phonemes:
        text = convert_num(text)

    # 5. decompose
    inp = h2j(text)

    # 6. special
    for func in (jyeo, ye, consonant_ui, josa_ui, vowel_ui, \
                 jamo, rieulgiyeok, rieulbieub, verb_nieun, \
                 balb, palatalize, modifying_rieul):
        inp = func(inp, descriptive, verbose)
    inp = re.sub("/[PJEB]", "", inp)

    # 7. regular table: batchim + onset
    for str1, str2, rule_ids in table:
        _inp = inp
        inp = re.sub(str1, str2, inp)

        if len(rule_ids) > 0:
            rule = "\n".join(rule_id2text.get(rule_id, "") for rule_id in rule_ids)
        else:
            rule = ""
        gloss(verbose, inp, _inp, rule)

    # 8 link
    for func in (link1, link2, link3, link4):
        inp = func(inp, descriptive, verbose)

    # 9. postprocessing
    if group_vowels:
        inp = group(inp)

    if to_syllable:
        inp = j2h(inp, add_placeholder_for_leading_vowels=True)
    return inp

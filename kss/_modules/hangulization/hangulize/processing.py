# -*- coding: utf-8 -*-
"""
    hangulize.processing
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2010-2017 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from kss._modules.hangulization.hangulize.hangul import EU, Null, NG, UnicodeHangulError, join, split
from kss._modules.hangulization.hangulize.models import Choseong, Impurity, Jongseong, Jungseong


__all__ = ['complete_syllable', 'complete_syllables', 'split_phonemes',
           'join_phonemes']


def complete_syllable(syllable):
    """Inserts the default jungseong or jongseong if it is not exists::

        >>> complete_syllable((Jungseong(YO),))
        (u'ㅇ', u'ㅛ', u'')
        >>> print hangulize.hangul.join(_)
        요

    """
    syllable = list(syllable)
    components = [type(ph) for ph in syllable]
    if Choseong not in components:
        syllable.insert(0, Choseong(NG))
    if Jungseong not in components:
        syllable.insert(1, Jungseong(EU))
    if Jongseong not in components:
        syllable.insert(2, Jungseong(Null))
    return tuple((ph.letter for ph in syllable))


def complete_syllables(phonemes):
    """Separates each syllables and completes every syllable."""
    components, syllable = [Choseong, Jungseong, Jongseong], []
    if phonemes:
        for ph in phonemes:
            comp = type(ph)
            new_syllable = (comp is Impurity or syllable and
                            components.index(comp) <=
                            components.index(type(syllable[-1])))
            if new_syllable:
                if syllable:
                    yield complete_syllable(syllable)
                    syllable = []
                if comp is Impurity:
                    yield (ph,)
                    continue
            syllable.append(ph)
        if syllable:
            yield complete_syllable(syllable)


def split_phonemes(word):
    """Returns the splitted phonemes from the word.

        >>> split_phonemes(u'안녕') #doctest: +NORMALIZE_WHITESPACE
        (<Choseong 'ㅇ'>, <Jungseong 'ㅏ'>, <Jongseong 'ㄴ'>,
         <Choseong 'ㄴ'>, <Jungseong 'ㅕ'>, <Jongseong 'ㅇ'>)
    """
    result = []
    for c in word:
        try:
            c = split(c)
            result.append(Choseong(c[0]))
            result.append(Jungseong(c[1]))
            if c[2] is not Null:
                result.append(Jongseong(c[2]))
        except UnicodeHangulError:
            result.append(Impurity(c))
    return tuple(result)


def join_phonemes(phonemes):
    """Returns the word from the splitted phonemes::

        >>> print join_phonemes((Jungseong(A), Jongseong(N),
        ...                      Choseong(N), Jungseong(YEO), Jongseong(NG)))
        안녕

    """
    syllables = complete_syllables(phonemes)
    chars = (join(syl) for syl in syllables)
    return reduce(unicode.__add__, chars)

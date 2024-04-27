# -*- coding: utf-8 -*-
from kss._modules.hangulization.hangulize import *


class Spanish(Language):
    """For transcribing Spanish."""

    __iso639__ = {1: 'es', 2: 'spa', 3: 'spa'}
    __tmp__ = 'X'

    vowels = u'aeiouüy'
    notation = Notation([
        (u'ññ',            u'ñ'),
        (u'ñ{@}',          'nY'),
        ('^y{@}',          'Y'),
        ('{@}y{@}',        'Y'),
        ('y',              'i'),
        ('aa',             'a'),
        ('ee',             'e'),
        ('ii',             'i'),
        ('oo',             'o'),
        ('uu',             'u'),
        ('hh',             'h'),
        ('k$',             'kX'), # X prevents conversion of preceding letter
                                  # to jongseong
        ('{@}cc{e|i}',     'ks'),
        ('ch{@}',          'C'),
        ('h',              None),
        ('ll',             'Y'),
        ('c{k|q|x}',       None),
        ('cc',             'c'),
        ('c{e|i}',         's'),
        ('c',              'k'),
        ('n{j|k|g|q|x}',   'N'),
        ('g{e|i}',         'j'),
        (u'{g|q}ü{a|e|i}', 'W'),
        (u'ü',             'u'),
        ('{g|q}u{e|i}',    None),
        ('{g|q}ua',        'Wa'),
        ('q',              'k'),
        ('ww',             'w'),
        ('^w{@}',          'W'),
        ('{@}w{@}',        'W'),
        ('w',              'XW'), # X prevents W from joining with preceding
                                  # letter
        ('xx',             'x'),
        ('^x{@}',          's'),
        ('{@}x',           'ks'),
        ('bb',             'b'),
        ('dd',             'd'),
        ('ff',             'f'),
        ('gg',             'g'),
        ('jj',             'j'),
        ('kk',             'k'),
        ('mm',             'm'),
        ('nn',             'n'),
        ('pp',             'p'),
        ('rr',             'r'),
        ('z',              's'),
        ('ss',             's'),
        ('tt',             't'),
        ('vv',             'v'),
        ('b',              Choseong(B)),
        ('C',              Choseong(C)),
        ('d',              Choseong(D)),
        ('f',              Choseong(P)),
        ('g',              Choseong(G)),
        ('j{@}',           Choseong(H)),
        ('j',              None),
        ('^k',             Choseong(K)),
        ('k{@|l|m|n|r|X}', Choseong(K)),
        ('{@}k',           Jongseong(G)),
        ('k',              Choseong(K)),
        ('^m',             'P'),
        ('^n',             'Q'),
        ('{m|n}l',         Choseong(L)),
        ('^l',             Choseong(L)),
        ('l{@}',           Jongseong(L), Choseong(L)),
        ('l',              Jongseong(L)),
        ('P',              Choseong(M)),
        ('m{@}',           Choseong(M)),
        ('m',              Jongseong(M)),
        ('Q',              Choseong(N)),
        ('n{@|Y}',         Choseong(N)),
        ('n',              Jongseong(N)),
        ('N',              Jongseong(NG)),
        ('p{@|l|m|n|r|X}', Choseong(P)),
        ('{@}p',           Jongseong(B)),
        ('p',              Choseong(P)),
        ('r',              Choseong(L)),
        ('s',              Choseong(S)),
        ('t',              Choseong(T)),
        ('v',              Choseong(B)),
        ('Ya',             Jungseong(YA)),
        ('Ye',             Jungseong(YE)),
        ('Yi',             Jungseong(I)),
        ('Yo',             Jungseong(YO)),
        ('Yu',             Jungseong(YU)),
        ('Wa',             Jungseong(WA)),
        ('We',             Jungseong(WE)),
        ('Wi',             Jungseong(WI)),
        ('a',              Jungseong(A)),
        ('e',              Jungseong(E)),
        ('i',              Jungseong(I)),
        ('o',              Jungseong(O)),
        ('u',              Jungseong(U)),
    ])

    def normalize(self, string):
        return normalize_roman(string, {u'Ñ': u'ñ', u'Ǘ': u'ü', u'Ü': u'ü'})


__lang__ = Spanish

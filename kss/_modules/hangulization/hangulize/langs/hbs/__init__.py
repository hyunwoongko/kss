# -*- coding: utf-8 -*-
from kss._modules.hangulization.hangulize import *


class SerboCroatian(Language):
    """For transcribing Serbo-Croatian."""

    __iso639__ = {3: 'hbs'}

    vowels = 'aeiouy'
    consonants = 'cCfhst'
    notation = Notation([
        (u'č',                   'C'),
        (u'ć',                   'C'),
        (u'đ',                   'D'),
        (u'š',                   'S'),
        (u'dž',                  'D'),
        (u'ž',                   'Z'),
        ('tj',                   'C'),
        ('S{@}',                 'sJ'),
        ('S$',                   'si'),
        ('S',                    'sJu'),
        ('^je',                  'Je'),
        ('{@|s}je',              'Je'),
        ('je',                   'e'),
        ('{l|n}j{@}',            'J'),
        ('{l|n}j',               None),
        ('j{@}',                 'J'),
        ('j',                    'i'),
        ('xx',                   'x'),
        ('x',                    'ks'),
        ('qu',                   'kv'),
        ('q',                    'k'),
        ('w',                    'v'),
        ('^y{@}',                'J'),
        ('y',                    'i'),
        ('aa',                   'a'),
        ('bb',                   'b'),
        ('dd',                   'd'),
        ('ee',                   'e'),
        ('ff',                   'f'),
        ('gg',                   'g'),
        ('hh',                   'h'),
        ('ii',                   'i'),
        ('kk',                   'k'),
        ('ll',                   'l'),
        ('{@}mm{@}',             Jongseong(M), Choseong(M)),
        ('mm',                   'm'),
        ('{@}nn{@}',             Jongseong(N), Choseong(N)),
        ('nn',                   'n'),
        ('oo',                   'o'),
        ('pp',                   'p'),
        ('rr',                   'r'),
        ('ss',                   's'),
        ('tt',                   't'),
        ('uu',                   'u'),
        ('vv',                   'v'),
        ('zz',                   'z'),
        ('^k',                   Choseong(K)),
        ('{@}k{<consonants>|p}', Jongseong(G)),
        ('^p',                   Choseong(P)),
        ('{@}p{<consonants>|k}', Jongseong(B)),
        ('k',                    Choseong(K)),
        ('p',                    Choseong(P)),
        ('C{@}',                 Choseong(C)),
        ('C',                    Choseong(C), Jungseong(I)),
        ('b',                    Choseong(B)),
        ('c',                    Choseong(C)),
        ('d',                    Choseong(D)),
        ('D{@}',                 Choseong(J)),
        ('D',                    Choseong(J), Jungseong(I)),
        ('f',                    Choseong(P)),
        ('g',                    Choseong(G)),
        ('h',                    Choseong(H)),
        ('^m',                   'P'),
        ('^n',                   'Q'),
        ('^l',                   Choseong(L)),
        ('{m|n}l',               Choseong(L)),
        ('l{@|J}',               Jongseong(L), Choseong(L)),
        ('l',                    Jongseong(L)),
        ('P',                    Choseong(M)),
        ('m{@|J|l|r|n}',         Choseong(M)),
        ('m',                    Jongseong(M)),
        ('Q',                    Choseong(N)),
        ('n{@|J}',               Choseong(N)),
        ('n',                    Jongseong(N)),
        ('r',                    Choseong(L)),
        ('s',                    Choseong(S)),
        ('t',                    Choseong(T)),
        ('v',                    Choseong(B)),
        ('z',                    Choseong(J)),
        ('Z{@}',                 Choseong(J)),
        ('Z',                    Choseong(J), Jungseong(U)),
        ('Ja',                   Jungseong(YA)),
        ('Je',                   Jungseong(YE)),
        ('Ji',                   Jungseong(I)),
        ('Jo',                   Jungseong(YO)),
        ('Ju',                   Jungseong(YU)),
        ('a',                    Jungseong(A)),
        ('e',                    Jungseong(E)),
        ('i',                    Jungseong(I)),
        ('o',                    Jungseong(O)),
        ('u',                    Jungseong(U))
    ])

    def normalize(self, string):
        return normalize_roman(string, {
            u'А': 'a', u'а': 'a', u'Б': 'b', u'б': 'b', u'В': 'v',
            u'в': 'v', u'Г': 'g', u'г': 'g', u'Д': 'd', u'д': 'd',
            u'Ђ': u'đ', u'ђ': u'đ', u'Е': 'e', u'е': 'e', u'Ж': u'ž',
            u'ж': u'ž', u'З': 'z', u'з': 'z', u'И': 'i', u'и': 'i',
            u'Ј': 'j', u'ј': 'j', u'К': 'k', u'к': 'k', u'Л': 'l',
            u'л': 'l', u'Љ': 'lj', u'љ': 'lj', u'М': 'm', u'м': 'm',
            u'Н': 'n', u'н': 'n', u'Њ': 'nj', u'њ': 'nj', u'О': 'o',
            u'о': 'o', u'П': 'p', u'п': 'p', u'Р': 'r', u'р': 'r',
            u'С': 's', u'с': 's', u'Т': 't', u'т': 't', u'Ћ': u'ć',
            u'ћ': u'ć', u'У': 'u', u'у': 'u', u'Ф': 'f', u'ф': 'f',
            u'Х': 'h', u'х': 'h', u'Ц': 'c', u'ц': 'c', u'Ч': 'C',
            u'ч': 'C', u'Џ': u'dž', u'џ': u'dž', u'Ш': u'š', u'ш': u'š',
            u'Č': u'č', u'Ć': u'ć', u'Đ': u'đ', u'Š': u'š', u'Ž': u'ž',
            u'Ǆ': u'dž', # DŽ digraph
            u'ǅ': u'dž', # Dž digraph
            u'Ǉ': 'lj', # LJ digraph
            u'ǈ': 'lj', # Lj digraph
            u'Ǌ': 'nj', # NJ digraph
            u'ǋ': 'nj' # Nj digraph
        })


__lang__ = SerboCroatian

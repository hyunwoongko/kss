# -*- coding: utf-8 -*-
from kss._modules.hangulization.hangulize import *


class Finnish(Language):
    """For transcribing Finnish."""

    __iso639__ = {1: 'fi', 2: 'fin', 3: 'fin'}
    __tmp__ = ',;%'

    vowels = 'aAeioOuy'
    ob = 'bdfgkpstT'
    notation = Notation([
        # Convention: A = ä, O = ö
        (u'å', 'o'),
        (u'ä', 'A'),
        (u'ö', 'O'),
        ('w', 'v'),
        ('xx', 'x'),
        ('x', 'ks'),
        ('z', 's'),
        ('ds', 'T'),
        ('ts', 'T'),
        ('c{e|i|y}', 's'),
        ('c', 'k'),
        ('q', 'k'),
        ('ng', 'N'),
        ('nk', 'Nk'),
        ('mn{@}', 'm,n'),
        ('mn', 'm'),
        ('th', 't'),
        ('^j{@}', 'J'),
        ('{@}j{@}', 'J'),
        ('{h|s|T}j', '%J'),
        ('j', 'i'),
        ('aa', 'a'),
        ('bb', 'b'),
        ('dd', 'd'),
        ('ee', 'e'),
        ('AA', 'A'),
        ('ff', 'f'),
        ('gg', 'g'),
        ('hh', 'h'),
        ('ii', 'i'),
        ('jj', 'j'),
        ('kk', 'k'),
        ('ll', 'l'),
        ('{@}mm{@}', 'm,m'),
        ('mm', 'm'),
        ('{@}nn{@}', 'n,n'),
        ('nn', 'n'),
        ('oo', 'o'),
        ('pp', 'p'),
        ('rr', 'r'),
        ('ss', 's'),
        ('tt', 't'),
        ('uu', 'u'),
        ('vv', 'v'),
        ('yy', 'y'),
        ('zz', 'z'),
        ('{@}b{<ob>}', 'p,'),
        ('{@}g{<ob>}', 'k,'),
        ('{@}k{<ob>}', 'k,'),
        ('{@}p{<ob>}', 'p,'),
        ('{@}t{<ob>}', 't,'),
        ('^l', 'l;'),
        ('^m', 'm;'),
        ('^n', 'n;'),
        ('l$', 'l,'),
        ('m$', 'm,'),
        ('n$', 'n,'),
        ('l{@|m,|n,|N}', 'l;'),
        ('{,}l', 'l;'),
        ('m{@}', 'm;'),
        ('n{@}', 'n;'),
        ('l', 'l,'),
        ('m', 'm,'),
        ('n', 'n,'),
        ('N', 'N,'),
        (',,', ','),
        (',;', None),
        (',l,', 'l,'),
        (',m,', 'm,'),
        (',n,', 'n,'),
        (',N,', 'N,'),
        ('l{m;|n;}', 'l,'),
        (';', None),
        ('b', Choseong(B)),
        ('d', Choseong(D)),
        ('f', Choseong(P)),
        ('g', Choseong(G)),
        ('h', Choseong(H)),
        ('k,', Jongseong(G)),
        ('k', Choseong(K)),
        ('^l', Choseong(L)),
        ('{,|-}l', Choseong(L)),
        ('-', None),
        ('l,', Jongseong(L)),
        ('l', Jongseong(L), Choseong(L)),
        ('m,', Jongseong(M)),
        ('m', Choseong(M)),
        ('n,', Jongseong(N)),
        ('n', Choseong(N)),
        ('N', Jongseong(NG)),
        ('p,', Jongseong(B)),
        ('p', Choseong(P)),
        ('r', Choseong(L)),
        ('s', Choseong(S)),
        ('t,', Jongseong(S)),
        ('t', Choseong(T)),
        ('T', Choseong(C)),
        ('v', Choseong(B)),
        ('%', Choseong(NG)),
        ('Ja', Jungseong(YA)),
        ('JA', Jungseong(YAE)),
        ('Je', Jungseong(YE)),
        ('Ji', Jungseong(I)),
        ('Jo', Jungseong(YO)),
        ('JO', Jungseong(OE)),
        ('Ju', Jungseong(YU)),
        ('Jy', Jungseong(WI)),
        ('a', Jungseong(A)),
        ('A', Jungseong(AE)),
        ('e', Jungseong(E)),
        ('i', Jungseong(I)),
        ('o', Jungseong(O)),
        ('u', Jungseong(U)),
        ('y', Jungseong(WI)),
        ('O', Jungseong(OE)),
    ])

    def normalize(self, string):
        return normalize_roman(string, {
            u'Å': u'å', u'Ǻ': u'å', u'ǻ': u'å', u'Ä': u'ä', u'Ö': u'ö'
        })


__lang__ = Finnish

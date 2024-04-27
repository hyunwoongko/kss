# -*- coding: utf-8 -*-
from kss._modules.hangulization.hangulize import *


class Hungarian(Language):
    """For transcribing Hungarian."""

    __iso639__ = {1: 'hu', 2: 'hun', 3: 'hun'}
    __tmp__ = ',;'

    vowels = 'aAeioOuU'
    cs = 'bcCdDfghklmnpqrsStvwxzZ'
    vl = 'cCfhkpsSt'
    notation = Notation([
        (u'á',         'A'),
        (u'ö',         'O'),
        (u'ü',         'U'),
        ('j',          'y'),
        ('cc',         'c'),
        ('cs',         'C'),
        ('ch',         'C'), # archaic spelling
        ('cz',         'c'), # archaic spelling
        ('dd',         'd'),
        ('dy',         'D'), # affrication
        ('dzs',        'D'),
        ('gg',         'g'),
        ('gy',         'D'),
        ('ny{@}',      'nJ'),
        ('ny',         'ni'),
        ('qq',         'q'),
        ('q{@}',       'kv'),
        ('q',          'k'),
        ('xx',         'x'),
        ('x',          'kS'),
        ('ss',         's'),
        ('sz',         'S'),
        ('tt',         't'),
        ('th',         't'), # archaic spelling
        ('ts',         'C'), # archaic spelling
        ('ty',         'C'),
        ('tz',         'c'), # archaic spelling
        ('zz',         'z'),
        ('zs',         'Z'),
        ('ll',         'l'),
        ('ly{@}',      'J'),
        ('ly',         'i'),
        ('^y{@}',      'J'),
        ('{@}y{@}',    'J'),
        ('y',          'i'),
        ('^Je',        'Ye'),
        ('{@|s|S}Je',  'Ye'),
        ('Je',         'e'),
        ('Y',          'J'),
        ('aa',         'a'),
        ('bb',         'b'),
        ('ee',         'e'),
        ('eO',         'O'), # archaic spelling
        ('ew',         'O'), # archaic spelling
        ('ff',         'f'),
        ('hh',         'h'),
        ('ii',         'i'),
        ('kk',         'k'),
        ('{@}mm{@}',   'm,m'),
        ('mm',         'm'),
        ('{@}nn{@|J}', 'n,n'),
        ('nn',         'n'),
        ('oo',         'o'),
        ('OO',         'O'),
        ('pp',         'p'),
        ('rr',         'r'),
        ('s{@}',       'SJ'),
        ('s$',         'Si'),
        ('s',          'SJu'),
        ('uu',         'u'),
        ('UU',         'U'),
        ('w',          'v'),
        ('vv',         'v'),
        ('C{<cs>}',    'Ci'),
        ('C$',         'Ci'),
        ('D{<cs>}',    'Di'),
        ('D$',         'Di'),
        ('Z{<cs>}',    'Zu'),
        ('Z$',         'Zu'),
        ('^l',         'l;'),
        ('^m',         'm;'),
        ('^n',         'n;'),
        ('l$',         'l,'),
        ('m$',         'm,'),
        ('n$',         'n,'),
        ('l{@|m,|n,}', 'l;'),
        ('{,}l',       'l;'),
        ('m{@}',       'm;'),
        ('n{@|J}',     'n;'),
        ('l',          'l,'),
        ('m',          'm,'),
        ('n',          'n,'),
        (',,',         ','),
        (',;',         None),
        (',l,',        'l,'),
        (',m,',        'm,'),
        (',n,',        'n,'),
        ('l{m;|n;}',   'l,'),
        (';',          None),       
        ('{@}k{<vl>}', 'k,'),
        ('{@}p{<vl>}', 'p,'),
        ('b',          Choseong(B)),
        ('c',          Choseong(C)),
        ('C',          Choseong(C)),
        ('d',          Choseong(D)),
        ('D',          Choseong(J)),
        ('f',          Choseong(P)),
        ('g',          Choseong(G)),
        ('h',          Choseong(H)),
        ('k,',         Jongseong(G)),
        ('k',          Choseong(K)),
        ('^l',         Choseong(L)),
        ('{,}l',       Choseong(L)),
        ('l,',         Jongseong(L)),
        ('l',          Jongseong(L), Choseong(L)),
        ('m,',         Jongseong(M)),
        ('m',          Choseong(M)),
        ('n,',         Jongseong(N)),
        ('n',          Choseong(N)),
        ('p,',         Jongseong(B)),
        ('p',          Choseong(P)),
        ('r',          Choseong(L)),
        ('S',          Choseong(S)),
        ('t',          Choseong(T)),
        ('v',          Choseong(B)),
        ('z',          Choseong(J)),
        ('Z',          Choseong(J)),
        ('Ja',         Jungseong(YEO)),
        ('JA',         Jungseong(YA)),
        ('Je',         Jungseong(YE)),
        ('Ji',         Jungseong(I)),
        ('Jo',         Jungseong(YO)),
        ('JO',         Jungseong(OE)),
        ('Ju',         Jungseong(YU)),
        ('JU',         Jungseong(WI)),
        ('a',          Jungseong(EO)),
        ('A',          Jungseong(A)),
        ('e',          Jungseong(E)),
        ('i',          Jungseong(I)),
        ('o',          Jungseong(O)),
        ('O',          Jungseong(OE)),
        ('u',          Jungseong(U)),
        ('U',          Jungseong(WI)),
    ])

    def normalize(self, string):
        return normalize_roman(string, {
            u'Á': u'á', u'Ö': u'ö', u'Ő': u'ö', u'ő': u'ö', u'Ü': u'ü',
            u'Ű': u'ü', u'ű': u'ü'
        })


__lang__ = Hungarian

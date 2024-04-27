#
# This file is part of KoreanCodecs.
#
# Copyright(C) 2002-2003 Hye-Shik Chang <perky@FreeBSD.org>.
#
# KoreanCodecs is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# KoreanCodecs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with KoreanCodecs; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# $Id: hangul.py,v 1.2 2003/10/15 19:24:53 perky Exp $
#
from itertools import chain


class UnicodeHangulError(Exception):

    def __init__(self, msg):
        self.msg = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.msg

    __str__ = __repr__


Null = u''


class Jaeum:
    Codes = (u'\u3131', u'\u3132', u'\u3133', u'\u3134', u'\u3135', u'\u3136',
             #    G         GG          GS         N          NJ         NH
             u'\u3137', u'\u3138', u'\u3139', u'\u313a', u'\u313b', u'\u313c',
             #    D         DD          L          LG         LM         LB
             u'\u313d', u'\u313e', u'\u313f', u'\u3140', u'\u3141', u'\u3142',
             #    LS        LT          LP         LH         M          B
             u'\u3143', u'\u3144', u'\u3145', u'\u3146', u'\u3147', u'\u3148',
             #    BB        BS          S          SS         NG         J
             u'\u3149', u'\u314a', u'\u314b', u'\u314c', u'\u314d', u'\u314e')
    #    JJ        C           K          T          P          H
    Width = len(Codes)
    G, GG, GS, N, NJ, NH, D, DD, L, LG, LM, LB, LS, LT, LP, LH, M, B, \
        BB, BS, S, SS, NG, J, JJ, C, K, T, P, H = Codes
    Choseong = [G, GG, N, D, DD, L, M, B, BB, S, SS, NG, J, JJ, C, K, T, P, H]
    Jongseong = [Null, G, GG, GS, N, NJ, NH, D, L, LG, LM, LB, LS, LT, \
                 LP, LH, M, B, BS, S, SS, NG, J, C, K, T, P, H]
    MultiElement = {
        GG: (G, G), GS: (G, S), NJ: (N, J), NH: (N, H), DD: (D, D),
        LG: (L, G), LM: (L, M), LB: (L, B), LS: (L, S), LT: (L, T),
        LP: (L, P), LH: (L, H), BB: (B, B), BS: (B, S), SS: (S, S),
        JJ: (J, J)
    }


class Moeum:
    Codes = (u'\u314f', u'\u3150', u'\u3151', u'\u3152', u'\u3153', u'\u3154',
             #    A          AE        YA         YAE         EO         E
             u'\u3155', u'\u3156', u'\u3157', u'\u3158', u'\u3159', u'\u315a',
             #    YEO        YE        O          WA          WAE        OE
             u'\u315b', u'\u315c', u'\u315d', u'\u315e', u'\u315f', u'\u3160',
             #    YO         U         WEO        WE          WI         YU
             u'\u3161', u'\u3162', u'\u3163')
    #    EU         YI        I
    Width = len(Codes)
    A, AE, YA, YAE, EO, E, YEO, YE, O, WA, WAE, OE, YO, \
        U, WEO, WE, WI, YU, EU, YI, I = Codes
    Jungseong = list(Codes)
    MultiElement = {
        AE: (A, I), YAE: (YA, I), YE: (YEO, I), WA: (O, A), WAE: (O, A, I),
        OE: (O, I), WEO: (U, EO), WE: (U, E), WI: (U, I), YI: (EU, I)
    }


# Aliases for your convinience
Choseong = Jaeum.Choseong
Jungseong = Moeum.Jungseong
Jongseong = Jaeum.Jongseong

for name, code in chain(Jaeum.__dict__.items(), Moeum.__dict__.items()):
    if name.isupper() and len(name) <= 3:
        exec('%s = %s' % (name, repr(code)))
del name, code

# Unicode Hangul Syllables Characteristics
ZONE = (u'\uAC00', u'\uD7A3')
NCHOSEONG = len(Choseong)
NJUNGSEONG = len(Jungseong)
NJONGSEONG = len(Jongseong)
JBASE_CHOSEONG = u'\u1100'
JBASE_JUNGSEONG = u'\u1161'
JBASE_JONGSEONG = u'\u11A8'
CHOSEONG_FILLER = u'\u115F'
JUNGSEONG_FILLER = u'\u1160'

_ishangul = (
    lambda code:
    ZONE[0] <= code <= ZONE[1] or
    code in Jaeum.Codes or
    code in Moeum.Codes
)

# Alternative Suffixes : do not use outside
ALT_SUFFIXES = {
    u'\uc744': (u'\ub97c', u'\uc744'),  # reul, eul
    u'\ub97c': (u'\ub97c', u'\uc744'),  # reul, eul
    u'\uc740': (u'\ub294', u'\uc740'),  # neun, eun
    u'\ub294': (u'\ub294', u'\uc740'),  # neun, eun
    u'\uc774': (u'\uac00', u'\uc774'),  # yi, ga
    u'\uac00': (u'\uac00', u'\uc774'),  # yi, ga
    u'\uc640': (u'\uc640', u'\uacfc'),  # wa, gwa
    u'\uacfc': (u'\uc640', u'\uacfc'),  # wa, gwa
}

# Ida-Varitaion Suffixes : do not use outside
IDA_SUFFIXES = {
    u'(\uc774)': (u'', u'\uc774'),  # (yi)da
    u'(\uc785)': (17, u'\uc785'),  # (ip)nida
    u'(\uc778)': (4, u'\uc778'),  # (in)-
}


def isJaeum(u):
    if u:
        for c in u:
            if c not in Jaeum.Codes:
                break
        else:
            return True
    return False


def isMoeum(u):
    if u:
        for c in u:
            if c not in Moeum.Codes:
                break
        else:
            return True
    return False


def ishangul(u):
    if u:
        for c in u:
            if not _ishangul(c):
                break
        else:
            return True
    return False


def join(codes):
    """ Join function which makes hangul syllable from jamos """
    if len(codes) != 3:
        raise UnicodeHangulError("needs 3-element tuple")
    if not codes[0] or not codes[1]:  # single jamo
        return codes[0] or codes[1]

    return chr(
        0xac00 + (
            Choseong.index(codes[0]) * NJUNGSEONG +
            Jungseong.index(codes[1])
        ) * NJONGSEONG + Jongseong.index(codes[2])
    )


def split(code):
    """ Split function which splits hangul syllable into jamos """
    if len(code) != 1 or not _ishangul(code):
        raise UnicodeHangulError("needs 1 hangul letter")
    if code in Jaeum.Codes:
        return (code, Null, Null)
    if code in Moeum.Codes:
        return (Null, code, Null)

    code = ord(code) - 0xac00
    return (
        Choseong[int(code / (NJUNGSEONG * NJONGSEONG))],  # Python3000 safe
        Jungseong[int(code / NJONGSEONG) % NJUNGSEONG],
        Jongseong[code % NJONGSEONG]
    )


def conjoin(s):
    obuff = []
    ncur = 0

    while ncur < len(s):
        c = s[ncur]
        if JBASE_CHOSEONG <= c <= u'\u1112' or c == CHOSEONG_FILLER:  # starts with choseong
            if len(s) > ncur + 1 and JUNGSEONG_FILLER <= s[ncur + 1] <= u'\u1175':
                cho = Choseong[ord(c) - ord(JBASE_CHOSEONG)]
                jung = Jungseong[ord(s[ncur + 1]) - ord(JBASE_JUNGSEONG)]
                if len(s) > ncur + 2 and JBASE_JONGSEONG <= s[ncur + 2] <= u'\u11C2':
                    jong = Jongseong[ord(s[ncur + 2]) - ord(JBASE_JONGSEONG) + 1]
                    ncur += 2
                else:
                    jong = Null
                    ncur += 1
                obuff.append(join([cho, jung, jong]))
            else:
                obuff.append(join([Choseong[ord(c) - ord(JBASE_CHOSEONG)], Null, Null]))
        elif JBASE_JUNGSEONG <= c <= u'\u1175':
            obuff.append(join([Null, Jungseong[ord(c) - ord(JBASE_JUNGSEONG)], Null]))
        else:
            obuff.append(c)
        ncur += 1

    return u''.join(obuff)


def disjoint(s):
    obuff = []
    for c in s:
        if _ishangul(c):
            cho, jung, jong = split(c)
            if cho:
                obuff.append(chr(ord(JBASE_CHOSEONG) + Choseong.index(cho)))
            else:
                obuff.append(CHOSEONG_FILLER)

            if jung:
                obuff.append(chr(ord(JBASE_JUNGSEONG) + Jungseong.index(jung)))
            else:
                obuff.append(JUNGSEONG_FILLER)

            if jong:
                obuff.append(chr(ord(JBASE_JONGSEONG) + Jongseong.index(jong) - 1))
        else:
            obuff.append(c)
    return u''.join(obuff)


def _has_final(c):
    # for internal use only
    if u'\uac00' <= c <= u'\ud7a3':  # hangul
        return 1, (ord(c) - 0xac00) % 28 > 0
    else:
        return 0, c in u'013678.bklmnptLMNRZ'


# Iterator Emulator for ancient versions before 2.1
try:
    iter
except:
    class iter:
        def __init__(self, obj):
            self.obj = obj
            self.ptr = 0

        def next(self):
            try:
                return self.obj[self.ptr]
            finally:
                self.ptr += 1

# Nested scope lambda emulation for versions before 2.2
import sys

if sys.hexversion < 0x2020000:
    class plambda:
        def __init__(self, obj):
            self.obj = obj

        def __call__(self):
            return self.obj
else:
    plambda = None
del sys


def format(fmtstr, *args, **kwargs):
    if kwargs:
        argget = lambda: kwargs
        if plambda:
            argget = plambda(kwargs)
    else:
        argget = iter(args).next

    obuff = []
    ncur = escape = fmtinpth = 0
    ofmt = fmt = u''

    while ncur < len(fmtstr):
        c = fmtstr[ncur]

        if escape:
            obuff.append(c)
            escape = 0
            ofmt = u''
        elif c == u'\\':
            escape = 1
        elif fmt:
            fmt += c
            if not fmtinpth and c.isalpha():
                ofmt = fmt % argget()
                obuff.append(ofmt)
                fmt = u''
            elif fmtinpth and c == u')':
                fmtinpth = 0
            elif c == u'(':
                fmtinpth = 1
            elif c == u'%':
                obuff.append(u'%')
        elif c == u'%':
            fmt += c
            ofmt = u''
        else:
            if ofmt and ALT_SUFFIXES.has_key(c):
                obuff.append(ALT_SUFFIXES[c][
                                 _has_final(ofmt[-1])[1] and 1 or 0
                                 ])
            elif ofmt and IDA_SUFFIXES.has_key(fmtstr[ncur:ncur + 3]):
                sel = IDA_SUFFIXES[fmtstr[ncur:ncur + 3]]
                ishan, hasfinal = _has_final(ofmt[-1])

                if hasfinal:
                    obuff.append(sel[1])
                elif ishan:
                    if sel[0]:
                        obuff[-1] = obuff[-1][:-1] + chr(ord(ofmt[-1]) + sel[0])
                else:
                    obuff.append(sel[0] and sel[1])
                ncur += 2
            else:
                obuff.append(c)

            ofmt = u''

        ncur += 1

    return u''.join(obuff)

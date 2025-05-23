# -*- coding: utf-8 -*-
from kss._modules.hangulization.hangulize import *


class NarrowGeorgian(Language):
    """For transcribing Georgian (narrow transcription).
    The lenis, fortis, and aspirated series of stops and affricates of Korean
    are all employed. The Georgian grapheme ვ is taken to be /w/ after an
    obstruent and before a vowel, to be /f/ after a vowel and before a
    voiceless stop or affricate, and to be /v/ in all other cases."""

    __iso639__ = {1: 'ka', 2: 'geo', 3: 'kat'}
    __tmp__ = ',;'

    vowels = u'აეიოუ'
    cs = u'ბგდვზთკლმნპჟრსტფქღყშჩცძწჭხჯჰV'
    vl = u'თკპტფქყჩცწჭ'
    ob = u'ბგდვზთკპჟსტფქღყშჩცძწჭხჯჰ'
    notation = Notation([
        (u'ჱ', u'ეჲ'),
        (u'ჲ', u'ი'),
        (u'უჳ', u'უ'),
        (u'ჳ', u'უ'),
        (u'ჴ', u'ხ'),
        (u'ჵ', u'ო'),
        (u'ჶ', u'ფ'),
        (u'{@}ვ{<vl>}', u'ჶ'),
        (u'ვ$', u'ჶ'),
        (u'ბბ', u'ბ'),
        (u'გგ', u'გ'),
        (u'დდ', u'დ'),
        (u'ვვ', u'ვ'),
        (u'ზზ', u'ზ'),
        (u'თთ', u'თ'),
        (u'კკ', u'კ'),
        (u'ლლ', u'ლ'),
        (u'მმ', u'მ,მ'),
        (u'ნნ', u'ნ,ნ'),
        (u'პპ', u'პ'),
        (u'ჟჟ', u'ჟ'),
        (u'რრ', u'რ'),
        (u'სს', u'ს'),
        (u'ტტ', u'ტ'),
        (u'ფფ', u'ფ'),
        (u'ქქ', u'ქ'),
        (u'ღღ', u'ღ'),
        (u'ყყ', u'ყ'),
        (u'შშ', u'შ'),
        (u'ხხ', u'ხ'),
        (u'ჰჰ', u'ჰ'),
        (u'დ{ძ|ჯ}', None),
        (u'თ{ჩ|ც}', None),
        (u'ტ{წ|ჭ}', None),
        (u'დჟ', u'ჯ'),
        (u'თშ', u'ჩ'),
        (u'ტშ', u'ჭ'),
        (u'დზ', u'ძ'),
        (u'თს', u'ც'),
        (u'ტს', u'წ'),
        (u'{<ob>}ვ{ა|ე|ი}', u'V'),
        (u'ჟ{<cs>}', u'ჟუ'),
        (u'ჟ$', u'ჟუ'),
        (u'შ{<cs>}', u'შუ'),
        (u'შ$', u'ში'),
        (u'ჩ{V}', u'ჩუ'),
        (u'ჩ{<cs>}', u'ჩი'),
        (u'ჩ$', u'ჩი'),
        (u'ძ{V}', u'ძუ'),
        (u'ძ{<cs>}', u'ძი'),
        (u'ძ$', u'ძი'),
        (u'ჭ{V}', u'ჭუ'),
        (u'ჭ{<cs>}', u'ჭი'),
        (u'ჭ$', u'ძი'),
        (u'^ლ', u'ლ;'),
        (u'^მ$', u'მ;'),
        (u'^ნ', u'ნ;'),
        (u'ლ$', u'ლ,'),
        (u'მ$', u'მ,'),
        (u'ნ$', u'ნ,'),
        (u'ლ{@|მ,|ნ,}', u'ლ;'),
        (u'{,}ლ', u'ლ;'),
        (u'მ{@}', u'მ;'),
        (u'ნ{@}', u'ნ;'),
        (u'ლ', u'ლ,'),
        (u'მ', u'მ,'),
        (u'ნ', u'ნ,'),
        (u',,', u','),
        (u',;', None),
        (u',ლ,', u'ლ,'),
        (u',მ,', u'მ,'),
        (u',ნ,', u'ნ,'),
        (u'ლ{მნ}', u'ლ,'),
        (u';', None),
        (u'აა', u'ა'),
        (u'ეე', u'ე'),
        (u'იი', u'ი'),
        (u'ოო', u'ო'),
        (u'უუ', u'უ'),
        (u'ბ', Choseong(B)),
        (u'გ', Choseong(G)),
        (u'დ', Choseong(D)),
        (u'ვ', Choseong(B)),
        (u'ზ', Choseong(J)),
        (u'თ', Choseong(T)),
        (u'კ', Choseong(GG)),
        (u'^ლ', Choseong(L)),
        (u'{,}ლ', Choseong(L)),
        (u'ლ,', Jongseong(L)),
        (u'ლ', Jongseong(L), Choseong(L)),
        (u'მ,', Jongseong(M)),
        (u'მ', Choseong(M)),
        (u'ნ,', Jongseong(N)),
        (u'ნ', Choseong(N)),
        (u'პ', Choseong(BB)),
        (u'ჟ', Choseong(J)),
        (u'რ', Choseong(L)),
        (u'ს', Choseong(S)),
        (u'ტ', Choseong(DD)),
        (u'ფ', Choseong(P)),
        (u'ქ', Choseong(K)),
        (u'ღ', Choseong(G)),
        (u'ყ', Choseong(GG)),
        (u'ჩ', Choseong(C)),
        (u'ც', Choseong(C)),
        (u'ძ', Choseong(J)),
        (u'წ', Choseong(JJ)),
        (u'ჭ', Choseong(JJ)),
        (u'ხ', Choseong(H)),
        (u'ჯ', Choseong(J)),
        (u'ჰ', Choseong(H)),
        (u'ჶ', Choseong(P)),
        (u'ჸ', Choseong(NG)),
        (u'შა', Choseong(S), Jungseong(YA)),
        (u'შე', Choseong(S), Jungseong(YE)),
        (u'ში', Choseong(S), Jungseong(I)),
        (u'შო', Choseong(S), Jungseong(YO)),
        (u'შუ', Choseong(S), Jungseong(YU)),
        (u'შჷ', Choseong(S), Jungseong(YEO)),
        (u'Vა', Choseong(NG), Jungseong(WA)),
        (u'Vე', Choseong(NG), Jungseong(WE)),
        (u'Vი', Choseong(NG), Jungseong(WI)),
        (u'ა', Jungseong(A)),
        (u'ე', Jungseong(E)),
        (u'ი', Jungseong(I)),
        (u'ო', Jungseong(O)),
        (u'უ', Jungseong(U)),
        (u'ჷ', Jungseong(EO)),
    ])

    def normalize(self, string):
        return normalize_roman(string, {
            u'Ⴀ': u'ა', u'ⴀ': u'ა', u'Ⴁ': u'ბ', u'ⴁ': u'ბ', u'Ⴂ': u'გ',
            u'ⴂ': u'გ', u'Ⴃ': u'დ', u'ⴃ': u'დ', u'Ⴄ': u'ე', u'ⴄ': u'ე',
            u'Ⴅ': u'ვ', u'ⴅ': u'ვ', u'Ⴆ': u'ზ', u'ⴆ': u'ზ', u'Ⴡ': u'ჱ',
            u'ⴡ': u'ჱ', u'Ⴇ': u'თ', u'ⴇ': u'თ', u'Ⴈ': u'ი', u'ⴈ': u'ი',
            u'Ⴉ': u'კ', u'ⴉ': u'კ', u'Ⴊ': u'ლ', u'ⴊ': u'ლ', u'Ⴋ': u'მ',
            u'ⴋ': u'მ', u'Ⴌ': u'ნ', u'ⴌ': u'ნ', u'Ⴢ': u'ჲ', u'ⴢ': u'ჲ',
            u'Ⴍ': u'ო', u'ⴍ': u'ო', u'Ⴎ': u'პ', u'ⴎ': u'პ', u'Ⴏ': u'ჟ',
            u'ⴏ': u'ჟ', u'Ⴐ': u'რ', u'ⴐ': u'რ', u'Ⴑ': u'ს', u'ⴑ': u'ს',
            u'Ⴒ': u'ტ', u'ⴒ': u'ტ', u'Ⴣ': u'ჳ', u'ⴣ': u'ჳ', u'Ⴍ': u'უ',
            u'ⴍ': u'უ', u'Ⴔ': u'ფ', u'ⴔ': u'ფ', u'Ⴕ': u'ქ', u'ⴕ': u'ქ',
            u'Ⴖ': u'ღ', u'ⴖ': u'ღ', u'Ⴗ': u'ყ', u'ⴗ': u'ყ', u'Ⴘ': u'შ',
            u'ⴘ': u'შ', u'Ⴙ': u'ჩ', u'ⴙ': u'ჩ', u'Ⴚ': u'ც', u'ⴚ': u'ც',
            u'Ⴛ': u'ძ', u'ⴛ': u'ძ', u'Ⴜ': u'წ', u'ⴜ': u'წ', u'Ⴝ': u'ჭ',
            u'ⴝ': u'ჭ', u'Ⴞ': u'ხ', u'ⴞ': u'ხ', u'Ⴤ': u'ჴ', u'ⴤ': u'ჴ',
            u'Ⴟ': u'ჯ', u'ⴟ': u'ჯ', u'Ⴠ': u'ჰ', u'ⴠ': u'ჰ', u'Ⴥ': u'ჵ',
            u'ⴥ': u'ჵ'
        })


__lang__ = NarrowGeorgian

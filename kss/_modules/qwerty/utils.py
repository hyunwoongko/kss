import math
import re

ENGLISH = "rRseEfaqQtTdwWczxvgASDFGZXCVkoiOjpuPhynbmlYUIHJKLBNM"
HANGUL = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅁㄴㅇㄹㅎㅋㅌㅊㅍㅏㅐㅑㅒㅓㅔㅕㅖㅗㅛㅜㅠㅡㅣㅛㅕㅑㅗㅓㅏㅣㅠㅜㅡ"
LEADS = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
VOWELS = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
TAILS = "ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ"

HANGUL_FIRST = 44032
HANGUL_LAST = 55203
VOWELS_FIRST = 28
CONSONANT_FIRST = 12593
VOWEL_LAST = 12643

ENGLISH_INDEX = (lambda en: {en[i]: i for i in range(len(en))})(ENGLISH)
HANGUL_INDEX = (lambda kr: {i: w for i, w in enumerate(kr)})(HANGUL)

CONNECTABLE_CONSONANTS = {
    'ㄱㅅ': 'ㄳ',
    'ㄴㅈ': 'ㄵ',
    'ㄴㅎ': 'ㄶ',
    'ㄹㄱ': 'ㄺ',
    'ㄹㅁ': 'ㄻ',
    'ㄹㅂ': 'ㄼ',
    'ㄹㅅ': 'ㄽ',
    'ㄹㅌ': 'ㄾ',
    'ㄹㅍ': 'ㄿ',
    'ㄹㅎ': 'ㅀ',
    'ㅂㅅ': 'ㅄ'
}

CONNECTABLE_VOWELS = {
    'ㅗㅏ': 'ㅘ',
    'ㅗㅐ': 'ㅙ',
    'ㅗㅣ': 'ㅚ',
    'ㅜㅓ': 'ㅝ',
    'ㅜㅔ': 'ㅞ',
    'ㅜㅣ': 'ㅟ',
    'ㅡㅣ': 'ㅢ'
}


def is_vowel(e):
    return [k for k, v in HANGUL_INDEX.items() if v == e][0] >= VOWELS_FIRST


def is_hangul(char):
    if len(char) > 1:
        raise Exception("`char` must be a single character.")
    return re.match("[ㄱ-ㅎㅏ-ㅣ가-힣]", char) is not None


def index_of(val, _list):
    try:
        return _list.index(val)
    except ValueError:
        return -1


def generate_hangul(*args):
    return chr(44032 + args[0][0] * 588 + args[0][1] * 28 + args[0][2] + 1)


def separate_hangul(hangul_text):
    code = ord(hangul_text)

    if HANGUL_FIRST <= code <= HANGUL_LAST:
        lead = math.floor((code - HANGUL_FIRST) / 588)
        vowel = math.floor((code - HANGUL_FIRST - lead * 588) / 28)
        tail = code - HANGUL_FIRST - lead * 588 - vowel * 28 - 1
        vowel_1, vowel_2, tail_1, tail_2 = vowel, -1, tail, -1

        if vowel == index_of("ㅘ", VOWELS):
            vowel_1, vowel_2 = index_of("ㅗ", HANGUL), index_of("ㅏ", HANGUL)
        elif vowel == index_of("ㅙ", VOWELS):
            vowel_1, vowel_2 = index_of("ㅗ", HANGUL), index_of("ㅐ", HANGUL)
        elif vowel == index_of("ㅚ", VOWELS):
            vowel_1, vowel_2 = index_of("ㅗ", HANGUL), index_of("ㅣ", HANGUL)
        elif vowel == index_of("ㅝ", VOWELS):
            vowel_1, vowel_2 = index_of("ㅜ", HANGUL), index_of("ㅓ", HANGUL)
        elif vowel == index_of("ㅞ", VOWELS):
            vowel_1, vowel_2 = index_of("ㅜ", HANGUL), index_of("ㅔ", HANGUL)
        elif vowel == index_of("ㅟ", VOWELS):
            vowel_1, vowel_2 = index_of("ㅜ", HANGUL), index_of("ㅣ", HANGUL)
        elif vowel == index_of("ㅢ", VOWELS):
            vowel_1, vowel_2 = index_of("ㅡ", HANGUL), index_of("ㅣ", HANGUL)

        if tail == index_of("ㄳ", TAILS):
            tail_1, tail_2 = index_of("ㄱ", HANGUL), index_of("ㅅ", HANGUL)
        elif tail == index_of("ㄵ", TAILS):
            tail_1, tail_2 = index_of("ㄴ", HANGUL), index_of("ㅈ", HANGUL)
        elif tail == index_of("ㄶ", TAILS):
            tail_1, tail_2 = index_of("ㄴ", HANGUL), index_of("ㅎ", HANGUL)
        elif tail == index_of("ㄺ", TAILS):
            tail_1, tail_2 = index_of("ㄹ", HANGUL), index_of("ㄱ", HANGUL)
        elif tail == index_of("ㄻ", TAILS):
            tail_1, tail_2 = index_of("ㄹ", HANGUL), index_of("ㅁ", HANGUL)
        elif tail == index_of("ㄼ", TAILS):
            tail_1, tail_2 = index_of("ㄹ", HANGUL), index_of("ㅂ", HANGUL)
        elif tail == index_of("ㄽ", TAILS):
            tail_1, tail_2 = index_of("ㄹ", HANGUL), index_of("ㅅ", HANGUL)
        elif tail == index_of("ㄾ", TAILS):
            tail_1, tail_2 = index_of("ㄹ", HANGUL), index_of("ㅌ", HANGUL)
        elif tail == index_of("ㄿ", TAILS):
            tail_1, tail_2 = index_of("ㄹ", HANGUL), index_of("ㅍ", HANGUL)
        elif tail == index_of("ㅀ", TAILS):
            tail_1, tail_2 = index_of("ㄹ", HANGUL), index_of("ㅎ", HANGUL)
        elif tail == index_of("ㅄ", TAILS):
            tail_1, tail_2 = index_of("ㅂ", HANGUL), index_of("ㅅ", HANGUL)

        if vowel_2 == -1 and vowel != -1:
            vowel_1 = index_of(VOWELS[vowel], HANGUL)
        if tail_2 == -1 and tail != -1:
            tail_1 = index_of(TAILS[tail], HANGUL)

        return [lead, vowel_1, vowel_2, tail_1, tail_2]

    elif CONSONANT_FIRST <= code <= VOWEL_LAST:
        if index_of(hangul_text, LEADS) > -1:
            lead = index_of(hangul_text, HANGUL)
            return [lead, -1, -1, -1, -1]

        elif index_of(hangul_text, VOWELS) > -1:
            vowel = index_of(hangul_text, VOWELS)
            vowel_1, vowel_2 = vowel, -1
            if vowel == index_of("ㅘ", VOWELS):
                vowel_1, vowel_2 = index_of("ㅗ", HANGUL), index_of("ㅏ", HANGUL)
            elif vowel == index_of("ㅙ", VOWELS):
                vowel_1, vowel_2 = index_of("ㅗ", HANGUL), index_of("ㅐ", HANGUL)
            elif vowel == index_of("ㅚ", VOWELS):
                vowel_1, vowel_2 = index_of("ㅗ", HANGUL), index_of("ㅣ", HANGUL)
            elif vowel == index_of("ㅝ", VOWELS):
                vowel_1, vowel_2 = index_of("ㅜ", HANGUL), index_of("ㅓ", HANGUL)
            elif vowel == index_of("ㅞ", VOWELS):
                vowel_1, vowel_2 = index_of("ㅜ", HANGUL), index_of("ㅔ", HANGUL)
            elif vowel == index_of("ㅟ", VOWELS):
                vowel_1, vowel_2 = index_of("ㅜ", HANGUL), index_of("ㅣ", HANGUL)
            elif vowel == index_of("ㅢ", VOWELS):
                vowel_1, vowel_2 = index_of("ㅡ", HANGUL), index_of("ㅣ", HANGUL)

            if vowel_2 == -1:
                vowel_1 = index_of(VOWELS[vowel], HANGUL)

            return [-1, vowel_1, vowel_2, -1, -1]

    return [-1, -1, -1, -1, -1]

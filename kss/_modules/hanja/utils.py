# -*- coding:utf-8 -*-
# This was copied from [hanja](https://github.com/suminb/hanja) and modified by Kss

import os

import yaml


def load_table(filename):
    """Loads the Hanja table."""
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import BaseLoader as Loader
    with open(filename) as fin:
        table = yaml.load(fin.read(), Loader=Loader)

    return table


basepath = os.path.abspath(os.path.dirname(__file__))
hanja_table = load_table(os.path.join(basepath, "assets", "table.yml"))


def separate(ch):
    """한글 자모 분리. 주어진 한글 한 글자의 초성, 중성 초성을 반환함."""
    uindex = ord(ch) - 0xAC00
    jongseong = uindex % 28
    # NOTE: Force integer-divisions
    joongseong = ((uindex - jongseong) // 28) % 21
    choseong = ((uindex - jongseong) // 28) // 21

    return choseong, joongseong, jongseong


def synthesize(choseong, joongseong, jongseong):
    return build(choseong, joongseong, jongseong)


def build(choseong, joongseong, jongseong):
    """초성, 중성, 종성을 조합하여 완성형 한 글자를 만듦. 'choseong',
    'joongseong', 'jongseong' are offsets. For example, 'ㄱ' is 0, 'ㄲ' is 1,
    'ㄴ' is 2, and so on and so fourth."""
    code = int(((((choseong) * 21) + joongseong) * 28) + jongseong + 0xAC00)
    return chr(code)


def dooeum(previous, current):
    """두음법칙을 적용하기 위한 함수."""
    p, c = separate(previous), separate(current)
    offset = 0

    current_head = build(c[0], c[1], 0)

    # 모음이나 ㄴ 받침 뒤에 이어지는 '렬, 률'은 '열, 율'로 발음한다.
    if previous.isalnum():
        if current in ("렬", "률") and is_hangul(previous) and p[2] in (0, 2):
            offset = 6
    # 한자음 '녀, 뇨, 뉴, 니', '랴, 려, 례, 료, 류, 리'가 단어 첫머리에 올 때
    # '여, 요, 유, 이', '야, 여, 예, 요, 유, 이'로 발음한다.
    elif current_head in ("녀", "뇨", "뉴", "니"):
        offset = 9
    elif current_head in ("랴", "려", "례", "료", "류", "리"):
        offset = 6
    # 한자음 '라, 래, 로, 뢰, 루, 르'가 단어 첫머리에 올 때 '나, 내, 노, 뇌,
    # 누, 느'로 발음한다.
    elif current_head in ("라", "래", "로", "뢰", "루", "르"):
        offset = -3

    return build(c[0] + offset, c[1], c[2])


def is_hangul(ch):
    if ch is None:
        return False
    else:
        return 0xAC00 <= ord(ch) <= 0xD7A3


def contains_hangul(text):
    if isinstance(text, str):
        # NOTE: Probably not an ideal solution in terms of performance
        tfs = map(lambda c: is_hangul(c), text)
        for tf in tfs:
            if tf:
                return True
    return False


def translate_syllable(previous, current):
    """Translates a single syllable."""

    if current in hanja_table:
        return dooeum(previous, hanja_table[current])

    return current


def _split_hanja(text):
    """주어진 문장을 한자로 된 구역과 그 이외의 문자로 된 구역으로 분리"""

    # TODO: Can we make this a bit prettier?
    if len(text) == 0:
        yield text
    else:
        ch = text[0]
        bucket = [ch]
        prev_state = is_hanja(ch)

        for ch in text[1:]:
            state = is_hanja(ch)

            if prev_state != state:
                yield "".join(bucket)
                bucket = [ch]
            else:
                bucket.append(ch)

            prev_state = state

        yield "".join(bucket)


def split_hanja(text):
    """Splits a given text into hanja and non-hanja parts."""
    return list(_split_hanja(text))


def get_format_string(mode, word):
    """
    :param mode: substitution | combination-text | combination-text-reversed | combination-html | combination-html-reversed
    """
    if mode == "combination-text" and is_hanja(word[0]):
        return u"{word}({translated})"
    elif mode == "combination-text-reversed" and is_hanja(word[0]):
        return u"{translated}({word})"
    elif mode in "combination-html" and is_hanja(word[0]):
        return u'<span class="hanja">{word}</span><span class="hangul">({translated})</span>'
    elif mode in "combination-html-reversed" and is_hanja(word[0]):
        return u'<span class="hangul">{translated}</span><span class="hanja">({word})</span>'
    else:
        return u"{translated}"


def translate(text, mode):
    """Translates entire text."""
    words = list(split_hanja(text))
    return "".join(
        map(
            lambda w, prev: translate_word(w, prev, get_format_string(mode, w)),
            words,
            [None] + words[:-1],
        )
    )


def translate_word(word, prev, format_string):
    """Translates a single word.

    :param word: Word to be translated
    :param prev: Preceeding word
    """
    prev_char = prev[-1] if prev else " "
    buf = []
    for c in word:
        new_char = translate_syllable(prev_char, c)
        buf.append(new_char)
        prev_char = new_char
    translated = "".join(buf)

    return format_string.format(word=word, translated=translated)


def is_hanja(ch):
    """Determines if a given character ``ch`` is a Chinese character."""
    return ch in hanja_table

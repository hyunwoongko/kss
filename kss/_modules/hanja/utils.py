from hanja import is_hanja as _is_hanja
from hanja import split_hanja as _split_hanja_generator
from hanja.impl import translate_word as _translate_word


def get_format_string(mode, word):
    """
    :param mode: substitution | combination-text | combination-text-reversed | combination-html | combination-html-reversed
    """
    if mode == "combination-text" and _is_hanja(word[0]):
        return u"{word}({translated})"
    elif mode == "combination-text-reversed" and _is_hanja(word[0]):
        return u"{translated}({word})"
    elif mode in "combination-html" and _is_hanja(word[0]):
        return u'<span class="hanja">{word}</span><span class="hangul">({translated})</span>'
    elif mode in "combination-html-reversed" and _is_hanja(word[0]):
        return u'<span class="hangul">{translated}</span><span class="hanja">({word})</span>'
    else:
        return u"{translated}"


def translate(text, mode):
    """Translates entire text."""
    words = list(_split_hanja(text))
    return "".join(
        map(
            lambda w, prev: _translate_word(w, prev, get_format_string(mode, w)),
            words,
            [None] + words[:-1],
        )
    )


def _split_hanja(text):
    return list(_split_hanja_generator(text))


def _hanja2hangul(text, combination=False, reverse=False, html=False):
    # translate hangul to hanja
    if combination is False:
        return translate(text, 'substitution')
    elif combination is True and reverse is False and html is False:
        return translate(text, 'combination-text')
    elif combination is True and reverse is True and html is False:
        return translate(text, 'combination-text-reversed')
    elif combination is True and reverse is False and html is True:
        return translate(text, 'combination-html')
    elif combination is True and reverse is True and html is True:
        return translate(text, 'combination-html-reversed')
    else:
        raise ValueError("Invalid combination of `combination`, `reverse`, and `html`")

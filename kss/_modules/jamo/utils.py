import re
import jamo


def _j2h_char(lead, vowel, tail=None):
    """Convert a jamo character to Hangul."""
    return jamo.j2h(lead, vowel, tail)


def _j2h(text, add_placeholder_for_leading_vowels=False):
    if add_placeholder_for_leading_vowels:
        # add 'ㅇ' for leading vowels (e.g. 'ㅐ플' -> '애플')
        # this is useful for g2p conversion
        text = re.sub(r"(^|[^\u1100-\u1112])([\u1161-\u1175])", r"\1ᄋ\2", text)
    # case 1: consonant + vowel + consonant
    syllables = set(re.findall(r"[\u1100-\u1112][\u1161-\u1175][\u11A8-\u11C2]", text))
    for syl in syllables:
        text = text.replace(syl, _j2h_char(*syl))
    # case 2: consonant + vowel
    syllables = set(re.findall(r"[\u1100-\u1112][\u1161-\u1175]", text))
    for syl in syllables:
        text = text.replace(syl, _j2h_char(*syl))
    # case 3: remained a single consonant or vowel
    return jamo.j2hcj(text)

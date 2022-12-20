# Copyright (C) 2021 Hyunwoong Ko <kevin.ko@tunib.ai> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.

import emoji
import regex

_emojis = {}
_specials = ["♡", "♥"]
_unicodes = [
    "‍",  # Zero width joiner
    "︀",  # Variation Selector-1
    "︁",  # Variation Selector-2
    "︂",  # Variation Selector-3
    "︃",  # Variation Selector-4
    "︄",  # Variation Selector-5
    "︅",  # Variation Selector-6
    "︆",  # Variation Selector-7
    "︇",  # Variation Selector-8
    "︈",  # Variation Selector-9
    "︉",  # Variation Selector-10
    "︊",  # Variation Selector-11
    "︋",  # Variation Selector-12
    "︌",  # Variation Selector-13
    "︍",  # Variation Selector-14
    "︎",  # Variation Selector-15
    "️",  # Variation Selector-16
]

try:
    for lang in ["pt", "it", "es", "en"]:
        _emojis.update(emoji.unicode_codes.UNICODE_EMOJI[lang])
        _emojis.update({k: "" for k in _specials})
        _emojis.update({k: "" for k in _unicodes})
except Exception as e:
    raise ImportError("Kss requires `emoji==1.2.0`. please install that version.")


def get_emoji(text):
    emoji_list = []
    flags = regex.findall("[\U0001F1E6-\U0001F1FF]", text)

    for grapheme in regex.findall(r"\X", text):
        if any(char in _emojis for char in grapheme):
            emoji_list.append(grapheme)

    return emoji_list + flags

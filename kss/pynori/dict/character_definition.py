"""
Character Definition

Reference: `char.def` file.
"""
import emoji
import regex

_emojis = {}
for lang in ["pt", "it", "es", "en"]:
    _emojis.update(emoji.UNICODE_EMOJI[lang])


def get_emoji(text):
    emoji_list = []
    flags = regex.findall("[\U0001F1E6-\U0001F1FF]", text)

    for grapheme in regex.findall(r"\X", text):
        if any(char in _emojis for char in grapheme):
            emoji_list.append(grapheme)

    return emoji_list + flags


def character_category_map(ch):
    hex_ch = ord(ch)

    # SPACE
    if hex_ch in [0x0020, 0x000D, 0x0009, 0x000B, 0x000A]:
        return "SPACE"

    # EMOJI
    if len(get_emoji(ch)) != 0:
        return "EMOJI"

    # ASCII
    elif hex_ch in range(0x0021, 0x002F + 1):
        return "SYMBOL"
    elif hex_ch in range(0x0030, 0x0039 + 1):
        return "NUMERIC"
    elif hex_ch in range(0x003A, 0x0040 + 1):
        return "SYMBOL"
    elif hex_ch in range(0x0041, 0x005A + 1):
        return "ALPHA"
    elif hex_ch in range(0x005B, 0x0060 + 1):
        return "SYMBOL"
    elif hex_ch in range(0x0061, 0x007A + 1):
        return "ALPHA"
    elif hex_ch in range(0x007B, 0x007E + 1):
        return "SYMBOL"

    # Latin
    elif hex_ch in range(0x00A1, 0x00BF + 1):
        return "SYMBOL"
    elif (
        hex_ch in range(0x00C0, 0x00FF + 1)
        or hex_ch in range(0x0100, 0x017F + 1)
        or hex_ch in range(0x0180, 0x0236 + 1)
        or hex_ch in range(0x1E00, 0x1EF9 + 1)
    ):
        return "ALPHA"

    # CYRILLIC
    elif hex_ch in range(0x0400, 0x04F9 + 1) or hex_ch in range(0x0500, 0x050F + 1):
        return "CYRILLIC"

    # GREEK
    elif hex_ch in range(0x0374, 0x03FB + 1):
        return "GREEK"

    # HANGUL
    elif (
        hex_ch in range(0xAC00, 0xD7A3 + 1)
        or hex_ch in range(0x1100, 0x11FF + 1)
        or hex_ch in range(0x3130, 0x318F + 1)
    ):
        return "HANGUL"

    # HIRAGANA
    elif hex_ch in range(0x3041, 0x309F + 1):
        return "HIRAGANA"

    # KATAKANA
    elif (
        hex_ch in range(0x30A1, 0x30FF + 1)
        or hex_ch in range(0x31F0, 0x31FF + 1)
        or hex_ch == 0x30FC
        or hex_ch in range(0xFF66, 0xFF9D + 1)
        or hex_ch in range(0xFF9E, 0xFF9F + 1)
    ):
        return "KATAKANA"

    # HANJA
    elif (
        hex_ch in range(0x2E80, 0x2EF3 + 1)
        or hex_ch == 0x3005
        or hex_ch == 0x3007
        or hex_ch in range(0x3400, 0x4DB5 + 1)
        or hex_ch in range(0x4E00, 0x9FA5 + 1)
        or hex_ch in range(0xF900, 0xFA2D + 1)
        or hex_ch in range(0xFA30, 0xFA6A + 1)
    ):
        return "HANJA"

    # KANJI
    elif hex_ch in range(0x2F00, 0x2FD5 + 1):
        return "KANJI"

    # HANJA-NUMERIC
    elif hex_ch in [
        0x4E00,
        0x4E8C,
        0x4E09,
        0x56DB,
        0x4E94,
        0x516D,
        0x4E03,
        0x516B,
        0x4E5D,
        0x5341,
        0x767E,
        0x5343,
        0x4E07,
        0x5104,
        0x5146,
    ]:
        return "HANJA"

    # ZENKAKU
    elif hex_ch in range(0xFF10, 0xFF19 + 1):
        return "NUMERIC"
    elif hex_ch in range(0xFF21, 0xFF3A + 1) or hex_ch in range(0xFF41, 0xFF5A + 1):
        return "ALPHA"
    elif (
        hex_ch in range(0xFF01, 0xFF0F + 1)
        or hex_ch in range(0xFF1A, 0xFF1F + 1)
        or hex_ch in range(0xFF3B, 0xFF40 + 1)
        or hex_ch in range(0xFF5B, 0xFF65 + 1)
        or hex_ch in range(0xFFE0, 0xFFEF + 1)
    ):
        return "SYMBOL"

    # OTHER SYMBOLS
    elif hex_ch in range(0x2070, 0x209F + 1) or hex_ch in range(0x2150, 0x218F + 1):
        return "NUMERIC"

    elif (
        hex_ch in range(0x2000, 0x206F + 1)
        or hex_ch in range(0x20A0, 0x20CF + 1)
        or hex_ch in range(0x20D0, 0x20FF + 1)
        or hex_ch in range(0x2100, 0x214F + 1)
        or hex_ch in range(0x2100, 0x214B + 1)
        or hex_ch in range(0x2190, 0x21FF + 1)
        or hex_ch in range(0x2200, 0x22FF + 1)
        or hex_ch in range(0x2300, 0x23FF + 1)
        or hex_ch in range(0x2460, 0x24FF + 1)
        or hex_ch in range(0x2501, 0x257F + 1)
        or hex_ch in range(0x2580, 0x259F + 1)
        or hex_ch in range(0x25A0, 0x25FF + 1)
        or hex_ch in range(0x2600, 0x26FE + 1)
        or hex_ch in range(0x2700, 0x27BF + 1)
        or hex_ch in range(0x27F0, 0x27FF + 1)
        or hex_ch in range(0x27C0, 0x27EF + 1)
        or hex_ch in range(0x2800, 0x28FF + 1)
        or hex_ch in range(0x2900, 0x297F + 1)
        or hex_ch in range(0x2B00, 0x2BFF + 1)
        or hex_ch in range(0x2A00, 0x2AFF + 1)
        or hex_ch in range(0x3300, 0x33FF + 1)
        or hex_ch in range(0x3200, 0x32FE + 1)
        or hex_ch in range(0x3000, 0x303F + 1)
        or hex_ch in range(0xFE30, 0xFE4F + 1)
        or hex_ch in range(0xFE50, 0xFE6B + 1)
    ):
        return "SYMBOL"

    # ELSE
    else:
        return


"""
CATEGORY_NAME: Name of category. you have to define DEFAULT class.
INVOKE: 1/0:   always invoke unknown word processing, evan when the word can be found in the lexicon
GROUP:  1/0:   make a new word by grouping the same chracter category
LENGTH: n:     1 to n length new words are added
"""
invokeMap = {
    "DEFAULT": 0,
    "SPACE": 0,
    "HANJA": 0,
    "KANJI": 0,
    "SYMBOL": 1,
    "NUMERIC": 1,
    "ALPHA": 1,
    "HANGUL": 0,
    "HIRAGANA": 1,
    "KATAKANA": 1,
    "HANJANUMERIC": 1,
    "GREEK": 1,
    "CYRILLIC": 1,
}
groupMap = {
    "DEFAULT": 1,
    "SPACE": 1,
    "HANJA": 0,
    "KANJI": 0,
    "SYMBOL": 1,
    "NUMERIC": 1,
    "ALPHA": 1,
    "HANGUL": 1,
    "HIRAGANA": 1,
    "KATAKANA": 1,
    "HANJANUMERIC": 1,
    "GREEK": 1,
    "CYRILLIC": 1,
}


class CharacterDefinition(object):
    invokeMap = []
    groupMap = []

    @staticmethod
    def getCharacterClass(ch):
        return character_category_map(ch)

    @staticmethod
    def isInvoke(ch):
        return invokeMap[character_category_map(ch)]

    @staticmethod
    def isGroup(ch):
        return groupMap[character_category_map(ch)]

    @staticmethod
    def isHangul(ch):
        if 0xAC00 < ord(ch) < 0xD7A3:  # 한글 음절 범위 (가 ~ 힣)
            return True
        return False

    @staticmethod
    def hasCoda(ch):
        if ((ord(ch) - 0xAC00) % 0x001C) == 0:
            return False  # 종성 없음 (ex. 키)
        else:
            return True  # 종성 있음 (ex. 킥)

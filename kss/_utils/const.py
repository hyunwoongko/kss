# Copyright (C) 2021 Hyunwoong Ko <kevin.ko@tunib.ai> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.

"""
Sets of characters, contain method in set is much faster than list
"""

# 0 ~ 9
numbers = set([str(_) for _ in range(0, 10)])

# a-z
lower_alphabets = set([chr(_) for _ in range(ord("a"), ord("z") + 1)])

# A-Z
upper_alphabets = set([_.upper() for _ in lower_alphabets])

# a-z|A-Z
alphabets = set()
alphabets.update(lower_alphabets)
alphabets.update(upper_alphabets)

# ㄱ-ㅎ
jaum = set([chr(_) for _ in range(ord("ㄱ"), ord("ㅎ") + 1)])

# ㅏ-ㅡ
moum = set([chr(_) for _ in range(ord("ㅏ"), ord("ㅡ") + 1)])

# ㄱ-ㅎ|ㅏ-ㅡ
jamo = set()
jamo.update(jaum)
jamo.update(moum)

# brackets | `<`, `>` 제외 (수학기호, 화살표로 쓰임)
brackets = {
    ")",
    "）",
    "〉",
    ">",
    "》",
    "]",
    "］",
    "〕",
    "】",
    "}",
    "｝",
    "』",
    "」",
    "(",
    "（",
    "〈",
    "<",
    "《",
    "[",
    "［",
    "〔",
    "【",
    "{",
    "｛",
    "「",
    "『",
}

# open -> close
bracket_open_to_close = {
    "(": ")",
    "（": "）",
    "〈": "〉",
    "<": ">",
    "《": "》",
    "[": "]",
    "［": "］",
    "〔": "〕",
    "【": "】",
    "{": "}",
    "｛": "｝",
    "「": "」",
    "『": "』",
}

# close -> open
bracket_close_to_open = {v: k for k, v in bracket_open_to_close.items()}

# doubles
double_quotes = {'"', "“", "”", "″"}

# singles
single_quotes = {"'", "‘", "’", "`"}

# open to close
double_quotes_open_to_close = {"“": "”", '"': '"', "″": "″"}

# close to open
double_quotes_close_to_open = {v: k for k, v in double_quotes_open_to_close.items()}

# open to close
single_quotes_open_to_close = {"‘": "’", "'": "'", "`": "`"}

# close to open
single_quotes_close_to_open = {v: k for k, v in single_quotes_open_to_close.items()}

# open to close
quotes_open_to_close = dict()
quotes_open_to_close.update(single_quotes_open_to_close)
quotes_open_to_close.update(double_quotes_open_to_close)

# close to open
quotes_close_to_open = dict()
quotes_close_to_open.update(single_quotes_close_to_open)
quotes_close_to_open.update(double_quotes_close_to_open)

# open to close
quotes_open_to_close_with_qtn = dict()
quotes_open_to_close_with_qtn.update(quotes_open_to_close)
quotes_open_to_close_with_qtn.update({"'": "'", '"': '"'})

# close to open
quotes_close_to_open_with_qtn = dict()
quotes_close_to_open_with_qtn.update(quotes_close_to_open)
quotes_close_to_open_with_qtn.update({"'": "'", '"': '"'})

# quotes
quotes = set()
quotes.update(single_quotes)
quotes.update(double_quotes)

# quotes or brackets
quotes_or_brackets = set()
quotes_or_brackets.update(quotes)
quotes_or_brackets.update(brackets)

# opened brackets or quotes
opened_quotes_or_brackets = set(
    [
        _
        for _ in list(bracket_open_to_close.keys())
        + list(single_quotes_open_to_close.keys())
        + list(double_quotes_open_to_close.keys())
        if _ not in ['"', "'", "`"]
    ]
)

# closed brackets or quotes
closed_quotes_or_brackets = set(
    [
        _
        for _ in list(bracket_close_to_open.keys())
        + list(single_quotes_close_to_open.keys())
        + list(double_quotes_close_to_open.keys())
        if _ not in ['"', "'", "`"]
    ]
)

# open to close
quotes_or_brackets_open_to_close = dict()
quotes_or_brackets_open_to_close.update(quotes_open_to_close)
quotes_or_brackets_open_to_close.update(bracket_open_to_close)

# close to open
quotes_or_brackets_close_to_open = dict()
quotes_or_brackets_close_to_open.update(quotes_close_to_open)
quotes_or_brackets_close_to_open.update(bracket_close_to_open)

# special symbols
special_symbols_for_split = (
    """§※○●◎◇◆□■△▲▽▼→←↑↓↔◁◀▷▶♤♠♧♣⊙◈▣◐◑▒▤▥▨▧▦▩♨☏☎☜☞¶†‡↕↗↙↖↘㉿	㈜№㏇㏂㏘℡ª*"""
)
faces = {":)", ":(", ":'(", "O:)", "&)", ">:(", "3:)", '<(")', ":-)", ":-(", "◡̈"}
number_with_quotes = {f"{num}'" for num in range(0, 9)}
alphabet_with_quotes = {f"{alpha}'" for alpha in alphabets}
number_with_bracket = {f"{num})" for num in range(0, 9)}
backup_etc = {"관야유적"}

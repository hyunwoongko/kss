# Copyright (C) 2021 Hyunwoong Ko <kevin.ko@tunib.ai> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.

"""
Sets of characters, contain method in set is much faster than list
"""
import re

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
special_symbols_for_split = "㈜*∗¶§※○●◎◇◆□■△▲▽▼→↑↓↔◁◀▷▶♤♠♧♣⊙◈▣◐◑▒▤▥▨▧▦▩♨☏☎☞↕↗↙↖↘ª"
special_symbols_for_suffix = "←☜㏂㏘℡"
daggers = """†‡⸶⸷⸸⹋‖*∗"""
spaces = " \n\t\f\v\r\u200b\u200c\u2060\ufeff"

_url_prefix = "https|http|mailto|ftp"
_url_suffix = (
    "com|net|org|edu|game|ebiz|club|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi"
    "|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd"
    "|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx"
    "|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm"
    "|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki"
    "|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms"
    "|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw"
    "|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf"
    "|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za"
    "|zm|zw|mp3|mp4|avi|html|idv|jpg|bmp|png|gif|htm|cdn|media"
)

url_pattern = re.compile(
    rf"""(?i)\b((?:{_url_prefix}?:(?:/{{1,3}}|[a-z0-9%])|[a-z0-9.\-]+[.](?:{_url_suffix})/)(?:[^\s()<>{{}}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{{}};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:{_url_suffix})/?(?!@)))""",
)
email_pattern = re.compile(
    r"[a-z0-9.\-+_]+@[a-z0-9.\-+_]+\.[a-z]+|[a-z0-9.\-+_]+@[a-z0-9.\-+_]+\.[a-z]+\.[a-z]"
)

faces = {":)", ":(", ":'(", "O:)", "&)", ">:(", "3:)", '<(")', ":-)", ":-(", "◡̈"}
number_with_quotes = {f"{num}'" for num in range(0, 9)}
alphabet_with_quotes = {f"{alpha}'" for alpha in alphabets}
number_with_bracket = {f"{num})" for num in range(0, 9)}
backup_etc = {"관야유적", "라요 바예카노", "알림 차단", "알림 수신", "알림 문자"}

papers = [
    " no",
    " No",
    " pp",
    " PP",
    " vol",
    " Vol",
    " vols",
    " Vols",
    " al",
    " ed",
    " Ed",
    " Eds",
    " trans",
    " Trans",
    " rev",
    " Rev",
    " p",
    " P",
    " n.p",
    " N.P",
    " N.p",
    " n.d",
    " N.D",
    " N.d",
    " page",
    " Page",
    " para",
    " Para",
    " comp",
    " Comp",
    " 항",
    " 조",
    " 호",
    " 절",
    " 권",
    " 쪽",
]

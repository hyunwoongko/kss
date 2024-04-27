# Copyright (C) 2021 Hyunwoong Ko <kevin.brain@kakaobrain.com> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.
import difflib
import logging
from logging import getLogger

logging.basicConfig(format="[Kss]: %(message)s", level=logging.WARNING)
logger = getLogger()


def highlight_diffs(old, new):
    red = lambda text: f"\033[38;2;255;0;0m{text}\033[0m"
    green = lambda text: f"\033[38;2;0;255;0m{text}\033[0m"

    result = ""
    codes = difflib.SequenceMatcher(a=old, b=new).get_opcodes()
    for code in codes:
        if code[0] == "equal":
            result += old[code[1]:code[2]]
        elif code[0] == "delete":
            result += red(old[code[1]:code[2]])
        elif code[0] == "insert":
            result += green(new[code[3]:code[4]])
        elif code[0] == "replace":
            result += (red(old[code[1]:code[2]]) + green(new[code[3]:code[4]]))
    return result
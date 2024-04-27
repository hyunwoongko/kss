# Copyright (C) 2021 Hyunwoong Ko <kevin.brain@kakaobrain.com> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.

from kss._elements.element import Element


class Syllable(Element):
    def __init__(self, text, pos, idx):
        if len(text) != 1:
            raise ValueError("Length of syllable must be 1.")
        super().__init__(text, pos, idx)


class Token(Element):
    def __init__(self, text, pos, idx, start, end):
        super().__init__(text, pos, idx)
        self.start = start
        self.end = end

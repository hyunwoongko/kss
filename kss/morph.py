#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Korean Sentence Splitter
# Split Korean text into sentences using heuristic algorithm.
#
# Copyright (C) 2021 Hyun-Woong Ko <kevin.ko@tunib.ai> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import logging
from typing import List, Tuple
from kss.pynori.korean_analyzer import KoreanAnalyzer


class MorphExtractor(object):
    def __init__(self):
        self.mecab = None
        self.pynori = None
    
    def initialize(self,backend='pynori'):
        if backend == 'mecab' :
            try:
                logging.warning("Initializing Mecab Tokenizer...")
                self.mecab = MecabTokenizer()
            except ImportError:
                raise ImportError(
                    "\n"
                    "You must install `python-mecab-ko` if you want to use `mecab` backend.\n"
                    "Please install using `pip install python-mecab-ko`.\n"
                    "Refer https://github.com/jonghwanhyeon/python-mecab-ko for more details.\n"
                )
            
        else :
            logging.warning("Initializing Pynori Tokenizer...")
            self.pynori = PynoriTokenizer()
        
    def pos(self, text, backend):
        from kss.base import Eojeol

        if backend.lower() == "pynori":
            if self.pynori is None:
                self.initialize("pynori")
            _pos = self.pynori.pos(text, preprocessed=True)

            return [
                Eojeol(eojeol, pos[1])
                for pos in zip(_pos["termAtt"], _pos["posTagAtt"])
                for eojeol in pos[0]
            ]

        elif backend.lower() == "mecab":
            if self.mecab is None:
                self.initialize("mecab")

            return [
                Eojeol(eojeol, pos[1])
                for pos in self.mecab.pos(text)
                for eojeol in pos[0]
            ]
        else:
            raise AttributeError(
                "Wrong backend ! currently, we only support `pynori`, `mecab`, `none` backend."
            )


class PynoriTokenizer:
    def __init__(self):
        self.pynori = KoreanAnalyzer(
            decompound_mode="NONE",
            infl_decompound_mode="NONE",
            discard_punctuation=False,
            output_unknown_unigrams=False,
            pos_filter=False,
            stop_tags=False,
            synonym_filter=False,
            mode_synonym=False,
        )
    def pos(
        self, 
        text: str,
        preprocessed: bool = True,
    ) -> List[Tuple[str, str]]:
        
        return self.pynori.do_analysis(text, preprocessed=preprocessed)


class MecabTokenizer:
    """
    References:
        PororoMecabKoTokenizer from Pororo (kakaobrain)
        https://github.com/kakaobrain/pororo/blob/master/pororo/tasks/tokenization.py#L250
    """

    def __init__(self):
        from mecab import MeCab

        self.mecab = MeCab()

    def pos(
        self,
        text: str,
        preserve_whitespace: bool = True,
    ) -> List[Tuple[str, str]]:

        text = text.strip()
        text_ptr = 0
        results = list()

        for unit in self.mecab.pos(text):
            token = unit[0]
            pos = unit[1]
            if preserve_whitespace:
                if text[text_ptr] == " ":
                    # Move text pointer to whitespace token to reserve whitespace
                    # cf. to prevent double white-space, we move pointer to next eojeol
                    while text[text_ptr] == " ":
                        text_ptr += 1
                    results.append((" ", "SP"))
            results.append((token, pos))
            text_ptr += len(token)

        return results

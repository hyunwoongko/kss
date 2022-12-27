# Copyright (C) 2021 Hyunwoong Ko <kevin.ko@tunib.ai> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.

from typing import List, Tuple

from kss._elements.subclasses import Syllable
from kss._modules.sentences.sentence_processor import SentenceProcessor
from kss._utils.const import (
    bracket_open_to_close,
    bracket_close_to_open,
    quotes_open_to_close,
    quotes_close_to_open,
    special_symbols_for_split,
    jamo,
    spaces,
    special_symbols_for_suffix,
    daggers,
)
from kss._utils.emojis import _emojis


class SentencePreprocessor(SentenceProcessor):
    _correction = {
        lambda c, p: c in special_symbols_for_split or c in daggers: "PF",  # Prefix
        lambda c, p: c in "!?.": "SF",
        lambda c, p: c in ",:/ㆍ": "SC",
        lambda c, p: c in "".join(bracket_open_to_close): "SSO",
        lambda c, p: c in "".join(bracket_close_to_open): "SSC",
        lambda c, p: c in "`'\"″": "QTN",  # quotes normal
        lambda c, p: c in "".join(quotes_open_to_close): "QTO",  # quotes open
        lambda c, p: c in "".join(quotes_close_to_open): "QTC",  # quotes close
        lambda c, p: c in jamo: "JAMO",
        lambda c, p: c == "요" and ("EC" in p or "JX" == p): "EF",
        lambda c, p: (
            c == "^" or c in _emojis or c in special_symbols_for_suffix
        ): "EMOJI",
        lambda c, p: c in spaces: "SP",
    }

    def preprocess(self, input_morphemes: List[Tuple[str, str]]) -> List[Syllable]:
        """
        Convert mecab morphemes to syllables and correct wrong tags

        Args:
            input_morphemes (List[Tuple[str, str]]): input morphemes

        Returns:
            List[Syllable]: syllables in input text
        """
        syllables = self._convert_morphemes_to_syllables(input_morphemes)
        syllables = self._correct_wrong_tags(syllables)
        return syllables

    def _convert_morphemes_to_syllables(
        self, input_morphemes: List[Tuple[str, str]]
    ) -> List[Syllable]:
        """
        Convert mecab morphemes to syllables.

        Args:
            input_morphemes (List[Tuple[str, str]]): input morphemes

        Returns:
            List[Syllable]: syllables in input text.
        """

        prev = None
        syllables = []
        for pos in input_morphemes:
            for char in pos[0]:
                tag = pos[1]
                for _func, _tag in self._correction.items():
                    if _func(char, pos[1]):
                        tag = _tag
                        break
                syllable = Syllable(char, tag)
                syllable.prev = prev
                if prev is not None:
                    prev.next = syllable
                syllables.append(syllable)
                prev = syllable

        return syllables

    def _correct_wrong_tags(self, syllables: List[Syllable]):
        """
        Convert mecab morphemes to syllables and preprocess syllables

        Args:
            syllables (List[Syllable]): input syllables

        Returns:
            List[Syllable]: syllables in input text
        """
        for syllable in syllables:
            if syllable.check_pos_and_text(
                "JKS", "이"
            ) and syllable.next.check_pos_and_text("MAG", "다"):
                self._change_poses(syllable, "VCP", "EF")

            if syllable.check_pos_and_text(
                "EF", "네"
            ) and syllable.next.check_pos_and_text("XSN", "용"):
                self._change_poses(syllable, "EF", "EF")

            if syllable.check_pos_and_text(
                "EC", "까"
            ) and syllable.next.check_pos_and_text("NNG", "용"):
                self._change_poses(syllable, "EF", "EF")

            if (
                syllable.check_pos_and_text("EF", "을")
                and syllable.next.check_pos_and_text("EF", "까")
                and syllable.next.next.check_pos_and_text("XSN", "용")
            ):
                self._change_poses(syllable, "EF", "EF", "EF")

            if (
                syllable.check_pos_and_text("EP", "였")
                and syllable.next.check_pos_and_text("EC", "게")
                and syllable.next.next.check_pos_and_text("NNG", "용")
            ):
                self._change_poses(syllable, "EP", "EF", "EF")

            if syllable.check_pos_and_text(
                "EC", "구"
            ) and syllable.next.check_pos_and_text("NNG", "용"):
                self._change_poses(syllable, "EF", "EF")

            if syllable.check_pos_and_text(
                "EF", "엇"
            ) and syllable.next.check_pos_and_text("IC", "음"):
                self._change_poses(syllable, "EP", "ETN")

            if syllable.check_pos_and_text("EC", "쥬"):
                self._change_poses(syllable, "EF")

            if syllable.check_pos_and_text(
                "EC", "어"
            ) and syllable.next.check_pos_and_text("EC", "용"):
                self._change_poses(syllable, "EF", "EF")

            if syllable.check_pos_and_text("UNKNOWN", "떄"):
                self._change_poses(syllable, "NNG")

        return syllables

    @staticmethod
    def _change_poses(syllable: Syllable, *poses: str):
        """
        Change poses from the given syllable.
        This method could make a huge problem, so this implemented in preprocessor class.

        Args:
            syllable (Syllable): input syllable
            *poses (str): poses to be changed
        """
        _next = syllable
        for pos in poses:
            _next.pos = pos
            _next = _next.next

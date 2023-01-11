# Copyright (C) 2021 Hyunwoong Ko <kevin.ko@tunib.ai> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.

from abc import ABC
from functools import lru_cache
from typing import Tuple, List, Any

from kss._modules.morphemes.utils import _get_mecab, _get_pecab, _preserve_space
from kss._utils.const import spaces


class Analyzer(ABC):
    _analyzer, _backend = None, None

    def pos(self, text: str, drop_space: bool) -> Any:
        raise NotImplementedError

    @staticmethod
    def _drop_space(tokens: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        return [token for token in tokens if token[0] not in spaces]


class MecabAnalyzer(Analyzer):
    # `_analyzer` object must be class variable because of multiprocessing
    _analyzer, _backend = _get_mecab()

    @lru_cache(maxsize=500)
    def pos(self, text: str, drop_space: bool) -> List[Tuple[str, str]]:
        """
        Get pos information.

        Args:
            text (str): input text
            drop_space (bool): drop all spaces or not.

        Returns:
            List[Tuple[str, str]]: output of analysis.
        """
        output = self._analyzer.pos(text)
        output = _preserve_space(text, output, spaces=" \n\r\t\v")

        if drop_space:
            output = self._drop_space(output)

        return output


class PecabAnalyzer(Analyzer):
    # `_analyzer` object must be class variable because of multiprocessing
    _analyzer, _backend = _get_pecab()

    @lru_cache(maxsize=500)
    def pos(self, text: str, drop_space: bool) -> List[Tuple[str, str]]:
        """
        Get pos information.

        Args:
            text (str): input text
            drop_space (bool): drop all spaces or not.

        Returns:
            List[Tuple[str, str]]: output of analysis.
        """
        output = self._analyzer.pos(text)
        output = _preserve_space(text, output, spaces=" \n\r\t\v\f")

        if drop_space:
            output = self._drop_space(output)

        return output


class CharacterAnalyzer(Analyzer):
    _analyzer, _backend = None, "character"

    @lru_cache(maxsize=500)
    def pos(self, text: str, drop_space: bool) -> List[Tuple[str, str]]:
        """
        Get pos information.

        Args:
            text (str): input text
            drop_space (bool): drop all spaces or not.

        Returns:
            List[Tuple[str, str]]: output of analysis.
        """
        output = [(char, "-") for char in text]

        if drop_space:
            output = self._drop_space(output)

        return output

# Copyright (C) 2021 Hyunwoong Ko <kevin.ko@tunib.ai> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.

from abc import ABC
from functools import lru_cache
from typing import Tuple, List, Any

from kss._modules.morphemes.utils import _get_mecab, _get_pecab, _preserve_space


class Analyzer(ABC):
    def pos(self, text: str) -> Any:
        raise NotImplementedError


class MecabAnalyzer(Analyzer):
    # `_analyzer` object must be class variable because of multiprocessing
    _analyzer, _backend = _get_mecab()

    @lru_cache(maxsize=500)
    def pos(self, text: str) -> List[Tuple[str, str]]:
        """
        Get pos information.

        Args:
            text (str): input text

        Returns:
            List[Tuple[str, str]]: output of analysis.
        """

        output = self._analyzer.pos(text)
        output = _preserve_space(text, output)
        return output


class PecabAnalyzer(Analyzer):
    # `_analyzer` object must be class variable because of multiprocessing
    _analyzer, _backend = _get_pecab()

    @lru_cache(maxsize=500)
    def pos(self, text: str) -> List[Tuple[str, str]]:
        """
        Get pos information.

        Args:
            text (str): input text

        Returns:
            List[Tuple[str, str]]: output of analysis.
        """
        return self._analyzer.pos(text, drop_space=False)

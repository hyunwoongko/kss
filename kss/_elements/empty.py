# Copyright (C) 2021 Hyunwoong Ko <kevin.ko@tunib.ai> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.

from dataclasses import dataclass
from typing import Optional, List, Tuple


@dataclass
class Empty(object):
    _next = None
    _prev = None

    def __init__(self, text="", pos=""):
        self.text = text
        self.pos = pos

    def __str__(self):
        return f"{self.__class__.__qualname__}()"

    def __repr__(self):
        return self.__str__()

    @property
    def next(self):
        return self

    @property
    def prev(self):
        return self

    @next.setter
    def next(self, _next):
        pass

    @prev.setter
    def prev(self, _prev):
        pass

    def next_skip(self, *poses, exclude=None):
        return self

    def prev_skip(self, *poses, exclude=None):
        return self

    def prev_skip_from_current(self, *poses, exclude=None):
        return self

    def next_skip_from_current(self, *poses, exclude=None):
        return self

    def check_pos(self, *poses, exclude: Optional[List[str]] = None) -> bool:
        """
        Check pos of given syllable.

        Args:
            poses (Tuple[str]): poses for check
            exclude (Optional[List[str]]): excluded poses

        Returns:
            bool: whether pos of the syllable is contained in poses or not.
        """
        return False

    def check_text(self, *texts, exclude: Optional[List[str]] = None) -> bool:
        """
        Check text of given syllable.

        Args:
            texts (Tuple[str]): texts for check
            exclude (Optional[List[str]]): excluded poses

        Returns:
            bool: whether text of the syllable is contained in pos_list or not.
        """
        return False

    def check_pos_and_text(
        self,
        poses: Tuple,
        texts: Tuple,
        exclude_poses: Optional[Tuple] = None,
        exclude_texts: Optional[Tuple] = None,
    ):
        """
        Check pos and text at the same time

        Args:
            poses: poses for check
            texts (Tuple): texts for check
            exclude_poses (Optional[Tuple]): excluded poses
            exclude_texts (Optional[Tuple]): excluded texts

        Returns:
            bool: whether pos and text of the syllable are contained in input poses and texts.
        """

    def check_texts(self, text: str) -> bool:
        """
        Check texts of current and next syllables

        Args:
            text (str): texts for check

        Returns:
            bool: whether text of the current and next syllables re contained in input text or not.
        """
        return False

# Copyright (C) 2021 Hyunwoong Ko <kevin.ko@tunib.ai> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.

from dataclasses import dataclass
from functools import lru_cache
from typing import Optional, Tuple, Union

from kss._elements.empty import Empty


@dataclass
class Element(object):
    _next: "Element" = None
    _prev: "Element" = None

    def __init__(self, text, pos):
        self.text = text
        self.pos = pos

    def __str__(self):
        return str((self.text, self.pos))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return other.text == self.text and other.pos == self.pos

    def __hash__(self):
        return hash((self.text, self.pos))

    @property
    def next(self):
        if self._next is None:
            return Empty()
        return self._next

    @next.setter
    def next(self, _next):
        self._next = _next

    @property
    def prev(self):
        if self._prev is None:
            return Empty()
        return self._prev

    @prev.setter
    def prev(self, _prev):
        self._prev = _prev

    def next_skip(self, *poses, exclude=None):
        _next = self.next

        if isinstance(_next, Empty):
            return _next

        while _next.check_pos(*poses, exclude=exclude):
            _next = _next.next

        return _next

    def prev_skip(self, *poses, exclude=None):
        _prev = self.prev

        if isinstance(_prev, Empty):
            return _prev

        while _prev.check_pos(*poses, exclude=exclude):
            _prev = _prev.prev

        return _prev

    def prev_skip_from_current(self, *poses, exclude=None):
        _prev = self

        if isinstance(_prev, Empty):
            return _prev

        while _prev.check_pos(*poses, exclude=exclude):
            _prev = _prev.prev

        return _prev

    def next_skip_from_current(self, *poses, exclude=None):
        _next = self

        if isinstance(_next, Empty):
            return _next

        while _next.check_pos(*poses, exclude=exclude):
            _next = _next.next

        return _next

    def check_pos(self, *poses, exclude: Optional[Tuple] = None) -> bool:
        """
        Check pos of given syllable.

        Args:
            poses (str): poses for check
            exclude (Optional[Tuple]): excluded poses

        Returns:
            bool: whether pos of the syllable is contained in input poses or not.
        """
        for target in poses:
            if target in self.pos:
                if exclude is not None:
                    for e in exclude:
                        if e in self.pos:
                            return False
                return True
        return False

    def check_text(self, *texts, exclude: Optional[Tuple] = None) -> bool:
        """
        Check text of given syllable.

        Args:
            texts (str): texts for check
            exclude (Optional[Tuple]): excluded texts

        Returns:
            bool: whether text of the syllable is contained in input texts or not.
        """
        for target in texts:
            if target in self.text:
                if exclude is not None:
                    for e in exclude:
                        if e in self.text:
                            return False
                return True
        return False

    def check_pos_and_text(
        self,
        poses: Union[str, Tuple],
        texts: Union[str, Tuple],
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
        if isinstance(poses, str):
            poses = (poses,)
        if isinstance(texts, str):
            texts = (texts,)

        return self.check_pos(*poses, exclude=exclude_poses) and self.check_text(
            *texts, exclude=exclude_texts
        )

    def check_texts(self, text: str) -> bool:
        """
        Check texts of current and next syllables

        Args:
            text (str): texts for check

        Returns:
            bool: whether text of the current and next syllables re contained in input text or not.
        """
        _node = self
        matches = []
        for char in text:
            same = _node.text == char
            if same is False:
                return False
            else:
                matches.append(same)
                _node = _node.next
        return all(matches)

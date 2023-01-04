# Copyright (C) 2021 Hyunwoong Ko <kevin.ko@tunib.ai> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.

from functools import lru_cache
from itertools import chain
from typing import List, Dict, Tuple, Iterable, Optional

from kss._elements.subclasses import Syllable
from kss._utils.const import (
    double_quotes,
    double_quotes_open_to_close,
    double_quotes_close_to_open,
    single_quotes,
    single_quotes_open_to_close,
    single_quotes_close_to_open,
    single_quotes_wo_direction,
    double_quotes_wo_direction,
)


class EmbracingProcessor:
    def __init__(self):
        self.single_stack, self.double_stack = [], []
        self.single_pop, self.double_pop = "'", '"'
        self.single_idx, self.double_idx = 0, 0
        self.single_sent_idx, self.double_sent_idx = 0, 0

    def empty(self) -> bool:
        """
        Check all stacks are empty or not.

        Returns:
            bool: True if all stacks are empty else False.
        """
        return self._empty([self.single_stack, self.double_stack], dim=2)

    def process(self, idx: int, sent_idx: int, syllable: Syllable):
        """
        Push or pop symbols to detect embraced sentences

        Args:
            idx (int): current syllable index
            sent_idx (int): current sentence index
            syllable (Syllable): current syllable object
        """
        if syllable.text in single_quotes_wo_direction:
            self.single_sent_idx = sent_idx
            self.single_idx = idx
            self.single_pop = self._pop_symbol(
                syllable=syllable,
                stack=self.single_stack,
                open_to_close=single_quotes_open_to_close,
                close_to_open=single_quotes_close_to_open,
            )
        elif syllable.text in double_quotes_wo_direction:
            self.double_sent_idx = sent_idx
            self.double_idx = idx
            self.double_pop = self._pop_symbol(
                syllable=syllable,
                stack=self.double_stack,
                open_to_close=double_quotes_open_to_close,
                close_to_open=double_quotes_close_to_open,
            )

    def update_index(self, idx: int, sent_idx: int, syllable: Syllable):
        """
        Update indices of syllables and sentences

        Args:
            idx (int): current syllable index
            sent_idx (int): current sentence index
            syllable (Syllable): current syllable object
        """

        if syllable.text in single_quotes:
            self.single_idx = idx
            self.single_sent_idx = sent_idx

        elif syllable.text in double_quotes:
            self.double_idx = idx
            self.double_sent_idx = sent_idx

    def realign(
        self,
        input_sentences: List[Syllable],
        output_sentences: List[List[Syllable]],
        func: "function",
    ) -> List[List[Syllable]]:
        """
        Realign wrongly split sentences because of all symbols.

        Args:
            input_sentences (List[Syllable]): input sentences
            output_sentences (List[List[Syllables]): split sentences from `_split_sentences`
            func (function): split function

        Returns:
            List[List[Syllable]]: corrected split sentences.
        """
        if len(self.single_stack) != 0:
            return self._realign_sentences(
                input_sentences=input_sentences,
                output_sentences=output_sentences,
                idx=self.single_idx,
                sent_idx=self.single_sent_idx,
                func=func,
            )

        if len(self.double_stack) != 0:
            return self._realign_sentences(
                input_sentences=input_sentences,
                output_sentences=output_sentences,
                idx=self.double_idx,
                sent_idx=self.double_sent_idx,
                func=func,
            )

        return output_sentences

    def _pop_symbol(
        self,
        syllable: Syllable,
        stack: List[str],
        open_to_close: Dict[str, str],
        close_to_open: Dict[str, str],
    ) -> str:
        """
        Pop symbols from given stack if the symbols are contained in given dictionaries.

        Args:
            syllable (Syllable): syllable object
            stack (List[str]): symbol stack
            open_to_close (Dict[str, str]): open to close dict
            close_to_open (Dict[str, str]): close to open dict

        Returns:
            str: popped symbol
        """
        if syllable.text in open_to_close.keys():
            pop = self._push_pop_symbol(
                stack=stack,
                symbol=open_to_close[syllable.text],
                current_char=syllable.text,
            )
        else:
            pop = self._push_pop_symbol(
                stack=stack,
                symbol=close_to_open[syllable.text],
                current_char=syllable.text,
            )
        return pop

    def _realign_sentences(
        self,
        input_sentences: List[Syllable],
        output_sentences: List[List[Syllable]],
        idx: int,
        sent_idx: int,
        func: "function",
    ) -> List[List[Syllable]]:
        """
        Realign wrongly split sentences because of specific symbol.

        Args:
            input_sentences (List[Syllable]): input sentences
            output_sentences (List[List[Syllables]): split sentences from `_split_sentences`
            idx (int): current syllable index
            sent_idx (int): current sentence index
            func (function): split function

        Returns:
            List[List[Syllable]]: corrected split sentences.
        """
        return output_sentences[:sent_idx] + self._realign_sub_sentences(
            output_sentences=tuple(chain(*output_sentences[sent_idx:])),
            syllable=input_sentences[idx],
            idx_in_sent=self.get_idx_in_sent(output_sentences, idx, sent_idx),
            func=func,
        )

    @lru_cache(maxsize=500)
    def _realign_sub_sentences(
        self,
        output_sentences: Tuple,
        syllable: Syllable,
        idx_in_sent: int,
        func: "function",
    ):
        """
        Realign wrongly split sub-sentences because of specific symbol.

        Args:
            output_sentences (Tuple): tuple of syllables
            syllable (Syllable): problematic syllable
            idx_in_sent (int): syllable index in sentence
            func (function): split function

        Returns:
            List[List[Syllable]]: corrected split sub-sentences.
        """
        before_quote = func(output_sentences[:idx_in_sent])
        before_last = before_quote[-1] if len(before_quote) > 0 else []
        before_quote = [] if len(before_quote) == 1 else before_quote[:-1]

        after_quote = func(output_sentences[idx_in_sent + 1 :])
        after_first = after_quote[0] if len(after_quote) > 0 else []
        after_quote = [] if len(after_first) == 1 else after_quote[1:]

        middle_quote = [before_last + [syllable] + after_first]
        return before_quote + middle_quote + after_quote

    @staticmethod
    def get_idx_in_sent(
        output_sentences: List[List[Syllable]],
        idx: int,
        sent_idx: int,
    ) -> int:
        """
        Get syllable index in the sentence.

        Args:
            output_sentences (List[List[Syllables]): split sentences from `_split_sentences`
            idx (int): current syllable index
            sent_idx (int): current sentence index

        Returns:
            int: syllable index in sentence
        """
        return idx - (
            0 if sent_idx == 0 else sum([len(o) for o in output_sentences[:sent_idx]])
        )

    @staticmethod
    def _top(stack: List[str], symbol: str) -> bool:
        """
        Is the symbol was top of the stack or not.

        Args:
            stack (List[str]): stack of symbols
            symbol (symbol): symbol string

        Returns:
            bool: whether the symbol was top of the stack or not.
        """
        return stack[len(stack) - 1] == symbol

    def _empty(self, obj: Iterable, dim: int = 1) -> bool:
        """
        Check the length of object is 0.

        Args:
            obj (Iterable): iterable object
            dim (int): object dimension

        Returns:
            bool: whether the length of object is 0 or not.
        """
        assert dim in [1, 2], "only 1 or 2 dimension iterable is supported."

        if dim == 1:
            return len(obj) == 0
        else:
            return all([self._empty(o) for o in obj])

    def _push_pop_symbol(
        self,
        stack: List[str],
        symbol: str,
        current_char: str,
    ) -> Optional[str]:
        """
        Push or pop symbol in the list.

        Args:
            stack (List[str]): stack of symbols
            symbol (str): symbol string
            current_char (str): current character of the syllable

        Returns:
            Optional[str]: popped symbol string if the symbol was top, else returns None.
        """
        if self._empty(stack):
            stack.append(symbol)

        else:
            if self._top(stack, current_char):
                return stack.pop()
            else:
                stack.append(symbol)

        return current_char

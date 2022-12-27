# Copyright (C) 2021 Hyunwoong Ko <kevin.ko@tunib.ai> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.

from typing import List

from kss._elements.subclasses import Syllable
from kss._modules.sentences.sentence_preprocessor import SentenceProcessor
from kss._utils.const import quotes_or_brackets_close_to_open, spaces, daggers


class SentencePostprocessor(SentenceProcessor):
    def postprocess(
        self,
        output_sentences: List[List[Syllable]],
        strip: bool,
    ) -> List[str]:
        """
        Postprocess output sentences by splitting rules

        Args:
            output_sentences (List[List[Syllable]]): output sentences by splitting rules in syllable object
            strip (bool): strip all sentences or not

        Returns:
            List[str]: postprocessed output setences in string
        """

        output_sentences = self._merge_broken_sub_sentence_in_quotes_or_brackets(
            output_sentences
        )
        output_sentences = self._move_first_footnote_in_sentence_to_previous(
            output_sentences
        )
        output_sentences = self._move_first_daggers_in_sentence_to_previous(
            output_sentences
        )
        output_sentences = self._move_non_structural_sub_sent_in_brackets_to_previous(
            output_sentences
        )
        output_sentences = self._move_unexpected_split_sentences_to_previous(
            output_sentences
        )
        output_sentences = self._move_symbol_sentences_only_to_previous(
            output_sentences
        )
        output_sentences = self._convert_syllables_to_sentences_with_cleaning(
            output_sentences, strip
        )
        return output_sentences

    def _merge_broken_sub_sentence_in_quotes_or_brackets(
        self, output_sentences: List[List[Syllable]]
    ) -> List[List[Syllable]]:
        """
        Merge broken sub-sentence in quotes or brackets.

        Args:
            output_sentences (List[List[Syllable]]): list of syllables

        Returns:
            List[List[Syllable]]: corrected list of syllables.

        Notes:
            열고 닫음이 분명한 괄호나 따옴표 안의 인용문/독백 등이 분리 된 경우 이를 찾아내서 병합한다.

            예시:
                입력: ["나는 생각했다. ", "(분명히 맞을 것이다. ", "그래야만 한다.) ", "그리곤 말했다."]
                출력: ["나는 생각했다. ", "(분명히 맞을 것이다. 그래야만 한다.) ", "그리곤 말했다."]
        """
        num_sentences = len(output_sentences)
        last_open, first_close = {}, {}

        for sentence_idx in range(num_sentences):
            found_close = False
            for syllable_idx, output_syllable in enumerate(
                output_sentences[sentence_idx]
            ):
                if output_syllable.check_pos("SSO", "QTO"):
                    if output_syllable.text not in last_open:
                        last_open[output_syllable.text] = [(sentence_idx, syllable_idx)]
                    else:
                        last_open[output_syllable.text].append(
                            (sentence_idx, syllable_idx)
                        )

                if output_syllable.check_pos("SSC", "QTC") and not found_close:
                    if output_syllable.text not in first_close:
                        first_close[output_syllable.text] = [
                            (sentence_idx, syllable_idx)
                        ]
                    else:
                        first_close[output_syllable.text].append(
                            (sentence_idx, syllable_idx)
                        )

            for syllable_close, close_values in first_close.items():
                if (
                    len(close_values) == 0
                    or syllable_close not in quotes_or_brackets_close_to_open
                ):
                    continue

                close_sent_idx, close_idx = close_values[-1]
                syllable_open = quotes_or_brackets_close_to_open[syllable_close]

                if syllable_open not in last_open:
                    continue

                open_values = [
                    (sent_i, syl_i)
                    for sent_i, syl_i in last_open[syllable_open]
                    if sent_i < close_sent_idx
                    or (sent_i == close_sent_idx and syl_i < close_idx)
                ]
                if len(open_values) == 0:
                    continue
                open_sent_idx, open_idx = open_values[-1]

                if close_sent_idx <= open_sent_idx:
                    continue
                for sub_sent_idx in range(open_sent_idx + 1, close_sent_idx + 1):
                    sub_sent = output_sentences[sub_sent_idx]
                    if sub_sent_idx == close_sent_idx:
                        sub_sent = sub_sent[: close_idx + 1]

                    for sub_syllable in sub_sent:
                        output_sentences[open_sent_idx].append(sub_syllable)

                    if sub_sent_idx == close_sent_idx:
                        output_sentences[sub_sent_idx] = output_sentences[sub_sent_idx][
                            close_idx + 1 :
                        ]
                    else:
                        output_sentences[sub_sent_idx] = []

                last_open[syllable_open].remove((open_sent_idx, open_idx))
                first_close[syllable_close].remove((close_sent_idx, close_idx))
        return self._remove_empty_sentence(output_sentences)

    @staticmethod
    def _check_text_from_character(output_syllable: Syllable, target: str):
        """
        Check given text is matched from character

        Args:
            output_syllable (Syllable): output syllable
            target (str): target string

        Returns:
            bool: match or not
        """
        _next = output_syllable
        if (not target.startswith(output_syllable.text)) and _next.text in target:
            split = target.split(_next.text)
            if len(split) > 1:
                target = output_syllable.text + target.split(_next.text)[1]

        for idx, char in enumerate(target):
            if _next.text != char:
                return False
            else:
                _next = _next.next
        return True

    def _move_first_daggers_in_sentence_to_previous(
        self, output_sentences: List[List[Syllable]]
    ) -> List[List[Syllable]]:
        """
        Move first daggers in sentence to previous.

        Args:
            output_sentences (List[List[Syllable]]): list of syllables

        Returns:
            List[List[Syllable]]: corrected list of syllables.

        Notes:
            칼표 처리:
                칼표가 처음으로 등장한 문장의 이전문장이 행갈이나 공백으로 끝난게 아니라면 칼표를 이전 문장으로 옮긴다.

            예시:
                입력: ["GPT3는 인공지능 모델이다.", "† 그러나 이 모델은""]
                출력: ["GPT3는 인공지능 모델이다.†", "그러나 이 모델은""] <--- 본문에 쓰인 각주로 인식.

                입력: ["GPT3는 인공지능 모델이다.\n", "† 그러나 이 모델은""]
                출력: ["GPT3는 인공지능 모델이다.\n", "† 그러나 이 모델은""]  <--- footer에 쓰인 각주로 인식. (그대로 유지)

                입력: ["GPT3는 인공지능 모델이다. ", "† 그러나 이 모델은""]
                출력: ["GPT3는 인공지능 모델이다. ", "† 그러나 이 모델은""]  <--- footer에 쓰인 각주로 인식. (그대로 유지)
        """

        for sentence_idx, output_sentence in enumerate(output_sentences):
            if sentence_idx != 0 and len(output_sentence) != 0:
                if output_sentence[0].next_skip_from_current("SP").text in daggers:
                    if output_sentences[sentence_idx - 1][-1].text not in " \r\n\v\f":
                        insert_idx = sentence_idx - 1
                        while insert_idx > 0 and len(output_sentences[insert_idx]) == 0:
                            insert_idx -= 1
                        output_sentences[insert_idx].append(output_sentence[0])
                        output_sentences[sentence_idx] = output_sentence[1:]

        return self._remove_empty_sentence(output_sentences)

    def _move_symbol_sentences_only_to_previous(
        self, output_sentences: List[List[Syllable]]
    ) -> List[List[Syllable]]:
        """
        Move symbol only sentences to previous

        Args:
            output_sentences (List[List[Syllable]]): list of syllables

        Returns:
            List[List[Syllable]]: corrected list of syllables.

        Notes:
            Symbol 처리:
                Symbol로만 이루어진 문장을 이전 문장으로 옮긴다.
        """
        for sentence_idx, output_sentence in enumerate(output_sentences):
            if (
                sentence_idx != 0
                and len(output_sentence) != 0
                and (
                    all(
                        [
                            syllable.check_pos("SY", "SF", "SE", "SC", "QT", "SS", "SP")
                            for syllable in output_sentence
                        ]
                    )
                )
            ):
                for output_syllable in output_sentence:
                    insert_idx = sentence_idx - 1
                    while insert_idx > 0 and len(output_sentences[insert_idx]) == 0:
                        insert_idx -= 1
                    output_sentences[insert_idx].append(output_syllable)
                output_sentences[sentence_idx] = []
        return self._remove_empty_sentence(output_sentences)

    def _move_first_footnote_in_sentence_to_previous(
        self, output_sentences: List[List[Syllable]]
    ) -> List[List[Syllable]]:
        """
        Move first footnote in sentence to previous.

        Args:
            output_sentences (List[List[Syllable]]): list of syllables

        Returns:
            List[List[Syllable]]: corrected list of syllables.

        Notes:
            각주 처리:
                최초로 발견되는 대괄호('[') 안에 있는 것이 각주이면 이를 이전 문장으로 옮긴다.

            예시:
                입력: ["그것은 사실이였다.", "[13] 하지만 그에 따라"]
                출력: ["그것은 사실이였다.[13]", "하지만 그에 따라"]

                출력: ["그것은 사실이였다.", "[편집]하지만 그에 따라"]
                출력: ["그것은 사실이였다.[편집]", "하지만 그에 따라"]

                출력: ["그것은 사실이였다.", "[편집]을 하고 싶지만 그에 따라"]
                출력: ["그것은 사실이였다.", "[편집]을 하고 싶지만 그에 따라"] <--- 유지

                출력: ["그것은 사실이였다.", "[더 보기] 마침 좋은 생각이 떠올랐다."]
                출력: ["그것은 사실이였다.[더 보기]", "마침 좋은 생각이 떠올랐다."]

                출력: ["그것은 사실이였다.", "[더 보기] 버튼을 눌러보세요."]
                출력: ["그것은 사실이였다.", "[더 보기] 버튼을 눌러보세요."] <--- 유지

                출력: ["그것은 사실이였다.", "[사각형]은"]
                출력: ["그것은 사실이였다.", "[사각형]은"] <--- 유지
        """

        for sentence_idx, output_sentence in enumerate(output_sentences):
            if sentence_idx != 0 and len(output_sentence) != 0:
                if output_sentence[0].next_skip_from_current("SP").text == "[":
                    close_idx = None
                    move = False
                    for syllable_idx, output_syllable in enumerate(output_sentence):
                        if output_sentences[sentence_idx - 1][
                            -1
                        ].text not in "\r\n\v\f" and (
                            output_syllable.text in "[0123456789*, ]"
                            or self._check_text_from_character(output_syllable, "편집]")
                            or self._check_text_from_character(output_syllable, "더 보기]")
                            or self._check_text_from_character(output_syllable, "더보기]")
                            or self._check_text_from_character(output_syllable, "스포일러]")
                            or self._check_text_from_character(output_syllable, "참고 ")
                        ):
                            move = True
                        else:
                            break

                        if output_syllable.text == "]":
                            close_idx = syllable_idx

                    if close_idx is not None:
                        if move is True:
                            if close_idx + 1 < len(output_sentence):
                                next_syllable = output_sentence[
                                    close_idx + 1
                                ].next_skip_from_current("SP")

                                move = (not next_syllable.pos.startswith("J")) and (
                                    not next_syllable.check_texts("버튼")
                                )

                        if move is True:
                            insert_idx = sentence_idx - 1
                            while (
                                insert_idx > 0
                                and len(output_sentences[insert_idx]) == 0
                            ):
                                insert_idx -= 1
                            output_sentences[insert_idx] += output_sentence[
                                : close_idx + 1
                            ]
                            output_sentences[sentence_idx] = output_sentence[
                                close_idx + 1 :
                            ]

        return self._remove_empty_sentence(output_sentences)

    def _move_non_structural_sub_sent_in_brackets_to_previous(
        self, output_sentences: List[List[Syllable]]
    ) -> List[List[Syllable]]:
        """
        Move non-structural sub sentence in brackets to previous.

        Args:
            output_sentences (List[List[Syllable]]): list of syllables

        Returns:
            List[List[Syllable]]: corrected list of syllables.

        Notes:
            최초로 발견되는 괄호('(') 안의 서브 문장이 명사(N*)로 끝나면서 공백을 제외한 다음 문자가
            조사(J*)가 아니라면 잘못 분리된 것으로 간주하고 이를 이전 문장으로 옮긴다.

            예시:
                입력: ["아니거든 !!! ", "(강한부정) 너가 먼자 말했잖아!"]
                출력: ["아니거든 !!! (강한부정)", " 너가 먼자 말했잖아!"]
        """
        for sentence_idx, output_sentence in enumerate(output_sentences):
            if sentence_idx != 0 and len(output_sentence) != 0:
                if output_sentence[0].next_skip_from_current("SP").text == "(":
                    close_idx, close_last = None, None
                    for syllable_idx, output_syllable in enumerate(output_sentence):
                        if output_syllable.text == ")":
                            close_idx = syllable_idx
                            close_last = syllable_idx == len(output_sentence) - 1
                            break

                    if close_idx is None:
                        continue

                    noun_finish = (
                        output_sentence[close_idx - 1]
                        .prev_skip_from_current(
                            *self._all_s_poses, exclude=self._all_s_exclude
                        )
                        .pos.startswith("N")
                    )

                    not_josa_start = close_last is True or not (
                        output_sentence[close_idx + 1]
                        .next_skip_from_current("SP")
                        .pos.startswith("J")
                    )

                    additional_merge = 0
                    if not close_last:
                        for output_syllable in output_sentence[close_idx + 1 :]:
                            if output_syllable.check_pos(
                                *self._all_s_poses, exclude=self._all_s_exclude
                            ):
                                additional_merge += 1
                            else:
                                break

                    if noun_finish and not_josa_start:
                        for output_syllable in output_sentence[
                            : close_idx + 1 + additional_merge
                        ]:
                            insert_idx = sentence_idx - 1
                            while (
                                insert_idx > 0
                                and len(output_sentences[insert_idx]) == 0
                            ):
                                insert_idx -= 1
                            output_sentences[insert_idx].append(output_syllable)
                        output_sentences[sentence_idx] = output_sentence[
                            close_idx + 1 + additional_merge :
                        ]

        return self._remove_empty_sentence(output_sentences)

    def _move_unexpected_split_sentences_to_previous(
        self, output_sentences: List[List[Syllable]]
    ) -> List[List[Syllable]]:
        """
        Move unexpected split sentences to previous.

        Args:
            output_sentences (List[List[Syllable]]): list of syllables

        Returns:
            List[List[Syllable]]: corrected list of syllables.

        Notes:
            분리된 문장이 조사(J*), 긍정지정사(VCP), 연결어미(EC), 보조용언(VX)으로 시작되면 이전 문장에 이어 붙인다.
            또는 문장이 칼표나 겹칼표 등의 주석 문자로 시작 했을때 다음 문자가 공백이 아니면

            예시:
                입력: ['반드시 막아야만 한다', '라고 했다']
                출력: ['반드시 막아야만 한다라고 했다']

                입력: ['반드시 막아야만 한다', '라고 했다']
                출력: ['반드시 막아야만 한다라고 했다']
        """
        for sentence_idx, output_sentence in enumerate(output_sentences):
            if (
                sentence_idx != 0
                and len(output_sentence) != 0
                and (
                    output_sentence[0].next_skip_from_current("SP").pos
                    in ("VCP+EC", "VX+EC")
                    or output_sentence[0]
                    .next_skip_from_current("SP")
                    .check_pos(
                        "J",
                        "VCP",
                        "EC",
                        "VX",
                        exclude=("MAJ", "+J", "+VCP", "+EC", "+VX"),
                    )
                )
            ):
                for output_syllable in output_sentence:
                    insert_idx = sentence_idx - 1
                    while insert_idx > 0 and len(output_sentences[insert_idx]) == 0:
                        insert_idx -= 1
                    output_sentences[insert_idx].append(output_syllable)
                output_sentences[sentence_idx] = []
        return self._remove_empty_sentence(output_sentences)

    @staticmethod
    def _convert_syllables_to_sentences_with_cleaning(
        output_sentences: List[List[Syllable]],
        strip: bool,
    ) -> List[str]:
        """
        Convert syllables to sentences with cleaning

        Args:
            output_sentences (List[List[Syllable]]): output syllables
            strip (bool): strip all sentences or not

        Returns:
            List[str]: output sentences list

        Notes:
            Syllable 객체를 모두 string으로 변경하고 각 문장에 strip을 수행한다.
        """
        final_output_sentences = []
        for output_sentence in output_sentences:
            output_sentence = "".join([syllable.text for syllable in output_sentence])
            if strip is True:
                output_sentence = output_sentence.strip(spaces)
            if len(output_sentence) != 0:
                final_output_sentences.append(output_sentence)

        return final_output_sentences

    @staticmethod
    def _remove_empty_sentence(output_sentences: List[List[Syllable]]):
        """
        Remove emtpy sentences after postprocessing

        Args:
            output_sentences (List[List[Syllable]]): split list of syllables

        Returns:
            List[List[Syllable]]: list of syllables without empty one
        """
        return [sentence for sentence in output_sentences if len(sentence) != 0]

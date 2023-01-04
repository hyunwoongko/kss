# Copyright (C) 2021 Hyunwoong Ko <kevin.ko@tunib.ai> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.

from functools import lru_cache
from typing import Tuple

from kss._elements.subclasses import Syllable
from kss._modules.sentences.sentence_processor import SentenceProcessor
from kss._utils.const import papers


class SentenceSplitter(SentenceProcessor):
    """
    Sentence Splitting Rules class

    Args:
        syllable (Syllable): current syllable
    """

    unavailable_next = set()
    unavailable_next.update({"시피", "거나", "의 "})
    unavailable_next.update({"에" + add for add in ["서", "선", "는", "도 "]})
    unavailable_next.update(
        {"라" + add for add in ["서", "는", "도 ", "던", "지만", "고", "건", "거나", "며", "면서"]}
    )
    unavailable_next.update(
        {"하" + add for add in ["여서", "여도", "였", "고는 ", "고서 ", "곤 ", "다는", "는데.", "며"]}
    )
    unavailable_next.update({"할" + add for add in ["텐데"]})

    def __init__(self, syllable: Syllable):
        self.syllable = syllable

    def __hash__(self):
        """Hash function for lru_cache"""
        return hash(self.syllable)

    ####################
    # Flow Controllers #
    ####################

    def check_split_start(self) -> bool:
        """
        Check whether the given syllable is split point or not.

        Returns:
            bool: whether the given syllable is split point or not.

        Notes:
            분할 시작 규칙:
                종결부호(SF), 캐릭터 휴리스틱 규칙, 4개의 어말어미(EF, EC, ETN, ETM) 규칙 중 하나라도 성립하면 분할한다.
        """
        return (
            self._sf()
            or self._ef()
            or self._ec()
            or self._etn()
            or self._etm()
            or self._char()
        )

    def check_split_end(self) -> Tuple[bool, bool]:
        """
        Check whether the given syllable is split end point or not.

        Returns:
            bool: whether the given syllable is split end point or not.

        Notes:
            분할 종료 규칙:
                1. 현재 문자 이후의 문자가 자모(JAMO)이면 분할을 뒤로 미룬다.
                2. 현재 문자 이후의 문자가 대부분의 부호에 속하거나 현재 문자가 쉼표(,)인데 다음 문자도 쉼표(,)이면 분할을 뒤로 미룬다.
                3. 현재 문자 이후의 문자도 분할이 가능하면 분할을 뒤로 미룬다.
                4. 위 세가지 규칙에 해당 사항이 없는 경우 분할한다.

            예외:
                1. 만약 현재 문자가 물음표(?) 혹은 느낌표(!)인데 공백을 제외한 다음 문자가 구두점(.)이면 즉시 분할한다.
                2. 만약 현재 문자가 하이푼(-)인데 공백을 제외한 다음 문자가 종결부호(SF)가 아닌 경우 지금 즉시 분할한다.
        """

        no_more_all_s = not self._check_pos(
            self._all_s_poses_wo_qtn, exclude=self._all_s_exclude
        )

        end_split = no_more_all_s and not (
            (self._check_text(",") and self._check_next_text(","))
            or (self._check_text(",") and self._check_prev_text(","))
        )

        end_split = end_split and not self.syllable.check_pos("JAMO")
        end_split = end_split and not self.check_split_start()
        end_split_exception = False

        if not end_split:
            # 예외 1
            if self._check_prev_skip_sp_text(
                ("?", "!")
            ) and self._check_next_skip_sp_text("."):
                end_split = True
                end_split_exception = True

            # 예외 2
            elif self._check_text(("－", "-", "–")) and not (
                self._check_next_skip_sp_pos("SF")
                or self._check_next_text(("－", "-", "–"))
            ):
                end_split = True
                end_split_exception = True

        return end_split, end_split_exception

    ###################
    # Splitting Rules #
    ###################

    def check_split_right_now(self) -> bool:
        """
        Check whether the given syllable is split end point or not.

        Returns:
            bool: whether the given syllable is split end point or not.

        Notes:
            단락기호(¶)가 등장하면 곧바로 분리한다.
        """
        available = self.syllable.check_text("¶")
        return available

    def _sf(self) -> bool:
        """
        Check whether the given syllable is split end point or not.

        Returns:
            bool: whether the given syllable is split end point or not.

        Notes:
            종결부호 분할 규칙:
                종결부호(SF) 뒤에 공백(SP) 혹은 기타 부호(SY), 열린 괄호(SSO), 이모지(EMOJI), 한글 자모(JAMO)가 존재하면 분할한다.

            예외:
                1. 현재 문자 앞의 공백(SP)과 종결부호(SP)을 제외한 이전 문자가 숫자이면 분할하지 않는다.
                2. 현재 문자 앞의 공백(SP)과 종결부호(SP)을 제외한 문자가 긍정지정사(VCP)이면 분할하지 않는다.
                3. 현재 문자 앞의 공백(SP)과 종결부호(SP)을 제외한 문자가 조사(J*)이면서 다음 문자가 구두점(.)이면 분할하지 않는다.
                4. 현재 문자 뒤의 공백(SP)과 종결부호(SP)을 제외한 문자가 긍정지정사(VCP)이면 분할하지 않는다.
                5. 현재 문자 뒤의 공백(SP)과 종결부호(SP)을 제외한 문자가 '만', '데+..' 등 이면 분할하지 않는다.
                6. 현재 문자 뒤의 공백(SP)과 종결부호(SF)을 제외한 문자가 접속부사(MAJ)이면 분할하지 않는다.
                7. 현재 문자 뒤의 공백(SP)을 제외한 문자가 마침표(.)가 아니고 그 뒤 문자가 곧 바로 마침표라면 분할하지 않는다.
                8. 현재 문자 뒤로 등장하는 한글 문자열이 몇가지 분할하지 않아야 하는 경우에 속하면 분할하지 않는다.
                9. 현재 문자가 ' no.', ' No.', ' vol.', ' p.', ' pp.', ' page.', ' al.', ' ed.', ' eds.'
                    ' 항.', ' 조.', ' 호.', ' 절.', ' 권.', " 쪽.' 등에 존재하면 분할하지 않는다.
        """

        available = False

        # 종결부호 분할 규칙
        if self._check_pos("SF") and (
            self._check_next_pos("SP")
            or self._check_next_skip_sp_pos(
                (
                    "SY",
                    "SSO",
                    "EMOJI",
                    "JAMO",
                )
            )
        ):
            # 예외 1
            available = not self._prev_skip(("SP", "SF")).text.isnumeric()

            # 예외 2
            available = available and not (
                self._check_prev_skip_spsf_pos("VCP", exclude="+VCP")
            )

            # 예외 3
            available = available and not (
                self._check_prev_skip_spsf_pos("J", exclude=("EMOJI", "JAMO", "+J"))
                and self._check_text(".")
                and self._check_prev_text(".")
            )

            # 예외 4
            available = available and not (
                self._check_next_skip_spsf_pos("VCP", exclude="+VCP")
            )

            # 예외 5
            available = available and not self._check_prev_skip_spsf_pos(("MAJ", "MAG"))

            # 예외 6
            available = available and not (
                (
                    self._check_prev_skip_spsf_pos("EC")
                    and self._check_prev_skip_spsf_text("만")
                )
                or (
                    self._check_prev_skip_spsf_pos(("EC", "NNB"))
                    and self._check_prev_skip_spsf_text("데")
                    and self._check_prev_text(".")
                )
            )

            # 예외 7
            next_skip_sp = self._next_skip("SP")
            prev_skip_sp = self._prev_skip("SP")

            available = (
                available
                and not (
                    not next_skip_sp.check_text(".")
                    and next_skip_sp.next_skip("SP").check_text(".")
                )
                and not (
                    not prev_skip_sp.check_text(".")
                    and prev_skip_sp.prev_skip("SP").check_text(".")
                )
            )

            # 예외 8
            available = available and not self._check_next_is_unavailable_split()

            # 예외 9
            available = available and (
                not self._check_multiple_prev_texts_from_before(*papers)
            )

        return available

    def _ef(self) -> bool:
        """
        Check whether the given syllable is split end point or not.

        Returns:
            bool: whether the given syllable is split end point or not.

        Notes:
            종결어미 분할 규칙:
                종결어미(EF)인 형태소의 마지막 문자이면 분할한다. 단, 현재 형태소에 조사(J*) 성분이 포함되면 분할하지 않는다.

            에외:
                1. 현재 문자 뒤의 공백(SP) 및 대부분 부호를 제외한 다음 문자가 쉼표(,)이면 분할하지 않는다. 단 ,,과 같이 연속되어 쓰이면 분할을 허용한다.
                2. 현재 문자 뒤의 공백(SP)을 제외한 다음 문자가 연결어미(EC), 조사(J*), 보조용언(VX) 중 하나이면 분할하지 않는다.
                3. 현재 형태소가 대명사(NP)+긍정지정사(VCP)+EF(종결어미)인데, 바로 뒤 문자가 종결부호(SF)가 아니면 분할하지 않는다.
                4. 현재 문자 바로 이전 문자가 공백(SP)이고 그 이전 문자가 보조용언(VX)이면 분할하지 않는다.
                5. 현재 문자 뒤로 등장하는 한글 문자열이 몇가지 분할하지 않아야 하는 경우에 속하면 분할하지 않는다.
        """

        available = False

        # 종결어미 분할 규칙
        if self._check_pos("EF", exclude="+J") and not self._check_next_skip_sp_pos(
            "EF"
        ):
            # 예외 1
            available = not self._check_non_doubled_comma()

            # 예외 2
            available = available and not (
                self._check_next_skip_sp_pos(
                    ("EC", "J", "VX"),
                    exclude=("MAJ", "EMOJI", "JAMO", "+VX", "+EC", "+J", "VX+"),
                )
            )

            # 예외 3
            if available and self._check_prev_pos("NP+VCP+EF"):
                available = self._check_next_pos("SF")

            # 예외 4
            available = available and not (
                self._check_prev_text(" ")
                and self.syllable.prev.check_pos("VX", exclude="VX+")
            )

            # 예외 5
            available = available and not self._check_next_is_unavailable_split()

        return available

    def _ec(self) -> bool:
        """
        Check whether the given syllable is split end point or not.

        Returns:
            bool: whether the given syllable is split end point or not.

        Notes:
            연결어미 분할 규칙:
                연결어미(EC)인 형태소의 마지막 문자가 '다'일 때, 다음 허용항을 만족하면 분할한다.
                본래, 연결어미(EC)는 분할하면 안되지만, 형태소 분석기의 성능 문제로 종결어미(EF)를 연결어미(EC)로 인식되는 경우에 대응하기 위함이다.
                단, 현재 형태소에 조사(J*) 성분이 포함되면 분할하지 않는다.

            허용:
                1. 현재 문자의 이전 문자가 선어말어미(EP)이고 현재 문자의 뒤의 공백(SP)을 제외한 다음 문자가 닫는 괄호(SSO), 닫는 따옴표(QTO), 부호(SF, SY, EMOJI) 중 하나이면 분할한다.
                2. 현재 문자의 이전 문자가 선어말어미(EP)이고 현재 문자 뒤의 공백(SP)을 제외한 다음 문자가 대명사(NP) 혹은 접속부사(MAJ)이면 분할한다.
                3. 현재 문자의 이전 문자가 연결어미(EC)이면서 '니'인데, 뒤의 문자가 '만'이면서 연결어미(EC)가 아니면 분할한다. 이는 '입니다' 및 '습니다'가 연결어미로 인식되는 경우에 대응하기 위함이다.

            예외:
                1. 현재 문자 뒤의 공백(SP) 및 대부분 부호를 제외한 다음 문자가 쉼표(,)이면 분할하지 않는다. 단 ,,과 같이 연속되어 쓰이면 분할을 허용한다.
                2. 현재 문자 뒤의 공백(SP)을 제외한 다음 문자가 긍정지정사(VCP) 조사(J*), 보조용언(VX) 중 하나이면 분할하지 않는다.
                3. 현재 문자 뒤로 등장하는 한글 문자열이 몇가지 분할하지 않아야 하는 경우에 속하면 분할하지 않는다.
        """
        available = False
        permission = False

        # 연결어미 분할 규칙
        if (
            self._check_text("다")
            and self._check_pos("EC", exclude="+J")
            and not self._check_next_skip_sp_pos("EC")
        ):
            # 예외 1
            available = not self._check_non_doubled_comma()

            # 예외 2
            available = available and not self._check_next_skip_sp_pos(
                ("VCP", "J", "VX"),
                exclude=("MAJ", "JAMO", "EMOJI", "+J", "+VCP", "+VX"),
            )

            # 예외 3
            available = available and not self._check_next_is_unavailable_split()

        if available:
            # 허용 1:
            permission = self._check_prev_pos("EP") and self._check_next_skip_sp_pos(
                ("SF", "SY", "SSO", "QTO", "EMOJI")
            )

            # 허용 2:
            permission = permission or (
                self._check_prev_pos("EP") and self._check_next_skip_sp_pos("NP", "MAJ")
            )

            # 허용 3:
            permission = permission or (
                self._check_prev_text("니")
                and self._check_prev_pos("EC")
                and not (self._check_next_text("만") and self._check_next_pos("EC"))
            )

        return available and permission

    def _etn(self) -> bool:
        """
        Check whether the given syllable is split end point or not.

        Returns:
            bool: whether the given syllable is split end point or not.

        Notes:
            명사형 전성어미 분할 규칙:
                 명사형 전성어미(ETN)인 형태소의 마지막 문자가 '기'나 '길'이 아니면 분할한다.
                 이는 명사형 전성어미가 종결형으로 사용 될 경우에 대응 하기 위함이다. (~함, ~음, ~됨 등)
                 단, 현재 형태소에 조사(J*) 및 접미사(XS*) 성분이 포함되면 분할하지 않는다.

            예외:
                1. 현재 문자 뒤의 공백(SP) 및 대부분 부호를 제외한 다음 문자가 쉼표(,)이면 분할하지 않는다. 단 ,,과 같이 연속되어 쓰이면 분할을 허용한다.
                2. 현재 문자 뒤의 바로 뒤 문자가 공백, 한글 자모(JAMO), 이모지, 부호 등이 아니면 분할하지 않는다.
                3. 현재 문자 뒤의 공백(SP)을 제외한 다음 문자가 조사(J*), 동사(VV), 형용사(VA), 보조용언(VA) 이면 분할하지 않는다.
                4. 현재 문자 뒤의 공백(SP)과 종결부호(SF)를 제외한 다음 문자가 관형사(MM) 혹은 닫는 괄호(SSC)이면 분할하지 않는다.
                5. 현재 문자 뒤의 명사형 전성어미(ETN)을 제외한 이전의 문자와 동일한 문자가 현재 문자의 바로 뒤에 등장하면 분할하지 않는다.
                6. 현재 문자 뒤로 등장하는 한글 문자열이 몇가지 분할하지 않아야 하는 경우에 속하면 분할하지 않는다.
        """
        available = False

        if (
            self._check_pos("ETN", exclude=("+J", "XS"))
            and not self._check_next_skip_sp_pos("ETN")
            and not self._check_text("기", "길")
        ):
            # 예외 1
            available = not self._check_non_doubled_comma()

            # 예외 2
            available = available and (
                self._check_next_pos(("SP", "SF", "SY", "SSO", "QTO", "EMOJI", "JAMO"))
            )

            # 예외 3
            available = available and not self._check_next_skip_sp_pos(
                ("J", "VV", "VA", "VX"),
                exclude=("MAJ", "EMOJI", "JAMO", "+J"),
            )

            # 예외 4
            available = available and not self._check_next_skip_spsf_pos(("MM", "SSC"))

            # 예외 5
            available = available and not (
                self._check_next_skip_all_s_text(
                    self._prev_skip("ETN")
                    .prev_skip(*self._all_s_poses, exclude=self._all_s_exclude)
                    .text
                )
            )

            # 예외 6
            available = available and not self._check_next_is_unavailable_split()

        return available

    def _etm(self) -> bool:
        """
        Check whether the given syllable is split end point or not.

        Returns:
            bool: whether the given syllable is split end point or not.

        Notes:
            관형형 전성어미 분할 규칙:
                관형형 전성어미(ETM)인 형태소의 마지막 문자이면 다음 허용항을 만족하면 분할한다.
                이는 관형형 전성어미가 종결형으로 사용 될 경우에 대응 하기 위함이다. (~다능, ~했다던... 등)
                단, 현재 형태소에 조사(J*) 및 접미사(XS*) 성분이 포함되면 분할하지 않는다.

            허용:
                1. 이전 문자가 '다' 이면서 현재 문자가 '능'이면 분할한다.
                2. 현재 문자 뒤의 공백(SP)을 제외한 다음 문자가 말줄임표(SE)이면 분할한다.

            예외:
                1. 현재 문자의 뒤의 공백(SP) 및 대부분 부호를 제외한 다음 문자가 쉼표(,)이면 분할하지 않는다. 단 ,,과 같이 연속되어 쓰이면 분할을 허용한다.
                2. 현재 문자 뒤의 공백(SP) 및 대부분의 부호를 제외한 다음 문자가 의존명사(NNB)이면 분할하지 않는다.
                3. 현재 문자 뒤의 공백(SP)을 제외한 다음 문자가 조사(J*)이면 분할하지 않는다.
                4. 현재 문자 뒤로 등장하는 한글 문자열이 몇가지 분할하지 않아야 하는 경우에 속하면 분할하지 않는다.
        """
        available = False
        permission = False

        if self._check_pos(
            "ETM", exclude=("+J", "XS")
        ) and not self._check_next_skip_sp_pos("ETM"):
            # 예외 1
            available = not self._check_non_doubled_comma()

            # 예외 2
            available = available and not self._check_next_skip_all_s_pos("NNB")

            # 예외 3
            available = available and not self._check_next_skip_sp_pos(
                "J", exclude=("MAJ", "EMOJI", "JAMO", "+J")
            )

            # 예외 4
            available = available and not self._check_next_is_unavailable_split()

        if available:
            # 허용 1
            permission = self._check_prev_texts("다능")

            # 허용 2
            permission = permission or self._check_next_skip_sp_pos("SE")

        return available and permission

    def _char(self):
        """
        Check whether the given syllable is split end point or not.

        Returns:
            bool: whether the given syllable is split end point or not.

        Notes:
            캐릭터 기반의 휴리스틱 분할 규칙:
                캐릭터 기반의 문장분리 휴리스틱 알고리즘 적용한다.

            허용:
                듯 규칙 1. 현재 문자가 의존명사(NNB)이면서 '듯'이고 공백(SP) 종결부호(SF)를 제외한 다음 문자가 한글 자모(JAMO), 이모지(EMOJI), 말 줄임표(SE)
                        중 하나이면 현재 문자 뒤로 이어지는 모든 자모(JAMO) 및 이모지(EMOJI) 뒤의 문자가 동사가 아닌 경우 분할한다.
        """

        # 듯 규칙 1.
        if (
            self._check_text("듯")
            and self._check_pos("NNB")
            and (
                self._check_next_skip_spsf_pos(("EMOJI", "JAMO"))
                or self._check_next_skip_spsf_text("…")
            )
        ):
            _next = self.syllable.next_skip("SP")
            while not _next.check_pos("JAMO", "EMOJI"):
                _next = _next.next_skip("SP")
            if not _next.check_pos("VV"):
                return True

        return False

    #####################
    # Utility functions #
    #####################

    @staticmethod
    def _tuple(exclude):
        if isinstance(exclude, str):
            exclude = (exclude,)
        return exclude

    @lru_cache(1)
    def _prev(self):
        return self.syllable.prev

    @lru_cache(1)
    def _next(self):
        return self.syllable.next

    @lru_cache(30)
    def _prev_skip(
        self,
        poses=None,
        exclude=None,
    ):
        return self.syllable.prev_skip(
            *self._tuple(poses),
            exclude=self._tuple(exclude),
        )

    @lru_cache(30)
    def _next_skip(
        self,
        poses=None,
        exclude=None,
    ):
        return self.syllable.next_skip(
            *self._tuple(poses),
            exclude=self._tuple(exclude),
        )

    @lru_cache(30)
    def _check_pos(
        self,
        poses=None,
        exclude=None,
    ):
        return self.syllable.check_pos(
            *self._tuple(poses),
            exclude=self._tuple(exclude),
        )

    @lru_cache(30)
    def _check_text(
        self,
        texts=None,
        exclude=None,
    ):
        return self.syllable.check_text(
            *self._tuple(texts),
            exclude=self._tuple(exclude),
        )

    @lru_cache(30)
    def _check_next_pos(
        self,
        poses=None,
        exclude=None,
    ):
        return self.syllable.next.check_pos(
            *self._tuple(poses),
            exclude=self._tuple(exclude),
        )

    @lru_cache(30)
    def _check_prev_pos(
        self,
        poses=None,
        exclude=None,
    ):
        return self.syllable.prev.check_pos(
            *self._tuple(poses),
            exclude=self._tuple(exclude),
        )

    @lru_cache(30)
    def _check_next_text(
        self,
        texts=None,
        exclude=None,
    ):
        return self.syllable.next.check_text(
            *self._tuple(texts),
            exclude=self._tuple(exclude),
        )

    @lru_cache(30)
    def _check_prev_text(
        self,
        texts=None,
        exclude=None,
    ):
        return self.syllable.prev.check_text(
            *self._tuple(texts),
            exclude=self._tuple(exclude),
        )

    @lru_cache(30)
    def _check_next_skip_pos(
        self,
        poses=None,
        exclude=None,
        skip=None,
        skip_exclude=None,
    ):
        return self.syllable.next_skip(
            *self._tuple(skip),
            exclude=self._tuple(skip_exclude),
        ).check_pos(
            *self._tuple(poses),
            exclude=self._tuple(exclude),
        )

    @lru_cache(30)
    def _check_prev_skip_pos(
        self,
        poses=None,
        exclude=None,
        skip=None,
        skip_exclude=None,
    ):
        return self.syllable.prev_skip(
            *self._tuple(skip),
            exclude=self._tuple(skip_exclude),
        ).check_pos(
            *self._tuple(poses),
            exclude=self._tuple(exclude),
        )

    @lru_cache(30)
    def _check_next_skip_text(
        self,
        texts=None,
        exclude=None,
        skip=None,
        skip_exclude=None,
    ):
        return self.syllable.next_skip(
            *self._tuple(skip),
            exclude=self._tuple(skip_exclude),
        ).check_text(
            *self._tuple(texts),
            exclude=self._tuple(exclude),
        )

    @lru_cache(30)
    def _check_prev_skip_text(
        self,
        texts=None,
        exclude=None,
        skip=None,
        skip_exclude=None,
    ):
        return self.syllable.prev_skip(
            *self._tuple(skip),
            exclude=self._tuple(skip_exclude),
        ).check_text(
            *self._tuple(texts),
            exclude=self._tuple(exclude),
        )

    @lru_cache(30)
    def _check_next_skip_sp_pos(
        self,
        poses=None,
        exclude=None,
    ):
        return self.syllable.next_skip("SP").check_pos(
            *self._tuple(poses),
            exclude=self._tuple(exclude),
        )

    @lru_cache(30)
    def _check_next_skip_from_current_pos(
        self,
        poses=None,
        exclude=None,
    ):
        return self.syllable.next_skip_from_current("SP").check_pos(
            *self._tuple(poses),
            exclude=self._tuple(exclude),
        )

    @lru_cache(30)
    def _check_prev_skip_sp_pos(
        self,
        poses=None,
        exclude=None,
    ):
        return self.syllable.prev_skip("SP").check_pos(
            *self._tuple(poses),
            exclude=self._tuple(exclude),
        )

    @lru_cache(30)
    def _check_next_skip_spsf_pos(
        self,
        poses=None,
        exclude=None,
    ):
        return self.syllable.next_skip("SP", "SF").check_pos(
            *self._tuple(poses),
            exclude=self._tuple(exclude),
        )

    @lru_cache(30)
    def _check_prev_skip_spsf_pos(
        self,
        poses=None,
        exclude=None,
    ):
        return self.syllable.prev_skip("SP", "SF").check_pos(
            *self._tuple(poses),
            exclude=self._tuple(exclude),
        )

    @lru_cache(30)
    def _check_next_skip_sp_text(
        self,
        texts=None,
        exclude=None,
    ):
        return self.syllable.next_skip("SP").check_text(
            *self._tuple(texts),
            exclude=self._tuple(exclude),
        )

    @lru_cache(30)
    def _check_prev_skip_sp_text(
        self,
        texts=None,
        exclude=None,
    ):
        return self.syllable.prev_skip("SP").check_text(
            *self._tuple(texts),
            exclude=self._tuple(exclude),
        )

    @lru_cache(30)
    def _check_next_skip_spsf_text(
        self,
        texts=None,
        exclude=None,
    ):
        return self.syllable.next_skip("SP", "SF").check_text(
            *self._tuple(texts),
            exclude=self._tuple(exclude),
        )

    @lru_cache(30)
    def _check_prev_skip_spsf_text(
        self,
        texts=None,
        exclude=None,
    ):
        return self.syllable.prev_skip("SP", "SF").check_text(
            *self._tuple(texts),
            exclude=self._tuple(exclude),
        )

    @lru_cache(30)
    def _check_next_skip_all_s_pos(
        self,
        poses=None,
        exclude=None,
    ):
        return self.syllable.next_skip(
            *self._all_s_poses,
            exclude=self._all_s_exclude,
        ).check_pos(
            *self._tuple(poses),
            exclude=self._tuple(exclude),
        )

    @lru_cache(30)
    def _check_next_skip_all_s_text(
        self,
        texts=None,
        exclude=None,
    ):
        return self.syllable.next_skip(
            *self._all_s_poses,
            exclude=self._all_s_exclude,
        ).check_text(
            *self._tuple(texts),
            exclude=self._tuple(exclude),
        )

    @lru_cache(30)
    def _check_texts(self, texts=None):
        return self.syllable.check_texts(*self._tuple(texts))

    @lru_cache(30)
    def _check_prev_texts(self, texts=None):
        return self.syllable.prev.check_texts(*self._tuple(texts))

    @lru_cache(30)
    def _check_next_skip_all_s_texts(self, texts=None):
        return self.syllable.next_skip_from_current(
            *self._all_s_poses,
            exclude=self._all_s_exclude,
        ).check_texts(*self._tuple(texts))

    @lru_cache(30)
    def _check_next_skip_all_s_multiple_texts(self, *texts):
        next_skip_all_s = self.syllable.next_skip(
            *self._all_s_poses,
            exclude=self._all_s_exclude,
        )

        for text in texts:
            if next_skip_all_s.check_texts(*self._tuple(text)):
                return True

        return False

    @lru_cache(1)
    def _check_next_is_unavailable_split(self):
        return self._check_next_skip_all_s_multiple_texts(*self.unavailable_next)

    @lru_cache(1)
    def _check_non_doubled_comma(self):
        next_all_s = self._next_skip(self._all_s_poses, exclude=self._all_s_exclude)
        return next_all_s.check_text(",") and not next_all_s.next_skip("SP").check_text(
            ","
        )

    @lru_cache(30)
    def _check_prev_texts_from_before(self, text):
        _prev = self.syllable
        for _ in text:
            _prev = _prev.prev

        return _prev.check_texts(text)

    @lru_cache(30)
    def _check_multiple_prev_texts_from_before(self, *texts):
        return any(self._check_prev_texts_from_before(t) for t in texts)

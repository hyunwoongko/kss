# Copyright (C) 2021 Hyunwoong Ko <kevin.ko@tunib.ai> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.

from kss._utils.const import (
    faces,
    alphabet_with_quotes,
    number_with_quotes,
    number_with_bracket,
    backup_etc,
)


class SentenceProcessor:
    _all_s_exclude = ("QTO",)
    _all_s_poses = ("SP", "SF", "SY", "SE", "SSC", "QTC", "QTN", "EMOJI")
    _all_s_poses_wo_qtn = ("SP", "SF", "SY", "SE", "SSC", "QTC", "EMOJI")

    _backup_strings = set()
    _backup_strings.update(faces)
    _backup_strings.update(alphabet_with_quotes)
    _backup_strings.update(number_with_quotes)
    _backup_strings.update(number_with_bracket)
    _backup_strings.update(backup_etc)

    _backup = {k: str(abs(hash(k))) for k in _backup_strings}
    _restore = {v: k for k, v in _backup.items()}

    @staticmethod
    def _replace(text: str, purpose_dict: dict):
        for k, v in purpose_dict.items():
            text = text.replace(k, v)
        return text

    def backup(self, text: str):
        return self._replace(text=text, purpose_dict=self._backup)

    def restore(self, text: str):
        return self._replace(text=text, purpose_dict=self._restore)
# Copyright (C) 2021 Hyunwoong Ko <kevin.ko@tunib.ai> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.
import re
from functools import lru_cache

from kss._utils.const import (
    alphabet_with_quotes,
    numbers_with_quotes,
    url_pattern,
    email_pattern,
    backup_normal,
)


class SentenceProcessor:
    _all_s_exclude = ("QTO",)
    _all_s_poses = ("SP", "SF", "SY", "SE", "SSC", "QTC", "QTN", "EMOJI", "JAMO")
    _all_s_poses_wo_qtn = ("SP", "SF", "SY", "SE", "SSC", "QTC", "EMOJI", "JAMO")

    _heavy_backup = {}
    _heavy_backup.update(
        {
            k: {_v: str(abs(hash(_v))) for _v in v}
            for k, v in numbers_with_quotes.items()
        }
    )
    _heavy_backup.update(
        {
            k: {_v: str(abs(hash(_v))) for _v in v}
            for k, v in alphabet_with_quotes.items()
        }
    )
    _normal_backup = {k: str(abs(hash(k))) for k in sorted(backup_normal)}

    @staticmethod
    def _replace(text: str, purpose_dict: dict, restore: bool = False):
        for k, v in purpose_dict.items():
            if restore is True:
                source, target = v, k
            else:
                source, target = k, v

            if source in text:
                text = text.replace(source, target)

        return text

    def _add_url_or_email(self, text):
        _url_or_email = {
            k: str(abs(hash(k)))
            for k in re.findall(url_pattern, text) + re.findall(email_pattern, text)
        }
        self._normal_backup.update(_url_or_email)

    def _backup_or_restore_heavy(self, target: str, check: str, restore: bool = False):
        for source, purpose_dict in self._heavy_backup.items():
            if source in check:
                target = self._replace(target, purpose_dict, restore=restore)
        return target

    @lru_cache(100)
    def backup(self, inputs: str):
        self._add_url_or_email(inputs)
        inputs = self._replace(inputs, self._normal_backup)
        inputs = self._backup_or_restore_heavy(inputs, inputs)
        return inputs

    @lru_cache(100)
    def restore(self, outputs: str, inputs: str):
        outputs = self._replace(outputs, self._normal_backup, restore=True)
        outputs = self._backup_or_restore_heavy(outputs, inputs, restore=True)
        return outputs

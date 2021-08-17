"""
bi-gram connection cost data from mecab

Reference: matrix.def
"""

import gzip
import pickle


class ConnectionCosts(object):
    """bi-gram connection cost data 를 관리하는 클래스."""

    @staticmethod
    def open(KNOWN_PATH):
        with gzip.open(KNOWN_PATH, "rb") as rf:
            entries = pickle.load(rf)

        if len(entries) == 0:
            return None
        else:
            return ConnectionCosts(entries)

    def __init__(self, total_entries):
        self.conCosts = total_entries  # 딕셔너리 타입 저장.

    def get(self, rightId, leftId):
        return self.conCosts[int(rightId)][int(leftId)]

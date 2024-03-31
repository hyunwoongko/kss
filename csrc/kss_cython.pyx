# Copyright (C) 2021 Hyunwoong Ko <kevin.brain@kakaobrain.com> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.

from libcpp.string cimport string
from libcpp.vector cimport vector

from typing import List

cdef extern from "csrc/sentence_splitter.h":
    vector[string] splitSentences(string)

def split_sentences_fast(str, **kwargs) -> List[str]:
    results = []
    # Convert Python's `bytes` to C++'s `std::string`.
    res = splitSentences(str.encode('utf-8'))
    for r in res:
        results.append(r.decode('utf-8'))

    return results
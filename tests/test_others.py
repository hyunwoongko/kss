#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from koalanlp import API
from koalanlp.Util import initialize, finalize
from koalanlp.proc import SentenceSplitter
from tqdm import tqdm

import kss

cases = open("test_uoneway.txt", "r").read().splitlines()
okt_cnt, hnn_cnt, kss_cpp_cnt = 0, 0, 0
okt_results, hnn_results, kss_cpp_results = [], [], []
initialize(OKT="LATEST", HNN="LATEST")

okt = SentenceSplitter(API.OKT)
hnn = SentenceSplitter(API.HNN)

for case in tqdm(cases):
    kss_cpp_result = kss.split_sentences(case)
    okt_result = okt(case)
    hnn_result = hnn(case)

    if len(kss_cpp_result) == 1:
        kss_cpp_cnt += 1
    else:
        kss_cpp_results.append(kss_cpp_result)

    if len(okt_result) == 1:
        okt_cnt += 1
    else:
        okt_results.append(okt_result)

    if len(hnn_result) == 1:
        hnn_cnt += 1
    else:
        hnn_results.append(hnn_result)

print(f"`kss cpp` error rate : {1 - (kss_cpp_cnt / len(cases))}")
print(f"`okt` error rate : {1 - (okt_cnt / len(cases))}")
print(f"`hnn` error rate : {1 - (hnn_cnt / len(cases))}")
print()

finalize()

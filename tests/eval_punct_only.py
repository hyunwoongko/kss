from koalanlp import API
from koalanlp.Util import initialize, finalize
from koalanlp.proc import SentenceSplitter
from tqdm import tqdm

import kss


def eval_punc_only_kss3():
    cases = open("test_uoneway.txt", "r").read().splitlines()
    nori_cnt, mecab_cnt = 0, 0
    nori_results, mecab_results = [], []

    mecab_available = False
    try:
        from mecab import MeCab  # noqa

        mecab_available = True
    except ImportError:
        pass

    for result in kss.split_sentences(cases, backend="pynori", use_heuristic=False):
        if len(result) != 1:
            nori_cnt += 1
            nori_results.append(result)

    if mecab_available:
        for result in kss.split_sentences(cases, backend="mecab", use_heuristic=False):
            if len(result) != 1:
                mecab_cnt += 1
                mecab_results.append(result)

    print(f"`pynori` error rate : {(nori_cnt / len(cases))}")
    print(f"`mecab` error rate : {(mecab_cnt / len(cases))}")
    print()

    print("pynori wrong segmentation:")
    for i in nori_results:
        print(i)
    print()

    print("mecab wrong segmentation:")
    for i in mecab_results:
        print(i)
    print()


def eval_punct_only_previous_kss():
    """
    (1) 2.5.1 test
        - pip install kss==2.5.1
        - run this function
    """
    cases = open("test_uoneway.txt", "r").read().splitlines()

    cnt = 0
    for case in tqdm(cases):
        result = kss.split_sentences(case, safe=True)
        # option named `safe` is old name of `use_heuristic`.

        if len(result) == 1:
            cnt += 1

    print(f"`prev version of kss` error rate : {1 - (cnt / len(cases))}")


def eval_punct_only_koalanlp():
    cases = open("test_uoneway.txt", "r", encoding="utf-8").read().splitlines()
    okt_cnt, hnn_cnt = 0, 0
    initialize(OKT="LATEST", HNN="LATEST")

    okt = SentenceSplitter(API.OKT)
    hnn = SentenceSplitter(API.HNN)

    for case in tqdm(cases):
        okt_result = okt(case)
        hnn_result = hnn(case)

        if len(okt_result) == 1:
            okt_cnt += 1

        if len(hnn_result) == 1:
            hnn_cnt += 1

    print(f"`okt` error rate : {1 - (okt_cnt / len(cases))}")
    print(f"`hnn` error rate : {1 - (hnn_cnt / len(cases))}")
    print()

    finalize()


if __name__ == "__main__":
    eval_punc_only_kss3()

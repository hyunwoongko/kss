from tqdm import tqdm
import kss


def eval_open_ended_kss3():
    cases = open("test_uoneway.txt", "r").read().splitlines()
    nori_cnt, mecab_cnt = 0, 0
    nori_results, mecab_results = [], []

    mecab_available = False
    try:
        from mecab import MeCab  # noqa

        mecab_available = True
    except ImportError:
        pass

    for result in kss.split_sentences(cases, backend="pynori"):
        if len(result) != 1:
            nori_cnt += 1
            nori_results.append(result)

    if mecab_available:
        for result in kss.split_sentences(cases, backend="mecab"):
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


def eval_open_ended_previous_kss():
    """
    (1) 1.3.1 test
        - pip install kss==1.3.1
        - run this function

    (2) 2.5.1 test
        - pip install kss==2.5.1
        - run this function
    """
    cases = open("test_uoneway.txt", "r").read().splitlines()

    cnt = 0
    for case in tqdm(cases):
        result = kss.split_sentences(case)

        if len(result) == 1:
            cnt += 1

    print(f"`prev version of kss` error rate : {1 - (cnt / len(cases))}")


if __name__ == "__main__":
    eval_open_ended_kss3()

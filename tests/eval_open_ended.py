from tqdm import tqdm
import kss


def eval_open_ended_kss3():
    cases = open("test_uoneway.txt", "r").read().splitlines()
    nori_cnt, mecab_cnt, nm_cnt = 0, 0, 0
    nori_results, mecab_results, nm_results = [], [], []

    mecab_available = False
    try:
        from mecab import MeCab  # noqa

        mecab_available = True
    except ImportError:
        pass

    for case in tqdm(cases):
        nori_result = kss.split_sentences(case, backend="pynori")
        non_morpheme_results = kss.split_sentences(case, backend="none")

        if len(nori_result) == 1:
            nori_cnt += 1
        else:
            nori_results.append(nori_result)

        if len(non_morpheme_results) == 1:
            nm_cnt += 1
        else:
            nm_results.append(non_morpheme_results)

        if mecab_available:
            mecab_result = kss.split_sentences(case, backend="mecab")

            if len(mecab_result) == 1:
                mecab_cnt += 1
            else:
                mecab_results.append(mecab_result)

    print(f"`pynori` error rate : {1 - (nori_cnt / len(cases))}")
    print(f"`mecab` error rate : {1 - (mecab_cnt / len(cases))}")
    print(f"`none` error rate : {1 - (nm_cnt / len(cases))}")
    print()

    print("pynori wrong segmentation:")
    for i in nori_results:
        print(i)
    print()

    print("mecab wrong segmentation:")
    for i in mecab_results:
        print(i)
    print()

    print("non-morpheme wrong segmentation:")
    for i in nm_results:
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

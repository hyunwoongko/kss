from time import time

import kss


def test_nori_versus_mecab():
    text = open("tests/test_sooftware.txt", "r", encoding="utf-8").read()

    start = time()
    output = kss.split_sentences(text, backend="pynori")
    print(time() - start)  # 1.012695074081421

    start = time()
    output = kss.split_sentences(text, backend="none")
    print(time() - start)  # 0.28556394577026367

    start = time()
    output = kss.split_sentences(text, backend="mecab")
    print(time() - start)  # 0.30152297019958496


if __name__ == "__main__":
    test_nori_versus_mecab()

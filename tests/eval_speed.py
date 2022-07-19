import gc
from time import time
import matplotlib.pyplot as plt
from kss import split_sentences


def draw(nori_mp, nori_non_mp, mecab_mp, mecab_non_mp, none_mp, none_non_mp):
    plt.plot(none_mp, "lime", label="multi processing (none)")
    plt.plot(none_non_mp, "forestgreen", label="serial processing (none)")
    plt.plot(mecab_mp, "red", label="multi processing (mecab)")
    plt.plot(mecab_non_mp, "brown", label="serial processing (mecab)")
    plt.plot(nori_mp, "cyan", label="multi processing (pynori)")
    plt.plot(nori_non_mp, "deepskyblue", label="serial processing (pynori)")

    plt.legend(loc="upper left")
    plt.xlabel("The number of data")
    plt.ylabel("Seconds")
    plt.title("Kss performance")
    plt.grid(True, which="both", axis="both")
    plt.savefig("assets/performance-of-mp.png")
    plt.close()


def split_sentences_(text, workers, backend, name):
    t = time()
    out = split_sentences(text, num_workers=workers, backend=backend)
    print(f"{name}: time={time() - t}, worker={workers}, out={out}")
    return out, time() - t


def mp_versus_non_mp(i, _input, backend):
    non_mp = split_sentences_(_input, num_workers, backend, f"{backend}-non-mp")
    use_mp = split_sentences_(_input, num_workers * -1, backend, f"{backend}-use-mp")
    print(f"{i}: output is {'same' if non_mp[0] == use_mp[0] else 'different'}.")
    assert non_mp[0] == use_mp[0], "output is difference !!"
    return non_mp[1], use_mp[1]


if __name__ == "__main__":
    num_workers = 1
    nori_mp, nori_non_mp = [], []
    mecab_mp, mecab_non_mp = [], []
    none_mp, none_non_mp = [], []

    for i in range(1, 101):
        input_text = """『분단국의 방송 교류』는 저자가 1997년 이래로 발표한 논문을 중심으로 집필되었다. 독일에서 1996년에 "분단 독일의 TV－동서독 방송 이데올로기 경쟁과 방송 교류(Das Fernsehen im geteilten Deutschland 1952∼1989)"라는 주제로 박사학위를 받고 귀국해 당시 방송개발원에서 학문을 업으로 삼아 연구자의 삶을 시작했다. 박사논문 때문인지 나에게 주어진 연구 프로젝트는 북한 방송이나 남북 방송 교류에 관한 것이었다. 그러다보니 자의반, 타의반 이 분야와 8년 동안 인연을 맺어왔다."""
        gc.disable()

        output = mp_versus_non_mp(i, [input_text] * i, backend="none")
        none_non_mp.append(output[0])
        none_mp.append(output[1])

        output = mp_versus_non_mp(i, [input_text] * i, backend="pynori")
        nori_non_mp.append(output[0])
        nori_mp.append(output[1])

        output = mp_versus_non_mp(i, [input_text] * i, backend="mecab")
        mecab_non_mp.append(output[0])
        mecab_mp.append(output[1])

        gc.enable()
        draw(nori_mp, nori_non_mp, mecab_mp, mecab_non_mp, none_mp, none_non_mp)
        print()

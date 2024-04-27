import hangul_jamo
import jamo

from kss import Kss


def test_h2j():
    h2j = Kss("h2j")
    text = "한글"
    output = h2j(text)
    assert output == jamo.h2j(text)


def test_h2hcj():
    h2hcj = Kss("h2hcj")
    text = "한글"
    output = h2hcj(text)
    assert output == hangul_jamo.decompose(text)


def test_j2h():
    j2h = Kss("j2h")
    text = jamo.h2j("한글")
    output = j2h(text)
    assert output == "한글"


def test_j2hcj():
    j2hcj = Kss("j2hcj")
    text = jamo.h2j("한글")
    output = j2hcj(text)
    assert output == hangul_jamo.decompose("한글")


def test_hcj2j():
    hcj2j = Kss("hcj2j")
    text = "ㅎ"
    output = hcj2j(text)
    assert output == jamo.h2j("ㅎ")


def test_hcj2h():
    hcj2h = Kss("hcj2h")
    text = hangul_jamo.decompose("한글")
    output = hcj2h(text)
    assert output == "한글"


if __name__ == '__main__':
    test_h2j()
    test_h2hcj()
    test_j2h()
    test_j2hcj()
    test_hcj2j()
    test_hcj2h()

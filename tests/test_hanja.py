from kss import Kss


def test_split_hanja():
    split_hanja = Kss("split_hanja")
    text = "大韓民國은 民主共和國이다."
    output = split_hanja(text)
    assert output == ["大韓民國", "은 ", "民主共和國", "이다."]


def test_is_hanja():
    is_hanja = Kss("is_hanja")
    text = "大"
    output = is_hanja(text)
    assert output is True
    text = "대"
    output = is_hanja(text)
    assert output is False


def test_hanja2hangul():
    hanja2hangul = Kss("hanja2hangul")
    text = "大韓民國은 民主共和國이다."
    output = hanja2hangul(text)
    assert output == "대한민국은 민주공화국이다."


if __name__ == '__main__':
    test_split_hanja()
    test_is_hanja()
    test_hanja2hangul()

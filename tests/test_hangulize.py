from kss import Kss


def test_hangulize():
    hangulize = Kss("hangulize")
    text = "Giro d'Italia"
    output = hangulize(text, lang="ita")
    assert output == "지로 디탈리아"


if __name__ == '__main__':
    test_hangulize()

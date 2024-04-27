from kss import Kss


def test_g2p():
    g2p = Kss("g2p")
    text = "어제는 맑았는데 오늘은 흐리다."
    output = g2p(text)
    assert output == "어제는 말간는데 오느른 흐리다."


if __name__ == '__main__':
    test_g2p()

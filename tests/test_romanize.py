from kss import Kss


def test_romanize():
    romanize = Kss("romanize")
    text = "안녕하세요"
    output = romanize(text)
    assert output == 'annyeonghaseyo'
    text = "대관령"
    output = romanize(text)
    assert output == 'daegwallyeong'

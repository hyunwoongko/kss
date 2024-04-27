from kss import Kss


def test_correct_spacing():
    correct_spacing = Kss("correct_spacing")
    text = "아버지가방에들어가시다"
    output = correct_spacing(text)
    assert output == '아버지가 방에 들어가시다'

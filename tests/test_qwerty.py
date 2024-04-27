from kss import Kss


def test_qwerty():
    qwerty = Kss("qwerty")
    text = "dkssudgktpdy"
    output = qwerty(text, src="en", tgt="ko")
    assert output == '안녕하세요'
    text = "안녕하세요"
    output = qwerty(text, src="ko", tgt="en")
    assert output == 'dkssudgktpdy'

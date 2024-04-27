from kss import Kss


def test_is_unsafe():
    is_unsafe = Kss("is_unsafe")
    text = "안녕하세요"
    assert is_unsafe(text) is False
    text = "안녕하세요. 씨발"
    assert is_unsafe(text) is True
    text = "안녕하세요. 씨발"
    assert is_unsafe(text, return_matches=True) == ['씨발']

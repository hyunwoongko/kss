import pytest

from kss import split_sentences


@pytest.mark.parametrize("backend", ["pecab", "punct"])
@pytest.mark.parametrize("whitespace", [" ", "  ", "\t", "\n", "\r\n"])
def test_preserve_whitespace_after_merged_brackets(backend, whitespace):
    before = (
        "《SING FOR YOU》는 2015년 12월 16일 기준 초동 판매량 "
        "(음반 발매 첫 주의 판매량. 예약판매량은 포함되지 않는다.)"
    )
    after = "27만장을 돌파하였고, 이것은 역대 초동 판매량 1위에 기록되었다."
    text = before + whitespace + after
    sentences = split_sentences(text, backend=backend, strip=False, num_workers=1)

    assert "".join(sentences) == text
    assert all(sentence.strip() for sentence in sentences)
    assert [sentence.strip() for sentence in sentences] == [before, after]
    assert split_sentences(text, backend=backend, strip=True, num_workers=1) == [
        sentence.strip() for sentence in sentences
    ]


@pytest.mark.parametrize("backend", ["pecab", "punct"])
def test_preserve_text_following_closing_bracket_in_same_sentence(backend):
    text = "첫 문장이다. (괄호 안 문장이다. 두 번째 문장이다.) 다음 문장이다."
    sentences = split_sentences(text, backend=backend, strip=False, num_workers=1)

    assert "".join(sentences) == text
    assert all(sentence.strip() for sentence in sentences)

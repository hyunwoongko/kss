from kss import Kss


def test_split_sentences():
    split_sentences = Kss("split_sentences")
    text = "회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요 다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다 강남역 맛집 토끼정의 외부 모습."
    output = split_sentences(text)
    assert output == ['회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요',
                      '다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다',
                      '강남역 맛집 토끼정의 외부 모습.']

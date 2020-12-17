import unittest
import kss


class KssTest(unittest.TestCase):

    def test_split(self):
        text = "회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요 다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다 강남역 맛집 토끼정의 외부 모습."
        splitted = kss.split_sentences(text)
        self.assertEqual(len(splitted), 3)

    def test_single_quotes(self):
        text = """여당이 내놓은 상가건물 임대차보호법 개정안, 이른바 ‘임대료 멈춤법’에 대한 논의가 급물살을 타면서 자영업자들과 임대인의 의견이 팽팽하게 맞서고 있다. 신종 코로나바이러스 감염증(코로나19) 확진자 급증세로 집합 제한·집합 금지 기간이 길어지면서 한계에 직면한 소상공인과 자영업자들 사이에서는 임대료 부담을 호소하며 "법안을 조속히 시행해 달라"는 목소리가 터져나오고 있다. 반면 임대인들은 임대료 인하를 강제화하는 것은 부당하다며 정부와 여당이 ‘나쁜 임대인(건물주)’ 프레임을 만들고 있다고 비판했다. 업계 전문가들 사이에서도 우려의 목소리가 여럿 있다. 재산권 침해 소지가 있고, 월세 수익이 끊기면 생활이 곤란해지는 ‘생계형 임대인’들이 피해를 볼 수 있는 등 또 다른 부작용이 발생할 수 있다는 것이다. 법 개정 자체만으로 상가 거래 시장이 위축될 가능성도 지적됐다."""
        splitted = kss.split_sentences(text)
        self.assertEqual(len(splitted), 6)

    def test_quote_misalignment(self):
        # testcase from https://github.com/likejazz/korean-sentence-splitter/issues/8
        text = """부부 싸움 규칙 가운데 ‘돈 히트 언더 더 벨트’(Don’t hit under the belt)가 있다. 권투할 때 벨트 아래를 치면 반칙이듯이, 상대가 너무 아파할 만한 것을 건드리면 회복하기 어렵다. 그 부분은 사람마다 다르다."""
        splitted = kss.split_sentences(text)
        self.assertEqual(len(splitted), 3)

        text = """안녕하십니까? 삼성전자가 11월 13일 삼성전자 서초사옥 다목적홀 5층에서 진행되는 2013 S'데이 멤버십 블루 강연회 "Challenge BLUE, 박찬호&이동우의 삶과 도전" 멤버십 블루 고객 480명을 초청한다.강연회는 삼성전자 멤버십 블루 회원들을 위해 마련된 고객 혜택 행사로 한국인 최초의 메이저리거 박찬호와 시각장애 개그맨 이동우를 초청, 그들의 삶 속에서 펼쳐진 다양한 도전기를 들을 수 있도록 마련했다."""
        splitted = kss.split_sentences(text)
        self.assertEqual(len(splitted), 3)

        text = """삼성전자가 11월 13일 삼성전자 서초사옥 다목적홀 5층에서 진행되는 2013 S'데이 멤버십 블루 강연회 "Challenge BLUE, 박찬호&이동우의 삶과 도전" 멤버십 블루 고객 480명을 초청한다.강연회는 삼성전자 멤버십 블루 회원들을 위해 마련된 고객 혜택 행사로 한국인 최초의 메이저리거 박찬호와 시각장애 개그맨 이동우를 초청, 그들의 삶 속에서 펼쳐진 다양한 도전기를 들을 수 있도록 마련했다."""
        splitted = kss.split_sentences(text)
        self.assertEqual(len(splitted), 2)

        text = """삼성전자가 11월 13일 삼성전자 서초사옥 다목적홀 5층에서 진행되는 2013 S"데이 멤버십 블루 강연회 "Challenge BLUE, 박찬호&이동우의 삶과 도전" 멤버십 블루 고객 480명을 초청한다.강연회는 삼성전자 멤버십 블루 회원들을 위해 마련된 고객 혜택 행사로 한국인 최초의 메이저리거 박찬호와 시각장애 개그맨 이동우를 초청, 그들의 삶 속에서 펼쳐진 다양한 도전기를 들을 수 있도록 마련했다."""
        splitted = kss.split_sentences(text)
        self.assertEqual(len(splitted), 2)

        text = """삼성전자가 11월 13일 삼성전자 서초사옥 다목적홀 5층에서 진행되는 2013 S"데'이 멤버십 블루 강연회 "Challenge BLUE, 박찬호&이동우의 삶과 도전" 멤버십 블루 고객 480명을 초청한다.강연회는 삼성전자 멤버십 블루 회원들을 위해 마련된 고객 혜택 행사로 한국인 최초의 메이저리거 박찬호와 시각장애 개그맨 이동우를 초청, 그들의 삶 속에서 펼쳐진 다양한 도전기를 들을 수 있도록 마련했'다."""
        splitted = kss.split_sentences(text)
        self.assertEqual(len(splitted), 2)


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import unittest
from time import time
import kss


class KssTest(unittest.TestCase):
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

    def test_prime(self):
        text = 'TV산업은 1926년 흑백 TV 개발, 1954년 RCA사가 Color TV(21") 양산/판매를 시작한 이래로 트리니트론 브라운관(1967년), 완전평면 브라운관(1996년) 개발 등 기술적인 발전을 거듭해 왔으나, 주요 국가 보급률이 90%를 넘어서면서 브라운관 TV사업의 성장은 정체되었습니다. 그러나 Flat Panel TV(LCD, PDP) 출시, 디지털 방송 확산(영/미 1998년~ )을 통해 TV 시장은 성장 모멘텀을 되찾았으며, FPTV는 화질, 디자인 등 제품 성능 향상과 지속적인 Set가격 하락을 통해 성장을 지속하며 기존 CRT 시장을 빠르게 대체하였습니다. 또한 2010년 입체감을 느낄 수 있는 3D TV가 출시되었고, 2011년부터 2012년에 걸쳐 인터넷 동영상 서비스 업체들의 부상과 스마트기기에 대한 사용자들의 관심 확대로 스마트 TV 시장이 태동하였습니다. 2013년에는 화질 및 해상도가 혁신적으로 높아진 UHD TV, 2014년에는 새로운 Form Factor인 Curved TV가 출시되었으며 2015년에는 퀀텀닷TV가 상용화되는 등 TV 시장은 끊임없이 진화하였습니다.전체 TV 수요는 2017년 기준 2억 1,510만대 수준으로 LCD TV 수요가 2억 1천만대로 99% 이상의 시장 점유를 이어 나갔으며, OLED 수요는 159만대로 성장하였으나 비중은 0.7%로 영향이 미미하였습니다. 2018년도 전체 TV 수요는 2억 2,100만대 이상을 기록하며 전년 대비 2.9% 성장하였습니다. 최근 TV시장은 고해상도 대형화면에 대한 Needs가 지속적으로 증가하여, UHD TV는 전년비 26% 증가한 99.6백만대로 시장 비중 45% 수준이 될 전망이며, 60"이상 대형시장은 약 19.7백만대를 초과하여 전년비 35% 성장, 75"이상 초대형 시장도 당사의 판매 드라이브로 전년비 76% 이상 성장이 전망되고 있습니다.'
        splitted = kss.split_sentences(text)
        self.assertEqual(len(splitted), 7)

    def test_apostrophe(self):
        text = "그는 말했다. I'm good 괜찮아요. But He’s mind was broken."
        splitted = kss.split_sentences(text)
        self.assertEqual(len(splitted), 3)

    def test_jyo(self):
        text = "아무래도 그땐 그랬었죠 많이 힘들었으니까요 근데 이제는 괜찮아요 친구들이 많아졌어요 그때만 힘들었던거죠 이젠 괜찮아요"
        splitted = kss.split_sentences(text)
        self.assertEqual(len(splitted), 5)

    def test_EC_EF_cases(self):
        text = "국내에 판매하는 OEM 수입차의 판매량이 2017년까지 하락세를 보이다 지난해 반등했으며 수입차 대비 비중도 높아질 전망이다."
        splitted = kss.split_sentences(text)
        self.assertEqual(len(splitted), 1)

        text = "전과 8범 A씨는 지난 17일 전자발찌를 끊고 도주하다 붙잡혀 전자발찌 부착기간이 2020년 8월14일까지 늘었다."
        splitted = kss.split_sentences(text)
        self.assertEqual(len(splitted), 1)

        text = "국내에 판매하는 OEM 수입차의 판매량은 내년 보다 높아질 전망이다."
        splitted = kss.split_sentences(text)
        self.assertEqual(len(splitted), 1)

        text = "개그맨 김병만 씨가 아르바이트를 하다 목숨을 잃을 뻔한 사연을 TV조선 '별별톡쇼'에서 전했다."
        splitted = kss.split_sentences(text)
        self.assertEqual(len(splitted), 1)

        text = "그것은 맛이 좋다 그러나 너무 비싸다"
        splitted = kss.split_sentences(text)
        self.assertEqual(len(splitted), 2)

    def test_eomies(self):
        text = "부디 만수무강 하소서 그런데 어제 했던 이야기는 어찌됐소?"
        splitted = kss.split_sentences(text)
        self.assertEqual(len(splitted), 2)

        text = "그러게나 말이에유 참말로 힘들구먼유 안그래유?"
        splitted = kss.split_sentences(text)
        self.assertEqual(len(splitted), 3)

        text = "따뜻하게 입으니까 이렇게 좋잖아? 안그래?"
        splitted = kss.split_sentences(text)
        self.assertEqual(len(splitted), 2)

        text = "어제 밥 먹었었음 그런데 너무 맛있었음 알겠삼?"
        splitted = kss.split_sentences(text)
        self.assertEqual(len(splitted), 3)

        text = "그것이 참말로 거시기 했당께? 거 참 내가 두 눈으로 똑똑히 봤당께"
        splitted = kss.split_sentences(text)
        self.assertEqual(len(splitted), 2)

    def test_quotes(self):
        text = "연비테스트를 진행하면서 들었던 의문점인 ‘트립 컴퓨터 정보'에 대한 신뢰도 문제였다. 3대의 차량 모두 연료를 더 이상 들어가지 않을 때 까지 가득 주유한 뒤 193km를 이동했다."
        splitted = kss.split_sentences(text)
        self.assertEqual(len(splitted), 2)

        text = '우리 팀 촬영 PD는 “지금까지 탔던 차 중에 가장 편했다"라고 말했다. 이런 쉐슬람 같은! 아니다.'
        splitted = kss.split_sentences(text)
        self.assertEqual(len(splitted), 2)

        text = """한 시민은 "코로나로 인해 '2020년'이란 시간은 멈춘 듯 하다"고 말했다."""
        splitted = kss.split_sentences(text)
        self.assertEqual(len(splitted), 1)

    def test_from_jaehyeongan(self):
        text = open("code_example.txt", "r", encoding="utf-8").read()
        start = time()
        kss.split_sentences(text)
        print(time() - start)

        text = open("news_example.txt", "r", encoding="utf-8").read()
        start = time()
        kss.split_sentences(text)
        print(time() - start)

    def test_from_sooftware(self):
        text = open("test_sooftware.txt", "r", encoding="utf-8").read()
        start = time()
        out = kss.split_sentences(text, backend="mecab")
        print(out)
        print(time() - start)

        start = time()
        out = kss.split_chunks(text, max_length=256, backend="mecab")
        print(out)
        print(time() - start)

        start = time()
        out = kss.split_chunks(text, max_length=256, backend="mecab", overlap=True)
        print(out)
        print(time() - start)

    def test_fightnyy(self):
        text = open("test_sooftware.txt", "r", encoding="utf-8").read().splitlines()

        start = time()
        out = kss.split_sentences(text, backend="pynori")
        print(out)
        print(time() - start)

    def test_chunks(self):
        data = [
            "안녕하세요 \n 반가워요. 잘지냈어요? 저는 치킨이 먹고싶어요. 헤헤.",
            "전하 아니되옵니다. 부디 용서하옵소서. 소인이 큰 죄를 저질렀사옵니다.",
            "크리스마스에는 축복을. 크리스마스에는 사랑을 \n 아빠 힘내세요. 우리가 있잖아요.",
        ]

        out = kss.split_chunks(data, max_length=24)
        print(out)
        out = kss.split_chunks(data, max_length=12, overlap=True)
        print(out)

        out = kss.split_chunks(
            "전하 아니되옵니다. 부디 용서하옵소서. 소인이 큰 죄를 저질렀사옵니다.\n", max_length=24
        )
        print(out)
        out = kss.split_chunks(
            "전하 아니되옵니다. 부디 용서하옵소서. 소인이 큰 죄를 저질렀사옵니다.\n", max_length=6, overlap=True
        )
        print(out)

    def test_yjy2026(self):
        output = kss.split_sentences("1'1″")
        print(output)

    def test_hannabros(self):
        output = kss.split_sentences("분리 할 수 ​​있다.")
        print(output)

    def test_lifelongeek(self):
        text = "우리가 타이라는 단어는 원래 동사로 묶다 엮다라는 표현이고요 그다음에 명사로 하게 되면 묶음이라는 표현이죠 그런데"
        output_1 = kss.split_sentences(text)
        for i in range(500):
            output = kss.split_sentences("안녕")
        text = "우리가 타이라는 단어는 원래 동사로 묶다 엮다라는 표현이고요 그다음에 명사로 하게 되면 묶음이라는 표현이죠 그런데"
        output_2 = kss.split_sentences(text)
        print(output_1, output_2)
        # 음.. 뭘까 잘 되는데

    def test_newdboy(self):
        tst = "그것이 잘 적혀 있는지 확인해야 한다고 했기 때문이다. EBS 미래교육연구소 최홍규 박사도 그렇게 말했다"
        output = kss.split_sentences(text=tst, backend="mecab", use_heuristic=True)
        print(output)

    def test_use_quotes_brackets_processing(self):
        result = kss.split_sentences(
            "'서울에는 유명한 맛집이 정말 많습니다. 가장 인기 있는 것 중 하나인 빙수 미식가를 말씀드릴 수 있습니다.' 그의 말은 정말 맞았다.",
            use_quotes_brackets_processing=False,
        )
        assert len(result) == 2
        result = kss.split_sentences(
            "'서울에는 유명한 맛집이 정말 많습니다. 가장 인기 있는 것 중 하나인 빙수 미식가를 말씀드릴 수 있습니다.' 그의 말은 정말 맞았다.",
            use_quotes_brackets_processing=True,
        )
        print(result)
        assert len(result) == 1

    def test_emoji(self):
        test = "이모지가 어떻게 되나 테스트해봅시다. ❤️❤️하트입니다. 두 번째는 😊😊웃는얼굴입니다. 세 번째는 👍👍엄지입니다."
        print(f"input: {test}")
        print(f"mecab: {kss.split_sentences(test, backend='mecab')}")
        print(f"none: {kss.split_sentences(test, backend='none')}")
        print(f"pynori: {kss.split_sentences(test, backend='pynori')}")

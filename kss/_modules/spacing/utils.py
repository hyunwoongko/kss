# Copied from ko-prfrdr (https://github.com/ychoi-kr/ko-prfrdr)
# And modified by Hyunwoong Ko [https://github.com/hyunwoongko]

import re
from functools import reduce

CONSONANTS = "ㄱㄲㄳㄴㄵㄶㄷㄸㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅃㅄㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
FIRST_CONSONANTS = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
VOWELS = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
FINAL_CONSONANTS = "ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ"
comma_with_numbers = re.compile(r'(\d+), (\d+)')


def offset(c):
    return CONSONANTS.index(c) + 1


def join(seq):
    def join_two(a, b):
        if re.match(r'[가-히]', a[-1]) and not hasfinalconsonant(a[-1]) and b in CONSONANTS:
            return ''.join([a[:-1], chr(ord(a[-1]) + offset(b))])
        else:
            return ''.join([a, b])

    return reduce(join_two, seq)


def concat(*seq):
    def concat_two(a, b):
        if re.match(r"[ㄱ-ㅎ]", a[-1]) and re.match(r"[ㅏ-ㅣ]", b):
            # return chr(ord("가") + (ord(b) - ord("ㅏ")) * (len(FINAL_CONSONANTS) + 1))
            return "".join([
                a[:-1],
                chr(
                    ord("가")
                    + (FIRST_CONSONANTS.find(a[-1]) * len(VOWELS) * (len(FINAL_CONSONANTS) + 1))
                    + ((len(FINAL_CONSONANTS) + 1) * (ord(b) - ord("ㅏ")))
                )
            ])
        elif re.match("[가-히]", a[-1]) and not hasfinalconsonant(a[-1]) and b in CONSONANTS:
            return "".join([a[:-1], chr(ord(a[-1]) + FINAL_CONSONANTS.find(b) + 1)])
        else:
            return "".join([a, b])

    if len(seq) == 2 and seq[1] == "":
        return seq[0]
    else:
        return reduce(concat_two, seq)


def splitsound(s):
    ret = ""
    chars = [c for c in s]
    for c in chars:
        if re.match("[가-힣]", c):
            v = ord(c) - 0xAC00
            ret += FIRST_CONSONANTS[v // (28 * 21)]
            ret += VOWELS[v // 28 % 21]
            # ret += FINALC[v % 28]
            ret += ([""] + [c for c in FINAL_CONSONANTS])[v % 28]

        else:
            ret += c
    return ret


def hasfinalconsonant(c):
    return len(splitsound(c)) == 3


def joinseq(*seq):
    return "|".join(sorted(set(reduce(lambda x, y: x + y, [x.split("|") for x in seq]))))


def conjugate(stems, *postfix):
    result = []
    for rt in stems.split("|"):
        args = [rt] + list(postfix)
        result.append(concat(*args))
    return result


def monosyllables(psv):
    return "|".join([s for s in psv.split("|") if len(s) == 1])


KJ_CA = "으로서"
KJ_CB = "보다"
KJ_CC = "처럼"
KJ_CF = "의"
KJ_CG = "께|에게|한테"
KJ_CI = "이다|이어야|이었[다던]|인|인[가지][는도를에]?|일"
KJ_CK = "와|과|이[고면]|이랑|랑|하고|고"
KJ_CL = "게|에|에게|에서"
KJ_CM = "로|으로|으로써"
KJ_CO = "을|를"
KJ_CQ = "라고|고"
KJ_CS = "이|가"
KJ_CT = "로|에로|으로"
KJ_C = joinseq(KJ_CA, KJ_CB, KJ_CC, KJ_CF, KJ_CG, KJ_CI, KJ_CK, KJ_CL, KJ_CM, KJ_CO, KJ_CQ, KJ_CS, KJ_CT)
KJ_IA = "도"
KJ_IC = "은|는"
KJ_ID = "이란|란"
KJ_IE = "마다"
KJ_IM = "들"
KJ_IO = "라도|이라도"
KJ_IP = "요"
KJ_IR = "부터|까지[가도는를]?"
KJ_IU = "만"
KJ_I = joinseq(KJ_IA, KJ_IC, KJ_ID, KJ_IE, KJ_IM, KJ_IO, KJ_IP, KJ_IR, KJ_IU)
KJ = joinseq(KJ_C, KJ_I)
KE_ECa = "게\\b|지\\b|어\\b"  # Help auxiliary(보조)
KE_ECc = "고\\b|으며\\b|며\\b|지마는|지만"  # coordinate(대등)
KE_ECs = "리만치\\b|어야|[으]면|[으]므로"  # subordinate(종속)
KE_EC = joinseq(KE_ECa, KE_ECc, KE_ECs)
KE_EDa = "은\\b|ㄴ\\b|을\\b|ㄹ\\b"  # adnominal
KE_EDn = "기\\b|음\\b|ㅁ\\b"  # noun
KE_EDv = "도록|게\\b"  # adVerbial
KE_ED = joinseq(KE_EDa, KE_EDn, KE_EDv)
KE_EFE = "구나\\b|세\\b"  # exclamination
KE_EFO = "라\\b|거라\\b"  # order
KE_EFQ = "나\\b|니\\b|는가\\b"  # question
KE_EFR = "자\\b|세\\b"  # request
KE_EFS = "다\\b|습니다|야|이다"  # statement
KE_EF = joinseq(KE_EFE, KE_EFO, KE_EFQ, KE_EFR, KE_EFS)
KE_E = joinseq(KE_EC, KE_ED, KE_EF)
KE_P = "시|었|더|겠"
KE = joinseq(KE_E, KE_P)
_FIRST_ = 44032
KL_ALL = "".join(
    [
        chr(_FIRST_ + (len(VOWELS) * (len(FINAL_CONSONANTS) + 1) * i) + ((len(FINAL_CONSONANTS) + 1) * j) + k)
        for i in range(len(FIRST_CONSONANTS))
        for j in range(len(VOWELS))
        for k in range(len(FINAL_CONSONANTS) + 1)
    ]
)
KL_NFC = "".join(
    [
        chr(_FIRST_ + (len(VOWELS) * (len(FINAL_CONSONANTS) + 1) * i) + ((len(FINAL_CONSONANTS) + 1) * j))
        for i in range(len(FIRST_CONSONANTS))
        for j in range(len(VOWELS))
    ]
)
KL_WFC = "".join(sorted(set(KL_ALL) - set(KL_NFC)))
KL_WFS = "".join(sorted(set(KL_WFC) - set(["들"])))
KL_WFL = "".join([chr(ord(c) + 8) for c in KL_NFC])
KL_WFN = "".join([chr(ord(c) + 4) for c in KL_NFC])
KL_NFL = "".join(sorted(set(KL_WFC) - set(KL_WFL)))
KL_NFN = "".join(sorted(set(KL_WFC) - set(KL_WFN)))
KS_Aa = "나ㅃ|바ㅃ"  # +ㅏ지다       +ㅡ+다   +ㅡ+ㄹ  +ㅡ+ㄴ  +ㅏ서        +ㅡ+게  +ㅡ+지
KS_Ab = '가까|귀여|더|무서|쉬|즐거|차가|추|해로'  # +워지다       +ㅂ+다   +울     +운     +워서        +ㅂ+게  +ㅂ+지
KS_Ac = '많|맑|않|작|좁'  # +아지다       +다      +을     +은     +아서        +게     +지
KS_Ad = '다'  # sweet                   # +ㄹ+아지다    +ㄹ+다   +ㄹ     +ㄴ     +ㄹ+아서     +ㄹ+게  +ㄹ+지
KS_Ae = '예ㅃ|ㅋ'  # +ㅓ지다       +ㅡ+다   +ㅡ+ㄹ  +ㅡ+ㄴ  +ㅓ서        +ㅡ+게  +ㅡ+지
KS_Af = '다'  # different               # +ㄹ+라지다    +르+다   +를     +른     +ㄹ+라서     +르+게  +르+지
KS_Ag = '건장|날씬|능숙|바람직|비슷|스마트|심각|적[정합]|착|불길|미약|병약|심약|참신|상이|익숙|진부'
KS_Ah = '간[결단명략]|간단|건강|긴요|깔끔|딱딱|똑똑|멍청|명확|못마땅|부지런|상세|씩씩|원만|장렬|적[당절]|졸렬|지저분|침착|화려'
KS_Ai = '붉'  # +어지다       +다      +을     +은     +어서        +게     +지
KS_Aj = '괜찮|낮|높|좋|짧'  # +아지다       +다      +을     +은     +아서        +게     +지
KS_Ak = '같|높'  # +아지다       +다      +을     +은     +아서        +게     +지     +이
KS_Al = '섣부'  # x             +르다    +를     +른     +ㄹ+러서     +르게   +르지   +ㄹ+리
KS_Am = '맛있'  # +어지다       +다      +을     +는     +어서        +게     +지
KS_An = '낯서|머|힘드'  # +ㄹ+어지다    +ㄹ+다   +ㄹ     +ㄴ     +ㄹ+어서     +ㄹ+게  +ㄹ+지
KS_Ao = '넓'  # +어지다       +다      +을     +은     +어서        +게     +지
KS_Ap = '희'  # +어지다       +다      +ㄹ     +ㄴ     +어서        +게     +지
KS_Ar = '이로|평화로'  # +와지다       +ㅂ+다   +울     +운     +와서        +ㅂ+게  +ㅂ+지
KS_As = '나'  # +아지다       +ㅅ+다   +을     +은     +아서        +ㅅ+게  +ㅅ+지
KS_Aw = '고'  # +와지다       +ㅂ+다   +울     +운     +와서        +ㅂ+게  +ㅂ+지
KS_Ay = '못ㄷ'  # +ㅚ+어+지다   +ㅚ+다,  +ㅚ+ㄹ  +ㅚ+ㄴ  +ㅚ+어ㅙ+서  +ㅚ+게  +ㅚ+지 ('ㅚ+어' can be shortend to 'ㅙ')
KS_Az = '간소|첨예'  # +해지다       +하다    +할     +한     +해서        +하게   +하지   +히  +화
KS_VGa = "매끈|시들|질척"  # -거리다(verb), -히, -대다, -하다(adjective)
KS_VGb = "거들먹"  # -거리다, -이다, -대다
KS_VCc = "낮|늦|맞|곧"  # 맞+다      맞+는+다   맞+았+다     맞+추+다     맞+추+었+다  맞+출
KS_VCe = "보"  # 보+다      보+ㄴ+다   보+았+다     보+이+다     보+였+다     보+일
KS_VCf = "감|맡"  # 맡+다      맡+는+다   맡+았+다     맡+기+다     맡+겼+다     맡+길
KS_VCg = "벗|숨|신|씻|웃"  # 숨+다      숨+는+다   숨+었+다     숨+기+다     숨+겼+다     숨+길
KS_VCh = "익|읽|입|앉|눕|맞"  # 읽+다      읽+는+다   읽+었+다     읽+히+다     읽+혔+다     읽+힐
KS_VCi = "끓|먹|붙|죽"  # 먹+다      먹+는+다   먹+었+다     먹+이+다     먹+였+다     먹+일
KS_VCj = "속"  # 속+다      속+는+다   속+았+다     속+이+다     속+였+다     속+일
KS_VCk = "돋|일|달|돗"  # 돗+다      돗+는+다   돗+았+다     돗+구+다     돗+구+었+다  돗+굴
KS_VCl = "노|도|사|아"  # 사+ㄹ+다   사+ㄴ+다   사+ㄹ+았+다  사+ㄹ+리+다  사+ㄹ+렸+다  사+ㄹ+릴
KS_VCm = "우"  # 우+ㄹ+다   우+ㄴ+다   우+ㄹ+었+다  우+ㄹ+리+다  우+ㄹ+렸+다  우+ㄹ+릴
KS_VCr = "주"  # 주+ㄹ+다   주+ㄴ+다   주+ㄹ+었+다  주+ㄹ+이+다  주+ㄹ+였+다  주+ㄹ+일
KS_VCu = "깨|세|씌|재|태"  # 깨+다      깨+ㄴ+다   깨+ㅆ+다     깨+우+다     깨+웠+다     깨+울
KS_VId = "거"  # '걷'                # 거+ㄷ+다    거+ㄷ+는+다    거+ㄹ+었+다
KS_VIa = "가"  # 가+다       가+ㄴ+다       가+ㅆ+다
KS_VIe = "야무|여무"  # 여무+ㄹ+다  여무+ㄴ+다     여무+ㄹ+었+다
KS_VIy = "숨죽ㅇ|생ㄱ|쓰러ㅈ|해ㅈ"  # 생ㄱ+ㅣ+다  생ㄱ+ㅣ+ㄴ+다  생ㄱ+ㅕ+ㅆ+다
KS_VIl = "조"  # 조+ㄹ+다    조+ㄴ+다       조+ㄹ+았+다
KS_VIn = '잘나'  # 잘나+다    잘나+ㅆ다       잘나+ㅆ었다
KS_VTg = "박|붙잡|잡"  # +다        +는+다     +았+다      +히+다        +힌+다           +혔+다
KS_VTh = "먹|읽|찍"  # +다        +는+다     +었+다      +ㅎ+ㅣ+다     +ㅎ+ㅣ+ㄴ+다     +ㅎ+ㅕ+ㅆ+다
KS_VTi = "보|쪼"  # +다        +ㄴ+다     +았+다      +ㅇ+ㅣ+다     +ㅇ+ㅣ+ㄴ+다     +ㅇ+ㅕ+ㅆ+다
KS_VTl = "가"  # grind               # +ㄹ+다     +ㄴ+다     +ㄹ+았+다   +ㄹ+ㄹ+ㅣ+다  +ㄹ+ㄹ+ㅣ+ㄴ+다  +ㄹ+ㄹ+ㅕ+ㅆ+다
KS_VTm = "거|드|미"  # +ㄹ+다     +ㄴ+다     +ㄹ+었+다   +ㄹ+ㄹ+ㅣ+다  +ㄹ+ㄹ+ㅣ+ㄴ+다  +ㄹ+ㄹ+ㅕ+ㅆ+다
KS_VTn = "빠"  # wash                # +ㄹ+다     +ㄴ+다     +ㄹ+았+다   +ㄹ+ㄹ+ㅣ+다  +ㄹ+ㄹ+ㅣ+ㄴ+다  +ㄹ+ㄹ+ㅕ+ㅆ+다
KS_VTy = "나ㄴ"  # +ㅜ+다     +ㅜ+ㄴ+다  +ㅝ+ㅆ+다   +ㅟ+다        +ㅟ+ㄴ+다        +ㅟ+었+다
KS_VAd = "넣"  # 넣+다         넣+는다        넣+었다        x               넣+음
KS_VAh = "가까이|뒷받침"  # 가까이+하+다  가까이+한+다   가까이+했+다   x               가까이+함
KS_VAi = "내ㅊ|당ㄱ|[되]?[돌살]ㄹ|망ㅊ|숨ㄱ|외ㅊ|[드]높|되뇌|죽|[보]살ㅍ"  # 외ㅊ+ㅣ다     외ㅊ+ㅣ+ㄴ+다  외ㅊ+ㅕ+ㅆ+다  x               외ㅊ+ㅣ+ㅁ
KS_VAj = '만드'  # 만드+ㄹ+다    만드+ㄴ+다     만드+ㄹ+었다   x               만+듦
KS_VAk = '모'  # 모+르+다      모+른+다       모+ㄹ+랐다     x               모+름
KS_VAl = "[되][돌살]|[쳐]올|[내때]"  # 돌+리다       돌+린다        돌+렸다        x               돌+림
KS_VAm = "빼|재"  # 넣+다         넣+는다        넣+었다        x               빼+ㅁ
KS_VAn = "만나"  # 만나+다       만나+ㄴ+다     만나+ㅆ+다     x               만나+ㅁ
KS_VAr = "내미|마|[받쳐]?드|허무"  # 내미+ㄹ+다    내미+ㄴ+다     내미+ㄹ+었다   x               내미+ㄻ
KS_VAu = "ㅊ|낮ㅊ|늦ㅊ"  # 늦ㅊ+ㅜ+다    늦ㅊ+ㅜ+ㄴ+다  늦ㅊ+ㅜ+었+다  늦ㅊ+ㅝ+ㅆ+다   늦ㅊ+ㅜ+ㅁ
KS_VAw = "[치채키]"
KC_D = "[되된돼됐]"
KC_H = "하고[는자]?|하[겠였]\\w+|하기|하[는니다며여]|하도록|하려[고는]?|하[?]면|하여[야]?|하지[만]?|한 [것뒤적후]|한 다음|한다[고는니며지]?|할|할까[요]?|할래|할지[도]?[요]?|함[을]?|함이다|함입니다|합니다|해보[니다면]|해볼[까래]?|해[서야요]?|해준다|했고[요]?|했기|했는데[요]?|했다[만]?|했습니다[만]?|했으[니면][서]?|했을[지]?|했지[만]?[요]?"
KW_NF = '|'.join(sorted(
    conjugate(KS_Ab, '움')
    + conjugate(KS_Ac, '음')
    + conjugate(KS_Ae, 'ㅡ', 'ㅁ')
    + conjugate(KS_Ai, '음')
    + conjugate(KS_Aj, '음')
    + conjugate(KS_Ak, '음')
    + conjugate(KS_Al, '름')
    + conjugate(KS_Am, '음')
    + conjugate(KS_Am, 'ㅁ')
    + conjugate(KS_Ao, '음')
    + conjugate(KS_Ap, 'ㅁ')
    + conjugate(KS_Ar, '움')
    + conjugate(KS_As, '음')
    + conjugate(KS_Aw, '움')
)
)
KW_NSf = "심각|[둔민]감|건강|간결|깔끔|[불]?가능|근면|정밀|곤란|부지런|무기력|이상|[단온지]순|비슷|[불]?성실|부실|[불]?확실|다양|치열|편안|동일|부족|[부]?적절|나태|공평|[명정]확"
KW_NSv = "명료|무의미|유사|[자섬]세|간소|[거장중]대|[중필]요|분포|난해"
KW_NS = joinseq(KW_NSf, KW_NSv)
KW_ASA = '|'.join(sorted(
    conjugate(KS_Aa, 'ㅏ')  # 나ㅃ+ㅏ(지다), 바ㅃ+ㅏ(지다), ...
    + conjugate(KS_Ab, '워')  # 귀여+워(지다), ...
    + conjugate(KS_Ac, '아')  # 맑+아(지다), ...
    + conjugate(KS_Ad, 'ㄹ', '아')  # 다+ㄹ+아(지다)(be sweety), ...
    + conjugate(KS_Ae, 'ㅓ')  # 예ㅃ+ㅓ(지다), ...
    + conjugate(KS_Af, 'ㄹ', '라')  # 다+ㄹ+라(지다)(be differentiated), ...
    + conjugate(KS_Ag, '해')  # 착+해(지다), ...
    + conjugate(KS_Ah, '해')  # 깔끔+해(지다), ...
    + conjugate(KS_Ai, '어')  # 붉+어(지다), ...
    + conjugate(KS_Aj, '아')  # 낮+아(지다), ...
    + conjugate(KS_Am, '어')  # 맛있+어(지다), ...
    + conjugate(KS_An, 'ㄹ', '어')  # 머+ㄹ+어(지다), ...
    + conjugate(KS_Ao, '어')  # 넓+어(지다), ...
    + conjugate(KS_Ap, '어')  # 희+어(지다), ...
    + conjugate(KS_Ar, '와')  # 이로+와(지다), ...
    + conjugate(KS_As, '아')  # 나+아(지다), ...
    + conjugate(KS_Aw, '와')  # 고+와(지다), ...
    + conjugate(KS_Ay, 'ㅙ')  # 못ㄷ+ㅙ(지다), ...
    + conjugate(KW_NS, '해')  # 필요+해(지다), ...
)
)
KW_ASL = '|'.join(sorted(
    conjugate(KS_Aa, 'ㅡ', 'ㄹ')  # 나ㅃ+ㅡ+ㄹ
    + conjugate(KS_Ab, '울')  # 귀여+울
    + conjugate(KS_Ac, '을')  # 맑+을
    + conjugate(KS_Ad, 'ㄹ')  # 다+ㄹ(sweet)
    + conjugate(KS_Ae, 'ㅡ', 'ㄹ')  # 예ㅃ+ㅡ+ㄹ
    + conjugate(KS_Af, 'ㄹ', 'ㅡ', 'ㄹ')  # 다+ㄹ+ㅡ+ㄹ(different)
    + conjugate(KS_Ag, '할')  # 착+할
    + conjugate(KS_Ah, '할')  # 깔끔+할
    + conjugate(KS_Ai, '을')  # 붉+을
    + conjugate(KS_Aj, '을')  # 낮+을
    + conjugate(KS_Al, '를')  # 맛있+을
    + conjugate(KS_Am, '을')  # 맛있+을
    + conjugate(KS_An, 'ㄹ')  # 머+ㄹ
    + conjugate(KS_Ao, '을')  # 넓+을
    + conjugate(KS_Ap, 'ㄹ')  # 희+ㄹ
    + conjugate(KS_Ar, '울')  # 이로+울
    + conjugate(KS_As, '을')  # 나+을
    + conjugate(KS_Aw, '울')  # 고+울
    + conjugate(KS_Ay, 'ㅚ', 'ㄹ')  # 못ㄷ+ㅚ+ㄹ
    + conjugate(KW_NS, '할')  # 필요+할
)
)
KW_ASN = '|'.join(sorted(
    conjugate(KS_Aa, 'ㅡ', 'ㄴ')  # 나ㅃ+ㅡ+ㄴ
    + conjugate(KS_Ab, '운')  # 귀여+운
    + conjugate(KS_Ac, '은')  # 맑+은
    + conjugate(KS_Ad, 'ㄴ')  # 다+ㄴ(sweet)
    + conjugate(KS_Ae, 'ㅡ', 'ㄴ')  # 예ㅃ+ㅡ+ㄴ
    + conjugate(KS_Af, '른')  # 다+ㄹ+ㅡ+ㄴ(different)
    + conjugate(KS_Ag, '한')  # 착+한
    + conjugate(KS_Ah, '한')  # 깔끔+한
    + conjugate(KS_Ai, '은')  # 붉+은
    + conjugate(KS_Aj, '은')  # 낮+은
    + conjugate(KS_Al, '는')  # 섣부+른
    + conjugate(KS_Am, '는')  # 맛있+는
    + conjugate(KS_An, 'ㄴ')  # 머+ㄴ
    + conjugate(KS_Ao, '은')  # 넓+은
    + conjugate(KS_Ap, 'ㄴ')  # 희+ㄴ
    + conjugate(KS_Ar, '운')  # 이로+운
    + conjugate(KS_As, '은')  # 나+은
    + conjugate(KS_Aw, '운')  # 고+운
    + conjugate(KS_Ay, 'ㅚ', 'ㄴ')  # 못ㄷ+ㅚ+ㄴ
    + conjugate(KW_NS, '한')  # 필요+한
)
)
KW_AS = joinseq(KW_ASA, KW_ASL, KW_ASN)
KW_A = joinseq(KW_AS)
KW_A1 = monosyllables(KW_A)
KW_PVAN = '|'.join(
    sorted(
        ["하는"]
        + conjugate(KS_VAd, '는')  # 넣+는
        + conjugate(KS_VAh, '하는')  # 가까이+하는
        + conjugate(KS_VAi, 'ㅣ', '는')  # 외ㅊ+ㅣ+는
        + conjugate(KS_VAj, '는')  # 만드+는
        + conjugate(KS_VAk, '르는')  # 모+르는
        + conjugate(KS_VAl, '리는')  # 올+리는
        + conjugate(KS_VAm, '는')  # 빼+는
        + conjugate(KS_VAn, '는')  # 만나+는
        + conjugate(KS_VAr, '는')  # 내미+는
        + conjugate(KS_VAu, 'ㅜ', '는')  # 낮ㅊ+ㅜ+는
        + conjugate(KS_VAw, '우', '는')  # 치+우+는
    )
)
KW_PVAP = '|'.join(
    sorted(
        ["했던"]
        + conjugate(KS_VAd, '었던')  # 넣+었
        + conjugate(KS_VAh, '했던')  # 가까이+했
        + conjugate(KS_VAi, 'ㅕ', 'ㅆ', '던')  # 외ㅊ+ㅕ+ㅆ
        + conjugate(KS_VAj, 'ㄹ', '었던')  # 만드+ㄹ+었
        + conjugate(KS_VAk, 'ㄹ', '랐던')  # 모+ㄹ+랐
        + conjugate(KS_VAl, '렸던')  # 올+렸
        + conjugate(KS_VAm, 'ㅆ', '던')  # 빼+ㅆ
        + conjugate(KS_VAn, 'ㅆ', '던')  # 만나+ㅆ
        + conjugate(KS_VAr, 'ㄹ', '었던')  # 내미+ㄹ+었
        + conjugate(KS_VAu, '췄던')  # 낮췄
        + conjugate(KS_VAw, '웠던')  # 치+웠
    )
)
KW_PVA = joinseq(KW_PVAN, KW_PVAP)
KW_PVTN = '|'.join(
    sorted(
        conjugate(KS_VTg, '던')
        + conjugate(KS_VTh, '던')
        + conjugate(KS_VTi, '던')
        + conjugate(KS_VTl, 'ㄹ', '던')
        + conjugate(KS_VTm, 'ㄹ', '던')
        + conjugate(KS_VTn, 'ㄹ', '던')
        + conjugate(KS_VTy, 'ㅜ', '던')
    )
)
KW_PVTP = '|'.join(
    sorted(
        conjugate(KS_VTg, '았던')
        + conjugate(KS_VTh, '었던')
        + conjugate(KS_VTi, '았던')
        + conjugate(KS_VTl, 'ㄹ', '았던')
        + conjugate(KS_VTm, 'ㄹ', '었던')
        + conjugate(KS_VTn, 'ㄹ', '았던')
        + conjugate(KS_VTy, 'ㅜ', '었던')
        + conjugate(KS_VTy, 'ㅝ', 'ㅆ', '던')
    )
)
KW_PVT = joinseq(KW_PVTN, KW_PVTP)
KW_PAN = '|'.join(
    sorted(
        conjugate(KS_Aa, 'ㅡ', 'ㄴ')  # 나ㅃ+ㅡ+ㄴ
        + conjugate(KS_Ab, '운')
        + conjugate(KS_Ac, '은')
        + conjugate(KS_Ad, 'ㄴ')
        + conjugate(KS_Ae, 'ㅡ', 'ㄴ')
        + conjugate(KS_Af, '른')
        + conjugate(KS_Ag, '한')
        + conjugate(KS_Ah, '한')
        + conjugate(KS_Ai, '은')
        + conjugate(KS_Aj, '은')
        + conjugate(KS_Al, '른')
        + conjugate(KS_Am, '는')
        + conjugate(KS_An, 'ㄴ')
        + conjugate(KS_Ao, '은')
        + conjugate(KS_Ap, 'ㄴ')
        + conjugate(KS_Ar, '운')
        + conjugate(KS_As, '은')
        + conjugate(KS_Aw, '운')
        + conjugate(KS_Ay, 'ㅚ', 'ㄴ')
        + conjugate(KW_NS, '한')
    )
)
KW_PAP = '|'.join(
    sorted(
        conjugate(KS_Aa, 'ㅏ', 'ㅆ', '던')
        + conjugate(KS_Ab, '웠던')
        + conjugate(KS_Ac, '았던')
        + conjugate(KS_Ad, 'ㄹ', '았던')
        + conjugate(KS_Ae, 'ㅓ', 'ㅆ', '던')
        + conjugate(KS_Af, 'ㄹ', '랐던')
        + conjugate(KS_Ag, '했던')
        + conjugate(KS_Ah, '했던')
        + conjugate(KS_Ai, '었던')
        + conjugate(KS_Aj, '았던')
        + conjugate(KS_Al, 'ㄹ', '렀던')
        + conjugate(KS_Am, '었던')
        + conjugate(KS_An, 'ㄹ', '었던')
        + conjugate(KS_Ao, '었던')
        + conjugate(KS_Ap, '었던')
        + conjugate(KS_Ar, '웠던')
        + conjugate(KS_As, '았던')
        + conjugate(KS_Aw, '왔던')
        + conjugate(KS_Ay, 'ㅚ', '었던')
        + conjugate(KS_Ay, 'ㅙ', 'ㅆ', '던')
        + conjugate(KW_NS, '했던')
    )
)
KW_PA = joinseq(KW_PAN, KW_PAP)
KW_NIf = "공간|느낌|맛|멋|판매량|확률|이름|성별|식|날짜"
KW_NIn = "차원"
KW_NIv = "몸무게|크기|빈도|나이"
KW_NI = joinseq(KW_NIf, KW_NIn, KW_NIv)
KW_BA = "가득|들쑥날쑥"
KW_BC = '|'.join(sorted(
    ['일부러']
    + conjugate(KS_Aa, 'ㅏ', '서')
    + conjugate(KS_Ab, '워서')
    + conjugate(KS_Ac, '아서')
    + conjugate(KS_Ad, 'ㄹ', '아서')
    + conjugate(KS_Ae, 'ㅓ', '서')
    + conjugate(KS_Af, 'ㄹ', '라서')
    + conjugate(KS_Ag, '해서')
    + conjugate(KS_Ah, '해서')
    + conjugate(KS_Ai, '어서')
    + conjugate(KS_Aj, '아서')
    + conjugate(KS_Al, 'ㄹ', '러서')
    + conjugate(KS_Am, '어서')
    + conjugate(KS_An, 'ㄹ', '어서')
    + conjugate(KS_Ao, '어서')
    + conjugate(KS_Ap, '어서')
    + conjugate(KS_Ar, '와서')
    + conjugate(KS_As, '아서')
    + conjugate(KS_Aw, '와서')
    + conjugate(KS_Ay, 'ㅙ', '서')
    + conjugate(KS_VAk, 'ㄹ', '라서')
))
KW_BD = '가장|거의|그다지|더|많이|별로|약간|얼마간|자주|잘|조금|훨씬'
KW_BM = '|'.join(
    sorted(
        ['그대로', '서로', '함부로']
        + conjugate(KS_Aa, 'ㅡ', '게')
        + conjugate(KS_Ab, 'ㅂ', '게')
        + conjugate(KS_Ac, '게')
        + conjugate(KS_Ad, 'ㄹ', '게')
        + conjugate(KS_Ae, 'ㅡ', '게')
        + conjugate(KS_Af, '르게')
        + conjugate(KS_Ag, '하게')
        + conjugate(KS_Ah, '하게')
        + conjugate(KS_Ai, '게')
        + conjugate(KS_Aj, '게')
        + conjugate(KS_Al, '르게')
        + conjugate(KS_Am, '게')
        + conjugate(KS_An, 'ㄹ', '게')
        + conjugate(KS_Ao, '게')
        + conjugate(KS_Ap, '게')
        + conjugate(KS_Ar, 'ㅂ', '게')
        + conjugate(KS_As, 'ㅅ', '게')
        + conjugate(KS_Aw, 'ㅂ', '게')
        + conjugate(KS_Ay, 'ㅚ', '게')
        + conjugate(KS_VAk, '르게')
    )
)
KW_BN = '|'.join(
    sorted(
        conjugate(KS_Aa, 'ㅡ', '지')
        + conjugate(KS_Ab, 'ㅂ', '지')
        + conjugate(KS_Ac, '지')
        + conjugate(KS_Ad, 'ㄹ', '지')
        + conjugate(KS_Ae, 'ㅡ', '지')
        + conjugate(KS_Af, '르지')
        + conjugate(KS_Ag, '하지')
        + conjugate(KS_Ah, '하지')
        + conjugate(KS_Ai, '지')
        + conjugate(KS_Aj, '지')
        + conjugate(KS_Al, '르지')
        + conjugate(KS_Am, '지')
        + conjugate(KS_An, 'ㄹ', '지')
        + conjugate(KS_Ao, '지')
        + conjugate(KS_Ap, '지')
        + conjugate(KS_Ar, 'ㅂ', '지')
        + conjugate(KS_As, 'ㅅ', '지')
        + conjugate(KS_Aw, 'ㅂ', '지')
        + conjugate(KS_Ay, 'ㅚ', '지')
        + conjugate(KS_VAk, '르지')
    )
)
KW_BI = '|'.join(
    sorted(
        conjugate(KS_Ac, '이')
        + conjugate(KS_Af, 'ㄹ', '리')
        + conjugate(KS_Ah, '히')
        + conjugate(KS_Ak, '이')
        + conjugate(KS_Al, 'ㄹ', '리')
        + conjugate(KS_Aw, '이')
    )
)
KW_BVa = "시들"  # -거리다, -하다(-해지다), -대다
KW_BVb = "굽신|생글"  # -거리다, -하다, -대다
KW_BVc = "이러쿵저러쿵"  # -하다
KW_BV = joinseq(KW_BVa, KW_BVb, KW_BVc)
KW_BW = '|'.join(
    sorted(
        conjugate(KW_NIf, '로')
        + conjugate(KW_NIn, '으로')
        + conjugate(KW_NIv, '로')
    )
)
KW_B = joinseq(KW_BD, KW_BM, KW_BN, KW_BI, KW_BV, KW_BW)
KW_B1 = monosyllables(KW_B)
KW_Fc = "[A-Za-z0-9]*earn|[A-Za-z0-9]*ime|[A-Za-z0-9]*one|LIME|VPN"
KW_Fl = "[A-Za-z0-9]*all|[A-Za-z0-9]*e[l]{1,2}|[A-Z]*ML|URL"
KW_Ff = joinseq(KW_Fc, KW_Fl)
KW_Fv = "[A-Za-z0-9]*ice|[A-Za-z0-9]*ocks|[A-Za-z0-9]*old|[A-Za-z0-9]*uy|[A-Za-z0-9]*dog|[A-Za-z0-9]*uire|[A-Za-z]*[a-z]+ter|[A-Z]*TP|DARPA|[D]?NS|ENQUIRE|UDP|URI|config"
KW_F = joinseq(KW_Ff, KW_Fv)
KW_NTAfc = "값|관측값|물건|[자지]금|학년|게놈|성능|돈|[능출]력|연령|프로그램|걸음|목적|전략|칼럼|입력|기록|블록|그룹|스트림|화면|별명|[품항]목|[구논]문|방법|재산|명산|[세형]상|인생|성|창의성|[속특]성|데이터셋|솔루션|커넥션|애플리케이션|웹 애플리케이션|[공방상지형]식|방안|직업|앱|영역|[내비]용|차원|웹|마음|도메인|디자인|요인|타입|점|규정|[단시장지]점|수준|알고리즘|인터넷|군집|대책|층|명칭|토큰|스택|스텝|시스템|패턴|팀|상품|토픽|국민[ ]?평형|모형|힙|DOM"
KW_NTAfl = "채널|모델|모듈|행렬|말|물|[동식]물|동식물|테이블|기술|현실|배열|연관 배열|[이]?메일|파일|스타일|품질|튜플"  # ends with letter which has ㄹ(lieul) as final consonant
KW_NTAf = joinseq(KW_NTAfc, KW_NTAfl)
KW_NTAv = "선전 포고|[과근선]거|결과|[용정]도|가이드|메서드|스레드|코드|사용료|미래|[자재]료|시류|메모리|라이브러리|카테고리|멤버|리뷰|경영비|의사|[요축]소|[난변소인홍함]수|[극]?소수|부동소수점수|분위수|[순질]서|마이크로서비스|서비스|시퀀스|인덱스|클래스|[단언]어|레이어|소프트웨어|아이디어|하드웨어|수요|범위|차이|글자|현재|일자|이미지|[시절]차|아키텍처|피처|[객물신옥형]체|가중치|관측치|배치|네트워크|에포크|태스크|세태|데이터|벡터|학습 데이터|[상형]태|세그먼트|이벤트|컴포넌트|크레이트|폰트|전자파|[분세점]포|[목좌]표|면허|번호|비밀번호|변화|기회"
KW_NTA = joinseq(KW_NTAf, KW_NTAv)
KW_NTBf = "시각|구간|모듈|간략|[대경]량|[병직]렬|[무유]료|그룹|일반|세분|공산|[가형]상|활성|간소|[가고]속|캡슐|상식|최신|현실|중앙|집약|공용|차원|일원|효율|균일|복잡|최적|다중|계층|패턴|디지털|공통|파편|현행|[대모소]형"
KW_NTBv = "체계|정규|카탈로그|[동무초]기|[극최]대|고도|의무|정보|[극최]소|독립변수|변수|특수|인스턴스|가시|해시|구조|민주|범주|내재|[고기액]체|수치|도커|[암복]호|무효"
KW_NTB = joinseq(KW_NTBf, KW_NTBv)
KW_NTCf = "Babel|NPM|레즈넷|레티나넷|로봇|모바일넷|런타임|툴|논리 풀"
KW_NTCv = "API|CPU|GPU|Grunt|gulp|기계|비행기|생성기|판별기|항공기|침대|[디인]코더|로더|마이크로 프런트엔드|백엔드|서버|웹[ ]?서버|장비|데이터베이스|브라우저|웹[ ]?브라우저|스토리지|[객기마열]?차|자동차|웹 워커|컴퓨터|클라이언트|태스크 러너|프런트엔드"
KW_NTC = joinseq(KW_NTCf, KW_NTCv)
KW_NTDf = "군|동|면|읍|지역|현"
KW_NTDv = "국가|구|시군구|도|리|부|시|주|카운티|국"
KW_NTD = joinseq(KW_NTDf, KW_NTDv)
KW_NTEf = "연극|소설|공연|책|웹툰"
KW_NTEv = "드라마|콘서트|영화"
KW_NTE = joinseq(KW_NTEf, KW_NTEv)
KW_NTFf = "국|귤|라면|밥|빵"
KW_NTFv = "국수|망고|바나나|배|사과|오렌지"
KW_NTF = joinseq(KW_NTFf, KW_NTFv)
KW_NTGf = "가남|강릉|경남|경북|곡성|광명|군산|김천|남원|논산|단양|대전|마산|만종|밀양|부발|부산|상봉|서울|세종|수원|순천|아산|양평|여천|오송|용산|울산|익산|인천|장호원|전남|전북|정동진|정읍|제천|창원|천안|청량리|충남|충북|포항|풍기|평창|행신|횡성"
KW_NTGv = "공주|광주|구미|구례|구포|김포|김해|나주|대구|동해|둔내|목포|묵호|영주|원주|전주|진주|충주"
KW_NTG = joinseq(KW_NTGf, KW_NTGv)
KW_NTHf = "한결|대궐|당금|불꽃|꿈|[끌놋]날|실낱|득달|댕돌|득돌|찰떡|똑|쥐똥|굴뚝|[다벼]락|벽력|전반|철벽|불|쥐뿔|[쏜]?살|추상|[목철]석|박속|장승|굴왕신|귀신|[개쥐]?좆|[감금깜무]쪽|주옥|악착|억척|왕청|[딴분철]통|바둑판|떡판"
KW_NTHv = "개코|감태|생때|신청부|생파리|납덩이|옴포동이|뚱딴지|불티|비호|성화"
KW_NTH = joinseq(KW_NTHf, KW_NTHv)
KW_NTIf = "로컬|피지컬|멘털"
KW_NTI = KW_NTIf
KW_NTJf = "비관|[비소적희]극|저돌|낭만|폭발|[이일추]상|[계부세영종지]속|실용|[대집]중|낙천"
KW_NTJv = "단계|[선영]구|대내|현대|실리|진보|보수|[도원임한]시|대외|행위|독자|경제|[민자]주|[구실자총]체|향토|사회"
KW_NTJ = joinseq(KW_NTJf, KW_NTJv)
KW_NTLAf = "파이썬|C#|HTML|Python|SQL|XML"
KW_NTLAv = "루비|자바|자바스크립트|타입스크립트|솔리디티|C|C[+][+]|Java|Java[Ss]cript|PHP"
KW_NTLNv = "독일어|북한어|스페인어|영어|이탈리아어|일본어|자연어|중국어|터키어|한국어"
KW_NTLf = KW_NTLAf
KW_NTLv = joinseq(KW_NTLAv, KW_NTLNv)
KW_NTL = joinseq(KW_NTLf, KW_NTLv)
KW_NTMf = "폭"
KW_NTMv = "개수|너비|넓이|높이|단위|수|숫자|크기"
KW_NTM = joinseq(KW_NTMf, KW_NTMv)
KW_NTNf = "[미영중한]국|대만|대한민국|일본|스페인|독일|[남북]한"
KW_NTNv = "이탈리아|터키|호주|프랑스"
KW_NTN = joinseq(KW_NTNf, KW_NTNv)
KW_NTOf = "Amazon|Google|공군|구글|기관|삼성|아마존|애플|육군|은행|인스타그램|해군"
KW_NTOv = "Microsoft|Tesla|군대|마이크로소프트|발행사|업소|엔비디아|위원회|테슬라|해병대|학교|한라|회사"
KW_NTO = joinseq(KW_NTOf, KW_NTOv)
KW_NTPf = "공원|공항|광장|극장|기차역|놀이터|선착장|승강장|영화관|주차장|플랫폼"
KW_NTPv = "출입구|항구"
KW_NTP = joinseq(KW_NTPf, KW_NTPv)
KW_NTSf = "그림|[경상시전]황|[국장화]면"
KW_NTSv = "뷰"
KW_NTS = joinseq(KW_NTSf, KW_NTSv)
KW_NTTf = "개발|시설|영업|운영|고객 지원|판촉|마케팅"
KW_NTTv = "회계|관리|[노법재총]무|인사|경제"
KW_NTT = joinseq(KW_NTTf, KW_NTTv)
KW_NTUf = "잔|컵|현수막|화투짝"
KW_NTUv = "장대|접시|샴푸"
KW_NTU = joinseq(KW_NTUf, KW_NTUv)
KW_NTvf = "개학|생일|월드컵|올림픽"
KW_NTvv = "유세|콘퍼런스|대회|운동회"
KW_NTWf = "말|매듭|일단락|결론|이름|밥|한숨|소설|[보]?약|옷|표정|줄|집|짝|아침"
KW_NTWv = "관계|노래|떼|[마]?무리|농사|미소|시|[중]?죄"
KW_NTW = joinseq(KW_NTWf, KW_NTWv)
KW_NTXf = "탭|라디오[ ]?버튼|폼"
KW_NTXv = "체크[ ]?박스"
KW_NTX = joinseq(KW_NTXf, KW_NTXv)
KW_NTYf = "문자[열]?형|불[린]?형|숫자형|정수형"
KW_NTY = KW_NTYf
KW_NTf = joinseq(KW_NTAf, KW_NTBf, KW_NTCf, KW_NTDf, KW_NTEf, KW_NTFf, KW_NTGf, KW_NTHf, KW_NTIf, KW_NTJf, KW_NTLf,
                 KW_NTMf, KW_NTNf, KW_NTOf, KW_NTSf, KW_NTTf, KW_NTUf, KW_NTvf, KW_NTWf, KW_NTXf, KW_NTYf)
KW_NTv = joinseq(KW_NTAv, KW_NTBv, KW_NTCv, KW_NTDv, KW_NTEv, KW_NTFv, KW_NTGv, KW_NTHv, KW_NTJv, KW_NTLv, KW_NTMv,
                 KW_NTNv, KW_NTOv, KW_NTSv, KW_NTTv, KW_NTUv, KW_NTvv, KW_NTWv, KW_NTXv, )
KW_NT = joinseq(KW_NTf, KW_NTv)
KW_NAOIf1 = "벌|찡|참"
KW_NAOIf2 = "일관|[입출]국|집권|[접출]근|기능|도달|탈락|[운]동|[중후]략|[노]력|[관]련|수렴|소멸|연명|[괄]목|함몰|[재폭]발|체벌|중복|손상|발생|연설|소송|통신|작업|[긴등성출퇴]장|경쟁|산적|[도발회]전|근접|방중|[부승약]진|[면유입재]학|방한|[동비서유]행"
KW_NAOIf3 = "불구경|수소문|하소연"
KW_NAOIf4 = "자리매김"
KW_NAOIf = joinseq(KW_NAOIf1, KW_NAOIf2, KW_NAOIf3, KW_NAOIf4)
KW_NAOIv1 = "묘|화"
KW_NAOIv2 = "[증참]가|[경방]과|붕괴|[경]기|연대|복무|방미|[공식퇴]사|감소|소외|[긴중필]요|합의|주지|[부실]패|저하|[전통]화"
KW_NAOIv4 = "대동소이"
KW_NAOIv = joinseq(KW_NAOIv1, KW_NAOIv2, KW_NAOIv4)
KW_NAOI = joinseq(KW_NAOIf, KW_NAOIv)
KW_NAOTf1 = "곱"
KW_NAOTf2 = "수감|[생착]각|보간|[가증]감|점검|공격|[가동연체해]결|[구변]경|[가제]공|[건]국|[총포]괄|송금|[공언지취]급|가늠|[차판]단|[배전]달|[담배해]당|[가기이작]동|[납취획]득|누락|사랑|[생]략|[입출]력|[마수제훈]련|[기수]록|정리|[발변설소작제조증]명|[주지]목|[주질]문|고민|위반|[개선]발|식별|[반]복|구분|[계연]산|[상연향]상|[검수탐]색|[재]생|[분해]석|개선|[건개배증해]설|[구생작완형]성|해소|[계상접]속|[방배전]송|[기저]술|[연학]습|[발송수임]신|의심|[장파]악|[고보제]안|[계예해]약|선언|[수성영작]업|검역|[구시재지]연|[나배사]열|오열|오염|[반운촬투]영|[사응이작적통포허활]용|[교훈]육|[기지]원|[대불]응|[방유]일|통일|[기도수출투]입|[동시조짐]작|[저]장|[누지축]적|[운]전|이전|조절|[가개걱검결교규선설수조지추측한확]정|[마]중|검증|증진|[결매모수편]집|[도장부집탈]착|칭찬|제창|[신요]청|[구압]축|[검구누도산수연인제진창추호]출|[계예]측|[강이]탈|[간선채]택|국한|분할|포함|[결부조취]합|[미발수시실운연진]행|[시실]험|[구실재표]현|[반변소전]환|[계구기노]획"
KW_NAOTf3 = "경원시|동일시|등한시|송수신|수출입|시운전|재기동|재실행"
KW_NAOTf = joinseq(KW_NAOTf1, KW_NAOTf2, KW_NAOTf3)
KW_NAOTv1 = "요"
KW_NAOTv2 = "[인추평]가|[공소전]개|[제준탈]거|설계|비교|[복연촉]구|[대분상연제표]기|안내|[임증초확]대|[시유주]도|계류|[고]려|신뢰|[완종치]료|[관격분수정처]리|연마|구매|소모|근무|확보|[공거기발]부|준비|[감반발복수조]사|[기축]소|[감준회]수|[감무실제출표]시|제어|[기부참]여|[제]외|[소]요|[논유정주회]의|투자|복제|[변참창]조|[감유의정중차폐]지|[기탑]재|[교대]체|[갈성수탈편]취|[납배설위]치|검토|돌파|배포|발표|보호|[분이화]해"
KW_NAOTv3 = "이야기|[재전후]처리|마무리|금기시|당연시|도외시|등한시|문제시|범죄시|신성시|유력시|중요시|확실시|재정의|재투자"
KW_NAOTv4 = "반신반의"
KW_NAOTv = joinseq(KW_NAOTv1, KW_NAOTv2, KW_NAOTv3, KW_NAOTv4)
KW_NAOT = joinseq(KW_NAOTf, KW_NAOTv)
KW_NAOf1 = joinseq(KW_NAOIf1, KW_NAOTf1)
KW_NAOf2 = joinseq(KW_NAOIf2, KW_NAOTf2)
KW_NAOf3 = joinseq(KW_NAOIf3, KW_NAOTf3)
KW_NAOf4 = KW_NAOIf4
KW_NAOfz = joinseq(KW_NAOf2, KW_NAOf3, KW_NAOf4)
KW_NAOf = joinseq(KW_NAOf1, KW_NAOfz)
KW_NAOh = '|'.join(conjugate("강|미|융|특", '화') + conjugate(KS_Az, '화') + conjugate(KW_NTB, '화'))
KW_NAOv1 = joinseq(KW_NAOIv1, KW_NAOTv1)
KW_NAOv2 = joinseq(KW_NAOIv2, KW_NAOTv2)
KW_NAOv3 = KW_NAOTv3
KW_NAOv4 = joinseq(KW_NAOIv4, KW_NAOTv4)
KW_NAOvz = joinseq(KW_NAOv2, KW_NAOv3, KW_NAOv4)
KW_NAOv = joinseq(KW_NAOv1, KW_NAOvz, KW_NAOh)
KW_NAOz = joinseq(KW_NAOfz, KW_NAOvz)
KW_NAO = joinseq(KW_NAOf, KW_NAOv)
KW_NABf = "비난|감동|처단|할당|[입출]력|주목|처방|[처]?벌|축복|상속|전송|제안|교육|환영|구원|[승확]인|위임|대입|연장|판정|강종|칭찬|추천|신청|부탁|선택|심판|반환|시험"
KW_NABv = "용서|계시|강요|기부|보조|오해"
KW_NAB = joinseq(KW_NABf, KW_NABv)
KW_NAFf1 = "[킥킵핑]"
KW_NAFf2 = "\\w{1}[깅닝딩링밍션싱징킹팅핑]|게임|클릭"
KW_NAFf3 = "\\w{2}[깅닝딩링밍션싱징킹팅핑]|임베딩|렌더링|로그인|컨트롤|컴파일"
KW_NAFf4 = "\\w{3}[깅닝딩링밍션싱징킹팅핑]|로그아웃"
KW_NAFf5 = "\\w{4}[깅닝딩링밍션싱징킹팅핑]"
KW_NAFf6 = "\\w{5}[깅닝딩링밍션싱징킹팅핑]"
KW_NAFf7 = "\\w{6}[깅닝딩링밍션싱징킹팅핑]"
KW_NAFfz = joinseq(KW_NAFf2, KW_NAFf3, KW_NAFf4, KW_NAFf5, KW_NAFf6)
KW_NAFf = joinseq(KW_NAFf1, KW_NAFfz)
KW_NAFv2 = "빌드|폴로|메모|캐시|링크"
KW_NAFv3 = "트리거|업로드|릴리스|팔로우|플레이|마사지|마운트|시프트|임포트|카운트|테스트"
KW_NAFv4 = "다운로드|리사이즈|노코멘트|언마운트|업데이트"
KW_NAFv5 = "다운사이즈|로컬라이즈"
KW_NAFv6 = "커스터마이즈"
KW_NAFvz = joinseq(KW_NAFv2, KW_NAFv3, KW_NAFv4, KW_NAFv5, KW_NAFv6)
KW_NAFv = KW_NAFvz
KW_NAF1 = KW_NAFf1
KW_NAFz = joinseq(KW_NAFfz, KW_NAFvz)
KW_NAF = joinseq(KW_NAFf, KW_NAFv)
KW_NAHf = joinseq(KW_NABf, KW_NAFf, KW_NAOf)
KW_NAHv = joinseq(KW_NABv, KW_NAFv, KW_NAOv)
KW_NAH = joinseq(KW_NAHf, KW_NAHv)
KW_NAEf = "각광|고난|고통|눈총|미움|버림|벌|복|사랑|영향"
KW_NAEv = "상처|죄"
KW_NAE = joinseq(KW_NAEf, KW_NAEv)
KW_NAf = joinseq(KW_NAFf, KW_NAOf)
KW_NAv = joinseq(KW_NAFv, KW_NAOv)
KW_NAz = joinseq(KW_NAFz, KW_NAOz)
KW_NA = joinseq(KW_NAf, KW_NAv)
KW_NXf = "보충 학습|자율 학습|복수 지원"
KW_NXv = "학습 지도|군 복무"
KW_NX = joinseq(KW_NXf, KW_NXv)
KW_NYf = "보충학습|자율학습|고객지원|교차지원|수시지원"
KW_NYv = "학습지도|군복무"
KW_NY = joinseq(KW_NYf, KW_NYv)
KW_NC = "녹색"
KW_ND = "것|밖|뿐"
KW_NPEf = "사람|인[간물]"
KW_NPEv = "인류"
KW_NPFf = "김|박|정|강|윤|장|임|한|신|권|황|안|송|류|전|홍|문|양|손|백|남|심|곽|성|민|진|엄|원|천|방|공|현|함|변|염|석|선|설|길|연|명|반|왕|금|옥|육|인|맹|남궁|탁|국|은|편|용|예|경|봉|황보|복|목|형|두|감|제갈|음|빈|동|온|사공|호|범|선우|팽|승|간|상|갈|서문|단|견|당|화|창|옹|순|빙|종|풍|엽|궁|평|독고|랑|판|로|궉|동방|묵|근|점|탄|만|필|돈|운|곡|섭|담|뢰|학|총|삼|독|관|영|등|란|산|증|난|망절|어금|무본|번|완|등정|탕|황목"
KW_NPFv = "이|최|조|오|서|고|배|허|유|노|하|차|주|우|구|라|지|채|여|추|도|소|마|위|기|표|제|모|어|사|가|부|태|계|피|좌|시|대|아|내|매|초|해|야|자|포|후|수|나|요|애|묘|미|비|무|교|다|보"
KW_NPF = joinseq(KW_NPFf, KW_NPFv)
KW_NPNf = "[비]?장애인|어른|소년"
KW_NPNv = "어린이|감염자|[고남여병환]자|[동양이]성애자|바보|아기|아이"
KW_NPN = joinseq(KW_NPNf, KW_NPNv)
KW_NPJf = "감독[관]?[님]?|강사님|[과대부팀회]장[님]?|교수님|[국군도동시]민|기업인|대[리표]님|대통령[님]?|마을 사람|[사의]원|[사소의회]장[님]?|시인|작[곡사]?가님|정치인|직장인|고교생|[대중]?학생|초등학생|[수해]병|이사장|초대 회장|회사원|군인|경찰|동호인"
KW_NPJv = "프로그래머|간호사|[강검의판]사|과학자|교[사수]|대[리표]|작[곡사]?가|전문가|개발자|데이터[ ]?분석가"
KW_NPJ = joinseq(KW_NPJf, KW_NPJv)
KW_NPKf = "[경병부차]장[님]?|[상이일]병|[대중소준][령장]|사령관|경찰청장"
KW_NPKv = "경[사위]|[대중소준][위좌]|[상중하]사|장교|통수권자"
KW_NPRf = "아들|아저씨|동문|조상|자손|식솔|[처]?자식|[부장]인|동창|[일사삼오육칠팔]촌|남편"
KW_NPRv = "[식친]구|처남|자녀|아내|아주머니|[어할]머니|아줌마|엄마|[고대부이]모|동료|며느리|[대형]부|아빠|[제형]수|아저씨|애인|사위|저|[자처형]제|[할]?아버지|제부|처형"
KW_NPR = joinseq(KW_NPRf, KW_NPRv)
KW_NPAf = "거지|고객|손님|애[견묘]인|[증행]인"
KW_NPAv = "수집가|애호가|프로|아마추어|글쓴이|엮은이|지은이|감[독시]자|강[연의]자|관[계련찰]자|당[사직]자|반[려역]자|발[제표]자|[사이]용자|소유자|운전자|응시자|[원]작자|제공자|참[가관석여]자|투자자|협력자|[가피]해자|팬"
KW_NPA = joinseq(KW_NPAf, KW_NPAv)
KW_NPf = joinseq(KW_NPEf, KW_NPFf, KW_NPNf, KW_NPJf, KW_NPKf, KW_NPRf, KW_NPAf)
KW_NPv = joinseq(KW_NPEv, KW_NPFv, KW_NPNv, KW_NPJv, KW_NPKv, KW_NPRv, KW_NPAv)
KW_NP = joinseq(KW_NPf, KW_NPv)
KW_NNC = "[일이삼사오육칠팔구십백천만]*[일이삼사오육칠팔구십백천만억조경]"
KW_NNDf = "십|백|천|만|억|경"
KW_NNDv = "조"
KW_NND = joinseq(KW_NNDf, KW_NNDv)
KW_NNAf = "[136780]|[0-9]*[0-9,.]*[136780]"
KW_NNAv = "[2459]|[0-9]*[0-9,.]*[2459]"
KW_NNA = "[0-9]|[0-9]+[0-9,.]*[0-9]+"
KW_NNMf = KW_NNA + KW_NNDf
KW_NNMv = KW_NNA + KW_NNDv
KW_NNM = joinseq(KW_NNMf, KW_NNMv)
KW_NNK = "[다여일아열스서마쉰예백]?[한두세네섯댓곱덟홉]"
KW_NN = joinseq(KW_NNC, KW_NND, KW_NNK)
KW_NRH = "http[s]?[:]//[A-Za-z0-9./\-_%#]+"  # HTTP
KW_NR = KW_NRH
KW_NUAf = "건|번"
KW_NUAv = "뭉치|회"
KW_NUA = joinseq(KW_NUAf, KW_NUAv)
KW_NUBf = "글자|단어|단원|문|문장|장|절|줄|항|행"
KW_NUBv = "부|파트"
KW_NUB = joinseq(KW_NUBf, KW_NUBv)
KW_NUCf = "루블|엔|원|위안"
KW_NUCv = "달러|리라|유로|페소"
KW_NUC = joinseq(KW_NUCf, KW_NUCv)
KW_NUDf = "광년"
KW_NUDv = "미터|리|킬로미터"
KW_NUD = joinseq(KW_NUDf, KW_NUDv)
KW_NUGf = "[mk]?g"
KW_NUGv = "[k]?[LlMm]"
KW_NUG = joinseq(KW_NUGf, KW_NUGv)
KW_NUIf = "큐빗"
KW_NUIv = "기[가비]바이트|메[가비]바이트|바이트|비트|엑사바이트|제타바이트|키비바이트|킬로바이트|테[라비]바이트"
KW_NUI = joinseq(KW_NUIf, KW_NUIv)
KW_NUMf = "곱"
KW_NUMv = "배"
KW_NUM = joinseq(KW_NUMf, KW_NUMv)
KW_NURf = "평"
KW_NURv = "제곱미터|평방미터"
KW_NUR = joinseq(KW_NURf, KW_NURv)
KW_NUSf = "그릇|권|달|명|방울|벌|병|쌍|장|줄|쪽|통"
KW_NUSv = "가지|개|구|마리|박스|봉지|채|페이지"
KW_NUSd = "대"  # should be handled carefully: '세 대(three device)' vs '3세대(third generation)'
KW_NUS = joinseq(
    KW_NUSf, KW_NUSv  # , KW_NUSd
)
KW_NUTf = "분|시간|일|달|주|월|개월|년|연도"
KW_NUTv = "밀리초|반기|분기|세기|세대|초"
KW_NUT = joinseq(KW_NUTf, KW_NUTv)
KW_NUVv = "세제곱미터"
KW_NUV = KW_NUVv
KW_NUWf = "그램|킬로그램|평"
KW_NUWv = "밀리리터|데시리터|리터|킬로리터|파운드"
KW_NUW = joinseq(KW_NUWf, KW_NUWv)
KW_NUf = joinseq(KW_NUAf, KW_NUBf, KW_NUCf, KW_NUDf, KW_NUGf, KW_NUIf, KW_NUMf, KW_NURf, KW_NUSf, KW_NUTf, KW_NUWf)
KW_NUv = joinseq(KW_NUAv, KW_NUBv, KW_NUCv, KW_NUDv, KW_NUGv, KW_NUIv, KW_NUMv, KW_NURv, KW_NUSv, KW_NUTv, KW_NUVv,
                 KW_NUWv)
KW_NU = joinseq(KW_NUf, KW_NUv)
KW_NLDf = "말"
KW_NLDv = "개|고양이|돼지|소|오리"
KW_NLD = joinseq(KW_NLDf, KW_NLDv)
KW_NLIf = "개미|딱정벌레|지네"
KW_NLIv = "[꿀]벌|[여]왕벌"
KW_NLI = joinseq(KW_NLIf, KW_NLIv)
KW_NLf = joinseq(KW_NLDf, KW_NLIf)
KW_NLv = joinseq(KW_NLDv, KW_NLIv)
KW_NL = joinseq(KW_NLf, KW_NLv)
KW_NVAm = '|'.join(
    sorted(
        conjugate(KS_VAd, '음')  # 넣+음
        + conjugate(KS_VAh, '함')  # 가까이+함
        + conjugate(KS_VAi, 'ㅣ', 'ㅁ')  # 외ㅊ+ㅣ+ㅁ
        + conjugate(KS_VAk, '름')  # 모+름
        + conjugate(KS_VAl, '림')  # 돌+림
        + conjugate(KS_VAm, 'ㅁ')  # 빼+ㅁ
        + conjugate(KS_VAn, 'ㅁ')  # 만나+ㅁ
        + conjugate(KS_VAr, 'ㄻ')  # 내미+ㄻ
        + conjugate(KS_VAu, 'ㅜ', 'ㅁ')  # 늦ㅊ+ㅜ+ㅁ
        + conjugate(KS_VAw, '움')  # 치+움
    )
)

KW_NVm = KW_NVAm
KW_NVAk = '|'.join(
    sorted(
        conjugate(KS_VAd, '기')  # 넣+기
        + conjugate(KS_VAh, '하기')  # 가까이+하기
        + conjugate(KS_VAi, 'ㅣ', '기')  # 외ㅊ+ㅣ+기
        + conjugate(KS_VAk, '르', '기')  # 모+르+기
        + conjugate(KS_VAl, '리기')  # 돌+리기
        + conjugate(KS_VAm, '기')  # 빼+기
        + conjugate(KS_VAn, '기')  # 만나+기
        + conjugate(KS_VAr, 'ㄹ', '기')  # 내미+ㄹ+기
        + conjugate(KS_VAu, 'ㅜ', '기')  # 늦ㅊ+ㅜ+기
        + conjugate(KS_VAw, '우기')  # 치+우기
    )
)
KW_NVIk = '|'.join(
    sorted(
        conjugate(KS_VIa, '기')  # 가+기
        + conjugate(KS_VId, 'ㄷ', '기')  # 거+ㄷ+기
        + conjugate(KS_VIe, 'ㄹ', '기')  # 여무+ㄹ+기
        + conjugate(KS_VIl, 'ㄹ', '기')  # 조+ㄹ+기
        + conjugate(KS_VIn, '기')  # 가+기
        + conjugate(KS_VIy, 'ㅣ', '기')  # 생ㄱ+ㅣ+기
    )
)
KW_NVTk = '|'.join(
    sorted(
        conjugate(KS_VTg, '기')  # 잡+기
        + conjugate(KS_VTh, '기')  # 먹+기
        + conjugate(KS_VTi, '기')  # 보+기
        + conjugate(KS_VTl, 'ㄹ', '기')  # 가+ㄹ+기
        + conjugate(KS_VTm, 'ㄹ', '기')  # 드+ㄹ+기
        + conjugate(KS_VTn, 'ㄹ', '기')  # 빠+ㄹ+기
        + conjugate(KS_VTn, 'ㅜ', '기')  # 나ㄴ+ㅜ+기
    )
)
KW_NVk = joinseq(KW_NVAk, KW_NVIk, KW_NVTk)
KW_NV = joinseq(KW_NVm, KW_NVk)
KW_MA = "다를"
KW_MD = "새|헌"
KW_MVl = "나아갈|부릴|어찌할"
KW_MVn = '|'.join(
    sorted(
        ["느낀", "다룬", "배운"]
        + conjugate(KW_NAO, '된')
    )
)
KW_MV = joinseq(KW_MVl, KW_MVn)
KW_M = joinseq(KW_MD, KW_MV, KW_MA)
KW_PPf = "당신|여러분"
KW_PPv = "[너저][희]?|내|우리"
KW_PP = joinseq(KW_PPf, KW_PPv)
KW_PTf = "[그이저]것"
KW_PTv = "[그이저]"
KW_PT = joinseq(KW_PTf, KW_PTv)
KW_P = joinseq(KW_PP, KW_PT)
KW_VADw = '|'.join(
    sorted(
        conjugate(KS_VAw, '웠다')  # 키 + 웠다
    )
)
KW_VAGw = '|'.join(
    sorted(
        conjugate(KS_VAw, '우', 'ㄴ', '다')  # 키우 + ㄴ + 다
    )
)
KW_VA = joinseq(KW_VADw, KW_VAGw)
KW_VJCi = conjugate(KW_ASA, '지')  # idea (ex: 나빠+지(다))
KW_VJCn = conjugate(KW_ASA, '진')  # progress (ex: 나빠+진(다))
KW_VJCp = conjugate(KW_ASA, '졌')  # past (ex: 나빠+졌(다))
KW_VPl = "갈리다"  # ends with '~리다(lida)'
KW_VPi = "쓰이다"  # ends with '~이다(ida)'
KW_VIn = '|'.join(
    sorted(
        conjugate(KS_VIa, 'ㄴ', '다')
        + conjugate(KS_VIe, 'ㄴ', '다')  # 여무 + ㄴ + 다
        + conjugate(KS_VIy, 'ㅣ', 'ㄴ', '다')  # 숨죽ㅇ + ㅣ + ㄴ + 다
        + conjugate(KS_VIl, 'ㄴ', '다')  # 조 + ㄴ + 다
    )
)
KW_VTCc = '|'.join(
    sorted(
        conjugate(KS_VCc, '추')
    )
)
KW_VTCg = '|'.join(
    sorted(
        conjugate(KS_VCf, '기')
        + conjugate(KS_VCg, '기')
    )
)
KW_VTCh = '|'.join(
    sorted(
        conjugate(KS_VCh, '히')
    )
)
KW_VTCi = '|'.join(
    sorted(
        conjugate(KS_VCi, '이')
        + conjugate(KS_VCj, '이')
        + conjugate(KS_VCe, '이')
        + conjugate(KS_VCr, 'ㄹ', '이')
    )
)
KW_VTCk = '|'.join(
    sorted(
        conjugate(KS_VCk, '구')
    )
)
KW_VTCl = '|'.join(
    sorted(
        conjugate(KS_VCl, 'ㄹ', '리')
        + conjugate(KS_VCm, 'ㄹ', '리')
    )
)
KW_VTCu = '|'.join(
    sorted(
        conjugate(KS_VCu, '우')
    )
)

KW_VTC = joinseq(KW_VTCc, KW_VTCg, KW_VTCh, KW_VTCi, KW_VTCk, KW_VTCl, KW_VTCu)
KW_VTO = '|'.join(
    sorted(
        map(lambda x: x + '시',
            ['하', '보이']
            + conjugate(KW_NAO, '하')  # 가공 + 하 + 시
            + conjugate(KS_VTg, '으')  # 박 + 으 + 시
            + conjugate(KS_VTh, '으')
            + conjugate(KS_VTi, '')
            + conjugate(KS_VTl, '')
            + conjugate(KS_VTm, '')
            + conjugate(KS_VTn, '')
            + conjugate(KS_VTy, 'ㅜ')
            )
    )
)
KW_VTOI = conjugate(KW_VTO, '오')

RULES = [
    {
        "name": "0067207a_동안",
        "desc": "https://wikidocs.net/67207#a",
        "cases": [
            [f"\\b(낮|이틀)동안", "() 동안"],
            [f"\\b({KW_ASN})[ ]?([기순시]간)동안", "() () 동안"]
        ],
        "exception": []
    },
    {
        "name": "0067207b_그동안",
        "desc": "https://wikidocs.net/67207#b",
        "cases": [
            [f"\\b그 동안", "그동안"]
        ],
        "exception": []
    },
    {
        "name": "0067208a_-되다(접미사)",
        "desc": "https://wikidocs.net/67208#a",
        "cases": [
            [f"\\b({KW_NA}) (되[고거는니면므어었지]|[된될됨됩돼됐])([가-잇잉-힣]*)", "()()()"]
        ],
        "exception": []
    },
    {
        "name": "0067208b1_되다(동사)",
        "desc": "https://wikidocs.net/67208#b",
        "cases": [
            [f"\\b(도움|문제)([되된될됨됩돼됐]\\w*)", "() ()"],
            [f"\\b(어찌|얼마)([되된될됨됩돼됐]\\w*)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0067208b2_되다(동사)",
        "desc": "https://wikidocs.net/67208#b",
        "cases": [
            [f"\\b([A-Za-z0-1]+[가이]|\\w+[으]?로)(될|될지\\w*|[돼됐되된됨됩]\\w*)\\b", "() ()"],
            [f"\\b({KW_NAOh})이([돼됐되된될됨됩]\\w*)", "()이 ()"],
            [f"\\b({KW_NTAf})이([돼됐되된될됨됩]\\w*)", "()이 ()"],
            [f"\\b({KW_NAOv})가([돼됐되된될됨됩]\\w*)", "()가 ()"],
            [f"\\b({KW_NTAv})이([돼됐되된될됨됩]\\w*)", "()이 ()"]
        ],
        "exception": []
    },
    {
        "name": "0067208c_-하게 되다",
        "desc": "https://wikidocs.net/67208#c",
        "cases": [
            [f"알게된[ ]?지", "알게 된 지"],
            [f"\\b(\\w*하게|알게)(되어|된다)\\b", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0067213a_-~해야",
        "desc": "→ 0152332a1",
        "cases": [],
        "exception": []
    },
    {
        "name": "0067213b1_-어야 한다",
        "desc": "https://wikidocs.net/67213#b",
        "cases": [
            [f"\\b([가-힣]+)([겨개궈내눠러려벼여져쳐춰펴혀해]야)([하한할함합해했]\\w*)", "()() ()"],
            [f"\\b([갈-받볶-핥]+)(아야)([하한할함합해했]\\w*)", "()() ()"],
            [f"\\b([걸-적죽-훑]+)(어야)([하한할함합해했]\\w*)", "()() ()"],
            [f"\\s([써커해]야)([하한할함합해했]\\w*)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0067213b2_-어야␣되다",
        "desc": "https://wikidocs.net/67213#b",
        "cases": [
            [f"([가-힣]+)([겨개궈내눠러려벼아여져쳐춰펴혀해]야)({KC_D})(\\w*)", "()() ()()"],
            [f"([가-죻죽-힣]+)(어야)({KC_D})(\\w*)", "()() ()()"],
            [f"\\s해야({KC_D})(\\w*)", "해야 ()()"]
        ],
        "exception": []
    },
    {
        "name": "0067213b3_~해 ~야 하다/되다",
        "desc": "https://wikidocs.net/67213#b",
        "cases": [
            [f"\\b({KW_NAOz})해(드려|보아|봐|주어)야([돼됐되된될됨됩하한할함합해했]\\w*)", "()해 ()야 ()"]
        ],
        "exception": []
    },
    {
        "name": "0067213c_~지␣않으면␣안␣되다",
        "desc": "https://wikidocs.net/67213#c",
        "cases": [],
        "exception": []
    },
    {
        "name": "0067214a_-별",
        "desc": "https://wikidocs.net/67214",
        "cases": [
            [f"\\b({KW_NT}) 별(|[로이])\\b", "()별()"],
            [f"\\b({KW_NT})(군|대) 별(|[로이])\\b", "()()별()"],
            [f"\\b({KW_NU}) 별(|[로이])\\b", "()별()"],
            [f"\\b(고객|기능|[사이]용자) 별(|[로이])\\b", "()별()"],
            [f"\\b(alpha|OS) 별(|[로이])\\b", "()별()"]
        ],
        "exception": []
    },
    {
        "name": "0067214b_‘별-’로 시작하는 단어",
        "desc": "https://wikidocs.net/67214#b",
        "cases": [
            [f"\\b별 (거|수)(|를)\\b", "별()()"],
            [f"\\b별 (생각)(|을)\\b", "별()()"],
            [f"\\b별 (걸)\\b", "별()"]
        ],
        "exception": []
    },
    {
        "name": "0067215a1_‘데’(의존 명사)",
        "desc": "https://wikidocs.net/67215#a",
        "cases": [
            [f"\\b({KW_NAO})하는(데[에]?) (그치[지]|좋다\\w*)\\b", "()하는 () ()"],
            [f"\\b({KW_NAO})하는(데[에]?) (필요)(|함)\\b", "()하는 () ()()"],
            [f"\\b({KW_NAO})하는(데[에]?) (소요|[사이활]용|[재]?투자)([되된됨됩될돼됐]\\w+)", "()하는 () ()()"],
            [f"\\b({KW_NAO})(|[를을] )하는(데[에]?) (걸리는|드는|부족한|빠듯한|소요되는|요구되는|적당한|충분한|필요한)[ ]?(기간|시간)(|을|이|이다|입니다)\\b",
             "()()하는 () () ()()"],
            [f"\\b({KW_NAO})하는(데[는에]?) (시간|중점|초점)(|을|이)\\b", "()하는 () ()()"],
            [f"\\b({KW_NAO})하는(데[는에]?) (한|두|석|세|넉|네|다섯|여섯|일곱|여덟|아홉|열)[ ]?(시간|달|해)[ ]?(정도)", "()하는 () () () ()"],
            [f"\\b({KW_NAO})하는(데[는에]?) (일|이|삼|사|오|육|칠|팔|구|십|이십|삼십|사십|오십)[ ]?(분|년)[ ]?(정도)", "()하는 () () () ()"],
            [f"(\\w+|[0-9,.]+[-~][0-9,.]+\\w*)([난는은인한])(데[에]?) (반[하한할해]\\w*)", "()() () ()"],
            [f"(\\w+는)(데) (정신없\\w+)", "() () ()"],
            [f"(\\w+)는(데[에]?[도]?) (기준|도움|목적|목표|어려움|의의|의미|지장)([가는를은을이] \\w+)", "()는 () ()()"],
            [f"(\\w+)는(데[에]?[도]?) (|꽤 |낮은 |높은 |매우 |상당한 |어떻게 |작은 |큰 )(도움|목적|목표|어려움|역할|의의|의미|지장|효과적)([가는를은을이]|이었다)\\b",
             "()는 () ()()()"],
            [f"(\\w+)는데 (약 \\w+[ ]?|\\w+[ ]?)({KW_NUT})([이가] | 정도[가]? )(걸[려렸리린릴]\\w*)", "()는 데 ()()()()"],
            [f"(\\w+)데는 ((\\w+ ){{,2}}(가까|가깝|거리|떨어|많|멀)\\w+)", "(1) 데는 (2)"],
            [f"(\\w+[둔둘할])(데가|데만|데로|데를|데[에]?[서]?)\\b", "() ()"],
            [f"(\\w+[를을])[ ]?({KW_PVAN})데[ ]?(있어[서]?)", "() () 데 ()"],
            [f"(\\w+[를을])[ ]?({KW_NAO})하는데[ ]?(있어[서]?)", "() ()하는 데 ()"],
            [f"(\\w*[기덮드먹보리사상싸우이주키푸하]는)(데[도에]?) (성공|기여|[사유이활]용|충분|필요|한몫)([하한할해했]\\w*)", "() () ()()"],
            [f"(\\w*[기덮드먹보리사상싸우이주키푸하]는)(데[도에]?) (걸[려렸리린릴]\\w*|쓰[여였인일임]\\w*|씁\\w*)", "() () ()"],
            [f"(\\w+는)(데[에]?) (매우|아주) (중요|유용|필요)([하한할해했]\\w*)", "() () () ()()"],
            [f"(\\w+로) (떠오른|부상한)(데에는)", "() ()"],
            [f"\\b({KS_Ah})한데(가|만|로|를|에[서]?|서)\\b", "()한 데()"],
            [f"\\b({KW_NA})한데(가|만|로|를|에[서]?|서)\\b", "()한 데()"],
            [f"\\b(가[는본])데가", "() 데가"],
            [f"\\b(늘어난)데다\\b", "() 데다"],
            [f"\\b({KW_NAO})한데다\\b", "()한 데다"],
            [f"<Noun> 같은데 있을", "() 같은 데 있을"],
            [f"\\b(\\w+는)데 (성공|실패)([!]+)", "() 데 ()()"],
            [f"\\b(맡길)(데) (없\\w+)", "() () ()"],
            [f"(방법인)(데다[가]?)", "() ()"]
        ],
        "exception": [
        ]
    },
    {
        "name": "0067215a11_‘데’(의존 명사)",
        "desc": "https://wikidocs.net/67215#a",
        "cases": [
            [f"(\\w+[란])(데가|데만|데로|데를|데[에]?[서]?)\\b", "() ()"]
        ],
        "exception": [f"라그란데"]
    },
    {
        "name": "0067497d_복합어인 본 용언의 활용형이 3음절 이상인 것과 보조 용언 ‘주다’의 띄어쓰기",
        "desc": "https://wikidocs.net/67497#d",
        "cases": [
            [f"\\b({KW_NAz})[ ]?[해헤](주고[는도]?|주어[도야]|주었다[고는며면]\\w*|[줄줌줘줬]\\w*|준다[고는며면]\\w*|준)\\b", "()해 ()"],
            [f"\\b({KW_NAz})[ ]?해(주세요|주었다|준다|줍[니시]다)[.]", "()해 ()."],
            [f"\\b({KW_NAz})[ ]?해(달[라란래랬])(\\w*)", "()해 ()()"],
            [f"\\b(나타내)(주세요|주자|준다|줍[니시]다)[.]", "() ()"],
            [f"\\b([가-힣]{{2,}}화)[ ]?해([주줄줌줘줬]\\w*|준다[고는며면]\\w*|준)\\b", "()해 ()"],
            [f"\\b([가-힣]{{2,}}화)[ ]?해(준다|줍[니시]다)[.]", "()해 ()"],
            [f"\\b([가-힣]{{2,}}화)[ ]?해본[ ]?(다음|바|적|후)", "()해 본 ()"]
        ],
        "exception": []
    },
    {
        "name": "0067501a_외래어와 ‘하다’의 띄어쓰기",
        "desc": "https://wikidocs.net/67501#a",
        "cases": [
            [f"\\b({KW_NAF}) (할|할지|할지라도|하고[는도서요자]?|하[는지다며면]\\w*|[한했]\\w*|함|함[이인입]\\w+|합니다|해|해[도서야]\\w*)\\b", "()()"],
            [f"\\b({KW_NAF}) 할때", "()할 때"],
            [f"\\b({KW_NAF1}) (해)([ ]?[보본봐서주준줄줘줬]\\w*)\\b", "()()()"],
            [f"\\b({KW_NAFz}) 해([보본봐주준줄줘줬]\\w*)\\b", "()해 ()"]
        ],
        "exception": [f"다운로드", "업로드", "한 번"]
    },
    {
        "name": "0067501d_외래어와 ‘하다’의 띄어쓰기",
        "desc": "https://wikidocs.net/67501#d",
        "cases": [
            [f"\\b(라이드|레벨|파워)[ ]?(업|온)([하한할함합해했]\\w*)", "() () ()"]
        ],
        "exception": []
    },
    {
        "name": "0071780a_-ㄹ수록",
        "desc": "https://wikidocs.net/71780",
        "cases": [
            [f"\\b({KW_ASL}) 수록\\b", "()수록"],
            [f"\\b(높)은 수록\\b", "()을수록"],
            [f"\\b([가-힣]*[아어와워커해]질) 수록", "()수록"],
            [f"\\b(지날|과할) 수록", "()수록"],
            [f"\\b({KW_NAO})([될일할]) 수록", "()()수록"]
        ],
        "exception": []
    },
    {
        "name": "0072685a_한 번",
        "desc": "https://wikidocs.net/72685#a",
        "cases": [
            [f"([두세네]|[다여]섯|일곱|여덟|아홉|열)번({KJ})", "() 번()"],
            [f"\\b한번[ ]?(가량|만큼|쯤)", "한 번()"],
            [f"\\b한번[ ]?(남짓|미만|이상|정도)", "한 번 ()"],
            [f"\\b한번 더\\b", "한 번 더"],
            [f"\\b한번([도에])\\b", "한 번()"],
            [f"\\b한번[ ]?만\\b", "한 번만"],
            [f"\\b(\\w*[을를]) 한번 (\\w*는 데)\\b", "() 한 번 ()"],
            [f"한번꼴", "한 번꼴"],
            [f"\\b(격주|일주일|2주일)(에) 한번(|씩)\\b", "()() 한 번()"]
        ],
        "exception": []
    },
    {
        "name": "0072685b_한번",
        "desc": "https://wikidocs.net/72685#b",
        "cases": [
            [f"\\b(?<!꼭 )한 번 ({KW_NAO})하면 (.*)(기존|다시|원래|전|후)(.*) (\\w*[쓸할] 수 없\\w+)", "한번 ()하면 ()()() ()"],
            [f"\\b(?<!꼭 )한 번 ({KW_NAO})하면 ({KW_NAO})(하기 전까지\\w*|할 수 없\\w+)", "한번 (1)하면 (2)(3)"],
            [f"\\b(꼭 |)한 번 ({KW_NAOz})[ ]?(해)[ ]?([보본볼봄봅봐봤]\\w*)", "()한번 ()() ()"],
            [f"\\b(꼭 |)한 번 ({KW_NAFz})[ ]?(해)[ ]?([보본볼봄봅봐봤]\\w*)", "()한번 ()() ()"],
            [f"\\b(?<!꼭 )한 번 ([알찾]아|[물밀]어|써)([ ]?[보본볼봄봅봐봤]\\w+)", "한번 ()()"],
            [f"\\b(꼭 |)한 번 (드셔|들어|먹어|읽어)([ ]?)(보세요|보[시]?는 것을|보[시]?기를|보아라|봐[라]?)\\b", "()한번 ()()()"]
        ],
        "exception": []
    },
    {
        "name": "0073567a_다시 한번",
        "desc": "https://wikidocs.net/73567",
        "cases": [
            [f"\\b(다시한[ ]?번|다시 한 번)", "다시 한번"]
        ],
        "exception": [f"번도", "번만", "번에", "번쯤"]
    },
    {
        "name": "0073568a_-드리다(합성어)",
        "desc": "https://wikidocs.net/73568#c",
        "cases": [
            [f"(모셔다) (드[려렸리린릴]\\w*)", "()()"]
        ],
        "exception": []
    },
    {
        "name": "0073568b_-드리다(‘-주다’가 한 단어로 사전에 올라 있는 것)",
        "desc": "https://wikidocs.net/73568#b",
        "cases": [
            [f"\\b(가져다|도와|돌려|바래다) (드[려렸리린릴]\\w*)", "()()"]
        ],
        "exception": []
    },
    {
        "name": "0073568e1_꾸밈을 받는 동작성 명사와 ‘-드리다’의 띄어쓰기",
        "desc": "https://wikidocs.net/73568#e",
        "cases": [
            [f"(깊은|큰) (감사|축하)(드[려렸리린릴립]\\w*)", "() () ()"],
            [f"(위로의) (말씀)(드[려렸리린릴립]\\w*)", "() () ()"],
            [f"(깊은|큰) (공양|불공|설명|추천)(드[려렸리린릴립]\\w*)", "() () ()"]
        ],
        "exception": []
    },
    {
        "name": "0073568e2_꾸밈을 받지 않는 동작성 명사와 ‘-드리다’의 띄어쓰기",
        "desc": "https://wikidocs.net/73568#d",
        "cases": [
            [f"(^|\\w*[가는도를서말에을이] )(감사|공양|말씀|불공|설명|추천|축하) (드[려렸리린릴립]\\w*)", "()()()"]
        ],
        "exception": []
    },
    {
        "name": "0075017a1_‘것’의 띄어쓰기",
        "desc": "https://wikidocs.net/75017#a",
        "cases": [
            [f"\\b(그런|아닌|없어진|작은|적은|적지 않은|짧은|많은|모든|큰)([거걸것]\\w*)", "() ()"],
            [f"\\b([난잘]|[가-힣']+[간긴는란린은을인친]|떠난)(거[구군라야지]|겁)(\\w*)", "() ()()"],
            [f"\\b([난잘]|[가-힣']+[간긴는란린은을인친]|떠난)(걸\\w+)", "() ()"],
            [f"\\b(난|[끝병성혼화]날|\\w+[간긴는란린은인친])([거것])(?=[ ]?(같\\w+|마냥|처럼))", "() ()"],
            [f"\\b(어느|어떤|[될들말볼살쌀온올울줄클할]|\\w+[갈긴는던들릴빨뺄쁜운울올은을일줄킬탄한할힐])(거[라]?|겁니\\w*|것\\w*)\\b", "() ()"],
            [
                f"\\b(교정|굽어|깔|내다|내려다|넘겨|노려|눈여겨|눌러|달아|대|[되뒤]돌아|둘러|들여다|떠|뜯어|맛|몰라|물어|바라다|바라|살펴|손|스쳐|알아|얕|여쭈어|여쭤|엿|욕|지내|지켜|찔러|찾아|톺아|훑어|훔쳐)[ ]?본(거[라]?|것\\w*)\\b",
                "()본 ()"],
            [f"\\b(그려|나눠|[들먹읽입]어|만들어|비교해|써|따져)([ ]?본)(거[라]?|것\\w*)\\b", "()() ()"],
            [f"({KW_NAO})([될한할])(것\\w*|거[라야]?)\\b", "()() ()"],
            [f"(\\w+실)(거죠)", "() ()"],
            [f"(?<=[를을] )([본])([거걸것]\\w*)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0075017a3_‘게’(‘것이’의 준말)",
        "desc": "https://wikidocs.net/75017",
        "cases": [
            [f"\\b(그런|다른|아닌|작은|적은|적지 않은|짧은|많은|모든|큰)([게]\\w*)", "() ()"],
            [f"\\b([될들말볼살쌀올울줄클할]|\\w+[갈들릴빨뺄울올을일줄킬할힐])게 ([없있])(\\w*)\\b", "() 게 ()()"],
            [f"\\b(어느|어떤|[온]|\\w+[긴는던쁜운은탄한])(게)\\b", "() ()"],
            [
                f"\\b(교정|굽어|깔|내다|내려다|넘겨|노려|눈여겨|눌러|달아|대|[되뒤]돌아|둘러|들여다|떠|뜯어|맛|몰라|물어|바라다|바라|살펴|손|스쳐|알아|얕|여쭈어|여쭤|엿|욕|지내|지켜|찔러|찾아|톺아|훑어|훔쳐)[ ]?본(게)\\b",
                "()본 ()"],
            [f"\\b(그려|나눠|[들먹읽입]어|만들어|비교해|써|따져)([ ]?본)(게)\\b", "()() ()"]
        ],
        "exception": []
    },
    {
        "name": "0075017b_이것 / 저것 / 그것",
        "desc": "https://wikidocs.net/75017#b",
        "cases": [
            [f"\\b그 것", "그것"],
            [f"\\b(이|저|그) 것(\\w+)", "()것()"]
        ],
        "exception": []
    },
    {
        "name": "0075017c_아무것",
        "desc": "https://wikidocs.net/75017#c",
        "cases": [
            [f"\\b(아무) 것(\\w+)", "()것()"]
        ],
        "exception": []
    },
    {
        "name": "0075024e_마침표의 띄어쓰기",
        "desc": "https://wikidocs.net/75024#e",
        "cases": [
            [f"\\b(\\w+[것다요음함])\\s+(\\.)", "()()"],
            [f"\\b(\\w+[것다요음함][.])(\\w+)", "() ()"],
            [f"\\b(\\w+[것다요음함][.])\\s{{2,}}(\\w+)", "() ()"],
            [f"(\\w*[니있한]다[.])([‘’'])([가-계곡곧-띵락-힣]\\w*)", "() ()()"]
        ],
        "exception": []
    },
    {
        "name": "0079436_양/량",
        "desc": "https://wikidocs.net/79436",
        "cases": [
            [f"(구름|기름)( 양|[ ]?량)", "()양"],
            [f"(데이터|알칼리|이온|칼슘|코드)( 양|[ ]?량)", "()양"],
            [f"\\b(가동|감산|감소|감쇠|계산|노동|생산|섭취|수출|연산|작업|증가|체지방|통신|획득)([ ]?양| 량)", "()량"],
            [f"\\b(설탕)[양량]", "() 양"]
        ],
        "exception": []
    },
    {
        "name": "0079916_따옴표",
        "desc": "https://wikidocs.net/79916",
        "cases": [
            [
                f"(\\w+[\"'”’]) (라[고는])",
                "()()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0079918b_쉼표의 띄어쓰기",
        "desc": "https://wikidocs.net/79918#b",
        "cases": [
            [f"(\\w+[,])([A-Za-z가-힣]+)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0079921a_소괄호 띄어쓰기",
        "desc": "https://wikidocs.net/79921#a",
        "cases": [
            [f"(\\w*[깝꾼넓는멀린쓴었였운이작좁진크한했]다|[하해]라) ([(].*[)][.])", "()()"],
            [f"(\\w+의|계속) ({KW_NT}) ([(][\\w ]+[)])(에)\\b", "() ()()()"],
            [f"(\\w+한 [뒤후]에) ([(][\\w ]+[)]),", "()(),"],
            [f"(\\w+)(됨|함|했음) ([(].+[)])([.;])", "()()()."],
            [f"(\\w+) ([(][가-힣 ]+[)])([과와]|하[고는며])\\b", "()()()"],
            [f"(\\w+) ([(][A-Za-z0-9][A-Za-z0-9._ ]+[)])([과와]|하[고는며])\\b", "()()()"]
        ],
        "exception": []
    },
    {
        "name": "0079970a_‘지’(의존 명사)",
        "desc": "https://wikidocs.net/79970#b",
        "cases": [
            [f"\\b(만난)(지)", "() ()"],
            [f"\\b({KW_NAO})한지 (수년)(|[도은이]|이다|째)\\b", "()한 지 ()"]
        ],
        "exception": []
    },
    {
        "name": "0079970b1_-ㄴ지",
        "desc": "https://wikidocs.net/79970#b",
        "cases": [
            [f"({KW_NAO})[ ]?(되었|[되됐]|하였|[하했])는 (지[가는를에의]?)\\b", "()()는()"],
            [f"(\\w+[는인한]) (지[가는를에]?) ({KW_NAO})(\\w+)", "()() ()()"],
            [f"(\\w+[는인한]) (지[가는를에]?) (궁금|나타|모르|알|알 수 [없있]|찾)(\\w+)", "()() ()()"],
            [f"(\\w+[를을]) (\\w+르는) (지[가는를에]?)\\b", "() ()()"],
            [f"(\\w+야)[ ]?(되는|하는) (지[가는를에]?)\\b", "() ()()"],
            [f"\\b(다른|[없있]는|[없있]지 않은) 지(|[가는를]|만큼[은]?|뿐\\w*|조차)\\b", "()지()"],
            [f"\\b(어느 쪽이|어떤 것이) (|더 )(나은) 지([가는를])\\b", "() ()()지()"]
        ],
        "exception": []
    },
    {
        "name": "0079970b2_-ㄴ지",
        "desc": "https://wikidocs.net/79970#b",
        "cases": [
            [f"({KW_NAO})[ ]?(되었|[되됐]|하였|[하했])는 (지도)\\b", "()()는()"],
            [f"(\\w+[를을]) (\\w+르는) (지도)\\b", "() ()()"],
            [f"(\\w+야)[ ]?(되는|하는) (지도)\\b", "() ()()"],
            [f"\\b(다른|[없있]는|[없있]지 않은) 지(도)\\b", "()지()"],
            [f"\\b(어느 쪽이|어떤 것이) (|더 )(나은) 지도\\b", "() ()()지도"]
        ],
        "exception": [f""]
    },
    {
        "name": "0079972a_-만(보조사)",
        "desc": "https://wikidocs.net/79972#a",
        "cases": [
            [f"\\b(\\w*하는 것|[그이저]것)[ ]?(|뿐) 만(으로|은|을| 가지고[는도서]?| 갖고[는도서]?| 아니라)\\b", "()()만()"],
            [f"\\b(\\w*[^것]) 뿐 (만 아니라)", "() 뿐()"],
            [f"\\b(\\w*[^뿐]) 만([을의이]|으로[는]?)\\b", "()만()"],
            [f"\\b(\\w+[값률율치][들]?|하나|한쪽|테이블) 만(|을)\\b", "()만()"],
            [f"\\b({KW_NNK}) ({KW_NUS}) 만(|으로|을)\\b", "() ()만()"]
        ],
        "exception": []
    },
    {
        "name": "0079972c_만",
        "desc": "https://wikidocs.net/79972",
        "cases": [
            [
                f"<Noun>만해지",
                "()만 해지"
            ],
            [
                f"<Noun>만한",
                "()만 한"
            ]
        ],
        "exception": []
    },
    {
        "name": "0079972f_만(의존 명사)",
        "desc": "https://wikidocs.net/79972#f",
        "cases": [
            [f"([0-9.,]+)({KW_NUT})(| 정도)만에", "()()() 만에"],
            [f"\\b(몇)[ ]?(밀리초|초|주|달|개월|분기|년|세기|광년)만에", "() () 만에"],
            [f"\\b(한|두|한두|두세|석|세|넉|다섯|여섯|일곱|여덟|아홉|열|열한|열두)[ ]?(시간|주|달|분기|해|세기)만에", "() () 만에"],
            [f"\\b([반한]나절|하루|이틀|하루 이틀|[사나]흘|사나흘|[닷엿]새|대엿새|이레|여드레|아흐레|열흘|열하로|삼칠일)만에", "() 만에"]
        ],
        "exception": []
    },
    {
        "name": "0079972g_만-하다",
        "desc": "https://wikidocs.net/79972#g",
        "cases": [
            [f"\\b({KW_NAO})(할 만 |할만 |할만)([해했하한할합]\\w*)", "(1)할 만(3)"],
            [f"\\b({KW_NAO})( 해[ ]?볼[ ]?만|해볼[ ]?만|해 볼만[ ]?)([해했하한할합]\\w*)", "(1)해 볼 만(3)"],
            [f"(믿을|버틸)만 ([해했하한할합]\\w*)", "() 만()"]
        ],
        "exception": [
            "역할만"
        ]
    },
    {
        "name": "0079973a1_-뿐(조사)",
        "desc": "https://wikidocs.net/79973#a",
        "cases": [
            [f"(\\w+)(에게) (뿐\\w*)", "()()()"],
            [f"(\\w+하는|\\w+[던린은진킨한]|\\w*[운]) 것 뿐(|이[다]|인[데]\\w*)\\b", "() 것뿐()"],
            [f"(\\w+하는|\\w+[던린은진킨한]|\\w*[운]) 것 뿐(이에요|이예요)[.]", "() 것뿐이에요."],
            [f"\\b([그이저])[ ]?것 뿐(\\w*)", "()것뿐()"],
            [f"\\b({KW_NI}) 뿐(\\w*)", "()뿐()"],
            [f"\\b({KW_NT}) 뿐(\\w*)", "()뿐()"],
            [f"\\b({KW_P}) 뿐(\\w*)", "()뿐()"],
            [f"\\b({KW_NTA})(|['’”]) (뿐\\w*)", "(1)(2)(3)"],
            [f"\\b({KW_NAO}) (뿐\\w*)", "()()"],
            [f"\\b({KW_NS})[ ]?해[ ]?진[ ]?것 (뿐\\w*)", "()해진 것()"]
        ],
        "exception": [f" 줄"]
    },
    {
        "name": "0079973a2_단위를 나타내는 명사 + ‘뿐’(조사)",
        "desc": "https://wikidocs.net/79973#a",
        "cases": [
            [f"\\b(\\d+[ ]?)({KW_NU}) 뿐(\\w*)", "()()뿐()"],
            [f"\\b(인수|친구)(가) (둘) (뿐\\w*)", "()() ()()"],
            [f"\\b(사람)(이) (둘) (뿐\\w*)", "()() ()()"],
            [f"\\b({KW_NT})([과와]) ({KW_NT}) (둘) (뿐\\w*)", "()() () ()()"],
            [f"\\b([한두세네]|다섯|여섯|일곱|여덟|아홉|스무|서른|마흔|쉰|예순|일흔|여든|아흔|백)[ ]?({KW_NU}) 뿐(\\w*)", "() ()뿐()"],
            [f"\\b(열|스물|서른|마흔|쉰|예순|일흔|여든|아흔)([한두세네]|다섯|여섯|일곱|여덟|아홉)[ ]?({KW_NU}) 뿐(\\w*)", "() ()뿐()"]
        ],
        "exception": []
    },
    {
        "name": "0079973b_뿐(의존명사)",
        "desc": "https://wikidocs.net/79973#b",
        "cases": [
            [f"(\\b[가-힣]+[길다을])(뿐|뿐[ ]?[이임]\\w*)\\b", "() ()"],
            [f"(\\b[가-힣]*[꿀낄놀밀쌀쏠쓸울일졸줄질짤찔칠할])(뿐|뿐[ ]?[이임]\\w*)\\b", "() ()"],
            [f"\\b(\\w+게 할|예뻐할)(뿐만)[ ]?(아니라)", "() () ()"]
        ],
        "exception": []
    },
    {
        "name": "0079973c_-ㄹ뿐더러",
        "desc": "https://wikidocs.net/79973#c",
        "cases": [
            [f"(\\w*[꿀닐둘될들를릴볼쁠울을일줄질칠클할]) 뿐더러", "()뿐더러"]
        ],
        "exception": []
    },
    {
        "name": "0079974a_'-받다'를 앞말에 붙여 써야 하는 경우",
        "desc": "https://wikidocs.net/79974#a",
        "cases": [
            [f"({KW_NAB}) (받\\w+)", "()()"],
            [f"({KW_NAO}) (받\\w+)", "()()"],
            [f"(\\w*[^길쁜운은을인일의큰픈플한할] )({KW_NAE}) (받\\w+)", "()()()"],
            [f"\\b(건네|내려|내리|내림|너름|넘겨|대|돌려|되|두남|들이|딱장|떠|맞|물려|물손|버림|법|본|세|씨|아금|안|응|이어|인정|주고|창|치고|치고|테) (받\\w+)", "()()"],
        ],
        "exception": [f"송금", "송신"]
    },
    {
        "name": "0079974b_'받다'를 앞말과 띄어 써야 하는 경우",
        "desc": "https://wikidocs.net/79974#b",
        "cases": [
            [
                f"(깊은|큰) ({KW_NAE})(받\\w+)",
                "() () ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0079974c_'받다'를 앞말과 항상 띄어 써야 하는 것",
        "desc": "https://wikidocs.net/79974#c",
        "cases": [
            [
                f"(달빛|손님|신호|예쁨|조명|칼|햇빛|환자)(받\\w+)",
                "() ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0080679a_'있다'/'없다'를 앞말과 붙여 써야 하는 것",
        "desc": "https://wikidocs.net/80679#a",
        "cases": [
            [
                f"\\b(가만|뜻|맛|멋|재미) (있\\w*)",
                "()()"
            ],
            [
                f"\\b(꼼짝|끊임|끝|막힘|맛|멋|변함|볼품|빈틈|빠짐|아낌|유례|재미|터무니|형편) (없\\w*)",
                "()()"
            ],
            [
                f"보잘 것 없(다)",
                "보잘것없(다)"
            ],
            [
                f"(^(셀)) 수 없이 (많\\w*)",
                "() 수없이 ()"
            ],
            [f"뜬금 없이", "뜬금없이"]
        ],
        "exception": []
    },
    {
        "name": "0080679b_'있다/없다'를 앞말과 띄어 써야 하는 것",
        "desc": "https://wikidocs.net/80679#b",
        "cases": [
            [
                f"\\b(개념|걱정|관[련심]|국한|깊이|동의|부담|사랑|성과|수정|실속|심도|의미|의심|이름|인기|일관성|자신|제[약한]|조건|조정|주저|준비|중단|증명|질서|차단|차질|책임|추론|튜닝|필요)([이가]?)([있없]\\w+)",
                "()() ()"],
            [f"\\b(별[ ]?볼일[ ]?|별볼[ ]?일[ ]?|별 볼 일)(없\\w+)", "별 볼 일 (2)"],
            [f"\\b별[ ]?수(없\\w*)", "별수 ()"]
        ],
        "exception": []
    },
    {
        "name": "0080679d1_문제없다/소용없다/손색없다/쓸데없다/쓸모없다(형용사)",
        "desc": "https://wikidocs.net/80679#d",
        "cases": [
            [f"(\\w+)({KJ}) (문제|소용|손색) (없\\w*)", "()() ()()"]
        ],
        "exception": []
    },
    {
        "name": "0080679d2_문제/소용/손색/쓸데/쓸모(아무 OO 없다)",
        "desc": "https://wikidocs.net/80679#d",
        "cases": [
            [f"(아무|별|별다른) (문제|소용|손색)(없\\w*)", "() () ()"],
            [f"(아무|별) 쓸 (데|모) (없\\w*)", "() 쓸() ()"],
            [f"(아무|별) 쓸[ ]?(데|모)(없\\w*)", "() 쓸() ()"],
            [f"(\\w+[가는은이]) 쓸[ ]?(데|모) (없\\w*)", "() 쓸()()"]
        ],
        "exception": []
    },
    {
        "name": "0080679d3_문제/소용/손색/쓸데/쓸모 있다",
        "desc": "https://wikidocs.net/80679#d",
        "cases": [
            [
                f"(문제|소용|손색)(있\\w+)",
                "() ()"
            ],
            [
                f"쓸[ ]?(데|모)(있\\w+)",
                "쓸() ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0080679e1_‘-없이’로 붙여 쓰는 것",
        "desc": "https://wikidocs.net/80679#e",
        "cases": [
            [f"\\b(값|관계) 없이", "()없이"]
        ],
        "exception": []
    },
    {
        "name": "0080679e2_앞말과 ‘없이’를 띄어 쓰는 것",
        "desc": "https://wikidocs.net/80679#e",
        "cases": [
            [f"\\b(구분)없이", "() 없이"]
        ],
        "exception": []
    },
    {
        "name": "0080679f_‘여지없이 / 여지 없이’",
        "desc": "https://wikidocs.net/80679#f",
        "cases": [
            [f"(\\w+[는은]) 여지 없이\\b", "() 여지없이"],
            [f"\\b(의심할|일말의|입추의) 여지없이", "() 여지 없이"]
        ],
        "exception": []
    },
    {
        "name": "0080784a_값",
        "desc": "https://wikidocs.net/80784#a",
        "cases": [
            [f"\\b변[수숫] 값", "변숫값"],
            [f"온[도돗] 값", "온돗값"]
        ],
        "exception": []
    },
    {
        "name": "0080784b_‘외래어 + 값’의 띄어쓰기",
        "desc": "https://wikidocs.net/80784#b",
        "cases": [
            [f"커[피핏] 값", "커피값"],
            [f"해[시싯] 값", "해시값"]
        ],
        "exception": []
    },
    {
        "name": "0080784d_사전에 ‘-값’으로 등재된 단어",
        "desc": "https://wikidocs.net/80784#d",
        "cases": [
            [f"\\b(관측|기[본준]|속성|설정|입력|중간|추정|출력) 값", "()값"],
            [f"\\b([경임])[계곗] 값", "()곗값"],
            [f"\\b최[고곳] 값", "최곳값"],
            [f"\\b결[과괏] 값", "결괏값"],
            [f"\\b초[기깃] 값", "초깃값"],
            [f"\\b([기절최])[대댓] 값", "()댓값"],
            [f"\\b진[리릿] 값", "진릿값"],
            [f"\\b([근])[사삿] 값", "()삿값"],
            [f"\\b([요최])[소솟] 값", "()솟값"],
            [f"\\b고[유윳] 값", "고윳값"],
            [f"\\b최[저젓] 값", "최젓값"],
            [f"\\b원자[재잿] 값", "원자잿값"],
            [f"\\b대[표푯] 값", "대푯값"],
            [f"\\b유[효횻] 값", "유횻값"]
        ],
        "exception": []
    },
    {
        "name": "0080784e_사전에 없지만 ‘-값’을 붙여 쓰는 것",
        "desc": "https://wikidocs.net/80784#e",
        "cases": [
            [f"\\b([계상실양음정])[수숫] 값", "()숫값"],
            [f"\\b관[계곗] 값", "관곗값"],
            [f"\\b대[체쳇] 값", "대쳇값"],
            [f"\\b상[태탯] 값", "상탯값"],
            [f"\\b실[제젯] 값", "실젯값"],
            [f"\\b여[유윳] 값", "여윳값"],
            [f"\\b잔[차찻] 값", "잔찻값"],
            [f"\\b차[이잇] 값", "차잇값"],
            [f"\\b통[계곗] 값", "통곗값"],
            [f"\\b특[이잇] 값", "특잇값"],
            [f"\\b표[시싯] 값", "표싯값"]
        ],
        "exception": []
    },
    {
        "name": "0080784h_‘값비싼’",
        "desc": "https://wikidocs.net/80784#g",
        "cases": [
            [
                f"\\b(값) (비[싸싼]\\w*)",
                "()()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0080788a_-상(上)",
        "desc": "https://wikidocs.net/80788#a",
        "cases": [
            [
                f"\\b(공간|미관|지구|인터넷|관계|소스 코드|코드|클라우드|분량|이론|스토리|스트림|화면|업무|서버|[일]?직선|전설|특성|커넥션|콘솔|서비스|인터페이스|통신|레이아웃|소프트웨어|\\w*차원|편의|온라인|구조|규정|알고리즘|웹[ ]?페이지|페이지|이미지|엑스축|[교규]칙|네트워크|데이터|시스템|사이트|웹사이트|포털 사이트|분포|API|[CGT]PU|Excel|JSX|Logflare|Storybook) 상(|과|까지[도는만]?|도|만|보다|부터|에|에서|으로[도는서써]?|은|을|의|이|이고|이다|이라|이라는|이란|이랑|처럼|하고)\\b",
                "()상()"],
            [f"\\b(사실) 상\\b", "()상"],
        ],
        "exception": []
    },
    {
        "name": "0080788b_-하(下)",
        "desc": "https://wikidocs.net/80788#b",
        "cases": [
            [
                f"(가정|감리|규정|상황|식민지|원칙|인솔|일념|전제|조건|주관|지도|지배|[체통]제) 하(가|까지|는|도|라고|라는|란|랑|로|를|만|보다|부터|에|에서|와|요|의|이고|이다|처럼|하고|)\\b",
                "()하()"]
        ],
        "exception": []
    },
    {
        "name": "0084578a_-씩",
        "desc": "https://wikidocs.net/84578",
        "cases": [
            [f"\\b({KW_NNK})[ ]?([명번벌병잔줄]) 씩", "() ()씩"],
            [f"\\b(\\d+[ ]?)([명번벌병잔줄]) 씩", "()()씩"],
            [f"([0-9]+)([ ]?)([년월일시분초]) 씩", "()()()씩"]
        ],
        "exception": []
    },
    {
        "name": "0084935a_-할지",
        "desc": "https://wikidocs.net/84935#a",
        "cases": [
            [f"({KW_NAO})[ ]?할 (지[를]?)\\b", "()할()"],
            [f"(\\w+)야[ ]?할 (지[가는도를에]?)\\b", "()야 할()"],
            [f"\\b(몇 [개등명]일|\\w+일) (지[가는도를에]?)\\b", "()()"],
            [f"(\\w+할|\\w*[될릴울]) (지[가는도를에]?) (걱정|궁금|모[르릅]|알|찾)(\\w+)", "()() ()()"],
            [f"\\b(돌아올|\\w+[겼났았었였렸쳤했]을) (지[도]?)\\b", "()()"]
        ],
        "exception": []
    },
    {
        "name": "0084935b_-할지라도",
        "desc": "https://wikidocs.net/84935#b",
        "cases": [
            [f"\\b(\\w*[멀쁠울을일질클할]) 지라도", "()지라도"]
        ],
        "exception": []
    },
    {
        "name": "0084944_작동 원리",
        "desc": "https://wikidocs.net/84944",
        "cases": [
            [
                f"(\\w+의) 작동(원리\\w*)",
                "() 작동 ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0085480a_하지/치",
        "desc": "https://wikidocs.net/85480",
        "cases": [
            [
                f"넉넉치 않(다)",
                "넉넉지 않(다)"
            ],
            [
                f"충분지 않(다)",
                "충분치 않(다)"
            ],
            [
                f"전달도록",
                "전달토록"
            ]
        ],
        "exception": []
    },
    {
        "name": "0085824a_또다시",
        "desc": "https://wikidocs.net/85824#a",
        "cases": [
            [
                f"또 다시",
                "또다시"
            ]
        ],
        "exception": []
    },
    {
        "name": "0085824b_또 다른",
        "desc": "https://wikidocs.net/85824#b",
        "cases": [
            [
                f"또다른",
                "또 다른"
            ]
        ],
        "exception": []
    },
    {
        "name": "0085826a_지난번/지난달/지난해",
        "desc": "https://wikidocs.net/85826#a",
        "cases": [
            [
                f"지난 (날|달|번|주|해)",
                "지난()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0085826b_이번 주, 저번 주",
        "desc": "https://wikidocs.net/85826#b",
        "cases": [
            [f"\\b([이저]번)주(|[가는도를]|에\\w*|의)\\b", "() 주()"]
        ],
        "exception": []
    },
    {
        "name": "0086003a_주의 깊다",
        "desc": "https://wikidocs.net/86003",
        "cases": [
            [
                f"\\b(사려|속|주의)(깊\\w+)",
                "() ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0086337_테(터이)",
        "desc": "https://wikidocs.net/86337",
        "cases": [
            [f"\\b([될할])(테니까)\\b", "() ()"],
            [f"\\b(\\d+[가이])([될할])(테니까)\\b", "() () ()"]
        ],
        "exception": []
    },
    {
        "name": "0086793a_‘첫’으로 시작하는 단어",
        "desc": "https://wikidocs.net/86793",
        "cases": [
            [f"\\b첫 (날|해)(\\w*)", "첫()()"],
            [f"\\b첫 (걸음)(\\w*)", "첫()()"]
        ],
        "exception": []
    },
    {
        "name": "0086793b_‘첫’과 뒷말을 띄어 쓰는 것",
        "desc": "https://wikidocs.net/86793#b",
        "cases": [
            [f"\\b첫(경험|만남|방송|수업|시험|사건|월급|화면)", "첫 ()"]
        ],
        "exception": []
    },
    {
        "name": "0090213b_-지 못하다(긴 ‘못’ 부정문)",
        "desc": "https://wikidocs.net/90213#b",
        "cases": [
            [f"(\\w+지) 못 ([하한할함해했]\\w*)", "() 못()"],
            [f"(\\w+지)못([하한할함해했]\\w*)", "() 못()"]
        ],
        "exception": []
    },
    {
        "name": "0090213c_못 하다(불가능)",
        "desc": "https://wikidocs.net/90213#c",
        "cases": [
            [f"(너무 [가-힣]+[서워] [가-힣]+[를을]) 못(하겠[가-힝]+)", "() 못 ()"]
        ],
        "exception": []
    },
    {
        "name": "0090213d_못 하다(짧은 ‘못’ 부정문)",
        "desc": "https://wikidocs.net/90213#d",
        "cases": [
            [f"\\b(감당|구분|말|무시)(|[도를을])[ ]?못(하게|할)\\b", "()() 못 ()"]
        ],
        "exception": []
    },
    {
        "name": "0090403a_-간",
        "desc": "https://wikidocs.net/90403",
        "cases": [
            [f"\\b(\\d+[ ]?|[일이삼사오육칠팔구십] |[이삼사오육칠팔구]십[일이삼사오육칠팔구]* |)(일|주|월|연|초|ms) 간(|[은의])\\b", "()()간()"],
            [f"\\b(며칠|몇 년|수년|이틀|사흘|나흘|닷새|엿새|열흘|한 달) 간", "()간"]
        ],
        "exception": []
    },
    {
        "name": "0090403b_간(間)이 붙어 한 단어로 굳어진 것",
        "desc": "https://wikidocs.net/90403#b",
        "cases": [
            [f"\\b(남매|다자|피차|형제) 간(\\w*)", "()간()"],
            [f"\\b(다소|얼마|잠시) 간(\\w*)", "()간()"]
        ],
        "exception": []
    },
    {
        "name": "0090403c1_간(間)을 앞말과 띄어 써야 하는 것",
        "desc": "https://wikidocs.net/90403#c",
        "cases": [
            [f"({KW_NT})([과와]) ({KW_NT})간(|[에은을의])\\b", "(1)(2) (3) 간(4)"]
        ],
        "exception": [f"시간", "약간"]
    },
    {
        "name": "0090403c2_간(間)을 앞말과 띄어 써야 하는 것",
        "desc": "https://wikidocs.net/90403#c",
        "cases": [
            [f"\\b(거점|노사|당국|상호|서로|서버)간(|[에을의])\\b", "() 간()"],
            [f"\\b({KW_NPA})간(|에)\\b", "() 간()"],
            [f"\\b({KW_NPJ})간(|에)\\b", "() 간()"],
            [f"\\b({KW_NTG})([~-]| [~-] )({KW_NTG})간", "()()() 간"]
        ],
        "exception": []
    },
    {
        "name": "0090403c3_간(間)을 앞말과 띄어 써야 하는 것",
        "desc": "https://wikidocs.net/90403#c",
        "cases": [
            [f"\\b({KW_NTA})([들]?)간(|[에은을의]|에[는도]?)\\b", "()() 간()"],
            [f"\\b({KW_NPJ})([들]?)간(|[에은을의]|에[는도]?)\\b", "()() 간()"],
            [f"\\b({KW_NTO})([들]?)간(|[에은을의]|에[는도]?)\\b", "()() 간()"]
        ],
        "exception": []
    },
    {
        "name": "0090404a_-내(內)",
        "desc": "https://wikidocs.net/90404#a",
        "cases": [
        ],
        "exception": []
    },
    {
        "name": "0090404b_-외(外)",
        "desc": "https://wikidocs.net/90404#b",
        "cases": [
            [f"\\b(예상) (외)(|[로의]|였다|[이]?다|이었다)\\b", "()()()"]
        ],
        "exception": []
    },
    {
        "name": "0090404c_‘내(內)’, ‘외(外)’를 앞말과 띄어 쓰는 것",
        "desc": "https://wikidocs.net/90404#c",
        "cases": [
            [f"([가-힣]+)외 (\\d+)([명인])", "() 외 ()()"],
            [f"<NNP>외", "<NNP> 외"],
            [f"\\b({KW_NTA})([내외]) ({KW_NT})", "() () ()"],
            [f"\\b({KW_NTA})([내외])({KJ})\\b", "() ()()"],
            [f"\\b({KW_NTT})[ ]?(팀)([내외])", "() () ()"],
            [f"\\b([A-Za-z]+)([내외])({KJ})\\b", "() ()()"],
            [f"\\b(\\w*값|[A-Za-z0-9_])(외\\w*)", "() ()"]
        ],
        "exception": ["대내외"]
    },
    {
        "name": "0090405_후",
        "desc": "https://wikidocs.net/90405",
        "cases": [
            [f"({KW_NAF})(한|)후", "()() 후"],
            [f"({KW_NAO})(한|)후", "()() 후"],
            [f"(\\w*[가이]) (열린)후", "() () 후"],
            [f"(\\w*[을를]) ([건쓴본]|\\w*[른신운은인킨힌])후", "() () 후"],
            [f"(\\w+ ({KW_NUT}))후", "() 후"],
            [f"\\b(며칠|얼마|잠시|한참)후", "() 후"]
        ],
        "exception": []
    },
    {
        "name": "0090406_말, 중, 초",
        "desc": "https://wikidocs.net/90406",
        "cases": [
            [f"\\b([상하]반기|[0-9]+년)([말중초])", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0090407_‘가능하다’의 띄어쓰기",
        "desc": "https://wikidocs.net/90407",
        "cases": [
            [f"\\b(|재)(사용|입력|출력|확장)(가능|불가능)(|하다|하므로|하여\\w*|한|합니다|할|할지\\w*|해[져졌지진짐집질]\\w*)\\b", "()() ()()"]
        ],
        "exception": []
    },
    {
        "name": "0090767a_수(數)",
        "desc": "https://wikidocs.net/90767#a",
        "cases": [
            [f"\\b(소|의석|인원|장절|재적|출석|투표) 수", "()수"],
            [f"\\b머리[ ]?수", "머릿수"],
            [f"\\b(가구|개체|답변|이용자|조회|추천|코어|회원)수\\b", "() 수"],
            [f"\\b(가구|개체|답변|이용자|조회|추천|코어|회원)수({KJ})\\b", "() 수()"]
        ],
        "exception": []
    },
    {
        "name": "0090767b1_자릿수",
        "desc": "https://wikidocs.net/90767#b1",
        "cases": [
            [f"\\b자리수(|[가는도를])\\b", "자릿수()"]
        ],
        "exception": [f"자리 수"]
    },
    {
        "name": "0090767e1_‘수(數)’를 붙여 써야 하는 것",
        "desc": "https://wikidocs.net/90767#e",
        "cases": [
            [f"\\b수 (개월|분|일|천)", "수()"],
            [f"\\b수 만[ ]?({KW_NUS})", "수만 ()"],
            [f"\\b(수 백만|수 백 만|수백 만)", "수백만"]
        ],
        "exception": []
    },
    {
        "name": "0090767e2_‘수년’",
        "desc": "https://wikidocs.net/90767#e",
        "cases": [
            [f"\\b({KW_NAO})한[ ]?지 수 년[ ]?([을]|이[다]?|째\\w*)\\b", "()한 지 수년()"]
        ],
        "exception": []
    },
    {
        "name": "0090767f_‘수(數)’를 띄어 써야 하는 것",
        "desc": "https://wikidocs.net/90767#f",
        "cases": [
            [f"\\b수(미터|킬로미터)", "수 ()"],
            [f"\\b수(m|km)", "수 ()"]
        ],
        "exception": []
    },
    {
        "name": "0091618a_쪽",
        "desc": "https://wikidocs.net/91618#a",
        "cases": [
            [f"\\b(다른|함수)(쪽\\w*)", "() ()"],
            [f"({KW_NTC})(쪽\\w*)", "() ()"],
            [f"({KW_NTN})(쪽\\w*)", "() ()"],
            [f"({KW_NTO})(쪽\\w*)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0091618b_쪽",
        "desc": "https://wikidocs.net/91618#b",
        "cases": [
            [f"\\b(그|아래|앞|오른|왼|위|이|저) (쪽\\w*)", "()()"]
        ],
        "exception": []
    },
    {
        "name": "0091618c1_~을 한 쪽",
        "desc": "https://wikidocs.net/91618#c",
        "cases": [
            [f"(\\w+[를을]) 한쪽은", "() 한 쪽은"]
        ],
        "exception": []
    },
    {
        "name": "0091618c2_한쪽",
        "desc": "https://wikidocs.net/91618#c",
        "cases": [
            [f"\\b(한) (쪽\\w*)", "()()"],
            [f"\\b한 쪽이 (\\w+이 될 때까지)", "한쪽이 ()"]
        ],
        "exception": [f"어느 한 쪽", "를 한 쪽", "을 한 쪽"]
    },
    {
        "name": "0091618c3_어느 한쪽",
        "desc": "https://wikidocs.net/91618#c",
        "cases": [
            [f"어느[ ]?한 쪽", "어느 한쪽"]
        ],
        "exception": []
    },
    {
        "name": "0091619a_체언 뒤의 ‘만큼’",
        "desc": "https://wikidocs.net/91619#a",
        "cases": [
            [f"\\b({KW_NT}) 만큼(|[도은을의이])\\b", "()만큼()"],
            [f"\\b(그) 만큼", "()만큼"],
            [f"([A-Za-z0-9]+) 만큼", "()만큼"]
        ],
        "exception": [
            "날 만큼",
            "한 만큼"
        ]
    },
    {
        "name": "0091619b_조사 + ‘만큼’",
        "desc": "https://wikidocs.net/91619#b",
        "cases": [
            [f"(\\w+)(에서|[이]?니) (만치|만큼)", "()()()"]
        ],
        "exception": [
        ]
    },
    {
        "name": "0091619c_관형사형 뒤의 ‘만큼’",
        "desc": "https://wikidocs.net/91619#c",
        "cases": [
            [f"<NNG><XSV><ETM>만큼", "<NNG><XSV><ETM> 만큼"],
            [f"<VV><ETM>만큼", "<VV><ETM> 만큼"],
            [f"\\b(받을)(만큼)", "() ()"],
            [f"\\b(어느)(만큼)", "() ()"],
            [f"\\b([낼쌀줄할]|\\w+[길낼릴을일줄칠킬할])[ ]?수[ ]?(있[는을])만큼", "() 수 () 만큼"]
        ],
        "exception": []
    },
    {
        "name": "0091620a_한 가지, 두 가지, 세 가지",
        "desc": "https://wikidocs.net/91620#a",
        "cases": [
            [f"\\b({KW_NNK})(가지|종류)", "() ()"],
            [f"\\b한가지 ({KW_NAO})[ ]?([하할해]\\w*)", "한 가지 ()()"],
            [f"\\b한가지[ ]?([밖뿐]\\w*)", "한 가지()"]
        ],
        "exception": [f"한가지"]
    },
    {
        "name": "0091620b_한가지",
        "desc": "https://wikidocs.net/91620#b",
        "cases": [
            [f"\\b(충효는) 한 (가지)(라)", "() 한()()"]
        ],
        "exception": []
    },
    {
        "name": "0091621a_-대로(조사)",
        "desc": "https://wikidocs.net/91621",
        "cases": [
            [f"\\b(\\w* 것) 대로", "()대로"],
            [f"\\b(법|의도|신청서|지침) (대로)\\b", "()()"]
        ],
        "exception": []
    },
    {
        "name": "0091621b_대로(의존 명사)",
        "desc": "https://wikidocs.net/91621",
        "cases": [
            [f"\\b(본)대로\\b", "() 대로"],
            [f"\\b(가르쳐|알려)준([ ]?데로|대로)\\b", "()준 대로"],
            [f"(\\w+[낀는던린은을한])대로\\b", "() 대로"]
        ],
        "exception": [f"무한대"]
    },
    {
        "name": "0091621c_되는대로(부사)",
        "desc": "https://wikidocs.net/91621#c",
        "cases": [
            [f"(\\w+으로) 되는 대로", "() 되는대로"]
        ],
        "exception": [f"무한대"]
    },
    {
        "name": "0091964a1_-밖",
        "desc": "https://wikidocs.net/91964#a",
        "cases": [
            [f"(하나의 \\w+) 밖에", "()밖에"],
            [f"(\\w+|\\w+[(][)]|[']\\w+[']) 밖에 ([모몰없]\\w+)", "()밖에 ()"],
            [f"(\\w*) 밖에 안[ ]?되(고|는[데]?|지[만]?|면[서]?)", "()밖에 안 되()"]
        ],
        "exception": [f"가지 밖", "번 밖"]
    },
    {
        "name": "0091964a2_-밖",
        "desc": "https://wikidocs.net/91964#a",
        "cases": [
            [f"\\b({KW_NNK})[ ]?가지 밖에 ([모몰없]\\w*)", "() 가지밖에 ()"],
            [f"(\\d+[ ]?)({KW_NUS}) 밖에 안[ ]?([되된될됨돼됐]\\w*)", "()()밖에 안 ()"],
            [f"(\\d+[ ]?)({KW_NUS}) 밖에 (\\w+지 않\\w+)", "()()밖에 ()"]
        ],
        "exception": []
    },
    {
        "name": "0091964b_-밖",
        "desc": "https://wikidocs.net/91964#b",
        "cases": [
            [f"({KW_NNK})[ ]?번 밖에", "() 번밖에"]
        ],
        "exception": []
    },
    {
        "name": "0091964c_밖",
        "desc": "https://wikidocs.net/91964#c",
        "cases": [
            [f"\\b(관심|예상)밖", "() 밖"],
            [f"(\\w+)밖(에서\\w*|의)\\b", "() 밖()"]
        ],
        "exception": []
    },
    {
        "name": "0091964d_밖",
        "desc": "https://wikidocs.net/91964#d",
        "cases": [
            [
                f", 그밖의",
                ", 그 밖의"
            ],
            [
                f"~나 그밖의",
                "~나 그 밖의"
            ],
            [
                f"\\b(그|이)밖에([도]?)",
                "() 밖에()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0091964f_수밖에",
        "desc": "https://wikidocs.net/91964#f",
        "cases": [
            [
                f"\\b수 밖에",
                "수밖에"
            ]
        ],
        "exception": []
    },
    {
        "name": "0092097a_다운로드하다, 업로드하다",
        "desc": "https://wikidocs.net/92097#a",
        "cases": [
            [f"(다운로드|업로드) ({KC_H})(\\w*)", "()()()"]
        ],
        "exception": []
    },
    {
        "name": "0092097b_다운로드받다, 내려받다",
        "desc": "https://wikidocs.net/92097#b",
        "cases": [
            [
                f"(다운로드) (받\\w*)",
                "()()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0092098a_건(의존명사)",
        "desc": "https://wikidocs.net/92098",
        "cases": [
            [f"(일곱)(건\\w*)", "() ()"],
            [f"([0-9,]+억 [0-9,]+만|[0-9,]+만)(건\\w*)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0092099a_~보다(동사)",
        "desc": "https://wikidocs.net/92099#a",
        "cases": [
            [
                f"\\b(교정|굽어|깔|내다|내려다|넘겨|노려|눈여겨|눌러|달아|대|[되뒤]돌아|둘러|들여다|떠|뜯어|맛|몰라|물어|바라다|바라|살펴|손|스쳐|알아|얕|여쭈어|여쭤|엿|욕|지내|지켜|찔러|찾아|톺아|훑어|훔쳐) ([보본볼봐봤]\\w+)",
                "()()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0092099b1_보다(조사)",
        "desc": "https://wikidocs.net/92099#b",
        "cases": [
            [f"\\b({KW_NI}|{KW_NA}|{KW_NP}|{KW_NL}) 보다", "()보다"],
            [f"\\b({KW_NF}) 보다", "()보다"],
            [f"\\b({KW_NT}) 보다", "()보다"],
            [f"\\b({KW_NN}|{KW_NU}) 보다", "()보다"],
            [f"(\\w+[A-Za-z0-9]) 보다[ ]?({KW_ASN})", "()보다 ()"],
            [f"(\\w+[A-Za-z0-9]) (보다[는]?)[ ]?(\\w+[이가])", "()() ()"],
            [f"(\\w+) (보다[는]?)[ ]?({KW_NTA})([이가]|[으]?로)", "()() ()()"],
            [f"(\\w+) 보다 는\\b", "()보다는"],
            [f"\\b수[ ]?년[ ]?([전후]) 보다([는도]?)\\b", "수년 ()보다()"],
            [f"\\b(이제|지금)까지 보다 (뛰어난|효율적으로)", "()까지보다 ()"],
            [f"\\b(경우)[ ]?([(].*[)]) 보다 (\\w+의 \\w+[가이]) (좋\\w*|안 좋\\w*)", "()()보다 () ()"]
        ],
        "exception": []
    },
    {
        "name": "0092099b2_-보다(조사)",
        "desc": "https://wikidocs.net/92099#b",
        "cases": [
            [f"(\\w+) 보다[ ]?({KW_BD})[ ]?({KW_ASN})", "()보다 () ()"],
            [f"(\\w+) 보다[ ]?({KW_BD})[ ]?({KW_BD})[ ]?({KW_ASN})", "()보다 () () ()"]
        ],
        "exception": [f"만 개 보다", "에 보다"]
    },
    {
        "name": "0092099b3_-보다(조사)",
        "desc": "https://wikidocs.net/92099#b",
        "cases": [
            [
                f"(\\w+)(기|는[ ]?것) (보다[도는]?)",
                "()()()"
            ],
            [
                f"\\b({KW_NNK})([ ]?)({KW_NUS}) (보다[도는]?)",
                "()()()()"
            ],
            [
                f"({KW_NNM})([ ]?)({KW_NUS}) (보다[도는]?)",
                "()()()()"
            ],
            [
                f"(\\w+[ ]?)([율률]|수치|지표) (보다[도는]?)",
                "()()()"
            ],
            [
                f"({KW_NNA}) (보다[도는]?)",
                "()()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0092099c_-보다",
        "desc": "https://wikidocs.net/92099#c",
        "cases": [
        ],
        "exception": []
    },
    {
        "name": "0092099d_보다",
        "desc": "https://wikidocs.net/92099",
        "cases": [
            [f"두고보(다)", "두고 보(다)"],
            [f"\\b미루어보아\\b", "미루어 보아"]
        ],
        "exception": []
    },
    {
        "name": "0092099g_복합어인 본 용언의 활용형이 3음절 이상인 것과 보조 용언 ‘보다’의 띄어쓰기",
        "desc": "https://wikidocs.net/92099#g",
        "cases": [
            [f"\\b({KW_NAz})[ ]?[해헤](보[고는며면지]\\w*|보[겠았]다[고는며면]\\w*|보자|[볼봐봤]\\w*|본다[고는며면]\\w*|본|봄[도은을이]?|봄으로\\w*)\\b",
             "()해 ()"],
            [f"\\b({KW_NAz})[ ]?해(보[겠았]다|보[겠았]습니다|본다|봅[니시]다)[.]", "()해 ()."],
            [f"\\b({KW_NAz})[ ]?해본[ ]?(다음|바|적|후)", "()해 본 ()"],
            [f"\\b(나타내)(보겠다|보겠습니다|본다|봅[니시]다)[.]", "() ()."],
            [f"\\b([가-힣]{{2,}}화)[ ]?해(보[고는며면지]\\w*|[볼봐봤]\\w*|본다[고는며면]\\w*|본|봄[도은을이]?|봄으로\\w*)\\b", "()해 ()"],
            [f"\\b([가-힣]{{2,}}화)[ ]?해(본다|봅[니시]다)[.]", "()해 ()"],
            [f"\\b(곱씹어|돌이켜)(보[고는며면지]\\w*|[본볼봅봐봤]\\w*|봄[도은을이]?|봄으로\\w*)\\b", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0092099h_‘보이다’의 띄어쓰기",
        "desc": "https://wikidocs.net/92099#h",
        "cases": [
            [f"\\b(나빠|못나|밝아|작아|좋아)(보여[도서요]?|보이는|보인다|보일)", "() ()"],
            [f"\\b(어려|없어|예뻐|있어|커)(보여[도서요]?|보이는|보인다|보일)", "() ()"],
            [f"\\b(쉬워|어두워|어려워)(보여[도서요]?|보이는|보인다|보일)", "() ()"],
            [f"\\b(날씬|둔|똑똑|뚱뚱|착)해(보여[도서요]?|보이는|보인다|보일)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0092101a_여러 번",
        "desc": "https://wikidocs.net/92101#a",
        "cases": [
            [f"여러번", "여러 번"]
        ],
        "exception": []
    },
    {
        "name": "0092101b_번째",
        "desc": "https://wikidocs.net/92101#b",
        "cases": [
            [f"\\b([첫두세네]) 번 째", "() 번째"]
        ],
        "exception": []
    },
    {
        "name": "0092101c_-째",
        "desc": "https://wikidocs.net/92101#c",
        "cases": [
            [f"\\b([첫둘세]|몇 [년달주]) 째", "()째"]
        ],
        "exception": []
    },
    {
        "name": "0093276_어느/어떤",
        "desc": "https://wikidocs.net/93276",
        "cases": [
            [f"어느(것|날|정도)", "어느 ()"],
            [f"어떤날", "어떤 날"],
            [f"\\b어느 (새|덧)", "어느()"]
        ],
        "exception": []
    },
    {
        "name": "0093276d_어느/어떤",
        "desc": "https://wikidocs.net/93276#d",
        "cases": [
            [f"\\b그[ ]?어느때[ ]?({KJ_C})({KJ_I})\\b", "그 어느 때()()"],
            [f"\\b(?<!그 )([어여]느)때", "() 때"]
        ],
        "exception": []
    },
    {
        "name": "0093834_한차례 / 한 차례",
        "desc": "https://wikidocs.net/93834",
        "cases": [
            [f"\\b(두|세)(차례)", "() ()"]
        ],
        "exception": [f"한차례"]
    },
    {
        "name": "0094354a_‘시(時)’를 앞말과 띄어 써야 하는 것",
        "desc": "https://wikidocs.net/94354#a",
        "cases": [
            [f"\\b({KW_NA})시(|[가는도를의]|까지|마다|에[는도]?|조차)\\b", "() 시()"],
            [f"\\b(야근|부도|에러|[근업]무|장애|pivot)시(|[가는도를의]|까지|마다|에[는도]?|조차)\\b", "() 시()"],
            [f"\\b(공사)(착공)시", "() () 시"],
            [f"\\b(신규)(설치)시", "() () 시"],
            [f"\\b(객실)(만실)시", "() () 시"],
            [f"\\b(제휴)(카드)시", "() () 시"],
            [f"\\b(\\w+[를을]) (어길)시", "() () 시"]
        ],
        "exception": [f"중요시"]
    },
    {
        "name": "0094354b_‘시(時)’로 끝나는 단어",
        "desc": "https://wikidocs.net/94354#b",
        "cases": [
            [f"\\b(평상|유사|필요|비상) (시\\w*)", "()()"]
        ],
        "exception": []
    },
    {
        "name": "0094734a_잘되다",
        "desc": "https://wikidocs.net/94734#a",
        "cases": [
            [f"\\b(공부|농사|바느질|분해|사업|일|일반화|장사|집중|컴파일|학습|훈련|해독)([가는도은이]) 잘 (되[게겠]|되는|되도록|되어|되지|된|돼|됐)(\\w*)",
             "()() 잘()()"],
            [
                f"\\b(공부|농사|바느질|분해|사업|일|일반화|장사|집중|컴파일|학습|훈련|해독)([가는도은이]) (더|동일하게|부드럽게|쉽게) 잘 (되[게겠]|되는|되도록|되어|되지|된|돼|됐)(\\w*)",
                "()() () 잘()()"]
        ],
        "exception": []
    },
    {
        "name": "0094734b_잘 되다",
        "desc": "https://wikidocs.net/94734#b",
        "cases": [
            [f"\\b(과적합|파손)([이가]) 잘(되[게겠]|되는|되도록|되어|된|돼)(\\w*)", "()() 잘 ()()"]
        ],
        "exception": []
    },
    {
        "name": "0094734c_잘하다",
        "desc": "https://wikidocs.net/94734#c",
        "cases": [
            [f"\\b(기가 막히게) 잘 ([하한할함해했]\\w*)", "() 잘()"],
            [f"\\b잘 (해야 한다\\w*)", "잘()"]
        ],
        "exception": []
    },
    {
        "name": "0096346a_미-",
        "desc": "https://wikidocs.net/96346#a",
        "cases": [
            [f"\\b미 ({KW_NAO})", "미()"]
        ],
        "exception": []
    },
    {
        "name": "0096346d_비(非)-",
        "desc": "https://wikidocs.net/96346#d",
        "cases": [
            [f"\\b비 (공식|무장|상업|선형|업무|일관|생산|정상)([적]?)", "비()()"]
        ],
        "exception": []
    },
    {
        "name": "0100750a1_단위를 나타내는 명사",
        "desc": "https://wikidocs.net/100750#a",
        "cases": [
            [f"\\b(\\d+|수천)[ ]?({KW_NNC})(평|그릇|권|달|명|방울|벌|쌍|장|줄|쪽|통|루블|엔|원|위안)(|[도만은을의이])\\b", "()() ()()"],
            [f"\\b([맥소양청]주|사이다|주스|콜라)[ ]?({KW_NNK})([병잔])[ ]?(|만|더)[ ]?(다오|주게|주소|주세요|줄래|줘)\\b", "() () ()() ()"],
            [f"\\b([맥소양청]주|사이다|주스|콜라)({KW_NNK}) ([병잔])\\b", "() () ()"],
            [f"\\b(\\d+|수천)[ ]?({KW_NNC})(제곱미터|평방미터|가지|개|구|마리|박스|봉지|채|페이지|회|대|달러|리라|유로|페소)(|[가는도를만의])\\b", "()() ()()"],
            [f"\\b수[ ]?({KW_NND})({KW_NUS})(|[가는도를을이])\\b", "수() ()()"],
            [f"\\b({KW_NNA})({KW_NND})({KW_NUB})\\b", "()() ()"]
        ],
        "exception": [
            "사회",
            "이명",
            "일명",
            "조명",
            "조회"
        ]
    },
    {
        "name": "0100750a2_단위를 나타내는 명사",
        "desc": "https://wikidocs.net/100750#a",
        "cases": [
            [f"\\b({KW_NNK})(개|구|권|달|명|병|벌|쌍|잔|장|줄|통|채)([가는도를만에은을의이]|이다|조차|뿐\\w*|[으]?로\\w*)\\b", "() ()()"],
            [f"\\b({KW_NNK})(그릇|방울|가지|마리|박스|봉지|페이지)(\\w*)", "() ()()"],
            [f"\\b([다여일아열스서마쉰예백]?[두세네섯댓곱덟홉])(쪽)([가는도를만에은을의이]|이다|조차|뿐\\w*|[으]?로\\w*)\\b", "() ()()"],
            [f"\\b([물술]|[맥소양청]주|딱)[ ]?([한두세네])([병잔])[ ]?씩(|[도만에은을의이]|이다|조차|뿐\\w*|[으]?로\\w*)\\b", "() () ()씩()"],
            [f"\\b([물술]|[맥소양청]주|딱)[ ]?([한두세네])([병잔])[ ]?([도만에은을의이]|이다|조차|뿐\\w*|[으]?로\\w*)\\b", "() () ()()"],
            [f"\\b([물술]|[맥소양청]주|딱)([한두세네])([병잔])\\b", "() () ()"],
            [f"\\b([옷]|딱)[ ]?([한두세네])([벌])[ ]?(|씩)([도만에은을의이]|이다|조차|뿐\\w*|[으]?로\\w*)\\b", "() () ()()()"],
            [f"\\b([시])[ ]?([한두세네])([수편])[ ]?(|씩)([가는도를만에은을의이]|[이]?다|조차|뿐\\w*|[으]?로\\w*)\\b", "() () ()()()"],
        ],
        "exception": [
            "한쪽"
        ]
    },
    {
        "name": "0100750a21_단위를 나타내는 명사",
        "desc": "https://wikidocs.net/100750#a",
        "cases": [
            [f"\\b([다여일아열스서마쉰예백]?[한두네섯댓곱덟홉])대([가는도를만에은을의이]|이다|조차|뿐\\w*|[으]?로\\w*)\\b", "() 대()"],
            [f"\\b({KW_NTC})([가는도를이]?) 세대([가]?) (있\\w*)", "()() 세 대() ()"],
            [f"\\b({KW_NTC}) 세대(에|에 나눠) (타\\w*|탑승\\w*)", "() 세 대() ()"]
        ],
        "exception": [
        ]
    },
    {
        "name": "0100750a3_단위를 나타내는 명사",
        "desc": "https://wikidocs.net/100750#a",
        "cases": [
            [f"\\b(백|수) ({KW_NND}) ({KW_NU})({KJ})", "()() ()()"],
            [f"\\b(백|수)[ ]?({KW_NND})({KW_NU})[ ]?({KW_NTA})", "()() () ()"]
        ],
        "exception": []
    },
    {
        "name": "0100751b_‘건’의 띄어쓰기",
        "desc": "https://wikidocs.net/100751#b",
        "cases": [
            [f"\\b(그런|다른|아닌|없어진|작은|적은|적지 않은|짧은|많은|모든|큰)([건]\\w*)", "() ()"],
            [f"\\b([난잘]|[가-힣']+[간긴는란린은을인친]|떠난)(건데\\w*)(\\w*)", "() ()()"],
            [f"\\b(어느|어떤)(건)\\b", "() ()"],
            [f"(?<!건 )([될들말볼살쌀온올울줄클할]|\\w+[갈긴는던들릴빨뺄쁜운울올은을일줄킬탄한할힐])(건)\\b", "() ()"],
            [
                f"\\b(교정|굽어|깔|내다|내려다|넘겨|노려|눈여겨|눌러|달아|대|[되뒤]돌아|둘러|들여다|떠|뜯어|맛|몰라|물어|바라다|바라|살펴|손|스쳐|알아|얕|여쭈어|여쭤|엿|욕|지내|지켜|찔러|찾아|톺아|훑어|훔쳐)[ ]?본(건)\\b",
                "()본 ()"],
            [f"\\b(그려|나눠|[들먹읽입]어|만들어|비교해|써|따져)([ ]?본)(건)\\b", "()() ()"],
            [f"(?<=[를을] )([본])([건]\\w*)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0101425a_한눈에",
        "desc": "https://wikidocs.net/101425#a",
        "cases": [
            [f"\\b한 눈에", "한눈에"]
        ],
        "exception": []
    },
    {
        "name": "0102779a_총-",
        "desc": "https://wikidocs.net/102779#a",
        "cases": [
            [f"(\\w+)의 총 합", "()의 총합"]
        ],
        "exception": []
    },
    {
        "name": "0102779b_총 0",
        "desc": "https://wikidocs.net/102779#b",
        "cases": [
            [f"총([1-9]?[0-9]+)", "총 ()"]
        ],
        "exception": []
    },
    {
        "name": "0102929a_좀 더",
        "desc": "https://wikidocs.net/102929",
        "cases": [
            [
                f"좀더",
                "좀 더"
            ]
        ],
        "exception": []
    },
    {
        "name": "0102986c1_‘십수 년’",
        "desc": "https://wikidocs.net/102986#c",
        "cases": [
            [f"\\b십[ ]?수년", "십수 년"]
        ],
        "exception": []
    },
    {
        "name": "0102986e_‘천 년’",
        "desc": "https://wikidocs.net/102986#e",
        "cases": [
            [f"\\b(\\d+|[이삼사오육칠팔구])[ ]?천년", "()천 년"]
        ],
        "exception": []
    },
    {
        "name": "0102986f_‘연, 월, 일’ + ‘평균’",
        "desc": "https://wikidocs.net/102986#f",
        "cases": [
            [f"\\b([일월년]) (평균)]", "()()"]
        ],
        "exception": []
    },
    {
        "name": "0102986g_‘연, 월, 일’ + ‘급여, 매출, 소득, 수익’",
        "desc": "https://wikidocs.net/102986#g",
        "cases": [
            [f"\\b([일월년])(급여|매출|소득|수익)", "() ()"]
        ],
        "exception": [f"연매출증가율", "연소득대비대출금액비율", "연소득대비주택가격비율", "연수익률"]
    },
    {
        "name": "0102986h_년, 월, 일",
        "desc": "https://wikidocs.net/102986#h",
        "cases": [
            [f"\\b(\\d+년)(\\d+월)(\\d+일)", "() () ()"],
            [f"\\b(\\d+월)(\\d+일)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0102986i1_몇 년",
        "desc": "https://wikidocs.net/102986#i",
        "cases": [
            [f"\\b몇년", "몇 년"]
        ],
        "exception": []
    },
    {
        "name": "0102986i2_몇 월",
        "desc": "https://wikidocs.net/102986#i",
        "cases": [
            [f"\\b몇월", "몇 월"]
        ],
        "exception": []
    },
    {
        "name": "0102987a1_단위(통화)",
        "desc": "https://wikidocs.net/102987",
        "comment": "'만원 → 만 원'은 0102987b로 검사",
        "cases": [
            [f"\\b([1-9][0-9,]*)({KW_NNC})({KW_NUC})([ 가는를만에은을의이])\\b", "()() ()()"],
            [f"\\b({KW_NNA})({KW_NND})({KW_NUC})대", "()() ()대"]
        ],
        "exception": []
    },
    {
        "name": "0102987a2_단위(통화)",
        "desc": "https://wikidocs.net/102987",
        "comment": "'만원 → 만 원'은 0102987b로 검사",
        "cases": [
            [f"\\b({KW_NNC})({KW_NUC})([ 가는를만에은을의이])", "() ()()"]
        ],
        "exception": [f"구원", "사유로", "이원", "이유로", "일원", "만원", "오리라"]
    },
    {
        "name": "0102987b_단위(통화)",
        "desc": "https://wikidocs.net/102987",
        "comment": "만원 → 만 원",
        "cases": [
            [
                f"\\b(가격|가진 건|가진 것|값|금전|돈|물건값|매도가|매수가|비상금|비용|소비자가|수입가|쌈짓돈|용돈|원가|이자|인건비|잔고|정가|헌금)(|[가는도로만은이]|으로|이라고[는]?|이래[ ]?봐야) (|겨우 |고작 |단돈 )만원(\\w*)",
                "()() ()만 원()"],
            [f"\\b(계좌|손|수중|[안]?주머니|지갑|통장)(에[는]?) (|겨우 |고작 |단돈 )만원(\\w*)", "()() 만 원()"],
            [f"\\b(\\d{{,5}})만원[ ]?([에을]|가량\\w*|대\\w*|어치\\w*|짜리\\w*|쯤\\w*)\\b", "()만 원()"],
            [f"\\b만원[ ](정도)", "만 원 ()"],
            [f"(만|수[천]?억)원(대\\w*)", "() 원()"]
        ],
        "exception": []
    },
    {
        "name": "0103093a_수(의존명사)",
        "desc": "https://wikidocs.net/103093#a",
        "cases": [
            [f"\\b({KW_NAO}) 할수(\\w*)", "()할 수()"],
            [f"\\b({KW_NNK})[ ]?({KW_NU})일수[ ]?([가는도]\\b)", "() ()일 수()"],
            [f"(그럴|\\w*[ ]?[길낼는될들물볼살쓸알올을일풀할힐]) 수도(있\\w+)", "() 수도 ()"],
            [f"\\b([길낼될들물볼살쓸알줄풀할])( 수[도]?|수[도]? |수[도]?)([없있][는다어었으을]\\w*)", "(1) 수 (3)"],
            [f"\\b(그럴|내릴|[^안 ]+[길낼는될들물볼살쓸알줄을일풀할힐])( 수|수 |수)([없있])([는다을]\\w*|[어었으]\\w+)\\b", "(1) 수 (3)(4)"],
            [f"(\\w*[ ]?[길낼는될들럴물볼살쓸알줄을풀힐])(수 |수)([가는도]\\b)", "(1) 수(3)"],
            [f"(\\w*[ ]?[길낼는될들럴물볼살쓸알줄을풀힐])(수 |수)([가는도])(있\\w*)", "(1) 수(3) (4)"]
        ],
        "exception": []
    },
    {
        "name": "0103093a1_수(의존명사)",
        "desc": "https://wikidocs.net/103093#a",
        "cases": [
            [
                f"(\\w*)[ ]?일(수 |수)([가는도]\\b)",
                "(1)일 수(3)"
            ]
        ],
        "exception": [f"근무 일수", "출석 일수", "휴가 일수"]
    },
    {
        "name": "0103093b_-일 수 있다",
        "desc": "https://wikidocs.net/103093#b",
        "cases": [
            [
                f"\\b(곁들|기울|기죽|끓|내보|녹|누|덧붙|들|떠먹|맞붙|먹|모아들|물들|보|붙|삭|선보|속|숙|썩|애먹|욕보|장가들|절|정들|졸|죽|줄) 일[ ]?수[ ]?(있\\w+)",
                "()일 수 ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0104959c_관형어 + ‘점’",
        "desc": "https://wikidocs.net/104959#c",
        "cases": [
            [f"\\b(좋은|나쁜)점(|[과도만에을이]|이다|입니다)", "() 점()"],
            [f"\\b(배울|\\w*[되하]는|잘한|잘못한)점(|[과도만에을이]|이다|입니다)", "() 점()"]
        ],
        "exception": []
    },
    {
        "name": "0105111a1_격 조사의 띄어쓰기",
        "desc": "https://wikidocs.net/105111#a",
        "cases": [
            [f"({KW_NL})([ ]?들) ({KJ_C})\\b", "()()()"],
            [f"({KW_NNM}) 일[ ]?(것|경우|때)", "()일 ()"],
            [f"({KW_NP})([ ]?들) ({KJ_C})\\b", "()()()"],
            [f"(['][A-Za-z0-9가-힣_() ]+[']) ({KJ_CA})\\b", "()()"],
            [f"(['][A-Za-z0-9가-힣_() ]+[']) ({KJ_CC})\\b", "()()"],
            [f"(['][A-Za-z0-9가-힣_() ]+[']) ({KJ_CF})\\b", "()()"],
            [f"(['][A-Za-z0-9가-힣_() ]+[']) ({KJ_CG})\\b", "()()"],
            [f"(['][A-Za-z0-9가-힣_() ]+[']) ({KJ_CI})\\b", "()()"],
            [f"(['][A-Za-z0-9가-힣_() ]+[']) ({KJ_CL})\\b", "()()"],
            [f"(['][A-Za-z0-9가-힣_() ]+[']) ({KJ_CM})\\b", "()()"],
            [f"(['][A-Za-z0-9가-힣_() ]+[']) ({KJ_CO})\\b", "()()"],
            [f"(['][A-Za-z0-9가-힣_() ]+[']) ({KJ_CQ})\\b", "()()"],
            [f"(['][A-Za-z0-9가-힣_() ]+[']) ({KJ_CS})\\b", "()()"],
            [f"(['][A-Za-z0-9가-힣_() ]+[']) ({KJ_CT})\\b", "()()"],
            [f"(['][A-Za-z0-9가-힣_() ]+[']) ({KJ_I})\\b", "()()"],
            [f"(['][A-Za-z0-9가-힣_() ]+[']) (와|과|이[고면]|이랑|랑)\\b", "()()"],
            [f"([=}}]) ([가로이])\\b", "()()"],
            [f"([A-Za-z]+) ({KJ_C})[ ]?([는도만요은]|라도)\\b", "()()()"],
            [f"([A-Za-z]+|것|누구|무엇) 인지([,]|에 따라[서]?)", "()인지()"],
            [f"([A-Za-z][A-Za-z0-9_(]*[)]) (가|이|[으]?로) ({KW_NA})(\\w*)", "()() ()()"],
            [f"(\\d+) 으로 (설정\\w*)", "()으로 ()"],
            [f"(\\w+) 일[ ]?(것|경우|때)", "()일 ()"],
            [f"(\\w+[기널를릴을흴] 위해서) (다|이다|일 것 같\\w*|일 것이다|일 것입니다|일 수[는도]?|일지[는도]?|입니다)\\b", "()()"],
            [f"(\\w+성) 을\\b", "()을"],
            [f"<Noun> 였다.", "()였다."],
            [f"<Noun> 이다.", "()이다."],
            [f"<Noun> 임에도", "()임에도"],
            [f"\\b({KW_NAO}) ([전후]) (에도)", "() ()()"],
            [f"\\b(끝나|[가먹보오하])기[ ]?전 (까지[는]?|에도)\\b", "()기 전()"],
            [f"\\b({KW_NT}) ({KJ_CA})\\b", "()()"],
            [f"\\b({KW_NT}) ({KJ_CC})\\b", "()()"],
            [f"\\b({KW_NT}) ({KJ_CF})\\b", "()()"],
            [f"\\b({KW_NT}) ({KJ_CG})\\b", "()()"],
            [f"\\b({KW_NT}) ({KJ_CI})\\b", "()()"],
            [f"\\b({KW_NT}) ({KJ_CK})\\b", "()()"],
            [f"\\b({KW_NT}) ({KJ_CL})\\b", "()()"],
            [f"\\b({KW_NT}) ({KJ_CM})\\b", "()()"],
            [f"\\b({KW_NT}) ({KJ_CO})\\b", "()()"],
            [f"\\b({KW_NT}) ({KJ_CQ})\\b", "()()"],
            [f"\\b({KW_NT}) ({KJ_CT})\\b", "()()"],
            [f"\\b({KW_NT}) ({KJ_I})\\b", "()()"],
            [f"\\b({KW_NT})(대로) (다|이다|일 것 같\\w*|일 것이다|일 것입니다|일 수[는도]?|일지[는도]?|입니다)\\b", "()()()"],
            [f"\\b({KW_NTL}) (가|이) (동작|작동)({KC_H})(\\w*)", "()() ()()()"],
            [f"\\b({KW_NTf}) 이\\b", "()이"],
            [f"(?<=같은 )(.{{,10}}) ([가이]) (아닌)", "()() ()"],
            [f"\\b({KW_NTv}) 가\\b", "()가"],
            [f"\\b(공격|[비]?공식|방어|악의|인도|즉각|합법)적 인\\b", "()적인"],
            [f"\\b각 (사) (|를|에서|은|을|의)\\b", "각 ()()"]
        ],
        "exception": [f"객체 인지", "시각 인지", "아마존 고"]
    },
    {
        "name": "0105111a2_격 조사의 띄어쓰기",
        "desc": "https://wikidocs.net/105111#a",
        "cases": [
            [f"<Noun> 과 ", "()과 "],
            [f"<Noun> 와 ", "()와 "],
            [f"({KW_NTA}) ([과와])[ ]?(도)\\b", "()()()"],
            [f"(\\[[A-Za-z0-9]+,[ ]?[A-Za-z0-9]+,.*\\]) (과[는도만]?)\\b", "()()"]
        ],
        "exception": []
    },
    {
        "name": "0105111a3_격 조사의 띄어쓰기",
        "desc": "https://wikidocs.net/105111#a",
        "cases": [
            [f"([{{]\\w+[}}]) (처럼)\\b", "()()"],
            [f"<Noun> 처럼", "()처럼"]
        ],
        "exception": []
    },
    {
        "name": "0105111a4_격 조사의 띄어쓰기",
        "desc": "https://wikidocs.net/105111#a",
        "cases": [
            [f"\\b것 인가(|[이]?다)", "것인가()"],
            [f"({KW_NT})([ ]?들) ({KJ_C})\\b", "()()()"]
        ],
        "exception": []
    },
    {
        "name": "0105111a5_‘라고’(직접 인용을 나타내는 격 조사)의 띄어쓰기",
        "desc": "https://wikidocs.net/105111#a",
        "cases": [
            [f"([“\"‘'])(.*)([”\"’']) (라고)", "()()()라고"]
        ],
        "exception": []
    },
    {
        "name": "0105111a6_‘하고’(격 조사)의 띄어쓰기",
        "desc": "https://wikidocs.net/105111#a",
        "cases": [
            [f"\\b(나|너) (하고)([는도]?)\\b", "()()()"],
            [f"\\b({KW_NPJ}) (하고)([는도]?)\\b", "()()()"]
        ],
        "exception": []
    },
    {
        "name": "0105111b_보조사의 띄어쓰기",
        "desc": "https://wikidocs.net/105111#b",
        "cases": [
            [f"({KW_NL})([ ]?들) ({KJ_I})\\b", "()()()"],
            [f"({KW_NP})([ ]?들) ({KJ_I})\\b", "()()()"],
            [f"({KW_NT})([ ]?들) ({KJ_I})\\b", "()()()"],
            [f"([A-Za-z0-9]+) ({KJ_I})\\b", "()()"],
            [f"([^\\s]*[^로서]) (부터)\\s", "()()"],
            [f"(\\w+[는던은을])[ ]?(것) ({KJ_I})([는]?)\\b", "() ()()()"],
            [f"(사실|이유|말)(인 즉| 인즉) (^슨)", "(1)인즉(3)"],
            [f"(사실|이유|말)(인 즉| 인즉)[ ]?슨\\b", "(1)인즉슨"],
            [f"<Noun> 이라도", "()이라도"],
            [f"(\\w+[게더터지]) 라도", "()라도"],
            [f"(\\w+[을]) 지라도", "()지라도"],
            [f"\\b(여러 개) 일지라도\\b", "()일지라도"],
            [f"\\b({KW_NNA})({KW_NUS}) (까지)", "()()()"],
            [f"\\b(관해서|대해서|[A-Za-z]+로) (만)\\b", "()()"],
            [f"({KW_NT})[ ]?([였이]) 기 (때문\\w*)", "()()기 ()"]
        ],
        "exception": [
            "1만", "2만", "3만", "4만", "5만", "6만", "7만", "8만", "9만", "0만"
        ]
    },
    {
        "name": "0105111c_접속 조사의 띄어쓰기",
        "desc": "https://wikidocs.net/105111#c",
        "cases": [
            [f"\\b([A-Z가-힣]+) (이고)\\b", "()()"],
            [f"\\b(\\d+년)[ ]?(\\d+월)[ ]?(\\d+일)({KJ}) (이고)\\b", "() () ()()()"],
            [f"\\b(\\d+월)[ ]?(\\d+일)({KJ}) (이고)\\b", "() ()()()"],
            [f"\\b(\\d+일)({KJ}) (이고)\\b", "()()()"],
            [f"\\b(\\d+[년월일]) ({KJ})\\b", "()()()"]
        ],
        "exception": []
    },
    {
        "name": "0105111d1_조사 + 어미",
        "desc": "https://wikidocs.net/105111#d",
        "cases": [
            [f"\\b({KW_NT}) ([이]?)[ ]?(어야|지만|기 때문\\w*)\\b", "()()()"],
            [f"(\\w+) (이며|이므로|임을)\\b", "()()"],
            [
                f"\\b(\\w+)([가감값건것격곳구국그기도드딩락림명물별본분성소숏스아언열원장적점정질청체크터태텔학형]|까지|부터|에서|[^었했]는지|인지) (였다|였습니다|[이]?[다야]|[이]?었다|입니다)[.]",
                "()()()."],
            [f"(것|까닭|때문|이유|정도) (인지[를]?|인지부터)\\b", "()()"],
            [f"(크기가) (\\d+) (인 것\\w+)", "() ()()"],
            [f"<Noun> 야.", "()야."],
            [f"<Noun> 입니다.", "()입니다."],
            [f"\\b([A-Za-z0-9]+[^\\w\\d\\s]?|[0-9.]+%) ([이]?야|[이]?[었였]?다|입니다)[.]", "()()."],
        ],
        "exception": []
    },
    {
        "name": "0105111d2_조사 + 어미",
        "desc": "https://wikidocs.net/105111#d",
        "cases": [
            [f"\\b({KW_NNA}) 일[ ]?(때\\w*)", "()일 ()"],
            [f"\\b({KW_NNK}) ({KW_NU}) 일(?=[ ]?[것수])", "() ()일"],
            [f"\\b({KW_NNK}) 시[ ]?(까지|부터) ([이]?다)", "() 시()()"]
        ],
        "exception": [f"일 단위"]
    },
    {
        "name": "0105111f_어미(라고, 라는)의 띄어쓰기",
        "desc": "https://wikidocs.net/105111#f",
        "cases": [
            [f"([가-힣]+[A-Za-z0-9 (]+[)]) ([이]?라[는]?|[이]?라고[도]?)\\b", "()()"],
            [f"\\b({KW_NAOf}) [이]?(라[는]?|라고[도]?)\\b", "()이()"],
            [f"\\b({KW_NTAf}) [이]?(라[는]?|라고[도]?)\\b", "()이()"],
            [f"\\b({KW_Ff}) [이]?(라[는]?|라고[도]?)\\b", "()이()"],
            [f"\\b({KW_NAOv}) [이]?(라[는]?|라고[도]?)\\b", "()()"],
            [f"\\b({KW_NTAv}) [이]?(라[는]?|라고[도]?)\\b", "()()"],
            [f"\\b({KW_Fv}) [이]?(라[는]?|라고[도]?)\\b", "()()"]
        ],
        "exception": []
    },
    {
        "name": "0105111g_‘중(中)’과 조사의 띄어쓰기",
        "desc": "https://wikidocs.net/105111",
        "cases": [
            [f"\\b({KW_NAF})[ ]?중 (에\\w*|의|이|이란다|이란 말[도을] [거믿]\\w*|이[다라며지진]\\w*|인|인[데지]\\w*|일|일지[가는도를]?|일진)\\b",
             "() 중()"],
            [f"\\b({KW_NAO})[ ]?중 (에\\w*|의|이|이란다|이란 말[도을] [거믿]\\w*|이[다라며지진]\\w*|인|인[데지]\\w*|일|일지[가는도를]?|일진)\\b",
             "() 중()"],
            [f"\\b({KW_NX})[ ]?중 (에\\w*|의|이|이란다|이란 말[도을] [거믿]\\w*|이[다라며지진]\\w*|인|인[데지]\\w*|일|일지[가는도를]?|일진)\\b",
             "() 중()"],
            [f"\\b({KW_NY})[ ]?중 (에\\w*|의|이|이란다|이란 말[도을] [거믿]\\w*|이[다라며지진]\\w*|인|인[데지]\\w*|일|일지[가는도를]?|일진)\\b",
             "() 중()"],
            [f"(\\w+[는던])[ ]?중 (에\\w*|의|이|이란다|이란 말[도을] [거믿]\\w*|이[다라며지진]\\w*|인|인[데지]\\w*|일|일지[가는도를]?|일진)\\b", "() 중()"]
        ],
        "exception": [f"이란에", "이란을", "이란 선박"]
    },
    {
        "name": "0105112a_대(大)",
        "desc": "https://wikidocs.net/105112#a",
        "cases": [
            [
                f"\\b(뉴욕|서울|하버드|MIT) (대\\w*)",
                "()()"
            ],
            [f"\\b스탠[포퍼]드 대(?!학*)", "스탠퍼드대"]
        ],
        "exception": []
    },
    {
        "name": "0105112c_대(臺)",
        "desc": "https://wikidocs.net/105112#c",
        "cases": [
            [f"\\b(수천억|억) (대\\w*)", "()()"],
            [f"(만|수[천]?억)[ ]?원 (대\\w*)", "() 원()"],
            [f"([0-9]+)(번|점) 대(여서|였\\w*|의|이[고다며면지]|인|인데\\w*|입니다)\\b", "()()대()"]
        ],
        "exception": []
    },
    {
        "name": "0106580a_한 단어이므로 '같다/같은/같이'를 앞말과 붙여야 하는 것",
        "desc": "https://wikidocs.net/106580#a",
        "cases": [
            [f"\\b({KW_NTH}) (같[다은이])", "()()"],
            [f"\\b(하나) (같[다은이])", "()()"]
        ],
        "exception": []
    },
    {
        "name": "0106580b_형용사 '같다' 및 형용사의 활용형 '같은'",
        "desc": "https://wikidocs.net/106580#b",
        "cases": [
            [f"\\b({KW_NTA})(같다)\\b", "() ()"],
            [f"\\b({KW_NPA})(같다)\\b", "() ()"],
            [f"<Noun>같은", "() 같은"],
            [f"(\\w*[간갈긴길나날린릴본볼빤빨산살싼쌀온올운울은을인일잔잘준줄쥔쥘친칠킨킬한할])[ ]?것같은", "() 것 같은"],
            [f"([‘'].*한다[’'])(같[다은])\\b", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0106580c_'같이'(부사)",
        "desc": "https://wikidocs.net/106580#c",
        "cases": [
            [f"(\\w+)({KJ})같이\\b", "()() 같이"],
            [f"<Adverb>같이", "<Adverb> 같이"],
            [f"\\b({KW_B})같이", "() 같이"]
        ],
        "exception": []
    },
    {
        "name": "0106580d_'같이'(조사)",
        "desc": "https://wikidocs.net/106580#d",
        "cases": [
            [f"\\b(눈|앵두) 같이 ([희흰]\\w*|붉은)", "()같이 ()"],
            [f"\\b(얼음장) 같이 ([차찬]\\w*)", "()같이 ()"],
            [f"\\b(소) 같이 (일\\w+)", "()같이 ()"],
            [f"\\b(매일|새벽|촉새|총알) 같이", "()같이"],
            [f"(\\w*[간갈긴길나날린릴본볼빤빨산살싼쌀온올운울은을인일잔잘준줄쥔쥘친칠킨킬한할])[ ]?것 같이", "() 것같이"]
        ],
        "exception": []
    },
    {
        "name": "0106580e_'같이하다'",
        "desc": "https://wikidocs.net/106580#e",
        "cases": [
            [
                f"(\\w+[을를]) (같이) ([하할])",
                "() ()()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0106580f1_그같이/이같이/저같이",
        "desc": "https://wikidocs.net/106580#f",
        "cases": [
            [f"\\b([그이저]) (같이)\\b", "()()"]
        ],
        "exception": []
    },
    {
        "name": "0106580f2_그 같은 / 이 같은 / 저 같은",
        "desc": "https://wikidocs.net/106580#f",
        "cases": [
            [f"\\b([그이저])(같은)\\b", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0109301a_그때, 이때",
        "desc": "https://wikidocs.net/109301#a",
        "cases": [
            [f"\\b([그이]) 때(?!문)", "()때"]
        ],
        "exception": [
        ]
    },
    {
        "name": "0109301c_그 후",
        "desc": "https://wikidocs.net/109301#c",
        "cases": [
            [f"그후", "그 후"]
        ],
        "exception": []
    },
    {
        "name": "0109301d_그 다음",
        "desc": "https://wikidocs.net/109301#d",
        "cases": [
            [f"그 다음", "그다음"]
        ],
        "exception": []
    },
    {
        "name": "0109301g_OO 다음 날",
        "desc": "https://wikidocs.net/109301#g",
        "cases": [
            [f"\\b(결혼식|사건|생일|입시|입학|추석|크리스마스|연휴) 다음날", "() 다음 날"]
        ],
        "exception": []
    },
    {
        "name": "0109302a1_그 외",
        "desc": "https://wikidocs.net/109302#a",
        "cases": [
            [f"\\b그외", "그 외"]
        ],
        "exception": []
    },
    {
        "name": "0109302a2_‘이외’와 앞말의 띄어 쓰기",
        "desc": "https://wikidocs.net/109302#a",
        "cases": [
            [f"\\b([A-Za-z0-9]+)이외", "() 이외"]
        ],
        "exception": []
    },
    {
        "name": "0109302a3_‘이 외’로 띄어 써야 하는 경우",
        "desc": "https://wikidocs.net/109302#a",
        "cases": [
            [f"(^|\\w+[,] )이(외\\w+)", "()이 ()"],
            [f"(그리고|그러나|그런데) 이외(에\\w*|의)\\b", "() 이 외()"],
            [f"\\b({KW_NT})(이외\\w*)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0109302b_그중",
        "desc": "https://wikidocs.net/109302#b",
        "cases": [
            [f"\\b그 중\\b", "그중"],
            [f"그 중<JKB>", "그중<JKB>"]
        ],
        "exception": []
    },
    {
        "name": "0109302c_이 중",
        "desc": "https://wikidocs.net/109302#c",
        "cases": [
            [f"\\b이(중에서)", "이 ()"]
        ],
        "exception": []
    },
    {
        "name": "0109302h_그 당시",
        "desc": "https://wikidocs.net/109302#h",
        "cases": [
            [f"\\b그당시", "그 당시"]
        ],
        "exception": []
    },
    {
        "name": "0112009b1_보조 용언 ‘있다’를 띄어 써야 하는 것",
        "desc": "https://wikidocs.net/112009#b1",
        "cases": [
            [f"\\b({KW_NAOf1})(되어)(있\\w+)", "()() ()"],
            [f"\\b({KW_NAOf2})(되어|[돼해])(있\\w+)", "()() ()"],
            [f"\\b({KW_NAOf3})(되어|[돼해])(있\\w+)", "()() ()"],
            [f"\\b({KW_NAOh})(되어|[돼해])(있\\w+)", "()() ()"],
            [f"\\b({KW_NAOv2})(되어|[돼해])(있\\w+)", "()() ()"],
            [f"\\b({KW_NAOv3})(되어|[돼해])(있\\w+)", "()() ()"]
        ],
        "exception": []
    },
    {
        "name": "0112009b2_‘-고 있다’",
        "desc": "https://wikidocs.net/112009#b2",
        "cases": [
            [f"(\\w+[를을]) 하고(있\\w+)", "() 하고 ()"],
            [f"\\b([놀누먹믿보살싸쓰자울참]|[논득명밥정칭]하)고있(긴 한\\w*|노라니|는데|다|어\\w*|으\\w*|자니)", "()고 있()"],
            [f"\\b({KW_NAO})하고있(는데|다|어\\w*|으\\w*)", "()하고 있()"]
        ],
        "exception": []
    },
    {
        "name": "0112009b3_보조 용언 ‘있다’를 띄어 써야 하는 것",
        "desc": "https://wikidocs.net/112009#b3",
        "cases": [
            [f"\\b(\\w+[려타]나|\\w+[어]가|\\w+[겨러려어워해]져|잠들어)(있\\w+)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0112009b4_‘하고’(격 조사) + ‘있다’(동사)",
        "desc": "https://wikidocs.net/112009#b4",
        "cases": [
            [f"\\b(나|너)[ ]?하고(있\\w+)", "()하고 ()"],
            [f"\\b({KW_NP})[ ]?하고(있\\w+)", "()하고 ()"]
        ],
        "exception": []
    },
    {
        "name": "0112010a_-마다",
        "desc": "https://wikidocs.net/112010",
        "cases": [
            [f"\\b({KW_NA})([ ]?시) 마다\\b", "()()마다"],
            [f"\\b({KW_NAB})시 마다", "() 시마다"],
            [f"\\b({KW_NTA}) 마다", "()마다"],
            [f"\\b(\\d*)({KW_NU}) 마다", "()()마다"],
            [f"\\b(\\w*[는될릴올한할])[ ]?([시때]) 마다\\b", "() ()마다"],
            [f"\\b(하나) 마다", "()마다"]
        ],
        "exception": []
    },
    {
        "name": "0112010b_-당",
        "desc": "https://wikidocs.net/112010",
        "cases": [
            [f"\\b({KW_NTA}) ({KW_NN}) (개) 당", "() () ()당"],
            [f"\\b({KW_NP}) ({KW_NN}) (명) 당", "() () ()당"],
            [f"\\b(마리|시간|에피소드|프런트엔드|하나) 당\\b", "()당"]
        ],
        "exception": []
    },
    {
        "name": "0112399_매-/매",
        "desc": "https://wikidocs.net/112399",
        "cases": [
            [f"\\b매 (년|달|월|주|일|시간|분|초|번)", "매()"],
            [f"\\b매(경기|단계|수업|순간|스텝|학기|회계[ ]?연도)", "매 ()"]
        ],
        "exception": []
    },
    {
        "name": "0122735a_-주다",
        "desc": "https://wikidocs.net/122735#a",
        "cases": [
            [f"(건네|넘겨|놓아|도와|알아) ([주준줄줌줍줘줬]\\w*)", "()()"]
        ],
        "exception": []
    },
    {
        "name": "0131942a_정리 정돈",
        "desc": "https://wikidocs.net/131942#a",
        "cases": [
            [
                f"정리정돈",
                "정리 정돈"
            ]
        ],
        "exception": []
    },
    {
        "name": "0132090b_-군(群)",
        "desc": "https://wikidocs.net/132090#b",
        "cases": [
            [f"\\b(식물|아파트|어선|직업|크로이츠|호수|화산) 군(|별\\w*|[도은을이의]|에[서]?|으로|을|이다)\\b", "()군()"]
        ],
        "exception": []
    },
    {
        "name": "0132156_-고 싶다",
        "desc": "https://wikidocs.net/132156",
        "cases": [
            [
                f"(\\w*고)(\\w*싶[다은을])",
                "() ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0147195a1_‘적’(의존 명사)",
        "desc": "https://wikidocs.net/147195#a",
        "cases": [
            [f"\\b({KW_NAO})[ ]?한적", "()한 적"],
            [f"\\b({KW_NAO})해 본적", "()해 본 적"],
            [f"\\b(사귄|[남섬벗]긴|베낀|[꾸달때말벌빌살올울차]린|어릴|싼|쓴|[갚맞]은|어렸을|[벌쏘죽]인|찬|핀|[당]?한|[입찍]힌)적", "() 적"],
            [f"\\b({KW_NPJ})([는도를은을]?) (본)적", "() () 적"],
            [f"\\b(귀신|사람|기사|뉴스|[동]?영상|[남여]자) (본)적", "() () 적"],
            [f"(\\w+[를을]) (낸|본)적", "() () 적"]
        ],
        "exception": []
    },
    {
        "name": "0147195a2_‘적’(의존 명사)",
        "desc": "https://wikidocs.net/147195#a",
        "cases": [
            [f"\\b(아이|처녀)적(에)\\b", "() 적()"],
            [f"\\b(아이|처녀)적[ ]?(일)(을|이다)\\b", "() 적 ()()"]
        ],
        "exception": []
    },
    {
        "name": "0147195b_-적(的)",
        "desc": "https://wikidocs.net/147195",
        "cases": [
            [
                f"\\b(가급|국가|기술|무작위|문화|비교|사교|악의|예외|일반|전국|[불]?확정|[비]?효율) 적(|으로[서]?|이[었]?고|이다|이[며면]|이었\\w*|입니다|인|일|일지[도]?)\\b",
                "()적()"],
            [f"(과학|이론)적(사고방식|원리)", "()적 ()"],
            [f"\\b(데이터) 적(으로|인)", "()적()"]
        ],
        "exception": []
    },
    {
        "name": "0148530_상반된 의미의 두 단어가 합쳐진 단어",
        "desc": "https://wikidocs.net/148530",
        "cases": [
            [f"\\b국내 외", "국내외"],
            [f"\\b동 서양", "동서양"],
            [f"\\b송 수신", "송수신"],
            [f"\\b앞 뒤", "앞뒤"],
            [f"\\b위 아래", "위아래"],
            [f"\\b입 출력", "입출력"],
            [f"\\b장 단점", "장단점"],
            [f"\\b전 후반", "전후반"],
            [f"\\b직 간접", "직간접"],
            [f"가로 세로", "가로세로"],
            [f"아침 저녁", "아침저녁"],
            [f"오르락 내리락", "오르락내리락"],
            [f"이리 저리", "이리저리"]
        ],
        "exception": []
    },
    {
        "name": "0150492_1억 2345만 6789",
        "desc": "https://wikidocs.net/150492",
        "comment": "'만원 → 만 원'은 0102987b로 검사",
        "cases": [
            [f"\\b(\\d+)억(\\d+)만({KW_NUC})", "()억 ()만 ()"],
            [f"\\b(\\d+)만(\\d+)({KW_NUR})", "()만 ()()"],
            [f"\\b(\\d+)만({KW_NUC})어치", "()만 ()어치"],
            [f"\\b(\\d+)만(\\d+)({KW_NUC})(|[을이]|가량|이다|이었다|입니다|짜리)\\b", "()만 ()()()"],
            [f"\\b(\\d+)만(\\d+)({KW_NUS})(|[을이]|가량|이다|이었다|입니다|짜리)\\b", "()만 ()()()"],
            [f"\\b(\\d+)m(\\d+)cm", "()m ()cm"]
        ],
        "exception": [f"만원"]
    },
    {
        "name": "0150596a_‘-분’(접사)",
        "desc": "https://wikidocs.net/150596#a",
        "cases": [
            [f"\\b(남편|독자|친구|환자) 분([들]?)(|[도은을의이]|께서|에게)\\b", "()분()()"]
        ],
        "exception": []
    },
    {
        "name": "0150636_-짜리",
        "desc": "https://wikidocs.net/150636",
        "cases": [
            [f"\\b({KW_NND})[ ]?원 짜리", "() 원짜리"],
            [f"\\b몇[ ]?({KW_NND})[ ]?원 짜리", "몇() 원짜리"],
            [f"(\\d+)조[ ]?(\\d)천억[ ]?원 짜리", "()조 ()천억 원짜리"],
            [f"\\b(\\d+[ ]?)호 짜리", "()호짜리"],
            [f"얼마 짜리", "얼마짜리"]
        ],
        "exception": []
    },
    {
        "name": "0151398a_측",
        "desc": "https://wikidocs.net/151398",
        "cases": [
            [f"\\b({KW_NTC})측", "() 측"],
            [f"\\b({KW_NTN})측", "() 측"],
            [f"\\b({KW_NTO})측", "() 측"]
        ],
        "exception": []
    },
    {
        "name": "0151845a_-용",
        "desc": "https://wikidocs.net/151845",
        "cases": [
            [f"(그래프|레이블|모델|분석|사무|상업|서버|시스템|어린이|업무|연습|영업|참고|클라우드) 용(|으로\\w*)\\b", "()용()"]
        ],
        "exception": []
    },
    {
        "name": "0152226a_-내다",
        "desc": "https://wikidocs.net/152226#a",
        "cases": [
            [f"\\b(가려|골라|꺼|끄집어|나타|밀어|밝혀|알아|지어|짜|찾아|캐|펴|해) (내[고는지며]|[낸냄낼냈]\\w*)\\b", "()()"]
        ],
        "exception": []
    },
    {
        "name": "0152226b_들어내다",
        "desc": "https://wikidocs.net/152226#b",
        "cases": [
            [
                f"들어 내(다)",
                "들어내(다)"
            ]
        ],
        "exception": [
            "예를 들어",
            "만들어"
        ]
    },
    {
        "name": "0152226c_‘내다’를 앞말과 띄어 써야 하는 것",
        "desc": "https://wikidocs.net/152226#c",
        "cases": [
            [f"\\b({KW_NAOz})해(내는|내다)", "()해 ()"]
        ],
        "exception": []
    },
    {
        "name": "0152332_목적어 + ‘하다’(동사)",
        "desc": "https://wikidocs.net/152332",
        "cases": [
            [f"(\\w+[를을])([하한할함합해했]\\w*)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0152332a1_‘~하다’(동사)",
        "desc": "https://wikidocs.net/152332#a1",
        "cases": [
            [f"\\b({KW_NAB}) ([할함해]|한 [것뒤적후]|함으로[써]?)\\b", "()()"],
            [f"(?<![은큰한] )\\b({KW_NAO}) ([할함해]|하거나|하듯[이]?|하면|하면서[는도]?|한 [것뒤적후]|함으로[써]?)\\b", "()()"],
            [f"\\b({KW_NAB}) 할[ ]?(듯|수)\\b", "()할 ()"],
            [f"\\b({KW_NAO}) 할[ ]?(듯|수)\\b", "()할 ()"],
            [f"\\b({KW_NAB}) ([하한할합했][고겠기까는니다도래려며보본볼봐서습여였으을음이인일임입지]\\w*|해[도서]\\w*)", "()()"],
            [
                f"\\b({KW_NAO}) (하[고겠기는다던든려련며여였지]\\w*|한다\\w*|할|할[까래지]\\w*|함[으을이인일임입]\\w*|합니다\\w*|해[도서]\\w*|했[고겠기던습지으음을]\\w*)\\b",
                "()()"],
            [f"\\b({KW_NAO}) 한 ({KW_NTA})", "()한 ()"],
            [f"\\b({KW_NAB}) 해야\\b", "()해야"],
            [f"\\b({KW_NAO}) 해야\\b", "()해야"],
            [f"\\b({KW_BV}) ([하한할함합해했]\\w*)", "()()"]
        ],
        "exception": [f"교차 검증", "이야기", "얘기", "취급"]
    },
    {
        "name": "0152332a11_부사 + ~하다",
        "desc": "https://wikidocs.net/152332#a1",
        "cases": [
            [f"\\b(그렇게|급히|나쁘게|대충|좋게|천천히|특별히) ({KW_NAO}) 할[ ]?(듯|수)\\b", "() ()할 ()"],
            [f"\\b(그렇게|급히|나쁘게|대충|좋게|천천히|특별히) ({KW_NAO}) ([하한할합해했][고겠기까는니다도래려며보본볼봐서습여였으을음이인일임입지]\\w*)", "() ()()"],
            [f"\\b(그렇게|급히|나쁘게|대충|좋게|천천히|특별히) ({KW_NAO}) 한 ({KW_NTA})", "() ()한 ()"],
            [f"\\b(그렇게|급히|나쁘게|대충|좋게|천천히|특별히) ({KW_NAO}) 해야\\b", "() ()해야"]
        ],
        "exception": []
    },
    {
        "name": "0152332a2_‘~하다’(형용사)",
        "desc": "https://wikidocs.net/152332#a2",
        "cases": [
            [f"\\b({KS_Ag}) ([하한합했히]\\w*|할|할[까지]\\w*|함|함[도에은을의이]\\w*|해[도서]?|해[져졌지진질짐집]\\w*)\\b", "()()"],
            [f"\\b({KS_Ah}) ([하한합했히]\\w*|할|할[까지]\\w*|함|함[도에은을의이]\\w*|해[도서]?|해[져졌지진질짐집]\\w*)\\b", "()()"],
            [f"\\b({KS_VGa}) ([하한합했히]\\w*|할|할[까지]\\w*|함|함[도에은을의이]\\w*|해[도서]?|해[져졌지진질짐집]\\w*)\\b", "()()"],
            [f"\\b({KW_BA}) ([하한합했히]\\w*|할|할[까지]\\w*|함|함[도에은을의이]\\w*|해[도서]?|해[져졌지진질짐집]\\w*)\\b", "()()"],
            [f"\\b({KW_NS}) ([하한합했히]\\w*|할|할[까지]\\w*|함|함[도에은을의이]\\w*|해[도서]?|해[져졌지진질짐집]\\w*)\\b", "()()"]
        ],
        "exception": [f"실행 가능 해", "단순 함수군에서"]
    },
    {
        "name": "0152332a3_외래어 형용사 + ‘~하다’",
        "desc": "https://wikidocs.net/152332#a3",
        "cases": [
            [f"\\b(나이브|드레시|로맨틱) ([하한할합해했히]\\w*|함[도에은을의이]\\w*)\\b", "()()"],
            [f"\\b(네거티브|디테일|럭셔리|리드미컬|리얼|모던|스포티|시니컬|클래시컬|파워풀) ([하한할합해했히]\\w*|함[도에은을의이]\\w*)\\b", "()()"],
            [f"\\b(액티브|인터랙티브|포지티브) ([하한할합해했히]\\w*|함[도에은을의이]\\w*)\\b", "()()"]
        ],
        "exception": []
    },
    {
        "name": "0152332b_하다",
        "desc": "https://wikidocs.net/152332#b",
        "cases": [
            [f"(기반|기초|끝|방법|본보기|시작|원칙|참고)(로|으로)([하한할함해했]\\w*)", "()() ()"],
            [f"\\b([가굴놀물밀싸썰울졸쫄차]|[되]?돌)([리]?기는|[리]?긴)([하한할함해했]\\w*)", "()() ()"],
            [f"\\b([그이]대로|[그이]렇게) (하려[고]?)([하한할함해했]\\w*)", "() () ()"],
            [f"\\b([막먹박보빼자쪼찾치하]|먹이|보이|삼키|새기|쏠리|지키)(기는|긴)([하한할함해했]\\w*)", "()() ()"],
            [f"\\b({KW_NAO})하고[ ]?있(기는|긴)([하한할함해했]\\w*)", "()하고 있() ()"],
            [f"\\b([쓰])고[ ]?있(기는|긴)([하한할함해했]\\w*)", "()고 있() ()"],
            [f"\\b([맞싫좋]|예쁘)(기는|긴)([하한할함해했]\\w*)", "()() ()"],
            [f"\\b(날씬|착)하(기는|긴)([하한할함해했]\\w*)", "()하() ()"],
            [f"\\b({KW_VTC})(려[고]?)([하한할함해했]\\w*)", "()() ()"],
            [f"\\b(가|가르치|감싸|까|꾸|나|놀|누|따|먹으|받으|보|빨|사|살|쌀|쓰|쏘|쓸|알|입으|자|졸|주|차|추|파|하)(려[고]?)([하한할함해했]\\w*)", "()() ()"],
            [f"~도록하(다)", "~도록 하(다)"]
        ],
        "exception": []
    },
    {
        "name": "0152332b2_관형어 + 동작성 명사 + 하다",
        "desc": "https://wikidocs.net/152332#b2",
        "cases": [
            [f"\\b(나쁜|이상한) ({KW_NAO})([하한할함합해했]\\w*)", "() () ()"],
            [f"\\b(특별) ({KW_NAO})([하한할함합해했]\\w*)", "() () ()"]
        ],
        "exception": []
    },
    {
        "name": "0152332b3_명사 + 동작성 명사 + 하다",
        "desc": "https://wikidocs.net/152332#b3",
        "cases": [
            [f"\\b({KW_NX})([하한할함합해했]\\w*)", "() ()"],
            [f"\\b(바보|애|어린애) ({KW_NAO})([하한할함합해했]\\w*)", "() () ()"]
        ],
        "exception": []
    },
    {
        "name": "0152332c1_이야기하다",
        "desc": "https://wikidocs.net/152332#c",
        "cases": [
            [f"(\\w+라고) (이야기|얘기) ([하한할함합해했]\\w*)", "() ()()"]
        ],
        "exception": []
    },
    {
        "name": "0152332c2_‘이야기’를 수식하는 관형어가 있는 경우",
        "desc": "https://wikidocs.net/152332#c",
        "cases": [
            [f"\\b(긴|나쁜|무서운|슬픈|재미있는|좋은|짧은) (이야기)([하한할함합해했]\\w*)", "() () ()"]
        ],
        "exception": []
    },
    {
        "name": "0152332d1_부사어 뒤의 ‘하다’",
        "desc": "https://wikidocs.net/152332#d",
        "cases": [
            [f"(필요)로([하한할함합해했]\\w*)", "()로 ()"]
        ],
        "exception": []
    },
    {
        "name": "0152332d2_-하다(접사)",
        "desc": "https://wikidocs.net/152332#d",
        "cases": [
            [f"(\\w+[을를]) (가까이|달리) ({KC_H})(\\w*)", "() ()()()"]
        ],
        "exception": []
    },
    {
        "name": "0152332e_하여야",
        "desc": "https://wikidocs.net/152332#e",
        "cases": [
            [f"\\b(일) ([하])[ ]?(여야)\\b", "()()()"],
            [f"\\b({KW_NA}) ([하])[ ]?(여야)\\b", "()()()"]
        ],
        "exception": []
    },
    {
        "name": "0152332f_전제로 하다",
        "desc": "https://wikidocs.net/152332#f",
        "cases": [
            [f"\\b(\\w+)([를을]) (전제로)([하한할함합해했]\\w*)", "()() () ()"]
        ],
        "exception": []
    },
    {
        "name": "0152792a_-어하다",
        "desc": "https://wikidocs.net/152792",
        "cases": [],
        "exception": []
    },
    {
        "name": "0152792a_-어하다",
        "desc": "https://wikidocs.net/152792#a",
        "cases": [
            [f"\\b힘[ ]?들어 ([하한할함합해했]\\w*)", "힘들어()"]
        ],
        "exception": []
    },
    {
        "name": "0152792b_-고 싶어 하다",
        "desc": "https://wikidocs.net/152792#b",
        "cases": [
            [f"(\\w*고)[ ]?싶어({KC_H})(\\w*)", "() 싶어 ()()"]
        ],
        "exception": []
    },
    {
        "name": "0153204a_-듯이(어미)",
        "desc": "https://wikidocs.net/153204#a",
        "cases": [
            [f"\\b({KW_NAH})했 듯이", "()했듯이"]
        ],
        "exception": []
    },
    {
        "name": "0153204b_듯(의존 명사)",
        "desc": "https://wikidocs.net/153204#b",
        "cases": [
            [f"\\b({KW_NAH})[ ]?할듯\\b", "()할 듯"],
            [f"\\b({KW_NS})[ ]?할듯\\b", "()할 듯"],
            [f"\\b(미친)(듯)(|이)", "() ()()"]
        ],
        "exception": []
    },
    {
        "name": "0153204c_그럴듯하다",
        "desc": "https://wikidocs.net/153204#c",
        "cases": [
            [f"\\b(그럴듯) ([하한할함합했]\\w*)", "()()"],
            [f"\\b(그럴듯) 해(보[여였이인일]\\w*)", "()해 ()"]
        ],
        "exception": []
    },
    {
        "name": "0153676_‘-시키다’의 띄어쓰기",
        "desc": "https://wikidocs.net/153676",
        "cases": [
            [f"(\\w+)([가를을이]|에게) ({KW_NA}) (시[켜켰키킨킬킵]\\w*)", "()() ()()"],
            [f"(\\w+)([가를을이]|에게) ({KW_NA})[ ]?([(][A-Za-z0-9 ,:]*[)]) (시[켜켰키킨킬킵]\\w*)", "()() ()()()"],
            [f"(\\w+)([가를을이]|에게) ({KW_NA}) ([(][A-Za-z0-9 ,:]*[)])[ ]?(시[켜켰키킨킬킵]\\w*)", "()() ()()()"]
        ],
        "exception": []
    },
    {
        "name": "0153717a_-ㄹ 때(-을 때)",
        "desc": "https://wikidocs.net/153717",
        "cases": [
            [f"\\b(될|[가-앉알-힣]*[갈꿀끌날널낼둘들될럴를릴볼불쁠설실열울을일줄질칠클할힐])[때떄]", "() 때"],
            [f"\\b않될때", "안될 때"]
        ],
        "exception": []
    },
    {
        "name": "0153785a_-지다",
        "desc": "https://wikidocs.net/153785#a",
        "cases": [
            [
                f"\\b(값|건방) (지다|진)",
                "()()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0153785b_-어지다",
        "desc": "https://wikidocs.net/153785#b",
        "cases": [
            [f"(\\w+[겨궈뎌라러려매빠워세쳐춰]|\\w+[구기누루수추]어|까|망가) (져[서]?|지[거기니면]\\w*|[졌짐]\\w*|진|진다[고니면]?|질)\\b", "()()"],
            [f"(굴곡|굽이) (져[서]?|지[거기니면]\\w*|[졌짐]\\w*|진|진다[고니면]?|질)", "()()"],
            [f"\\b({KW_ASA}) (져[서]?|지[거기니면]\\w*|[졌짐]\\w*|진|진다[고니면]?|질)", "()()"],
            [f"\\b([끊넘떨멀벌엎짊째틀흩]|비뚤|이루|허물)어 (져[서]?|지[거기니면]\\w*|[졌짐]\\w*|진|진다[고니면]?|질)", "()어()"]
        ],
        "exception": [f"지니 계수"]
    },
    {
        "name": "0153785c_-해지다(‘-하여지다’의 준말)",
        "desc": "https://wikidocs.net/153785#c",
        "cases": [
            [f"\\b({KS_Ag}) (해[져졌지진질짐]\\w*|집니다)", "()()"],
            [f"\\b({KS_Ag})[ ]?해 ([져졌지진질짐]\\w*|집니다)", "()해()"],
            [f"\\b({KS_Ah}) (해[져졌지진질짐]\\w*|집니다)", "()()"],
            [f"\\b({KS_Ah})[ ]?해 ([져졌지진질짐]\\w*|집니다)", "()해()"],
            [f"\\b({KS_VGa}) (해[져졌지진질짐]\\w*|집니다)", "()()"],
            [f"\\b({KS_VGa})[ ]?해 ([져졌지진질짐]\\w*|집니다)", "()해()"],
            [f"\\b({KW_BVa}) (해[져졌지진질짐]\\w*|집니다)", "()()"],
            [f"\\b({KW_BVa})[ ]?해 ([져졌지진질짐]\\w*|집니다)", "()해()"],
            [f"\\b({KW_NS}) (해[져졌지진질짐]\\w*|집니다)", "()()"],
            [f"\\b({KW_NS})[ ]?해 ([져졌지진질짐]\\w*|집니다)", "()해()"]
        ],
        "exception": []
    },
    {
        "name": "0153785d_형용사 + ‘하다’",
        "desc": "https://wikidocs.net/153785#d",
        "cases": [
            [f"(궁금|급급)해 ([하한할함합해했]\\w*)", "()해()"]
        ],
        "exception": []
    },
    {
        "name": "0156008a_안되다",
        "desc": "https://wikidocs.net/156008#a",
        "cases": [
            [f"(공부|농사|안색)([가이]) 안 (돼|되어|된)(\\w*)", "()() 안()()"],
            [f"(공부|농사|안색)([가이]) 안 되[.]", "()() 안돼"],
            [f"(공부|농사|장사)([가이]) 잘 안 (돼|되어|된)(\\w*)", "()() 잘 안()()"],
            [f"(공부|농사|장사)([가이]) 잘 안 되[.]", "()() 잘 안돼."]
        ],
        "exception": []
    },
    {
        "name": "0156008b_안 되다",
        "desc": "https://wikidocs.net/156008#b",
        "cases": [
            [f"(?<=면)[ ]*(왜[ ]*안돼|왜안[ ]*돼)[?]", "왜 안 돼?"],
            [f"({KW_NAFf})이 안(되는|된)", "()이 안 ()"],
            [f"({KW_NAFv})가 안(되는|된)", "()가 안 ()"],
            [f"\\b({KW_NAO}) 안됨", "() 안 됨"],
            [f"({KW_NAOf})이 안(되\\w*)", "()이 안 ()"],
            [f"({KW_NAOv})가 안(되\\w*)", "()가 안 ()"],
            [f"(\\w*[어쳐해])(서는|선) 안([되된될됨됩돼됐]\\w*)", "()() 안 ()"],
            [f"\\b(가지|만지|변하|쓰|않으|\\w+되)면 안(돼|되는|된다[고는며면]?)\\b", "()면 안 ()"],
            [f"(몇|얼마)([ ]?\\w*) 안([되된될돼]\\w*)", "()() 안 ()"]
        ],
        "exception": []
    },
    {
        "name": "0156008b1_말도 안 되다",
        "desc": "https://wikidocs.net/156008#b",
        "cases": [
            [f"\\b(말)도 안(되[고는며지다]\\w*|된다|됩니다)", "()도 안 ()"]
        ],
        "exception": []
    },
    {
        "name": "0156008d_안",
        "desc": "https://wikidocs.net/156008#d",
        "cases": [
            [f"안([먹읽])(고|다|으[니면])", "안 ()()"],
            [f"안(지키)(고|다|니[까]?|면)", "안 ()()"]
        ],
        "exception": []
    },
    {
        "name": "0156799a_‘순(順)’을 앞말과 띄어 쓰는 경우",
        "desc": "https://wikidocs.net/156799#a",
        "cases": [
            [f"\\b만[ ]?나이순(|으로|이[고다며면지]\\w*|인[데]?|입니다)\\b", "만 나이 순()"],
            [f"\\b(많은)(순으로)\\b", "() ()"],
            [f"\\b({KW_NI}), ({KW_NI}), ({KW_NI})(순으로)", "(), (), () ()"]
        ],
        "exception": []
    },
    {
        "name": "0156799b_‘순(順)’으로 끝나는 단어",
        "desc": "https://wikidocs.net/156799#b",
        "cases": [
            [f"\\b(\\d+[ ]?)({KW_NU}) (가운데|중) (나이|날짜|몸무게|빈도|이름|크기|판매량) 순(으로)\\b", "()() () ()순()"],
            [f"\\b(\\w+)([는를은을]) (나이|날짜|몸무게|빈도|이름|크기|판매량) 순(이 아니[다라]|이다)\\b", "()() ()순()"],
            [f"\\b(가나다|내림차|도착|선착|신장|오름차|키) 순(|으로[나든]?)\\b", "()순()"],
            [f"\\b(나이|날짜|몸무게|빈도|이름|크기|판매량) 순(|으로[나든]?)\\b", "()순()"],
            [f"\\b(성별) 순(|으로[나든]?)\\b", "()순()"],
            [f"\\b(내림|오름) (차순)", "()()"],
        ],
        "exception": [
            "나이,",
            "날짜,",
            "이름,",
            "몸무게,",
            "빈도,",
            "성별,",
            "판매량,"
        ]
    },
    {
        "name": "0156799c_‘순(順)’을 앞말에 붙여 쓰는 경우",
        "desc": "https://wikidocs.net/156799#c",
        "cases": [
            [f"(?<!, )(재산|지지율|생년월일) 순(|으로)\\b", "()순()"]
        ],
        "exception": []
    },
    {
        "name": "0157188a_이전",
        "desc": "https://wikidocs.net/157188#a",
        "cases": [
            [f"\\b({KW_NT})의 이 전 ({KW_NT})", "()의 이전 ()"],
            [f"\\b이 전([의]?) ([계연]산) 결과", "이전() () 결과"]
        ],
        "exception": []
    },
    {
        "name": "0157188d_한자어 ‘이후’로 보아 붙여 쓰는 경우",
        "desc": "https://wikidocs.net/157188#d",
        "cases": [
            [f"\\b이 후 (벌어[지진]\\w*)", "이후 ()"],
            [f"\\b(\\d+시) 이 후(\\w*)", "() 이후()"]
        ],
        "exception": []
    },
    {
        "name": "0157188e_지시관형사와 명사로 보아 ‘이 후’로 띄어 쓰는 경우",
        "desc": "https://wikidocs.net/157188#e",
        "cases": [
            [f"(\\w+[는은]) 이후(의 일이다)", "() 이 후()"]
        ],
        "exception": []
    },
    {
        "name": "0158051a_~로부터",
        "desc": "https://wikidocs.net/158051#a",
        "cases": [
            [
                f"(\\w+)에게로[ ]?부터",
                "()로부터"
            ],
            [
                f"(\\w*[^게])로 부터",
                "()로부터"
            ]
        ],
        "exception": []
    },
    {
        "name": "0158051b_~에서부터",
        "desc": "https://wikidocs.net/158051#b",
        "cases": [
            [
                f"([^\\s]*[^로]) (부터)\\s",
                "()()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0158147a_'-당하다'를 앞말에 붙여 써야 하는 경우",
        "desc": "https://wikidocs.net/158147#a",
        "cases": [
            [f"(\\w+[^길쁜운은을인일의큰픈플한할] |\\b)(괴롭힘|놀림|따돌림|봉변|비웃음) (당[하한할해했]\\w*)", "()()()"],
            [f"(?<![길쁜운은을인일의큰픈플한할] )({KW_NAO}) (당[하한할해했]\\w*)", "()()"]
        ],
        "exception": []
    },
    {
        "name": "0158147b_'당하다'를 앞말과 띄어 써야 하는 경우",
        "desc": "https://wikidocs.net/158147#a",
        "cases": [
            [f"\\b(고통|사고)당({KC_H})(\\w+)", "() 당()()"],
            [f"(\\w+[길쁜운은을인일의큰픈플한할]) (거절|괴롭힘|놀림|따돌림|무시|봉변|비웃음|압제|이용|체포|침해|혹사)당({KC_H})(\\w+)", "()() 당()()"]
        ],
        "exception": []
    },
    {
        "name": "0158192_이상/이하/이내",
        "desc": "https://wikidocs.net/158192",
        "cases": [
            [f"([1-9][0-9]*|max|min)(미만|이[내상하]|초과)", "() ()"],
            [f"([1-9][0-9]*])([ ]?[개원일자])(미만|이[내상하]|초과)", "() ()"],
            [f"\\b({KW_NNK})[ ]?개(미만|이[내상하]|초과)", "() 개 ()"],
            [f"([1-9][0-9]*][ ]?년)([전후])", "() ()"],
            [f"\\b(\\d+)(m|년)이상", "()() 이상"],
            [f"\\b(\\d+억)원이상", "() 원 이상"]
        ],
        "exception": []
    },
    {
        "name": "0158193a_-팀",
        "desc": "https://wikidocs.net/158193#a",
        "cases": [
            [f"\\b(강|단일|선발|야구|혼성) (팀\\w+)", "()()"]
        ],
        "exception": []
    },
    {
        "name": "0158193b_팀",
        "desc": "https://wikidocs.net/158193#b",
        "cases": [
            [f"고객지원팀", "고객 지원 팀"],
            [f"\\b({KW_NTL})팀", "() 팀"],
            [f"\\b({KW_NTO})팀", "() 팀"],
            [f"\\b({KW_NTT})팀", "() 팀"],
            [f"\\b(전담|출전)팀", "() 팀"],
        ],
        "exception": []
    },
    {
        "name": "0158255a_'-잡다'를 앞말과 붙여야 하는 것",
        "desc": "https://wikidocs.net/158255#a",
        "cases": [
            [
                f"(흠) (잡[게고다아으은을지])",
                "()()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0158255b_'잡다'를 앞말과 띄어야 하는 것",
        "desc": "https://wikidocs.net/158255#b",
        "cases": [
            [
                f"(자리)(잡[게고다아으은을지])",
                "() ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0158739_-여",
        "desc": "https://wikidocs.net/158739",
        "cases": [
            [f"\\b([십백천만])여([건년명종줄]|차례)(?!간)", "()여 ()"],
            [f"\\b({KW_NNA})([십백천만]?)여([건년명종줄]|차례)(?!간)", "()()여 ()"],
            [f"\\b({KW_NNA})([십백천만]?)여([일주년])([ ]?간)", "()()여 ()간"],
            [f"\\b([\\d,]+)[ ]?여([개대])(|[가는를의])\\b", "()여 ()()"],
            [f"\\b(\\d+)여({KW_NUS})(|[을이]|가량|이다|이었다|입니다|짜리)\\b", "()여 ()()"]
        ],
        "exception": []
    },
    {
        "name": "0158830a_-짓다",
        "desc": "https://wikidocs.net/158830#a",
        "cases": [
            [f"(갈래|결론|결말|결정|관련|규정|농사|눈물|매듭|반|종결|죄|줄|척|축|특징|편|한숨|환|희) (지[어었으음을]\\w*|짓\\w+)", "()()"]
        ],
        "exception": []
    },
    {
        "name": "0158830b_짓다",
        "desc": "https://wikidocs.net/158830#b",
        "cases": [
            [f"\\b(구분|단정|떼|마무리|미소|연결|연관|이름|일단락|한정)(지[어었으음을]\\w*|짓\\w+)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0158830c_짝 짓다",
        "desc": "https://wikidocs.net/158830#c",
        "cases": [
            [f"\\b(짝)(지[어었으음을]\\w*|짓\\w+)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0158989d_OOO 님",
        "desc": "https://wikidocs.net/158989#d",
        "cases": [
            [f"\\b(\\w+)[(](.*?)[)](님\\w*)", "(1)((2)) (3)"]
        ],
        "exception": []
    },
    {
        "name": "0158989f_‘씨’",
        "desc": "https://wikidocs.net/158989#f",
        "cases": [
            [f"\\b({KW_NPF})(모)(씨)", "(1) (2) (3), (1)(2) (3)"]
        ],
        "exception": []
    },
    {
        "name": "0159357d_발",
        "desc": "https://wikidocs.net/159357#d",
        "cases": [
            [
                f"({KW_NNK})(발[을이]?) ([더]?[ ]?남[겨아았은]\\w*)",
                "() () ()"
            ],
            [
                f"({KW_NNK})(발) (\\w*[ ]?)(장전\\w+)",
                "() () ()()"
            ],
            [
                f"(총[알]?[을]?) ({KW_NNK})(발[을]?) (?=>[^맞쏘쏠쐈])",
                "() () ()"
            ],
            [
                f"(\\w*)({KW_NN})(발[을]?) ([맞쏘쏠쐈]\\w*)",
                "()() () ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0159939c_‘앞’을 띄어 써야 하는 것",
        "desc": "https://wikidocs.net/159939#c",
        "cases": [
            [f"\\b앞(장|절|항)(에서)", "앞 ()()"]
        ],
        "exception": []
    },
    {
        "name": "0159939e_‘앞’으로 시작하는 단어",
        "desc": "https://wikidocs.net/159939#e",
        "cases": [
            [f"\\b앞 (가림|뒤|마당|면|모습|무릎|바퀴|부분|사람|일|줄|쪽|차|표지)(|[가과는도를은을이]|까지|부터|에서\\w*|와[의]?)\\b", "앞()()"]
        ],
        "exception": []
    },
    {
        "name": "0159939f_‘앞’을 띄어 써야 하는 것",
        "desc": "https://wikidocs.net/159939#f",
        "cases": [
            [f"\\b앞(글자|방향)", "앞 ()"],
            [f"(아파트) 앞동", "() 앞 동"],
            [f"(집|학교|병원|회사|건물|빌딩|문)(앞)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0160386a_-게 하다",
        "desc": "https://wikidocs.net/160386#a",
        "cases": [
            [f"\\b(\\w+[게케])({KC_H})\\b", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0160575a_끼",
        "desc": "https://wikidocs.net/160575#a",
        "cases": [
            [
                f"\\b(한|두|네|다섯|여섯)(끼\\w*)",
                "() ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0160678_",
        "desc": "https://wikidocs.net/160861",
        "cases": [
            [
                f"나쁜짓",
                "나쁜 짓"
            ]
        ],
        "exception": []
    },
    {
        "name": "0160679a_-속",
        "desc": "https://wikidocs.net/160679#a",
        "cases": [
            [f"\\b(가슴|굴|마음|물) (속\\w*)", "()()"],
            [f"\\b[귀귓] (속\\w*)", "귓()"],
            [f"\\b[코콧] (속\\w*)", "콧()"],
            [f"\\b머리 속(에 떠오\\w*)", "머릿속()"]
        ],
        "exception": []
    },
    {
        "name": "0160679a1_바닷속, 핏속",
        "desc": "https://wikidocs.net/160679#a",
        "cases": [
            [f"\\b(바[다닷] 속|바다속)(|에|의)", "바닷속(2)"],
            [f"\\b([피핏] 속|피속)(|에|의)", "핏속(2)"]
        ],
        "exception": []
    },
    {
        "name": "0160679b_속",
        "desc": "https://wikidocs.net/160679#b",
        "cases": [
            [f"\\b(사회|상황|수풀)(속\\w*)", "() ()"],
            [f"\\b(두[피핏])(속\\w*)", "두피 (2)"]
        ],
        "exception": []
    },
    {
        "name": "0160679e_머릿속",
        "desc": "https://wikidocs.net/160679#b",
        "cases": [
            [f"(\\w+[을를]) 머리 속에 (그리\\w+)", "() 머릿속에 ()"],
            [f"머리 속(|[에의이]) (물음표|지우개)(\\w*)", "머릿속() ()()"]
        ],
        "exception": []
    },
    {
        "name": "0160680a_‘전(前)’으로 시작하는 단어",
        "desc": "https://wikidocs.net/160680#a",
        "cases": [
            [f"\\b전 (일|주|월|년도)(|[가는를만에은을이의]|까지|부터|[이]?면)\\b", "전()"]
        ],
        "exception": []
    },
    {
        "name": "0160680b_‘후(後)’로 끝나는 단어",
        "desc": "https://wikidocs.net/160680#b",
        "cases": [
            [f"\\b향 후", "향후"]
        ],
        "exception": []
    },
    {
        "name": "0160680c_전, 후",
        "desc": "https://wikidocs.net/160680#c",
        "cases": [
            [f"([0-9]+[ ]?[년])([전후])", "() ()"],
            [f"([0-9]+[-~][0-9]+[ ]?)({KW_NUT})([전후])", "()() ()"],
            [f"\\b(경기|시험)([전])(|[에의]|이나|이라든지)\\b", "() ()"],
            [f"\\b(경기|시험)([후])(|[에의]|나|라든지)\\b", "() ()"],
            [f"\\b({KW_NVk})(전에)", "() ()"],
            [f"\\b({KW_NAO})하기(전에)", "()하기 ()"]
        ],
        "exception": []
    },
    {
        "name": "0160681_때",
        "desc": "https://wikidocs.net/160861",
        "cases": [
            [f"\\b(고교|대학|\\w*학교)([때땐])\\b", "() ()"],
            [f"\\b(고종|만남|세트플레이|생방송|전쟁|임기|일제|정권|평가전|프리킥|슬럼프)([때땐])\\b", "() ()"],
            [f"\\b({KW_NAO})([때땐])\\b", "() ()"],
            [f"\\b({KW_NTv})([때땐])\\b", "() ()"],
            [f"(\\d+일)([때땐]\\w*)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0160870a_곳",
        "desc": "https://wikidocs.net/160870#a",
        "cases": [
            [f"({KW_PVT})(곳\\w*)", "() ()"],
            [f"({KW_PA})(곳\\w*)", "() ()"]
        ],
        "exception": [
            "때문"
        ]
    },
    {
        "name": "0160870b_이곳",
        "desc": "https://wikidocs.net/160870#b",
        "cases": [
            [f"\\b이 곳", "이곳"]
        ],
        "exception": [
            "때문"
        ]
    },
    {
        "name": "0161515a_사이",
        "desc": "https://wikidocs.net/161515#a",
        "cases": [
            [f"([가-힣]+)(사이)(|에서)\\b", "() ()()"],
            [f"\\b({KW_NNA})사이", "() 사이"]
        ],
        "exception": [f"그사이", "밤사이", "프사이"]
    },
    {
        "name": "0161110_단어와 단어는 띄어 쓴다",
        "desc": "https://wikidocs.net/161110",
        "cases": [
            [f" 같이<Noun> ", " 같이 <Noun> "],
            [f"(?=시 )(\\d+)({KW_NAO})", "() ()"],
            [f"({KW_NAO})되는({KW_BD})\\b", "()되는 ()"],
            [f"([0-9.]+[이가] 아닌)(\\d+)({KJ})", "() ()()"],
            [f"([A-Za-z0-9]+)({KJ})([A-Za-z0-9]+)({KJ})", "()() ()()"],
            [f"([A-Za-z0-9가-힣.]+[을를])({KW_NAO})({KC_H})\\b", "() ()()"],
            [f"([A-Za-z]+)([은는])({KW_ASN}) ({KW_NT})({KJ})", "()() () ()()"],
            [f"([가-힣]+)(['‘])(변화는.*)([’'])", "() ()()()"],
            [f"(\\S+)(으로)(\\w*할)수(|[가는도])\\b", "()() () 수()"],
            [f"(\\d+)(칸)(규모)(|[의])", "()() ()()"],
            [f"(\\w+)(에서)({KW_NAO})({KC_D})(\\w*)", "()() ()()()"],
            [f"(\\w+)(으로)({KW_NAF})(\\w*)", "()() ()()"],
            [f"(\\w+[는을인한할])(경우|[때땐])", "() ()"],
            [f"(\\w+[를을]) (누리게|받게|얻게|주게)([되된될됨됩돼됐]\\w*)", "() () ()"],
            [f"(\\w+[어서])(\\d+)(\\w+로)\\b", "() ()()"],
            [f"(\\w+다면)(\\w+[를을])", "() ()"],
            [f"(\\w+로)(인하여|인해)", "() ()"],
            [f"(\\w+의)([A-Za-z]+ [A-Za-z]+)([를을])", "() ()()"],
            [f"<Noun>교환권", "() 교환권"],
            [f"<Noun>와함께", "()와 함께"],
            [f"\\b({KW_BD})([A-Za-z]+) ([가-힣]+)({KJ})\\b", "() () ()()"],
            [f"\\b({KW_NAF})된({KW_NAO}) ({KW_NT})(|라고)", "()된 () ()()"],
            [f"\\b({KW_NAO})된([A-Za-z]+)", "()된 ()"],
            [f"\\b({KW_NNK}) ([번벌병잔])[ ]?씩더(\\w*)", "() ()씩 더()"],
            [f"\\b({KW_NNK}) ([번벌병잔])더(\\w*)", "() () 더()"],
            [f"\\b({KW_NT})([으]?로)({KW_NT})([를을])", "()() ()()"],
            [f"\\b({KW_NTAf})과(중앙 집중적)([인])", "()과 ()()"],
            [f"\\b({KW_NTAf})이({KW_NAO})([돼됐되된될됨됩]\\w*)", "()이 ()()"],
            [f"\\b([A-Za-z]+)와([A-Za-z]+)", "()와 ()"],
            [
                f"\\b([‘']?\\w+[’']?[,가과는를을은와이인]|\\w+[어여해]서|\\w+로[서써]|\\w+[에]?도|\\w+[는든면한])([‘'][A-Za-z0-9가-힣_() ]+[’'])([,가과란를을와의이]|[다라]는|[으]?로\\w*|[이]?다|[이]?라[고는며]?|[입]?니다| 위에서)\\b",
                "() ()()"],
            [f"\\b(\\w+[과와] 같이|\\w+지만|따라서)([A-Za-z0-9^]+)(|라는|의)\\b", "() ()()"],
            [f"\\b(골자|최소)로([하한할함합해했]\\w*)", "()로 ()"],
            [f"\\b(나쁘게|다시|달리|바꿔|작게|좋게|크게)(말[하한할함합해했]\\w*)", "() ()"],
            [f"\\b(눈에)([띄띈]\\w*)", "() ()"],
            [f"\\b(어떤)(식)({KJ})\\b", "() ()()"],
            [f"\\b(어찌)([되됐]든)", "() ()"],
            [f"\\b(어찌|이러다)(보[니면])", "() ()"],
            [f"\\b(타는)({KW_NTP})(까지\\w*)", "() ()()"]
        ],
        "exception": []
    },
    {
        "name": "0161110a1_사전에 한 단어로 올라 있는 것",
        "desc": "https://wikidocs.net/161110#a1",
        "cases": [
            [f"\\b가족 회의", "가족회의"],
            [f"\\b거듭 제곱", "거듭제곱"],
            [f"\\b광 케이블", "광케이블"],
            [f"\\b단[추춧] 구멍", "단춧구멍"],
            [f"\\b(등비|등차) (수열)", "()()"],
            [f"\\b메인 (보드|이벤트|타이틀)", "메인()"],
            [f"\\b비밀 번호", "비밀번호"],
            [f"\\b산 꼭대기", "산꼭대기"],
            [f"\\b(막대|선|원) 그래프", "()그래프"],
            [f"\\b메타 (단백질|데이터베이스)", "메타()"],
            [f"\\b집 값", "집값"],
            [f"\\b차 주전자", "찻주전자"],
            [f"\\b도둑 (맞[기아았은을음]\\w*)", "도둑()"],
            [f"\\b(쓸어) (내[려렸리린릴림립]\\w*)", "()()"],
            [f"\\b(와일드) (카드)", "()()"],
            [f"\\b(작은|큰) (따옴표)", "()()"],
            [f"\\b(충분|필요) (조건)", "()()"],
            [f"\\b(폭) (넓[다은])", "()()"]
        ],
        "exception": []
    },
    {
        "name": "0161110a31_단어와 단어는 띄어 쓴다(명사와 명사)",
        "desc": "https://wikidocs.net/161110#a3",
        "cases": [
            [f"(?<=\\s간의) (전력)차", "() 차"],
            [f"(C/C[+][+])(언어)", "(1) (2)"],
            [f"({KW_NTA})([A-Za-z]+[A-Za-z0-9_]*)", "() ()"],
            [
                f"([A-Za-z]+[A-Za-z0-9_]*|<[a-z]+[/]?>)(결과|개념|객체|규칙|기능|기반|내부|단계|블록|라벨|명령[어]?|메서드|문|방식|변수|설정|이벤트|인자|인잣값|전체|절|주소|쪽|칼럼|크기|클래스|탭|파일|패키지|필드|함수|헤더|현상|형태|환경)",
                "(1) (2)"],
            [f"\\b({KW_NNK})(기능|기반|블록|명령|방식|설정|인잣값|절|칼럼|파일)(|[은을이])\\b", "() ()()"],
            [f"\\b({KW_NNK})(결과|객체|단계|명령어|메서드|변수|이벤트|인자|크기|클래스|패키지|함수|형태)(|[가는를])\\b", "() ()()"],
            [f"([A-Za-z]+[A-Za-z0-9_]*\\([ ]?\\))(결과|메서드|함수)", "(1) (2)"],
            [f"([A-Za-z]+[A-Za-z0-9_]*)(모터 드라이버)", "(1) (2)"],
            [f"(\\[[A-Za-z]+\\]|[A-Za-z]+)(키)", "() ()"],
            [f"\\b([0-9]+[A-Za-z0-9.]*|최신)(버전)", "() ()"],
            [f"(\\w+)(때문|대신)(|[도만에]\\w*|이[다라며면]\\w*|입니다)\\b", "() ()()"],
            [f"\\b({KW_NTC})(번호|키)({KJ})\\b", "() ()()"],
            [f"\\b({KW_NTC})(용도)[ ]?([가는도]|로\\w*|였\\w*|이다|입니다|뿐\\w*)", "() ()()"],
            [f"\\b({KW_NTO})({KW_NPR})([들]?)", "() ()()"],
            [f"\\b([XYZ]축)(거리)", "() ()"],
            [f"\\b([맥소양청]주|물|사이다|우유|음료수|주스|콜라)({KW_NNK}) ([병잔])(|[도만에을]|까지[는도]?|씩\\w*|조차)\\b", "() () ()()"],
            [f"\\b([비]?동기)(처리)", "() ()"],
            [f"\\b(\\w+) 중하나", "() 중 하나"],
            [f"\\b(가로|세로)(폭)", "() ()"],
            [f"\\b(가중치|실습|예제)(코드|파일)", "() ()"],
            [f"\\b(검색|게시|네트워크|등록|로그인|메모리|소스|속성|스타일|요소|입력|접근성|테스트 케이스)(폼|탭)", "() ()"],
            [f"\\b(계산)(비용)", "() ()"],
            [f"\\b(고객)(중심)", "() ()"],
            [f"\\b(과학기술|사업|전공|전문|활용)(분야)", "() ()"],
            [f"\\b(구인|채용)공고", "() 공고"],
            [f"\\b(기본)(개념)", "() ()"],
            [f"\\b(낮|아침)(기온)", "() ()"],
            [f"\\b(내|우리)(집)", "() ()"],
            [f"\\b(다음|마지막)(장|절)(\\w*)", "() ()()"],
            [f"\\b(단어|문자|문자소|바이트|서브워드|시간|음절|의미|형태소)(단위)", "() ()"],
            [f"\\b(디렉터리|칼럼|파일|폴더)(구조|내용|이름|형식)", "() ()"],
            [f"\\b(만든)(다음)", "() ()"],
            [f"\\b(명령)(프롬프트)", "() ()"],
            [f"\\b(메인)(함수)", "() ()"],
            [f"\\b(모델)(성능)", "() ()"],
            [f"\\b(모방)(작품)", "() ()"],
            [f"\\b(목표)(지점)", "() ()"],
            [f"\\b(문서)(요약)", "() ()"],
            [f"\\b(변환|실행)(결과|과정)", "() ()"],
            [f"\\b(보안)(이슈)", "() ()"],
            [f"\\b(뷰어|서버|클라이언트)(프로그램)", "() ()"],
            [f"\\b(블로그)(글)", "() ()"],
            [f"\\b(비단|헝겊)(자투리)", "() ()"],
            [f"\\b(사용)(예)", "() ()"],
            [f"\\b(세부)(전략)", "() ()"],
            [f"\\b소[수숫]점(이[상하])", "소수점 ()"],
            [f"\\b(분|초)(단위)", "() ()"],
            [f"\\b(신규)(가입|아이템|채용)", "() ()"],
            [f"\\b(신문)(기사)", "() ()"],
            [f"\\b(여백)(생성)", "() ()"],
            [f"\\b(열|전원|지진)(대책)", "() ()"],
            [f"\\b(요약문)(생성)", "() ()"],
            [f"\\b(이미지)(축소|표시|확대)", "() ()"],
            [f"\\b(일반)(가정|국민|사람|서민)([들]?)", "() ()()"],
            [f"\\b(일정)(기간)", "() ()"],
            [f"\\b(임시|전체)({KW_NTA})", "() ()"],
            [f"\\b(자기)(자신)", "() ()"],
            [f"\\b(전문)(강사)", "() ()"],
            [f"\\b(전자)(칠판)", "() ()"],
            [f"\\b(전쟁)(기간)", "() ()"],
            [f"\\b(그|생성|접근)(자체)({KJ})\\b", "() ()()"],
            [f"\\b(정부)(기관)", "() ()"],
            [f"\\b(제품)(홍보)", "() ()"],
            [f"\\b(제휴)(카드)", "() ()"],
            [f"\\b(주문)(수량)", "() ()"],
            [f"\\b(주변)(관계자)", "() ()"],
            [f"\\b(지식)(격차)", "() ()"],
            [f"\\b(채팅)[서써]버", "() 서버"],
            [f"\\b(청원)(데이터)", "() ()"],
            [f"\\b(최고)(등급)", "() ()"],
            [f"\\b(최상단)(요소)", "() ()"],
            [f"\\b(최종)(준비)", "() ()"],
            [f"\\b(클래스|인스턴스)(메서드)", "() ()"],
            [f"\\b(타입)(검사)", "() ()"],
            [f"\\b(파라미터|토픽)(수)", "() ()"],
            [f"\\b(탈북자)(문제)", "() ()"],
            [f"\\b(특이)(취향)", "() ()"],
            [f"\\b(표)(형식)", "() ()"],
            [f"\\b(한 가지)(더)", "() ()"],
            [f"\\b(한글|해당)(문서|정보)", "() ()"],
            [f"\\b(회원)(관리)", "() ()"],
            [f"\\b딱한 ([명벌병잔])(|[도만에을]|까지[는도]?|씩\\w*|조차)\\b", "딱 한 ()()"]
        ],
        "exception": []
    },
    {
        "name": "0161110a32_단어와 단어는 띄어 쓴다(명사와 명사)",
        "desc": "https://wikidocs.net/161110#a3",
        "cases": [
            [f"\\b(개발자|학급)회의", "() 회의"],
            [f"\\b({KW_NTA})(조합)", "() ()"],
            [f"\\b({KW_NUT})에({KW_NAO})([를을])", "()에 ()()"],
            [f"\\b({KW_NTC})({KW_NAO})({KJ})", "() ()()"],
            [f"\\b(데이터|이론)(설명|시각화)", "() ()"]
        ],
        "exception": [f"기계학습", "데이터분석", "도입"]
    },
    {
        "name": "0161110a33_단어와 단어는 띄어 쓴다(명사와 명사)",
        "desc": "https://wikidocs.net/161110#a3",
        "cases": [
            [f"([A-Za-z]+)({KW_NTA})", "() ()"],
            [f"([A-Za-z0-9_]*[A-Za-z0-9])({KW_NA})", "() ()"]
        ],
        "exception": [f"인가", "회의", "\\n", "%28", "화"]
    },
    {
        "name": "0161110a34_단어와 단어는 띄어 쓴다(명사와 명사)",
        "desc": "https://wikidocs.net/161110#a3",
        "cases": [
            [f"\\b({KW_NNK})(문)(|[은을이])\\b", "() ()()"]
        ],
        "exception": [f"한문"]
    },
    {
        "name": "0161110a4_의존 명사 ‘등(等)’",
        "desc": "https://wikidocs.net/161110#a4",
        "cases": [
            [f"([A-Za-z_]+)(등)(|[에은을의]|으로\\w*|[이인일입]\\w*)\\b", "() ()()"],
            [f"\\b({KW_NAO})등(|[에은을의이])\\b", "() 등()"],
            [f"\\b({KW_NT}), ({KW_NT})(등|등등)", "(1), (2) (3)"],
            [f"\\b({KW_NT})(등|등등) (각종|다양하게|다양한|많은|여러 가지|여러|잡다한)", "() () ()"],
            [f"\\b({KW_NT})등([에은의]|으로\\w*|[이인일입]\\w*)\\b", "() 등()"],
            [f"\\b({KW_NT})등을(?! [두둔둘둠둡둬뒀])", "() 등을"],
            [f"\\b(공지)(글)(등)", "() () ()"],
            [f"\\b({KW_NTL})(등)", "() ()"],
            [f"\\b({KW_NTO})(등)", "() ()"]
        ],
        "exception": [f"동등"]
    },
    {
        "name": "0161110b1_단어와 단어는 띄어 쓴다(부사와 형용사)",
        "desc": "https://wikidocs.net/161110#b",
        "cases": [
            [f"({KW_BD})[ ]?({KW_BD})({KW_A})", "() () ()"],
            [f"\\b({KW_BM})({KW_A})", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0161110b2_단어와 단어는 띄어 쓴다(부사와 부사)",
        "desc": "https://wikidocs.net/161110#b",
        "cases": [
            [f"({KW_BD})({KW_B})", "() ()"],
            [f"({KW_BD})못[ ]?({KW_VIn})", "() 못 ()"],
            [f"다함께", "다 함께"]
        ],
        "exception": []
    },
    {
        "name": "0161110c1_단어와 단어는 띄어 쓴다(형용사 + 명사)",
        "desc": "https://wikidocs.net/161110#c",
        "comment": "‘긴, 낮은, 넓은, 높은, 작은, 좁은, 큰’은 따로 검사",
        "cases": [
            [f"\\b({KW_ASN})({KW_NAF})({KJ})", "() ()()"],
            [f"\\b([그이저]런|[다빠]른|느린|[비]?싼|아름다운|무서운|[같많적좋짧]은|거친|거대한|불량한|비슷한|[강약]한|이상한|친절한|저렴한|[간불]?편한|양호한)({KW_NTA})",
             "() ()"],
            [f"\\b([그이저]런|[다빠]른|느린|[비]?싼|아름다운|무서운|[같많적좋짧]은|거친|거대한|불량한|비슷한|[강약]한|이상한|친절한|저렴한|[간불]?편한|양호한)({KW_NAO})",
             "() ()"],
            [f"\\b(재미있는|재밌는)({KW_NTE})", "() ()"],
            [f"\\b(맛[없있]는)({KW_NTF})", "() ()"],
            [f"\\b({KW_B}) ({KW_ASN})({KW_NTM})({KJ})", "() () ()()"]
        ],
        "exception": []
    },
    {
        "name": "0161110c2_형용사 ‘긴’과 명사의 띄어쓰기",
        "desc": "https://wikidocs.net/161110#c",
        "comment": "사전에 ‘긴’으로 시작하는 단어가 실렸는지 확인할 것",
        "cases": [
            [f"\\b긴({KW_NTA})", "긴 ()"],
            [f"\\b긴({KW_NAO})", "긴 ()"]
        ],
        "exception": [f"긴가민가", "긴가지", "긴관", "긴급", "긴긴", "긴꼬리", "긴꽃", "긴나라", "긴날", "긴네모", "긴다리", "긴담", "긴뜨기", "긴말", "긴맥",
                      "긴머리", "긴무", "긴밀", "긴바늘", "긴바지", "긴병", "긴뼈", "긴살", "긴소리", "긴소매", "긴수염", "긴아리랑", "긴잎", "긴지름", "긴축",
                      "긴치마", "긴코", "긴팔", "긴요"]
    },
    {
        "name": "0161110c3_형용사 ‘낮은’과 명사의 띄어쓰기",
        "desc": "https://wikidocs.net/161110#c",
        "comment": "사전에 ‘낮은’으로 시작하는 단어가 실렸는지 확인할 것",
        "cases": [
            [f"\\b낮은({KW_NTA})", "낮은 ()"],
            [f"\\b낮은({KW_NAO})", "낮은 ()"]
        ],
        "exception": [f"낮은말", "낮은숲", "낮은음", "낮은청", "낮은홀소리"]
    },
    {
        "name": "0161110c4_형용사 ‘넓은’과 명사의 띄어쓰기",
        "desc": "https://wikidocs.net/161110#c",
        "comment": "사전에 ‘넓은’으로 시작하는 단어가 실렸는지 확인할 것",
        "cases": [
            [f"\\b넓은({KW_NTA})", "넓은 ()"],
            [f"\\b넓은({KW_NAO})", "넓은 ()"]
        ],
        "exception": [f"넓은귀", "넓은끌", "넓은도랑", "넓은딱지", "넓은잎", "넓은잔대"]
    },
    {
        "name": "0161110c5_형용사 ‘높은’과 명사의 띄어쓰기",
        "desc": "https://wikidocs.net/161110#c",
        "comment": "사전에 ‘높은’으로 시작하는 단어가 실렸는지 확인할 것",
        "cases": [
            [f"\\b높은({KW_NTA})", "높은 ()"],
            [f"\\b높은({KW_NAO})", "높은 ()"]
        ],
        "exception": [f"높은밥", "높은음", "높은이랑", "높은청", "높은홀소리"]
    },
    {
        "name": "0161110c6_형용사 ‘작은’과 명사의 띄어쓰기",
        "desc": "https://wikidocs.net/161110#c",
        "comment": "사전에 ‘작은’으로 시작하는 단어가 실렸는지 확인할 것",
        "cases": [
            [f"\\b작은({KW_NTA})", "작은 ()"],
            [f"\\b작은({KW_NAO})", "작은 ()"]
        ],
        "exception": []
    },
    {
        "name": "0161110c7_형용사 ‘좁은’과 명사의 띄어쓰기",
        "desc": "https://wikidocs.net/161110#c",
        "comment": "사전에 ‘좁은’으로 시작하는 단어가 실렸는지 확인할 것",
        "cases": [
            [f"\\b좁은({KW_NTA})", "좁은 ()"],
            [f"\\b좁은({KW_NAO})", "좁은 ()"]
        ],
        "exception": [f"좁은가슴", "좁은골반", "좁은잎"]
    },
    {
        "name": "0161110c8_형용사 ‘큰’과 명사의 띄어쓰기",
        "desc": "https://wikidocs.net/161110#c",
        "comment": "사전에 ‘큰’으로 시작하는 단어가 실렸는지 확인할 것",
        "cases": [
            [f"\\b큰({KW_NTA})", "큰 ()"],
            [f"\\b큰({KW_NAO})", "큰 ()"]
        ],
        "exception": [f"큰고래", "큰골", "큰골발", "큰곰", "큰기러기", "큰기침", "큰길", "큰누나", "큰누님", "큰대", "큰돈"]
    },
    {
        "name": "0161110c9_관형사 ‘새’와 명사의 띄어쓰기",
        "desc": "https://wikidocs.net/161110#c",
        "cases": [
            [f"\\b새(창)", "새 ()"]
        ],
        "exception": []
    },
    {
        "name": "0161110d_단어와 단어는 띄어 쓴다(관형어 + 의존 명사)",
        "desc": "https://wikidocs.net/161110#d",
        "cases": [
        ],
        "exception": []
    },
    {
        "name": "0161110e_단어와 단어는 띄어 쓴다(관형어 + 명사)",
        "desc": "https://wikidocs.net/161110#d",
        "cases": [
            [f"(\\w*[는런한])([‘']\\w+[’'])({KJ})", "() ()()"],
            [f"\\b({KW_MV})([가-닣닥-맣박-힣][가-힣]*)", "() ()"],
            [f"\\b(어릴)(적부터)", "() ()"],
            [f"\\b(이런)({KW_NI})({KJ})", "() ()()"],
            [f"\\b(이런)({KW_NT})({KJ})", "() ()()"],
            [f"무슨<Noun>", "무슨 <Noun>"],
            [f"지지난주", "지지난 주"],
            [f"\\b({KW_NAO})[ ]?한뒤", "()한 뒤"],
            [f"\\b(알)(방법)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0161110g_단어와 단어는 띄어 쓴다(부사 + 명사)",
        "desc": "https://wikidocs.net/161110#g",
        "cases": [
            [f"\\b더이상", "더 이상"]
        ],
        "exception": []
    },
    {
        "name": "0161110h_단어와 단어는 띄어 쓴다(목적어 + 서술어)",
        "desc": "https://wikidocs.net/161110#h",
        "cases": [
            [f"(\\w+[를을])(\\w+기 위[하한할함합해했]\\w*|통[하한할함합해했]\\w*)\\b", "() ()"],
            [f"\\b({KW_NAOf})(위해)\\b", "()(을) ()"],
            [f"\\b({KW_NAOv})(위해)\\b", "()(를) ()"],
            [f"\\b(예를)(들어)\\b", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0162995a_‘중(中)’의 띄어쓰기",
        "desc": "https://wikidocs.net/162995#a",
        "cases": [
            [f"\\b({KW_NAF})중(|에\\w*|의|이|이란[다]?|이[다라며지진]\\w*|인|인[데지]\\w*|일|일지[가는도를]?|일진)\\b", "() 중()"],
            [f"\\b({KW_NAO})중(|에\\w*|의|이|이란[다]?|이[다라며지진]\\w*|인|인[데지]\\w*|일|일지[가는도를]?|일진)\\b", "() 중()"],
            [f"\\b({KW_NX})중(|에\\w*|의|이|이란[다]?|이[다라며지진]\\w*|인|인[데지]\\w*|일|일지[가는도를]?|일진)\\b", "() 중()"],
            [f"\\b({KW_NY})중(|에\\w*|의|이|이란[다]?|이[다라며지진]\\w*|인|인[데지]\\w*|일|일지[가는도를]?|일진)\\b", "() 중()"],
            [f"(\\w+[는던])중(|에\\w*|의|이|이란[다]?|이[다라며지진]\\w*|인|인[데지]\\w*|일|일지[가는도를]?|일진)\\b", "() 중()"]
        ],
        "exception": [f"이란에", "이란을", "이란 선박"]
    },
    {
        "name": "0162995b1_중",
        "desc": "https://wikidocs.net/162995#b",
        "cases": [
            [f"(\\w+)[ ]?들중(|에\\w*|의|이|이[다며지진]\\w*|인|인[데지]\\w*|일|일지[가는도를]?|일진)\\b", "()들 중()"],
            [f"\\b({KW_NLD})중(|에\\w*|의|이|이[다며지진]\\w*|인|인[데지]\\w*|일|일지[가는도를]?|일진)\\b", "() 중()"],
            [f"\\b({KW_NPJ})중(|에\\w*|의|이|이[다며지진]\\w*|인|인[데지]\\w*|일|일지[가는도를]?|일진)\\b", "() 중()"],
            [f"\\b({KW_NTA})중(|에\\w*|의|이|이[다며지진]\\w*|인|인[데지]\\w*|일|일지[가는도를]?|일진)\\b", "() 중()"],
            [f"\\b({KW_NTC})중(|에\\w*|의|이|이[다며지진]\\w*|인|인[데지]\\w*|일|일지[가는도를]?|일진)\\b", "() 중()"],
            [f"\\b({KW_NTM})중(|에\\w*|의|이|이[다며지진]\\w*|인|인[데지]\\w*|일|일지[가는도를]?|일진)\\b", "() 중()"],
            [f"\\b({KW_NTX})중(|에\\w*|의|이|이[다며지진]\\w*|인|인[데지]\\w*|일|일지[가는도를]?|일진)\\b", "() 중()"],
            [f"\\b(것|기간|오늘내일|오[전후]|[a-z-]+)중(|에\\w*|의|이|이[다며지진]\\w*|인|인[데지]\\w*|일|일지[가는도를]?|일진)\\b", "() 중()"]
        ],
        "exception": [f"군중", "그중", "다중", "도중", "마중", "수중", "와중", "집중", "청중"]
    },
    {
        "name": "0162995b2_수중, 수 중",
        "desc": "https://wikidocs.net/162995#b",
        "cases": [
            [f"(나열한|위의|여러) 수중(에[서]?)", "() 수 중()"]
        ],
        "exception": []
    },
    {
        "name": "0163080_안(內)",
        "desc": "https://wikidocs.net/163080",
        "cases": [
            [f"\\b(세포|시간)안(에)\\b", "() 안()"],
            [f"\\b({KW_NTA})(안) ({KW_NT})", "() () ()"],
            [f"\\b({KW_NTA})(안)({KJ})\\b", "() ()()"],
            [f"\\b([A-Za-z]+)(안)({KJ})\\b", "() ()()"]
        ],
        "exception": [f"A안", "B안", "C안", "1안", "2안", "3안", "방안"]
    },
    {
        "name": "0163511_‘값’, ‘지점’, ‘좌표’ 앞에 영문이 올 때의 띄어쓰기",
        "desc": "https://wikidocs.net/163511",
        "cases": [
            [f"\\b([A-Za-z]+\\w*)(값|지점|좌표)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0163540_‘형(形)’으로 끝나는 단어",
        "desc": "https://wikidocs.net/163540",
        "cases": [
            [f"\\b(타워) 형(|으로|의)\\b", "()형()"]
        ],
        "exception": []
    },
    {
        "name": "0163792_-사(社)",
        "desc": "https://wikidocs.net/163792",
        "cases": [
            [
                f"\\b(IBM) 사({KJ})",
                "()사()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0163793_‘전(全)’으로 시작하는 단어",
        "desc": "https://wikidocs.net/163793#a",
        "cases": [
            [f"\\b전 (교생)", "전()"]
        ],
        "exception": []
    },
    {
        "name": "0163809a_N 개",
        "desc": "https://wikidocs.net/163809#a",
        "cases": [
            [f"\\b([A-Za-z_]+[0-9]*)(개|개사)(|[가는도를]|에서\\w*|였\\w*|이다|입니다|의)\\b", "() ()()"]
        ],
        "exception": []
    },
    {
        "name": "0164323_맨",
        "desc": "https://wikidocs.net/164323",
        "cases": [
            [
                f"\\b맨(꼭대기|꼴지|끝|나중|뒤|마지막|먼저|아래|오른쪽|왼쪽|처음)",
                "맨 ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0164399b_관계 없다 / 관계없다, 관계 있다 / 관계있다, 상관 없다 / 상관없다, 상관 있다 / 상관있다",
        "desc": "https://wikidocs.net/0164399#b",
        "cases": [
            [
                f"(아무|별) (관계|상관)([없있]\\w*)",
                "() () ()"
            ],
            [
                f"(\\w+)({KJ}) (관계|상관) ([없있]\\w*)",
                "()() ()()"
            ]
        ],
        "exception": []
    },
    {
        "name": "0164408a_색상을 나타내는 말",
        "desc": "https://wikidocs.net/164408#a",
        "cases": [
            [f"(빨강|파랑|노랑)색", "()"]
        ],
        "exception": []
    },
    {
        "name": "0164408d_색상을 나타내는 말 - 붙여 쓰는 것",
        "desc": "https://wikidocs.net/164408#d",
        "cases": [
            [f"(검은) (건|건반|고니|곰팡이|깨|누룩곰팡이|돈|빛|손|자|자위|콩|팥|흙)({KJ})", "()()()"],
            [f"(검정) (개|고양이|깨|막|말|소|이|콩|학)({KJ})", "()()()"],
            [f"(노란) (곰팡이|불|빛|색|연두|잠자리)({KJ})", "()()()"],
            [f"\\b(분홍) (빛)", "()()"],
            [f"\\b(빨간) (불|빛|색|약)(|[도은을이])\\b", "()()()"],
            [f"\\b(빨간) (딱지|집모기)(|[가는도를])\\b", "()()()"],
            [f"(초록) (빛|색)({KJ})", "()()()"],
            [f"(파란) (불|빛|색)({KJ})", "()()()"],
            [f"(흰) (건|건반|곰|깨|나비|누룩|눈색|둥이|떡|말|머리|모래|무늬|밥|빛|색|소리|쌀|쌀밥|엿|옷|인|자|자위|죽|쥐|콩|토끼|팥|피톨|회색)({KJ})", "()()()"]
        ],
        "exception": []
    },
    {
        "name": "0164408e_색상을 나타내는 말 - 띄어 쓰는 것",
        "desc": "https://wikidocs.net/164408#e",
        "cases": [
            [f"(노[란랑]|녹색|빨[간강]|초록|파[란랑]|하얀)(머리|선|점|집)({KJ})\\b", "() ()()"],
            [f"(노[란랑]|녹색|빨[간강]|초록|파[란랑]|하얀)(머리|선|점|집)\\b", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0164486_재-",
        "desc": "https://wikidocs.net/164486",
        "cases": [
            [f"\\b재 (교육|기동|부팅|사용|설치|수용|시작|시험|작년|접근|정렬|편성|학습|흡수)", "재()"],
            [f"\\b재 ({KW_NAO})[ ]?([되된될돼됐하한할해했]\\w*)", "재()"]
        ],
        "exception": [
        ]
    },
    {
        "name": "0164881_정도",
        "desc": "https://wikidocs.net/164881",
        "cases": [
            [f"\\b(그|이)(정도\\w*)", "() ()"],
            [f"([0-9]+[%])(정도\\w*)", "() ()"],
            [f"([0-9]+)({KW_NUG})(정도\\w*)", "() ()"],
            [f"\\b([0-9]+[ ]?)({KW_NUT})(정도\\w*)", "()() ()"],
            [f"\\b({KW_NNK})[ ]?({KW_NUT})(정도\\w*)", "() () ()"],
            [f"\\b(못할)(정도)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0164985_-고 나서",
        "desc": "https://wikidocs.net/164985",
        "cases": [
            [f"(\\w+고)(나서)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0165221b_‘-ㄴ가/-ㄴ지’ + 조사",
        "desc": "https://wikidocs.net/165221#b",
        "cases": [
            [f"(\\w+)었(는[가지]) (이[었]?다|[였]\\w+)", "()()()"],
            [f"\\b({KW_NAO})하는 ([가지])({KJ})", "()하는()()"]
        ],
        "exception": []
    },
    {
        "name": "0165395_-투성이",
        "desc": "https://wikidocs.net/165395",
        "cases": [
            [f"<Noun> 투성이", "()투성이"]
        ],
        "exception": []
    },
    {
        "name": "0165553a_~ 나다",
        "desc": "https://wikidocs.net/165553#a",
        "cases": [
            [f"\\b(결정|구멍|냄새|땀내|배탈|윤|짜증|짜증|판가름|향기)([이가]?)([나날났]\\w*)", "()() ()"]
        ],
        "exception": []
    },
    {
        "name": "0165767b_바(의존명사)",
        "desc": "https://wikidocs.net/165767#b",
        "cases": [
            [f"({KW_MA})바({KJ})", "() 바()"],
            [f"({KW_MV})바({KJ})", "() 바()"],
            [f"({KW_MVn})바 (있\\w+)", "() 바 ()"]
        ],
        "exception": []
    },
    {
        "name": "0165945a_해 두다",
        "desc": "https://wikidocs.net/165945#a",
        "cases": [
            [f"\\b({KW_NAz})해(두[고는다었]\\w*|둔다[고는지며]\\w*|[두둔둘둠둡둬뒀]\\w*)", "()해 ()"]
        ],
        "exception": [f"많은", "작은", "큰"]
    },
    {
        "name": "0165945b_해 두다",
        "desc": "https://wikidocs.net/165945#b",
        "cases": [
            [f"(많은|큰) ({KW_NAO})(해[ ]?)([두둔둘둠둡둬뒀]\\w*)", "() () ()()"]
        ],
        "exception": []
    },
    {
        "name": "0166234a_곧이어",
        "desc": "https://wikidocs.net/166234#a",
        "cases": [
            [f"\\b곧 이어\\b(?! 나[가간갈갔])", "곧이어"]
        ],
        "exception": []
    },
    {
        "name": "0166639a_여러",
        "desc": "https://wikidocs.net/166639#a",
        "cases": [
            [f"\\b여러(개|명|사람)", "여러 ()"]
        ],
        "exception": []
    },
    {
        "name": "0166639b_여러모로",
        "desc": "https://wikidocs.net/166639#b",
        "cases": [
            [f"\\b여러 모로", "여러모로"]
        ],
        "exception": []
    },
    {
        "name": "0166639c1_여러분(이인칭 대명사)",
        "desc": "https://wikidocs.net/166639#c",
        "cases": [
            [f"\\b({KW_NPJ}) 여러 분(|[에은을이]|에게|께[서]?)\\b", "() 여러분()"],
            [f"\\b({KW_NPN}) 여러 분(|[에은을이]|에게|께[서]?)\\b", "() 여러분()"],
            [f"^여러 분[,!]?", "여러분,"]
        ],
        "exception": []
    },
    {
        "name": "0166664a_한마디",
        "desc": "https://wikidocs.net/166664#a",
        "cases": [
            [f"\\b한 마디로 (말해[도서]?|말하[자]?면)\\b", "한마디로 ()"],
            [f"\\b한 마디로 (['\"‘“]?\\w+['\"’”]?라고) (|간단히 )(말[하한할함합해했]\\w*)", "한마디로 () ()()"],
            [f"\\b한 마디로 (설명|거절|표현)(\\w*)", "한마디로 ()()"],
            [f"(\\w+[는은]) 한 마디로 ({KW_NTA})(이다|입니다)", "() 한마디로 ()()"]
        ],
        "exception": []
    },
    {
        "name": "0166664b_한마디",
        "desc": "https://wikidocs.net/166664#b",
        "cases": [
            [f"\\b단[ ]?한마디", "단 한 마디"],
            [f"\\b한마디[ ]?한마디", "한 마디 한 마디"],
            [f"\\b한마디씩", "한 마디씩"]
        ],
        "exception": []
    },
    {
        "name": "0167001a_정(正)",
        "desc": "https://wikidocs.net/167001#a",
        "cases": [
            [f"\\b정 (가운데|중앙)", "정()"]
        ],
        "exception": []
    },
    {
        "name": "0167340a_들어가다",
        "desc": "https://wikidocs.net/167340#a",
        "cases": [
            [f"\\b(곳으로) 들어 ([가간갈감갑갔]\\w*)", "() 들어()"]
        ],
        "exception": []
    },
    {
        "name": "0169284_꽃",
        "desc": "https://wikidocs.net/169284",
        "cases": [
            [f"\\b(벚|산수유|진달래|유채|코스모스) (꽃)", "()()"]
        ],
        "exception": []
    },
    {
        "name": "0169435d_‘-다운’, ‘-다움’",
        "desc": "https://wikidocs.net/169435",
        "cases": [
            [f"\\b({KW_NP}) (다운|다[우움울워웠]\\w*|답[고다게죠지]\\w*)\\b", "()()"],
            [f"\\b({KW_NTO}) (다운|다[우움울워웠]\\w*|답[고다게죠지]\\w*)\\b", "()()"],
            [f"\\b(프로그램) (다운) (프로그램)", "()() ()"]
        ],
        "exception": []
    },
    {
        "name": "0170161b_한편",
        "desc": "https://wikidocs.net/170161#b",
        "cases": [
            [f"\\b한 편({KJ})", "한편()"],
            [f"한 편\\b", "한편"]
        ],
        "exception": [f"영화 한 편", "한 편의 영화"]
    },
    {
        "name": "0170419a_단음절로 된 단어의 띄어쓰기",
        "desc": "https://wikidocs.net/170419#a",
        "cases": [
            [f"\\b([공])([한두서세너네])[ ]?(개)\\b", "(1) (2) (3), (1) (2)(3)"],
            [f"\\b([금])([한두서세너네])[ ]?(돈)\\b", "(1) (2) (3), (1) (2)(3)"],
            [f"\\b([물술])([한두서세너네])[ ]?(병)\\b", "(1) (2) (3), (1) (2)(3)"],
            [f"\\b([시])([한두서세너네])[ ]?([수편])\\b", "(1) (2) (3), (1) (2)(3)"],
            [f"\\b([옷])([한두서세너네])[ ]?(벌)\\b", "(1) (2) (3), (1) (2)(3)"],
            [f"\\b([집])([한두서세너네])[ ]?(채)\\b", "(1) (2) (3), (1) (2)(3)"],
            [f"\\b([차])([한두서너네])[ ]?([대잔])\\b", "(1) (2) (3), (1) (2)(3)"]
        ],
        "exception": []
    },
    {
        "name": "0171275a_공",
        "desc": "https://wikidocs.net/171275#a",
        "cases": [
            [f"\\b(골프|농구|럭비|야구|정구|축구|탁구|테니스) 공(|[만은을의이]|보다|으로|이다|입니다)", "()공()"]
        ],
        "exception": [f"영화 한 편"]
    },
    {
        "name": "0172183a_뒤로하다",
        "desc": "https://wikidocs.net/172183#a",
        "cases": [
            [f"(\\w+[을를]) 뒤로 ([해했하한할]\\w*)", "() 뒤로()"]
        ],
        "exception": []
    },
    {
        "name": "0174103a_각(各)",
        "desc": "https://wikidocs.net/174103#a",
        "cases": [
            [f"\\b각 (국|지)(|를|에서|은|을|의)\\b", "각()()"],
            [f"\\b각 (급|류|명|인|방|부|살림|성|소|종|처|체|층|칙|항|호)({KJ})\\b", "각()()"],
            [f"\\b각 파(에서|의)", "각파()"],
            [f"\\b각 (가지|급|류|명|인|방|부|살림|성|소|종|처|체|층|칙|파|항|호)\\b", "각()"]
        ],
        "exception": []
    },
    {
        "name": "0174103b_각(各)",
        "desc": "https://wikidocs.net/174103#a",
        "cases": [
            [f"\\b각(\\d+)(부)", "각 ()()"],
            [f"\\b각({KW_NTA})", "각 ()"]
        ],
        "exception": [f"각가지", "각급", "각류", "각명", "각인", "각방", "각부", "각살림", "각성", "각소", "각종", "각지", "각처", "각체", "각층", "각칙",
                      "각파", "각항", "각호"]
    },
    {
        "name": "0174103c1_각 사",
        "desc": "https://wikidocs.net/174103#c",
        "cases": [
            [f"\\b각사가 (.*)(제공|축적)(\\w*)\\b", "각 사가 ()()()"],
            [f"\\b각사를 (방문)(\\w*)\\b", "각 사를 ()()"],
            [f"\\b각사마다(.*)(사양)(\\w*)\\b", "각 사마다()()()"],
            [f"\\b각사(에[는도서]?\\w*)\\b", "각 사()"],
            [
                f"\\b각사의 (.*)(가격[안]?|가족|강점|경영진|경우|경쟁력|경험|계약|계정|공고|공장|관계자|관리|금리|기술|네트워크|노하우|담당자|대표이사|독립|동향|등급제|라인업|만족도|모델|목표|매출액|방법|배터리|부문|분석기|비전|사업|사원|사이즈|사정|상표|상품|상황|센터|소봉투|손해율|솔루션|수장|수준|시리즈|시스템|신용도|실험실|역량|역할|영역|움직임|위반|의견|이사회|인적자원|임원|임플란트|자료|장점|전략|전문성|정보|정책|정체성|재직자|제도|제품|조직|주주|증감분|지분율|참여|커버율|특성|편집인|평가|프로그램|플랫폼|해석|혜택|현황|홈페이지|환경|환원율|회원|CSR|HR|IP|NCC|[Ss]erver)",
                "각 사의 ()()"]
        ],
        "exception": []
    },
    {
        "name": "0174103c2_각사",
        "desc": "https://wikidocs.net/174103#c",
        "cases": [
            [f"\\b각 사의 (모양)", "각사의"]
        ],
        "exception": []
    },
    {
        "name": "0174298a_들",
        "desc": "https://wikidocs.net/174298#a",
        "cases": [
            [f"\\b({KW_NTF}), (\\w+), (\\w+)들([이])", "(), (), () 들()"]
        ],
        "exception": []
    },
    {
        "name": "0174298b_-들",
        "desc": "https://wikidocs.net/174298#b",
        "cases": [
            [f"(?<!,)\\b({KW_NT}) 들(|에[는도]?|을)\\b", "()들()"],
            [f"(?<!,)\\b({KW_NP}) 들(|에[는도]?|을)\\b", "()들()"]
        ],
        "exception": []
    },
    {
        "name": "0174391_-성(性)",
        "desc": "https://wikidocs.net/174391",
        "cases": [
            [f"\\b(가격[ ]?탄력|가능|가독|가망|가변|가소|가연|가용|가인식|가치|가학|가혹|간결|계절) 성(|의)\\b", "()성()"]
        ],
        "exception": []
    },
    {
        "name": "0174488_고(高)-/저(低)-",
        "desc": "https://wikidocs.net/174488",
        "cases": [
            [f"\\b([고저]) (감도|강도|연령|지방|출력)", "()()"]
        ],
        "exception": []
    },
    {
        "name": "0174714a_면(面)",
        "desc": "https://wikidocs.net/174714#a",
        "cases": [
            [f"\\b([‘']?)(가격|내용|동시성|속도|시설|안정성|형식)([’']?)면(|에서)\\b", "(1)(2)(3) 면(4)"],
            [f"\\b(경제)(면에서 어려운)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0174714d_면(麵)",
        "desc": "https://wikidocs.net/174714#d",
        "cases": [
            [f"\\b(메밀|스파게티|파스타)면", "() 면"]
        ],
        "exception": []
    },
    {
        "name": "0175395d_복합어인 본 용언의 활용형이 3음절 이상인 것 + 버리다",
        "desc": "https://wikidocs.net/175395#d",
        "cases": [
            [f"\\b(가져와|떠내려가|사라져)(버[려렸리린릴림립]\\w*)", "() ()"],
            [f"\\b({KW_NAz})해(버[려렸리린릴림립]\\w*)", "()해 ()"]
        ],
        "exception": []
    },
    {
        "name": "0176450_몇",
        "desc": "https://wikidocs.net/176450",
        "cases": [
            [f"\\b몇([개번]|정류장)(\\w*)", "몇 ()"]
        ],
        "exception": []
    },
    {
        "name": "0178247a_‘한-’으로 시작하는 단어",
        "desc": "https://wikidocs.net/178247#a",
        "cases": [
            [f"\\b(한) (걱정|길|시름|가운데|겨울|낮|밤중|복판|잠|패|마을|집안)(|[가로를은을에여였이인일의]\\w*)\\b", "()()()"]
        ],
        "exception": []
    },
    {
        "name": "0179881a_‘차’로 끝나는 단어",
        "desc": "https://wikidocs.net/179881#a",
        "cases": [
            [f"\\b(시각) 차(|[가를])\\b", "()차()"]
        ],
        "exception": []
    },
    {
        "name": "0181944a_‘나가다’의 띄어쓰기 - 한 단어로 사전에 올라 있는 것",
        "desc": "https://wikidocs.net/181944#a",
        "cases": [
            [f"\\b(값|떠|뛰어|뛰쳐|빗|빠져|엇|잘|지|풀려) (나[가간갈감갑갔]\\w*)", "()()"]
        ],
        "exception": []
    },
    {
        "name": "0181944b_‘나가다’의 띄어쓰기 - 앞말이 명사일 때",
        "desc": "https://wikidocs.net/181944#b",
        "cases": [
            [f"\\b(집|집회)(나[가간갈감갑갔]\\w*)", "() ()"],
            [f"\\b({KW_NAO})(나[가간갈감갑갔]\\w*)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0181944c_‘나가다’의 띄어쓰기 - 동사의 활용형 뒤의 ‘나가다’가 본용언으로 쓰일 때",
        "desc": "https://wikidocs.net/181944#c",
        "cases": [
            [f"\\b(밀고)(나[가간갈감갑갔]\\w*)", "() ()"],
            [f"(\\w+[가이] \\w+에) 잘려(나[가간갈감갑갔]\\w*)", "() 잘려 ()"],
            [f"\\b(짐을) (꾸려)(나[가간갈감갑갔]\\w*)", "() () ()"]
        ],
        "exception": []
    },
    {
        "name": "0181944e_‘나가다’의 띄어쓰기 - 본용언이 복합어이고 그 활용형이 3음절 이상인 경우",
        "desc": "https://wikidocs.net/181944#e",
        "cases": [
            [f"\\b({KW_NAO})(시켜|해)(나[가간갈감갑갔]\\w*)", "()() ()"]
        ],
        "exception": []
    },
    {
        "name": "0182726_‘무사(無事)’",
        "desc": "https://wikidocs.net/182726#a",
        "cases": [
            [f"\\b(무사)(귀[가환])", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0183030b_빈",
        "desc": "https://wikidocs.net/183030#b",
        "cases": [
            [f"\\b(빈)(곳)(|[도에은을의이]|으로\\w*)\\b", "() ()()"],
            [f"\\b(빈)(수레|차)(|[가도에은를의]|로\\w*)\\b", "() ()()"],
            [f"\\b(빈)(줄)(|[도만에은을의이]|로\\w*)\\b", "() ()()"]
        ],
        "exception": []
    },
    {
        "name": "0183912_구성(構成)’의 띄어쓰기",
        "desc": "https://wikidocs.net/183912",
        "cases": [
            [f"\\b(면)(구성)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0184629a11_‘돌아가다’",
        "desc": "https://wikidocs.net/184629#a1",
        "cases": [
            [f"\\b(고향)(에|으로) 돌아 ([가간갈감갑갔]\\w*)", "()() 돌아()"],
            [f"\\b({KW_NP})(께서) 돌아 ([가간갈감갑갔]\\w*)", "()() 돌아()"],
            [f"\\b(느리게|바쁘게|부드럽게|빠르게|잘) 돌아 ([가간갈감갑갔]\\w*)", "()() 돌아()"]
        ],
        "exception": []
    },
    {
        "name": "0184629a12_‘돌아 가다’",
        "desc": "https://wikidocs.net/184629#a1",
        "cases": [
            [f"\\b(앞 건물|모퉁이)([를을]) 돌아([가간갈감갑갔]\\w*)", "()() 돌아 ()"]
        ],
        "exception": []
    },
    {
        "name": "0184629b2_‘넘어가다’",
        "desc": "https://wikidocs.net/184629#b2",
        "cases": [
            [f"\\b(넘어) ([가간갈감갑갔]\\w*)", "()()"]

        ],
        "exception": []
    },
    {
        "name": "0184629c1_장소를 나타내는 명사와 ‘가다’의 띄어 쓰기",
        "desc": "https://wikidocs.net/184629#c1",
        "cases": [
            [
                f"\\b(무기고|창고|가게|군대|게임방|노래방|멀티방|피시방|PC방|관계사|기획사|회사|녹음실|집무실|회의실|[공학]원|경기장|운동장|현장|훈련장|편의점|집|업체|[모호]텔|교회|고향|마트|클럽|\\w*학교)(가[는니다도보봐서자]\\w*|간|간다[고는며지]?|간 [거걸것뒤듯후]\\w*|갈|갈게\\w*|[감갑갔]\\w*)\\b",
                "() ()"],
            [f"\\b([A-Za-z0-9]+)(가[는니다도보봐서자]\\w*|갈|갈게\\w*|[감갑갔]\\w*)\\b", "() ()"],
            [f"\\b([A-Za-z0-9]+)(간다[고는며지]?)\\b", "() ()"],
        ],
        "exception": []
    },
    {
        "name": "0184629c31_본 용언인 ‘가다’와 앞말의 띄어 쓰기",
        "desc": "https://wikidocs.net/184629#c31",
        "cases": [
            [f"\\b(떠밀려)가([ ]?버[려렸리린릴림립]\\w*)", "() 가()"]

        ],
        "exception": []
    },
    {
        "name": "0184629c32_‘내려가다’와 앞말의 띄어 쓰기",
        "desc": "https://wikidocs.net/184629#c32",
        "cases": [
            [f"\\b(걸어)내려[ ]?([가간갈감갑갔]\\w*)", "() 내려()"]

        ],
        "exception": []
    },
    {
        "name": "0185998a_‘-삼다’로 끝나는 단어",
        "desc": "https://wikidocs.net/185998#a",
        "cases": [
            [f"\\b(거울|일|자랑|장난|주장|참고) 삼([다아았으은을]\\w*)", "()삼()"]

        ],
        "exception": []
    },
    {
        "name": "0185998b_‘삼다’와 앞말을 띄어 쓰는 것",
        "desc": "https://wikidocs.net/185998#b",
        "cases": [
            [f"\\b(대중|동무|문제|벗|시험|연습|운동|\\w*거리)삼([다아았으은을]\\w*)", "() 삼()"]

        ],
        "exception": []
    },
    {
        "name": "0187243c1_읽을거리",
        "desc": "https://wikidocs.net/187243#c",
        "cases": [
            [f"\\b읽을 거리", "읽을거리"]
        ],
        "exception": [f"더 읽을", "가볍게 읽을"]
    },
    {
        "name": "0187243c2_읽을 거리",
        "desc": "https://wikidocs.net/187243#c",
        "cases": [
            [f"\\b(가볍게|더) 읽을거리", "() 읽을 거리"]

        ],
        "exception": []
    },
    {
        "name": "0187342_‘여부’의 띄어쓰기",
        "desc": "https://wikidocs.net/187342",
        "cases": [
            [f"\\b(결혼|수행|해당)여부", "() 여부"]

        ],
        "exception": []
    },
    {
        "name": "0187675d_복합어의 활용형이 3음절 이상인 것 + ‘오다’",
        "desc": "https://wikidocs.net/187675#d",
        "cases": [
            [f"\\b({KW_NAOz})[ ]?해([오온올옴옵와왔]\\w*)", "()해 ()"]
        ],
        "exception": []
    },
    {
        "name": "0188057a_‘생각’과 ‘나다’를 띄어 써야 하는 것",
        "desc": "https://wikidocs.net/188057#a",
        "cases": [
            [f"\\b(좋은) (생각)([나난날남납났]\\w*)", "() () ()"]
        ],
        "exception": []
    },
    {
        "name": "0188057b_‘생각나다’로 붙여 써야 하는 것",
        "desc": "https://wikidocs.net/188057#b",
        "cases": [
            [f"\\b({KW_NP})([가이]) (생각) ([나난날남납났]\\w*)", "()() ()()"],
            [f"\\b(불현듯|잘) (생각) ([나난날남납났]\\w*)", "() ()()"]
        ],
        "exception": []
    },
    {
        "name": "0195351b_직하다",
        "desc": "https://wikidocs.net/195351#b",
        "cases": [
            [f"\\b({KW_NAOz})[ ]?해(봄직|봄 직| 봄직)([하한할함합해했]\\w*)", "(1)해 봄 직(3)"]
        ],
        "exception": []
    },
    {
        "name": "0195930_‘이, 그, 저’의 띄어쓰기",
        "desc": "https://wikidocs.net/195930#a",
        "cases": [
            [f"\\b([그이저])(물건|사람|옵션|자리)", "() ()"],
            [f"\\b그(자체)", "그 ()"]
        ],
        "exception": []
    },
    {
        "name": "0197861a_‘-식’(접미사)",
        "desc": "https://wikidocs.net/197861#a",
        "cases": [
            [f"\\b(강의|계단|고정|공랭|기계|기업|나열|무기명|문어발|반자동|서양|수랭|유압|자동|재래|현대|흐름) 식(으로|의)\\b", "()식()"],
            [
                f"\\b(개관|개교|개업|개원|개장|개통|개학|결혼|기공|기념|대관|봉정|분열|선발|선서|성년|송별|수료|수상|시상|약혼|혼|은혼|입성|입학|전달|조례|즉위|착공|축하|취임|표창|현판|혼례|화형) 식(을|의)\\b",
                "()식()"]
        ],
        "exception": []
    },
    {
        "name": "0197861c_식(의존 명사)",
        "desc": "https://wikidocs.net/197861#c",
        "cases": [
            [f"\\b(농담하는|살펴보는)(식으로)\\b", "() ()"],
            [f"\\b(그런)(식으로나마)\\b", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0215483_‘사항’의 띄어쓰기",
        "desc": "https://wikidocs.net/215483",
        "cases": [
            [f"\\b(건의|결정|고려|공지|문의|미흡|선택|세부|요청|유의|지시|참고)(사항)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "0219799b_‘긷다’",
        "desc": "https://wikidocs.net/219799",
        "cases": [
            [f"\\b(물을) 길러[ ]?([오온올와왔]\\w*)", "() 길어 ()"]
        ],
        "exception": []
    },
    {
        "name": "bnd0300a_등교 전",
        "desc": "https://bookndebate.tistory.com/300",
        "cases": [
            [f"\\b(등교)(전)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "bnd0300b_얼마 전",
        "desc": "https://bookndebate.tistory.com/300",
        "cases": [
            [f"\\b(얼마)(전)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "cokl2008_띄어쓰기(국어책임관)",
        "desc": "https://www.korean.go.kr/attachFile/viewer/202209/36d2c7f7-3b41-4633-8bbe-6d1f4a31e115_0.pdf.htm",
        "cases": [
            [f"\\b(\\d+개)(업체)({KJ})\\b", "() ()()"],
            [f"\\b(고려)토록하고", "()하도록 하고"],
            [f"\\b다음사항", "다음 사항"],
            [f"\\b둘째자리", "둘째 자리"],
            [f"\\b매회계년도", "매 회계 연도"],
            [f"\\b못미쳐", "못 미쳐"],
            [f"\\b미 사용시", "미사용 시"],
            [f"\\b미입력 된", "미입력된"],
        ],
        "exception": []
    },
    {
        "name": "cplus101_~에서조차도",
        "desc": "이것만 알아두면 맞춤법은 끝나(http://cultureplus.com/)",
        "cases": [
            [
                f"<Noun>에서 조차도",
                "()에서조차도"
            ]
        ],
        "exception": []
    },
    {
        "name": "cplus201_자주 헷갈리는 띄어쓰기",
        "desc": "이것만 알아두면 맞춤법은 끝나(http://cultureplus.com/)",
        "cases": [
            [
                f"\\b([1-2][0-9]{{3}})년 경",
                "()년경"
            ],
            [
                f"\\b(기간)동안",
                "() 동안"
            ],
            [
                f"\\b(생일) 다음날",
                "() 다음 날"
            ],
            [
                f"두 말할 것 없이",
                "두말할 것 없이"
            ],
            [
                f"({KW_NNC})({KW_NUT})(만\\w)",
                "() () ()"
            ],
            [
                f"오랜 (만이\\w)",
                "오랜()"
            ],
            [
                f"\\b(이민) 간지",
                "() 간 지"
            ]
        ],
        "exception": []
    },
    {
        "name": "ewha2280_마주",
        "desc": "http://eomun.ewha.ac.kr/sub/sub05_01.php?mNum=5&sNum=1&boardid=qna&mode=view&idx=2280&goPage=&g_idx=",
        "cases": [
            [f"\\b(마주)(앉\\w*|보고 앉\\w*|보면)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "faq09289_큰코다치다",
        "desc": "https://korean.go.kr/front/mcfaq/mcfaqView.do?mn_id=&mcfaq_seq=9289",
        "cases": [
            [f"(\\w*다가는) 큰[ ]?코 다([쳐치친칠침칩]\\w*)", "() 큰코다()"]
        ],
        "exception": [
        ]
    },
    {
        "name": "jg238176_머지않다",
        "desc": "https://www.joongang.co.kr/article/23817690#home",
        "cases": [
            [f"\\b머지 (않\\w+)", "머지()"]
        ],
        "exception": [
        ]
    },
    {
        "name": "kns11308_힘듦",
        "desc": "https://www.korean.go.kr/news/index.jsp?control=page&part=view&idx=11308",
        "cases": [
            [f"\\b힘 듦(|[을])\\b", "힘듦()"]
        ],
        "exception": [
        ]
    },
    {
        "name": "kw230897_불리다",
        "desc": "http://world.kbs.co.kr/service/contents_view.htm?lang=k&menu_cate=learnkorean&id=&board_seq=230897&page=81",
        "cases": [
            [f"\\b불리우([고기는다며면지진]\\w*)", "불리()"]
        ],
        "exception": [
        ]
    },
    {
        "name": "lvtedu01_-기 위해",
        "desc": "https://m.cafe.daum.net/lovethedu/MKGS/1519",
        "cases": [
            [
                f"(\\w+기)(위[한해])",
                "() ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "media11a_띄어쓰기 - 단위 명사",
        "desc": "신문과 방송의 언어 사용 실태 조사, 2011",
        "cases": [
            [f"\\b(\\d{{1,2}}월)(\\d{{1,2}}~\\d{{1,2}}일)", "() ()"],
            [f"\\b(\\d+시간)(\\d+분)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "media11d_띄어쓰기 - 단어와 단어",
        "desc": "신문과 방송의 언어 사용 실태 조사, 2011",
        "cases": [
            [f"\\b他지역", "타(他) 지역"],
            [f"\\b박용하씨", "박용하 씨"],
            [f"\\b박씨", "박 씨"],
            [f"\\b명수군", "명수 군"],
            [f"\\b쉬는건", "쉬는 건"],
            [f"\\b아산공장내", "아산공장 내"],
            [f"\\b사측이", "회사 측이"],
            [f"\\b놔둘텐가", "놔둘 텐가"],
            [f"\\b않은채", "않은 채"],
            [f"\\b어쩔거야", "어찌할 거야"],
            [f"\\b못가는", "못 가는"],
            [f"\\b웬말", "웬 말"],
            [f"\\b허리부상", "허리 부상"],
            [f"\\b올시즌", "올 시즌"],
            [f"\\b날선", "날 선"],
            [f"\\b술먹는", "술 먹는"],
            [f"\\b푸념어린", "푸념 어린"]
        ],
        "exception": []
    },
    {
        "name": "nklife12_국어 오용 사례(국어생활 12호, 1988)",
        "desc": "https://www.korean.go.kr/nkview/nklife/1988_1/12_20.html",
        "cases": [
            [f"\\b(풀칠) ([하한할합해했]\\w*)", "()()"]
        ],
        "exception": []
    },
    {
        "name": "nm200212_띄어쓰기 잘못(어문 규범 준수 실태 조사, 2002)",
        "desc": "https://www.korean.go.kr/front/reportData/reportDataView.do?mn_id=45&report_seq=39",
        "cases": [
            [f"\\b(이회창)(씨)(측)", "() () ()"],
            [f"\\b(최)(씨의)", "() ()"],
            [f"\\b(불법)(대출)", "() ()"],
            [f"\\b한번을 더", "한 번을 더"],
            [f"\\b(한)(부분)({KJ})", "() ()()"],
            [f"\\b(한)(개|시간)(씩)", "() ()()"],
            [f"\\b(전화)(왔\\w+)", "() ()"],
            [f"\\b(두|세)(사람|팀)", "() ()"],
            [f"\\b(반)(층)", "() ()"],
            [f"\\b(청약)(\\d+)(순위)", "() ()()"],
            [f"\\b(오픈)(예정)", "() ()"],
            [f"\\b(시장 분석|시장|청구)(데이터)", "() ()"],
            [f"\\b(지식)(강자)", "() ()"],
            [f"(구찌)(스타일)", "() ()"],
            [f"(포워딩) (되는)", "()()"],
            [f"(다운로드) (하기)(전)", "()() ()"],
            [f"(다운로드) (하시거나|할)", "()()"],
            [f"(첨삭)(지도)", "() ()"],
            [f"(데이터) (전송)(시)", "() () ()"],
            [f"(피할)(수)", "() ()"],
            [f"(디지털)(시대)", "() ()"],
            [f"(뚝심)(좋은)", "() ()"],
            [f"(베컴)(슛)", "() ()"],
            [f"(링크) (되어)(있는)", "()() ()"],
            [f"(레드)(상의와) (블랙)(하의)", "() () () ()"],
            [f"(링크)(걸기)", "() ()"],
            [f"(최근에 \\w+된) (\\w+) (순으로) (검색)", "() ()() ()"],
            [f"(업데이트) (됩니다)", "()()"],
            [f"(모토)(아래)", "() ()"],
            [f"\\b(새)(아이템)", "() ()"],
            [f"\\b(놀이)(계획)", "() ()"],
            [f"\\b(거리)(캠페인)", "() ()"],
            [f"\\b(업데이트) (하여)", "()()"],
            [f"\\b(오픈)(한)(지)", "()() ()"],
            [f"\\b(구사)(능력)", "() ()"],
            [f"\\b(주소로) (부터)", "()()"],
            [f"\\b(\\d+)(개)(팀)", "()() ()"],
            [f"\\b(이)(땅)(의)", "() ()()"],
            [f"\\b(귀)(단체)", "() ()"],
            [f"\\b(이용하실)(때)", "() ()"],
            [f"\\b(검색)(찬스)", "() ()"],
            [f"\\b(공부하는)(건)", "() ()"],
            [f"\\b(지금) (이)(시간)", "() () ()"],
            [f"\\b(업데이트) (되고)", "()()"],
            [f"\\b(지뢰)(유실)", "() ()"],
            [f"\\b(샘플)(보기)", "() ()"],
            [f"\\b(리더) (님[들]?)", "()()"],
            [f"\\b(숙박)(시설)", "() ()"],
            [f"\\b(계모)(스토리)", "() ()"],
            [f"\\b(광고)(기법)", "() ()"],
            [f"\\b(테스트) (기간)(동안)", "() () ()"],
            [f"\\b(노미네이트) ([되된될돼됐]\\w*)", "()()"],
            [f"\\b(투자)(자금)", "() ()"],
            [f"\\b(특정)(아이디)", "() ()"],
            [f"\\b(더블)(클릭)(후)", "() () ()"],
            [f"\\b(채팅을)(할)(수가)", "() () ()"],
            [f"\\b(페이지를 쉽게) (찾아) (볼 수)", "() ()()"],
            [f"\\b(한)(번의) (ID|아이디) (로그인)(만으로)", "() () () ()()"],
            [f"\\b(해당)(게임을)", "() ()"],
            [f"\\b(환경)(문제)(가| 해결을)", "() ()()"],
            [f"\\b(보기)(좋은)", "() ()"],
            [f"\\b(광고)(소재)", "() ()"],
            [f"\\b(매매)(타이밍)", "() ()"],
            [f"\\b(리스크)(관리)", "() ()"],
            [f"\\b(상품)(리스트)", "() ()"],
            [f"\\b(\\w*은행) 맞은 편", "() 맞은편"],
            [f"\\b(블랙)(컬러)(빌딩)", "() () ()"],
            [f"\\b(십지)(지문)", "() ()"],
            [f"\\b(위헌)(소송)", "() ()"],
            [f"\\b(카페)(개설)", "() ()"],
            [f"\\b각계 각층", "각계각층"],
            [f"\\b채용정보", "채용 정보"],
            [f"\\b(\\d+)([천만])(마력)", "()() ()"]
        ],
        "exception": []
    },
    {
        "name": "nskm6622_붙여 써야 할 단어",
        "desc": "https://blog.naver.com/neweskimo/220588006622",
        "cases": [
            [f"([0-9]+세) (가량)", "()()"],
            [f"가득 하다", "가득하다"],
            [f"갉아 (먹\\w+)", "갉아()"],
            [f"감람 산", "감람산"],
            [f"\\b값 없다", "값없다"],
            [f"(건너|끌려|데려|돌아|따라|살아|앞서|오래) ([가갈])\\b", "()()"],
            [f"(건너|끌려|데려|돌아|따라|살아|앞서|오래) ([가간갈갔])({KJ_I})\\b", "()()()"],
            [f"걸어 (오\\w+)", "걸어()"],
            [f"고부 (간\\w*)", "고부()"],
            [f"교통 사고", "교통사고"],
            [f"(그리|까딱) ([해하]\\w+)", "()()"],
            [f"그지 (없\\w+)", "그지()"],
            [f"그 해(|KJ)\\b", "그해()"],
            [f"꿇어 (앉[혀혔히힌]\\w+)", "꿇어()"],
            [f"\\b끌어 ([들올]\\w+)", "끌어()"],
            [f"난생 처음", "난생처음"],
            [f"날아 ([오올]\\w+)", "날아()"],
            [f"내려 ([놓앉]\\w+)", "내려()"],
            [f"내려다 ([보본]\\w+)", "내려다()"],
            [f"내리자 마자", "내리자마자"],
            [f"(\\w+[을를]) 내 (주\\w+)", "() 내()"],
            [f"넘어 (서\\w+)", "넘어()"],
            [f"눈 앞", "눈앞"],
            [f"\\b(늘어|빼|올려|털어) (놓\\w+)", "()()"],
            [f"\\b다가 (오\\w+)", "다가()"],
            [f"닫아 (걸\\w+)", "닫아()"],
            [f"\\b달아 ([나날났]\\w+)", "달아()"],
            [f"\\b도로 변", "도로변"],
            [f"\\b돌려 (보[내낸낼냄냅냈]\\w+)", "돌려()"],
            [f"동여 (매\\w+)", "동여()"],
            [f"(된장|두부) (전골|찌개)", "()()"],
            [f"두려워 ([해했하한할]\\w*)", "두려워()"],
            [f"뒤 표지", "뒤표지"],
            [f"들러 (붙\\w*)", "들러()"],
            [f"따라 (다[녀녔니닌]\\w*|[오온왔]다\\w*|올\\b|잡\\w+)", "따라()"],
            [f"딸 아이", "딸아이"],
            [f"땅 (끝|속)", "땅()"],
            [f"때 아닌", "때아닌"],
            [f"뛰어 (내[려렸리린릴]\\w*)", "뛰어()"],
            [f"마음 고생", "마음고생"],
            [f"마음 속", "마음속"],
            [f"마주 (하\\w+)", "마주()"],
            [f"마지 (않\\w+)", "마지()"],
            [f"만지작 거리다", "만지작거리다"],
            [f"말씀 드리다", "말씀드리다"],
            [f"매 시간", "매시간"],
            [f"먹고 사는", "먹고사는"],
            [f"\\b(모녀|부부|부자) 간", "()간"],
            [f"몰려 (오\\w+)", "몰려()"],
            [f"몰아 (내\\w+)", "몰아()"],
            [f"못 쓰다", "못쓰다"],
            [f"못지 (않\\w+)", "못지()"],
            [f"물 김치", "물김치"],
            [f"물샐틈 (없\\w+)", "물샐틈()"],
            [f"박수 갈채", "박수갈채"],
            [f"받아 (들이\\w+)", "받아()"],
            [f"발 아래", "발아래"],
            [f"백 분의 일", "백분의 일"],
            [f"자기 뱃 속 채우는 데에만 (급급\\w+)", "자기 뱃속 채우는 데에만 ()"],
            [f"\\b버려 (두\\w+)", "버려()"],
            [f"버섯 나물", "버섯나물"],
            [f"\\b별 반\\b", "별반"],
            [f"별 의별", "별의별"],
            [f"\\b병 문안", "병문안"],
            [f"보잘[ ]?것 (없\\w+)", "보잘것()"],
            [f"\\b복 중 태아", "복중 태아"],
            [f"\\b본 ([떠떴뜨뜬]\\w*)", "본()"],
            [f"부여 (잡\\w+)", "부여()"],
            [f"불러 (일으키\\w+)", "불러()"],
            [f"불어 (넣\\w+)", "불어()"],
            [f"불 ([타탄탔]\\w*)", "불()"],
            [f"\\b빈 칸", "빈칸"],
            [f"빈틈 없이", "빈틈없이"],
            [f"빠져 (나[가간감갑갈갔]\\w*|들\\w*)", "빠져()"],
            [f"\\b빼 (내\\w+)", "빼()"],
            [f"뿜어 (내\\w+)", "뿜어()"],
            [f"\\b사 (들이\\w+)", "사()"],
            [f"\\b살아 (남\\w+)", "살아()"],
            [f"살아 (오\\w+)", "살아()"],
            [f"\\b성 ([문벽안])", "성()"],
            [f"\\b소개 말", "소개말"],
            [f"\\b손 아귀", "손아귀"],
            [f"\\b수 년간", "수년간"],
            [f"스며 (들\\w+)", "스며()"],
            [f"\\b신 (나\\w+)", "신()"],
            [f"\\b써 (먹\\w*)", "써()"],
            [f"\\b쓸어 (버리\\w*)", "쓸어()"],
            [f"\\b앉은 자리", "앉은자리"],
            [f"알아 ([내채]\\w+)", "알아()"],
            [f"앞 표지", "앞표지"],
            [f"\\b어느 새", "어느새"],
            [f"어두워 (지\\w+)", "어두워()"],
            [f"어이 (없\\w+)", "어이()"],
            [f"언짢아 (하\\w+)", "언짢아()"],
            [f"얼굴 빛", "얼굴빛"],
            [f"에덴 동산", "에덴동산"],
            [f"여기 저기", "여기저기"],
            [f"여러 모로", "여러모로"],
            [f"(여지|염치) (없\\w+)", "()()"],
            [f"영원 무궁", "영원무궁"],
            [f"오래 (되\\w+)", "오래()"],
            [f"오므라 (들\\w+)", "오므라()"],
            [f"\\b올 여름", "올여름"],
            [f"외래 문화", "외래문화"],
            [f"운동 선수", "운동선수"],
            [f"움츠러 (들\\w+)", "움츠러()"],
            [f"의사 소통", "의사소통"],
            [f"이곳 저곳", "이곳저곳"],
            [f"\\b이 달(|[은의]|만\\w*|에\\w*)\\b", "이달()"],
            [f"이때 껏", "이때껏"],
            [f"이런 저런", "이런저런"],
            [f"\\b이 분(|까지|에게|이)\\b", "이분()"],
            [f"\\b이 생(까지|마저|에는|의|은|을|조차)\\b", "이생()"],
            [f"이야기 (하\\w+)", "이야기()"],
            [f"\\b이 자는 누구", "이자는 누구"],
            [f"인간 관계", "인간관계"],
            [f"인사 차", "인사차"],
            [f"잊어 (버리\\w+)", "잊어()"],
            [f"자기 반성", "자기반성"],
            [f"잘못 (하\\w+)", "잘못하다"],
            [f"\\b제 때에", "제때에"],
            [f"\\b제 시간", "제시간"],
            [f"\\b제 자리", "제자리"],
            [f"\\b제 정신", "제정신"],
            [f"줄달음 (치\\w+)", "줄달음()"],
            [f"줄어 (들\\w+)", "줄어()"],
            [f"중간 중간", "중간중간"],
            [f"지난 여름", "지난여름"],
            [f"지어 (내\\w+)", "지어()"],
            [f"\\b집 터", "집터"],
            [f"천부당[ ]?만부당 (하\\w+)", "천부당만부당()"],
            [f"\\b첫 해", "첫해"],
            [f"\\b쳐 (들\\w*)", "쳐()"],
            [f"\\b초 읽기", "초읽기"],
            [f"춥디 추운", "춥디추운"],
            [f"\\b큰 일", "큰일"],
            [f"택시 비", "택시비"],
            [f"\\b팀 원", "팀원"],
            [f"\\b하루 치", "하루치"],
            [f"\\b하자 마자", "하자마자"],
            [f"\\b한 데 묶어", "한데 묶어"],
            [f"\\b한 동안", "한동안"],
            [f"(\\w*고) 말할 걸", "() 말할걸"],
            [f"\\b해 (치우\\w+)", "해()"],
            [f"\\b핵 폐기물", "핵폐기물"],
            [f"(행복|황송)해 (하\\w+)", "()해()"],
            [f"흘러 (나오\\w+)", "흘러()"],
            [f"\\b흰 머리", "흰머리"],
            [f"\\b힘 겨루기", "힘겨루기"]
        ],
        "exception": []
    },
    {
        "name": "od0735010_웹사이트",
        "desc": "https://opendict.korean.go.kr/dictionary/view?sense_no=735010&viewType=confirm",
        "cases": [
            [f"\\b웹 사이트", "웹사이트"]
        ],
        "exception": []
    },
    {
        "name": "od0768634_계산식",
        "desc": "https://opendict.korean.go.kr/dictionary/view?sense_no=768634&viewType=confirm",
        "cases": [
            [f"\\b계산 식", "계산식"]
        ],
        "exception": []
    },
    {
        "name": "od0786251_불특정 다수",
        "desc": "https://opendict.korean.go.kr/dictionary/view?sense_no=786251&viewType=confirm",
        "cases": [
            [f"불특정다수", "불특정 다수"]
        ],
        "exception": []
    },
    {
        "name": "od0905061_영화 팬",
        "desc": "https://opendict.korean.go.kr/dictionary/view?sense_no=905061&viewType=confirm",
        "cases": [
            [f"\\b영화팬", "영화 팬"]
        ],
        "exception": []
    },
    {
        "name": "od1144841_명령줄",
        "desc": "https://opendict.korean.go.kr/dictionary/view?sense_no=1144841&viewType=confirm",
        "cases": [
            [f"\\b명령 줄 (인자)", "명령줄 ()"]
        ],
        "exception": []
    },
    {
        "name": "o1282889_보조 도구",
        "desc": "https://opendict.korean.go.kr/dictionary/view?sense_no=1282889&viewType=confirm",
        "cases": [
            [f"\\b(보조)(도구)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "qa000268_걱정하지 마",
        "desc": "https://wikidocs.net/181967#268",
        "cases": [
            [f"({KW_NAO})하지([마말]\\w*)", "()하지 ()"]
        ],
        "exception": []
    },
    {
        "name": "qa002843_오랜 시간",
        "desc": "https://wikidocs.net/181967#2843",
        "cases": [
            [f"\\b오랜시간", "오랜 시간"]
        ],
        "exception": []
    },
    {
        "name": "qa007529_‘상자’, ‘박스’",
        "desc": "https://wikidocs.net/181967#7529",
        "cases": [
            [f"\\b({KW_NC})(박스)", "() ()"],
            [f"\\b([뇌보선]물|사과|용돈|라면)(박스|상자)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "qa007828_안 좋다",
        "desc": "https://wikidocs.net/181967#7828",
        "cases": [
            [f"\\b안(좋다[고면]?|좋아[서]?|좋으\\w+|좋을 것|좋을 텐더|좋을까\\w*)", "안 ()"],
            [f"\\b안좋을[ ]?뿐더러", "안 좋을뿐더러"]
        ],
        "exception": []
    },
    {
        "name": "qa007881_외",
        "desc": "https://wikidocs.net/181967#7881",
        "comment": "--> 0090404c",
        "cases": [
        ],
        "exception": []
    },
    {
        "name": "qa008414_산 속",
        "desc": "https://wikidocs.net/181967#8414",
        "cases": [
            [f"\\b깊은 산 속", "깊은 산속"],
            [f"\\b(바닷속.*) 산 속", "() 산속"]
        ],
        "exception": []
    },
    {
        "name": "qa009474",
        "desc": "https://wikidocs.net/181967#9474",
        "cases": [
            [f"\\b불 ([길빛])", "불()"],
            [f"\\b햇 ([빛])", "햇()"],
            [f"\\b([가-힣]+)선생께", "() 선생님께"],
            [f"\\b찾아(나[서선설섰]\\w*)", "찾아 ()"],
            [f"\\b(낯설지도)(않\\w+)", "() ()"],
            [f"\\b밤 중", "밤중"],
            [f"\\b([능성원익친]숙) (해[지진질져졌]\\w*)", "()()"],
            [f"\\b(소리)(없\\w*)", "() ()"],
            [f"\\b맴 돌(\\w*)", "맴돌()"],
            [f"\\b(맴[돌]) 뿐 (입니다)", "() 뿐()"],
            [f"\\b(짐을 졌)으매 (따라\\w*)", "()음에 ()"],
            [f"\\b(짐을) 졌음에 (무겁\\w*)", "() 졌으매 ()"],
            [f"\\b([종총]) (소리\\w*)", "()()"],
            [f"\\b(결의|분노)에([차찬찰참찼]\\w*)", "()에 ()"],
            [f"\\b(넓힌|녹인|늘린|말린|불린|삶은|식힌|졸인|줄인|태운)후({KJ})", "() 후()"]
        ],
        "exception": []
    },
    {
        "name": "qa011900_눈치채다",
        "desc": "https://wikidocs.net/181967#11900",
        "cases": [
            [f"\\b눈치 (채\\w+)", "눈치()"]
        ],
        "exception": []
    },
    {
        "name": "qa015230_‘어떤가’",
        "desc": "https://wikidocs.net/181967#15230",
        "cases": [
            [f"\\b어떤 가(에)\\b", "어떤가()"]
        ],
        "exception": []
    },
    {
        "name": "qa015712_오래전",
        "desc": "https://wikidocs.net/181967#15712",
        "cases": [
            [f"\\b오래 전", "오래전"]
        ],
        "exception": [f"아주"]
    },
    {
        "name": "qa027863_타",
        "desc": "https://wikidocs.net/181967#27863",
        "cases": [
            [f"\\b타(거점|문화|업소|지역)", "타 ()"]
        ],
        "exception": []
    },
    {
        "name": "qa027952_-고 있다",
        "desc": "https://wikidocs.net/181967#27952",
        "cases": [
            [
                f"\\b(갖|기다리|듣|먹|자|지니|하)고(있\\w*)",
                "()고 ()"
            ],
            [
                f"(\\w+[을를]) (매|안|쥐)고(있\\w*)",
                "()고 ()"
            ],
            [
                f"\\b({KW_NA})되고(있\\w*)",
                "()되고 ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "qa028675a_미소 짓다",
        "desc": "https://wikidocs.net/181967#28675",
        "cases": [
            [
                f"(미소)([지지졌]\\w*)",
                "() ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "qa028675b_방 안",
        "desc": "https://wikidocs.net/181967#28675",
        "cases": [
            [
                f"\\b(방)(안으로 들어[가갈갔]\\w*)",
                "() ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "qa028675c_몇 초",
        "desc": "https://wikidocs.net/181967#28675",
        "cases": [
            [
                f"몇초",
                "몇 초"
            ]
        ],
        "exception": []
    },
    {
        "name": "qa035951_한두 달",
        "desc": "https://wikidocs.net/181967#35951",
        "cases": [
            [f"\\b한두달", "한두 달"]
        ],
        "exception": []
    },
    {
        "name": "qa046510_기대되다",
        "desc": "https://wikidocs.net/181967#46510",
        "cases": [
            [f"\\b(기대) (되[고는며지]\\w*)", "()()"],
            [f"\\b(기대) ([된될됨됩돼됐]\\w*)", "()()"]
        ],
        "exception": []
    },
    {
        "name": "qa052181_조차",
        "desc": "https://wikidocs.net/181967#52181",
        "cases": [
            [f"\\b({KW_NI}) 조차", "()조차"],
            [f"\\b(철수|영희) 조차", "()조차"],
            [f"\\b({KW_NV}) 조차", "()조차"],
            [f"\\b(나|너|우리) 조차", "()조차"],
            [f"\\b({KW_NPR})([들]?)(에게서|에서) 조차", "()()()조차"],
            [f"\\b({KW_NT})(에게서|에서) 조차", "()()조차"],
            [f"\\b({KW_NAO})할[ ]?수 조차", "()할 수조차"],
            [f"(\\w+는지) 조차", "()조차"]
        ],
        "exception": []
    },
    {
        "name": "qa052875_가량",
        "desc": "https://wikidocs.net/181967#52875",
        "cases": [
            [f"(\\d+%) (가량)", "()()"]
        ],
        "exception": []
    },
    {
        "name": "qa065247_주식회사",
        "desc": "https://wikidocs.net/181967#65247",
        "cases": [
            [f"주식 회사", "주식회사"],
            [f"(\\w+)주식[ ]?회사", "() 주식회사"],
            [f"\\b주식[ ]?회사(\\w+)\\b", "주식회사 ()"],
            [f"\\b주식[ ]?회사(\\w+)({KJ})\\b", "주식회사 ()()"]
        ],
        "exception": [f"각가지", "각급", "각류", "각명", "각인", "각방", "각부", "각살림", "각성", "각소", "각종", "각지", "각처", "각체", "각층", "각칙",
                      "각파", "각항", "각호"]
    },
    {
        "name": "qa073127_씨",
        "desc": "https://wikidocs.net/181967#73127",
        "cases": [
            [f"홍걸씨", "홍걸 씨"]
        ],
        "exception": []
    },
    {
        "name": "qa073333_삼다",
        "desc": "https://wikidocs.net/181967#73333",
        "cases": [
            [f"<Noun>삼아", "() 삼아"]
        ],
        "exception": []
    },
    {
        "name": "qa078024_단 한 번",
        "desc": "https://wikidocs.net/181967#78024",
        "cases": [
            [
                f"\\b(단|오직)[ ]?한(번[ ]?뿐)",
                "() 한 번뿐"
            ],
            [
                f"\\b(단|오직)[ ]?한(번[ ]?[^뿐]\\w*)",
                "() 한 ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "qa079849_가져오다",
        "desc": "https://wikidocs.net/181967#79849",
        "cases": [
            [
                f"\\b(가져) ([오온올왔]\\w*)",
                "()()"
            ]
        ],
        "exception": []
    },
    {
        "name": "qa081555_여러 가지",
        "desc": "https://www.wikidocs.net/181967#81555",
        "cases": [
            [
                f"여러가지",
                "여러 가지"
            ]
        ],
        "exception": []
    },
    {
        "name": "qa084889_똑같은",
        "desc": "https://wikidocs.net/181967#84889",
        "cases": [
            [f"\\b똑 같은", "똑같은"]
        ],
        "exception": []
    },
    {
        "name": "qa086153_오도 가도",
        "desc": "https://www.wikidocs.net/181967#86153",
        "cases": [
            [f"오도가도", "오도 가도"]
        ],
        "exception": []
    },
    {
        "name": "qa090073_한때",
        "desc": "https://www.wikidocs.net/181967#90073",
        "cases": [
            [f"(\\w+[는은]) 한 (때의 \\w+[를을])", "() 한()"]
        ],
        "exception": []
    },
    {
        "name": "qa091617_때문",
        "desc": "https://www.wikidocs.net/181967#91617",
        "cases": [
            [f"\\b([그이])(때문\\w*)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "qa092387_훨씬 더",
        "desc": "https://www.wikidocs.net/181967#92387",
        "cases": [
            [f"훨씬더", "훨씬 더"]
        ],
        "exception": []
    },
    {
        "name": "qa094384a_집안",
        "desc": "https://www.wikidocs.net/181967#94384",
        "cases": [
            [f"\\b집 안([의]?) (식구|어른|운수)", "집안() ()"],
            [f"\\b집 안이 (망[하한할했]|안되|화합)(\\w*)", "집안이 ()()"]
        ],
        "exception": []
    },
    {
        "name": "qa094384b_집 안",
        "desc": "https://www.wikidocs.net/181967#94384",
        "cases": [
            [f"\\b집안(|에 있는|의) (각종 \\w+|물건|시설)", "집 안() ()"]
        ],
        "exception": []
    },
    {
        "name": "qa097252_우리말",
        "desc": "https://www.wikidocs.net/181967#97252",
        "cases": [
            [
                f"우리 말",
                "우리말"
            ]
        ],
        "exception": []
    },
    {
        "name": "qa102618_몇",
        "desc": "https://wikidocs.net/181967#102618",
        "cases": [
            [
                f"몇(가지|개|차례)",
                "몇 ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "qa103407_-명(名)",
        "desc": "https://wikidocs.net/181967#103407",
        "cases": [
            [
                f"\\b(디렉터리|메서드|물품|범주|변수|서비스|수도|지역|칼럼|클래스|파일|패키지|포장|폴더|함수|회사) 명(|까지\\w*|마다|마저\\w*|부터\\w*|뿐|에서\\w*|으로\\w*|을|이|조차\\w*)\\b",
                "()명()"]
        ],
        "exception": []
    },
    {
        "name": "qa105055_일어나다",
        "desc": "https://wikidocs.net/181967#105055",
        "cases": [
            [f"\\b일어 ([나난남날났]\\w*)", "일어()"]
        ],
        "exception": []
    },
    {
        "name": "qa109219_고장 나다",
        "desc": "https://wikidocs.net/181967#109219",
        "cases": [
            [f"\\b고장(나[는도서]|난|났\\w+)\\b", "고장 ()"]
        ],
        "exception": []
    },
    {
        "name": "qa113293_빈자리 / 빈 자리",
        "desc": "https://www.wikidocs.net/181967#113293",
        "cases": [
            [f"\\b빈 자리(나 가서|에) (앉\\w*)", "빈자리() ()"],
            [f"\\b빈 자리를 (노[리려]\\w*)", "빈자리를 ()"],
            [f"\\b(\\w+에) 빈 자리가 ([나날났]\\w*)", "() 빈자리가 ()"],
            [f"\\b빈 자리를 (메우.*사람\\w*)", "빈자리를 ()"]
        ],
        "exception": []
    },
    {
        "name": "qa113419_용지",
        "desc": "https://www.wikidocs.net/181967#113419",
        "cases": [
            [f"\\b([A-B][0-9]+)용지", "() 용지"]
        ],
        "exception": []
    },
    {
        "name": "qa114568_끝부분",
        "desc": "https://www.wikidocs.net/181967#114568",
        "cases": [
            [f"\\b끝 부분", "끝부분"]
        ],
        "exception": []
    },
    {
        "name": "qa116306_스타트업",
        "desc": "https://www.wikidocs.net/181967#116306",
        "cases": [
            [f"\\b스타트 업(|[도은을에이]|에서[도는만]?|이다|입니다)\\b", "스타트업()"]
        ],
        "exception": []
    },
    {
        "name": "qa116469_할 일 / 할 말",
        "desc": "https://www.wikidocs.net/181967#116469",
        "cases": [
            [f"\\b할([일말]\\w*)", "할 ()"]
        ],
        "exception": []
    },
    {
        "name": "qa117010_배",
        "desc": "https://www.wikidocs.net/181967#117010",
        "cases": [
            [f"\\b({KW_NNK})배(|[고나는다로를만면인일]|만큼|보다|여서[가는도]|였다|였습니다|이다|[이]?지만|임에도|입니다|쯤)\\b", "() 배()"]
        ],
        "exception": [f"한배 새끼"]
    },
    {
        "name": "qa117048_-까지 하다",
        "desc": "https://www.wikidocs.net/181967#117048",
        "cases": [
            [
                f"(고맙기까지)(하다)",
                "() ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "qa118484_봉지",
        "desc": "https://www.wikidocs.net/181967#118484",
        "cases": [
            [f"\\b(비닐) 봉지", "()봉지"],
            [f"\\b(설탕|종이)봉지", "() 봉지"]
        ],
        "exception": []
    },
    {
        "name": "qa124192_라, 라고",
        "desc": "https://wikidocs.net/181967#124192",
        "cases": [
            [f"(\\w*[^를을 ]) 라[ ]?([고]?)\\b", "()라()"]
        ],
        "exception": []
    },
    {
        "name": "qa124217_~에 따라",
        "desc": "https://wikidocs.net/181967#124217",
        "cases": [
            [f"(\\w+에)(따라[서]?)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "qa127230_와닿다",
        "desc": "https://wikidocs.net/181967#127230",
        "cases": [
            [f"b와 (닿[고는다아았은을지]\\w*)", "와()"]
        ],
        "exception": []
    },
    {
        "name": "qa127895_어처구니없다",
        "desc": "https://wikidocs.net/181967#127895",
        "cases": [
            [
                f"(어처구니) (없\\w*)",
                "()()"
            ]
        ],
        "exception": []
    },
    {
        "name": "qa129566_처리",
        "desc": "https://wikidocs.net/181967#129566",
        "cases": [
            [f"\\b(사고|일|주석|행정)(처리)", "() ()"],
            [f"\\b(처리)(속도)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "qa133755a_모양",
        "desc": "https://wikidocs.net/181967#133755",
        "cases": [
            [f"<Noun>모양", "() 모양"]
        ],
        "exception": []
    },
    {
        "name": "qa133790_가능한 한",
        "desc": "https://wikidocs.net/181967#133790",
        "cases": [
            [
                f"가능한한",
                "가능한 한"
            ]
        ],
        "exception": []
    },
    {
        "name": "qa133893_놀이 기구",
        "desc": "https://wikidocs.net/181967#133893",
        "cases": [
            [f"놀이기구", "놀이 기구"]
        ],
        "exception": []
    },
    {
        "name": "qa135077_한 해",
        "desc": "https://wikidocs.net/181967#135077",
        "cases": [
            [f"\\b(올|건강한) 한해\\b", "() 한 해"]
        ],
        "exception": []
    },
    {
        "name": "qa136393_더없이",
        "desc": "https://wikidocs.net/181967#136393",
        "cases": [
            [f"\\b더 없이 (행복)(\\w*)", "더없이 ()()"]
        ],
        "exception": []
    },
    {
        "name": "qa137856_오(誤)",
        "desc": "https://wikidocs.net/181967#137856",
        "cases": [
            [f"\\b오 ({KW_NAO})", "오()"]
        ],
        "exception": [f"빅-오", "빅 오"]
    },
    {
        "name": "qa139240_컵",
        "desc": "https://wikidocs.net/181967#139240",
        "cases": [
            [f"\\b(유리) 컵", "()컵"],
            [f"\\b(사기|청동)컵", "() 컵"]
        ],
        "exception": []
    },
    {
        "name": "qa142356_만 0세",
        "desc": "https://wikidocs.net/181967#142356",
        "cases": [
            [f"만([1-9]?[0-9]+)세", "만 ()세"]
        ],
        "exception": []
    },
    {
        "name": "qa145034_몸 둘 바",
        "desc": "https://wikidocs.net/181967#145034",
        "cases": [
            [f"\\b몸둘 바({KJ})", "몸 둘 바()"]
        ],
        "exception": []
    },
    {
        "name": "qa147892_나누어떨어지다",
        "desc": "https://wikidocs.net/181967#147892",
        "cases": [
            [f"\\b(나누어) (떨어[져졌지진질짐집]\\w*)", "()()"]
        ],
        "exception": []
    },
    {
        "name": "qa158311_초중반, 중후반",
        "desc": "https://wikidocs.net/181967#158311",
        "cases": [
            [
                f"초 중반",
                "초중반"
            ],
            [
                f"중 후반",
                "중후반"
            ]
        ],
        "exception": []
    },
    {
        "name": "qa158573_잘못되다",
        "desc": "https://wikidocs.net/181967#158573",
        "cases": [
            [f"(규정|규칙|문제|법|보기|예제|일|코드)(가|이) (잘못) ([되된될됐]\\w+)", "()() ()()"]
        ],
        "exception": []
    },
    {
        "name": "qa171555_방 안",
        "desc": "https://wikidocs.net/181967#171555",
        "cases": [
            [f"\\b(|내 )방안(|에[서]?) (가득|가보면|가서|\\w+ 공방|누가|누구|무슨 소리가|음악\\w*)", "()방 안() ()"]
        ],
        "exception": [f"감소", "강화", "개선", "개편", "결정", "관리", "관한", "대응", "도입", "발전", "방지", "방향", "보호", "설립", "시각화", "시행",
                      "실천", "운영", "육성", "저감", "제고", "처리", "확보", "활성화", "활용", "효율화"]
    },
    {
        "name": "qa174403_책임져 주다",
        "desc": "https://korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=174403",
        "cases": [
            [f"\\b(책임져)([주준줄줌줍]\\w*)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "qa177648_이렇다 할",
        "desc": "https://wikidocs.net/181967#177648",
        "cases": [
            [
                f"이렇다할",
                "이렇다 할"
            ]
        ],
        "exception": []
    },
    {
        "name": "qa179712_별다른",
        "desc": "https://wikidocs.net/181967#179712",
        "cases": [
            [f"\\b별 다른", "별다른"]
        ],
        "exception": []
    },
    {
        "name": "qa180311_쉴 새 없다",
        "desc": "https://wikidocs.net/181967#180311",
        "cases": [
            [f"\\b쉴새 (없\\w+)", "쉴 새 ()"],
            [f"\\b(쉴)[ ]?새(없\\w+)", "() 새 ()"]
        ],
        "exception": []
    },
    {
        "name": "qa184692_전(全)",
        "desc": "https://wikidocs.net/181967#184692",
        "cases": [
            [
                f"\\b전(국민|세계)",
                "전 ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "qa186744_따라가다",
        "desc": "https://wikidocs.net/181967#186744",
        "cases": [
            [f"\\b따라 (가며|가면서|가다|간|간다|갈|갈지[는도를만]?|감|갑니다|갔\\w*)\\b", "따라()"]
        ],
        "exception": []
    },
    {
        "name": "qa188364_디테일하다",
        "desc": "https://wikidocs.net/181967#188364",
        "cases": [
            [f"\\b디테일 ([하한할함해했]\\w*)", "디테일()"]
        ],
        "exception": []
    },
    {
        "name": "qa190403_그런가이다",
        "desc": "https://wikidocs.net/181967#190403",
        "cases": [
            [
                f"(그런가|그런지|그러냐|그럴까)[?]? ([이]?[었였]?다)\\b",
                "()()"
            ]
        ],
        "exception": []
    },
    {
        "name": "qa190536_하다 보면",
        "desc": "https://wikidocs.net/181967#190536",
        "cases": [
            [f"(\\w*하다|\\w*해[ ]?가다)(보면)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "qa192958_몸속",
        "desc": "https://wikidocs.net/181967#192958",
        "cases": [
            [f"\\b몸 속(|[도에은을의]|마저[도]?|만[도은을이]?|으로[는도]?|이[고다며면]?|이지[만]?|입니다|조차[도]?)\\b", "몸속()"]
        ],
        "exception": []
    },
    {
        "name": "qa195789_신경 쓰다",
        "desc": "https://wikidocs.net/181967#195789",
        "cases": [
            [f"\\b(신경)([써썼쓰쓴쓸씁]\\w*)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "qa200935a_모습",
        "desc": "https://wikidocs.net/181967#200935",
        "cases": [
            [f"\\b(생활|속)모습", "() 모습"]
        ],
        "exception": []
    },
    {
        "name": "qa200935b_겉모습",
        "desc": "https://wikidocs.net/181967#200935",
        "cases": [
            [f"\\b겉 모습", "겉모습"]
        ],
        "exception": []
    },
    {
        "name": "qa202694_올해",
        "desc": "https://wikidocs.net/181967#202694",
        "cases": [
            [f"올 해(?= 단 한 번)", "올해"]
        ],
        "exception": []
    },
    {
        "name": "qa203393_아주 오래전",
        "desc": "https://wikidocs.net/181967#203393",
        "cases": [
            [f"아주 오래 전", "아주 오래전"]
        ],
        "exception": []
    },
    {
        "name": "qa204769a_깨나",
        "desc": "https://wikidocs.net/181967#204769",
        "cases": [
            [f"<Noun> 깨나 ", "<Noun>깨나"]
        ],
        "exception": []
    },
    {
        "name": "qa204769b_꽤나",
        "desc": "https://wikidocs.net/181967#204769",
        "cases": [
            [f"<Noun>꽤나 ", "<Noun> 꽤나"]
        ],
        "exception": []
    },
    {
        "name": "qa205783_~하기만 하다",
        "desc": "https://wikidocs.net/181967#205783",
        "cases": [
            [f"\\b(\\w*[받보]|\\w*[려어워]지|미루|빼|숨)(기만)([하한할함합해했]\\w*)", "()() ()"],
            [f"\\b(귀찮|끔찍하|낯설|놀랍|두렵|멀|무겁|무섭|불길하|싫|아프|어색하|좋)(기만)([하한할함합해했]\\w*)", "()() ()"]
        ],
        "exception": []
    },
    {
        "name": "qa207925_야심 차다",
        "desc": "https://www.korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=&qna_seq=207925",
        "cases": [
            [f"\\b(야심)([차찬찰참찹]\\w*)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "qa208850_건너뛰다",
        "desc": "https://wikidocs.net/181967#208850",
        "cases": [
            [f"건너 ([뛰뛴]\\w*)", "건너()"]
        ],
        "exception": []
    },
    {
        "name": "qa209890_띄어쓰기",
        "desc": "https://www.korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=&qna_seq=209890",
        "cases": [
            [f"\\b(명령)(없이)", "() ()"],
            [f"\\b(예하|의뢰)(부대)", "() ()"],
            [f"\\b(임무)(수행)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "qa215319a_‘-ㄴ바’",
        "desc": "https://wikidocs.net/181967#215319",
        "cases": [
            [
                f"(\\w*한) (바[,]? 사실과 달랐다)",
                "()()"
            ]
        ],
        "exception": []
    },
    {
        "name": "qa215319b_‘바’",
        "desc": "https://wikidocs.net/181967#215319",
        "cases": [
            [
                f"(\\w*[진한])(바[가와])\\b",
                "() ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "qa219282_‘백스페이스’",
        "desc": "https://wikidocs.net/181967#219282",
        "cases": [
            [f"\\b백 스페이스", "백스페이스"]
        ],
        "exception": []
    },
    {
        "name": "qa219377_알 게",
        "desc": "https://wikidocs.net/181967#219377",
        "cases": [
            [f"\\b알게 (뭐야)", "알 게 ()"]
        ],
        "exception": []
    },
    {
        "name": "qa219618_‘꿈 꾸다’",
        "desc": "https://korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=219618",
        "cases": [
            [f"\\b(좋은) 꿈([꾸꾼꿀꿈꿉꿔꿨]\\w*)", "() 꿈 ()"]
        ],
        "exception": []
    },
    {
        "name": "qa220604a_개선 방안, 실천 방안",
        "desc": "https://korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=220604&pageIndex=1",
        "cases": [
            [f"\\b(개선|실천)(방안)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "qa222235_자료 요청",
        "desc": "https://wikidocs.net/181967#222235",
        "cases": [
            [f"자료요청", "자료 요청"]
        ],
        "exception": []
    },
    {
        "name": "qa222598a_사용 중",
        "desc": "https://wikidocs.net/181967#222598",
        "cases": [
            [
                f"([이사활]용)(중\\w*)",
                "() ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "qa224699_멍들다",
        "desc": "https://korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=224699",
        "cases": [
            [f"\\b멍 든 (|내 )가슴", "멍든 ()가슴"]
        ],
        "exception": []
    },
    {
        "name": "qa224845_빈자리",
        "desc": "https://www.wikidocs.net/181967#224845",
        "cases": [
            [f"\\b(네) 빈 자리가 (너무 [커크]\\w*)", "() 빈자리가 ()"]
        ],
        "exception": []
    },
    {
        "name": "qa225230_‘꿈꾸다’",
        "desc": "https://korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=225230",
        "cases": [
            [f"\\b꿈 ([꾸꾼꿀꿈꿉꿔꿨]\\w*)", "꿈()"]
        ],
        "exception": [f"나쁜", "무서운", "별난", "신기한", "웃기는", "유쾌한", "이상한", "재미있는", "재밌는", "좋은", "즐거운", "황당한", "희한한"]
    },
    {
        "name": "qa227135_안, 아니",
        "desc": "https://wikidocs.net/181967#227135",
        "cases": [
            [f"\\b(너무 \\w+서) 안(보[여였이인일임]\\w*)", "() 안 ()"],
            [f"\\b(안|아니)([넣]\\w+)", "() ()"],
            [f"\\b(잘) 안(보[여였이인일임]\\w*)", "() 안 ()"],
            [f"\\b안(\\w+키면|하려[고니면])", "안 ()"]
        ],
        "exception": []
    },
    {
        "name": "qa228050_가득 차다",
        "desc": "https://wikidocs.net/181967#228050",
        "cases": [
            [f"\\b가득([차찬찰참찹찼]\\w*)", "가득 ()"]
        ],
        "exception": []
    },
    {
        "name": "qa228324_-마저(보조사)",
        "desc": "https://www.korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=228324",
        "cases": [
            [f"\\b([그이저]|너) (마저|마저도)\\b", "()()"]
        ],
        "exception": []
    },
    {
        "name": "qa228949_디자인되다",
        "desc": "https://wikidocs.net/181967#228949",
        "cases": [
            [f"\\b(디자인) ([돼됐되된될됨됩]\\w*)", "()()"]
        ],
        "exception": []
    },
    {
        "name": "qa229580_일수",
        "desc": "https://wikidocs.net/181967#229580",
        "cases": [
            [f"\\b(연체)일수", "() 일수"],
            [f"\\b(연체)([된]?)[ ]?일 수(만큼)", "()() 일수()"],
            [f"\\b일 수 (차이)", "일수 ()"]
        ],
        "exception": []
    },
    {
        "name": "qa229929_‘방식’의 띄어쓰기",
        "desc": "https://www.korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=229929",
        "cases": [
            [f"\\b(어떤)(방식)", "() ()"],
            [f"\\b(생성|업무[ ]?처리|작동|표현|호출)(방식)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "qa234751_게임 회사",
        "desc": "https://wikidocs.net/181967#234751",
        "cases": [
            [
                f"(게임)(회사)",
                "() ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "qa235107_현 상태",
        "desc": "https://www.korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=235107",
        "cases": [
            [f"\\b현상태", "현 상태"]
        ],
        "exception": []
    },
    {
        "name": "qa235571_접두사 ‘기-’",
        "desc": "https://korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=235571&pageIndex=1",
        "cases": [
            [f"\\b기 (신청|참가)", "기()"]
        ],
        "exception": []
    },
    {
        "name": "qa236477_한데",
        "desc": "https://wikidocs.net/181967#236477",
        "cases": [
            [f"\\b한 데 (모[아았여였으은을이인일임]\\w*)", "한데 ()"]
        ],
        "exception": []
    },
    {
        "name": "qa237177_‘건’의 띄어쓰기",
        "desc": "https://korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=237177",
        "cases": [
            [f"\\b(요청|지출)건(|[에은을이임]|으로|이[고다]|이지\\w*|입니다)\\b", "() 건()"]
        ],
        "exception": []
    },
    {
        "name": "qa238217_마음가짐",
        "desc": "https://wikidocs.net/181967#238217",
        "cases": [
            [f"마음 가짐", "마음가짐"]
        ],
        "exception": []
    },
    {
        "name": "qa238792_바로 바로",
        "desc": "https://korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=238792",
        "cases": [
            [f"바로바로", "바로 바로"]
        ],
        "exception": []
    },
    {
        "name": "qa239943_-기 쉽다",
        "desc": "https://wikidocs.net/181967#239943",
        "cases": [
            [
                f"(\\w*기)([쉬쉽]\\w*)",
                "() ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "qa242312_책임지다",
        "desc": "https://korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=242312",
        "cases": [
            [f"\\b(책임) (져[라요]?)\\b", "()()"],
            [f"\\b(책임) (져)([주준줄줌줍]\\w*)", "()() ()"],
            [f"\\b(책임) ([졌지진질짐집]\\w*)", "()()"]
        ],
        "exception": []
    },
    {
        "name": "qa242860_자리 잡다",
        "desc": "https://korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=242860",
        "cases": [
            [f"\\b(자리)(잡[고는다아았은을지]\\w*)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "qa243287_~들 하다",
        "desc": "https://korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=243287",
        "cases": [
            [f"\\b(너무)들([하한]다\\w*)", "()들 ()"],
            [f"\\b(놀고)들(있\\w*)", "()들 ()"]
        ],
        "exception": []
    },
    {
        "name": "qa245039_최우선 순위",
        "desc": "https://korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=245039",
        "cases": [
            [f"\\b(최우선)(순위)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "qa245625_줄",
        "desc": "https://wikidocs.net/181967#245625",
        "cases": [
            [f"\\b({KW_NAO})([된한])(줄)", "()() ()"]
        ],
        "exception": []
    },
    {
        "name": "qa246790_남짓 되다",
        "desc": "https://wikidocs.net/181967#246790",
        "cases": [
            [f"\\b(남짓)([돼됐되된된됨됩]\\w*)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "qa249863_책임져 보라지",
        "desc": "https://korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=249863",
        "cases": [
            [f"\\b(책임져)(보라지)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "qa250547_둘째(로) 치다",
        "desc": "https://korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=250547",
        "cases": [
            [f"\\b둘째(치[고더]\\w*)", "둘째 ()"]
        ],
        "exception": []
    },
    {
        "name": "qa254392_흉내 내다",
        "desc": "https://korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=254392",
        "cases": [
            [f"\\b(흉내)(내|내[고는다지]|내[ ]?[보본볼봄봅봐봤]\\w*|[낼냈]\\w+|낸\\w*)\\b", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "qa254557_이어 붙이다",
        "desc": "https://korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=254557",
        "cases": [
            [f"\\b(이어)(붙[여였이인일임]\\w*)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "qa259483_첫 삽",
        "desc": "https://korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=259483&pageIndex=1",
        "cases": [
            [f"\\b첫삽(|을)\\b", "첫 삽()"]
        ],
        "exception": []
    },
    {
        "name": "qa267989a_‘-쯤’(접미사)의 띄어쓰기",
        "desc": "https://korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=267989",
        "cases": [
            [f"\\b({KW_NT}) 쯤", "()쯤"]
        ],
        "exception": []
    },
    {
        "name": "scourt01_띄어쓰기 (법원 맞춤법 자료집)",
        "desc": "https://blog.kakaocdn.net/dn/lr24s/btqGxPXXP3n/sGKLZ7RKK4sOSksoCH14U0/%EB%B2%95%EC%9B%90%20%EB%A7%9E%EC%B6%A4%EB%B2%95%20%EC%9E%90%EB%A3%8C%EC%A7%91%20%EC%B5%9C%EC%A2%85.pdf?attach=1&knm=tfile.pdf",
        "cases": [
            [f"\\b(앞) ([서선설섰]\\w*)", "()()"]
        ],
        "exception": []
    },
    {
        "name": "sd059795_날것",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=59795&searchKeywordTo=3",
        "cases": [
            [f"\\b날 것(으로|을)\\b", "날것()"]
        ],
        "exception": []
    },
    {
        "name": "sd065304_너무",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=65304&searchKeywordTo=3",
        "cases": [
            [
                f"\\b(너무)(가[까깝]|가[는늘]|가[벼볍]|[긴길]|꽉|[끼낀]|넓|뜨[거겁]|[머먼멀]|몰라라|무[서섭]|반[가갑]|시끄|어[려렵]|예[쁘쁜쁠]|작|좁|좋|짧|차[가갑]|[차찬]|[커크큰])(\\w*)",
                "() ()()"],
            [f"\\b(너무)(걱정|잘)([하한할함합해했]\\w*)", "() ()()"],
            [f"\\b(너무)(위험|조용|한심|헐렁)([하한할함합해했]\\w*)", "() ()()"]
        ],
        "exception": []
    },
    {
        "name": "sd066207_너무너무",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=66207&searchKeywordTo=3",
        "cases": [
            [f"\\b너무 너무", "너무너무"]
        ],
        "exception": []
    },
    {
        "name": "sd092920_둘러싸다",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=92920&searchKeywordTo=3",
        "cases": [
            [f"\\b둘러 (싸여|싼)", "둘러()"]
        ],
        "exception": []
    },
    {
        "name": "sd108846_마이크로초",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=108846&searchKeywordTo=3",
        "cases": [
            [f"\\b(마이크로) (초)(|에)\\b", "()()()"]
        ],
        "exception": []
    },
    {
        "name": "sd109178_마찬가지",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=109178&searchKeywordTo=3",
        "cases": [
            [f"\\b마찬 가지", "마찬가지"]
        ],
        "exception": []
    },
    {
        "name": "sd131144_반세기",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=131144&searchKeywordTo=3",
        "cases": [
            [f"\\b반 세기(가 지난)\\b", "반세기()"]
        ],
        "exception": []
    },
    {
        "name": "sd153137_붙이다",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=153137&searchKeywordTo=3",
        "cases": [
            [f"(\\w+[를을]) 붙 ([여였]\\w*|이[고는다지며면]\\w*|입니다)", "() 붙()"]
        ],
        "exception": []
    },
    {
        "name": "sd168191_사고방식",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=168191&searchKeywordTo=3",
        "cases": [
            [f"사고 방식", "사고방식"]
        ],
        "exception": []
    },
    {
        "name": "sd196444_소중하다",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=196444&searchKeywordTo=3",
        "cases": [
            [f"\\b소 중([하한할함합해했]\\w*)", "소중()"]
        ],
        "exception": []
    },
    {
        "name": "sd205007_시기상조",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=205007&searchKeywordTo=3",
        "cases": [
            [f"\\b시기 상조", "시기상조"]
        ],
        "exception": []
    },
    {
        "name": "sd300317_제아무리",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=300317&searchKeywordTo=3",
        "cases": [
            [f"\\b제 아무리\\b", "제아무리"]
        ],
        "exception": []
    },
    {
        "name": "sd307099_주어지다",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=307099&searchKeywordTo=3",
        "cases": [
            [f"\\b(주어) (져[도서]?|졌\\w*|지[고는다며면지]\\w*|진|진다[고는며면]?|질|질지[는도]?|짐|집니다)\\b", "()()"]
        ],
        "exception": []
    },
    {
        "name": "sd321549_첫선",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=321549&searchKeywordTo=3",
        "cases": [
            [f"\\b첫 선을\\b", "첫선을"]
        ],
        "exception": []
    },
    {
        "name": "sd238080_열수",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=238080&searchKeywordTo=3",
        "cases": [
            [f"\\b열 수([.])", "열수"]
        ],
        "exception": []
    },
    {
        "name": "sd365913_행수",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=365913&searchKeywordTo=3",
        "cases": [
            [f"\\b행 수([가는도를와]?)\\b", "행수()"]
        ],
        "exception": []
    },
    {
        "name": "sd372807_형제자매",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=372807&searchKeywordTo=3",
        "cases": [
            [f"\\b형제 자매", "형제자매"]
        ],
        "exception": []
    },
    {
        "name": "sd385449_흘러가다",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=385449&searchKeywordTo=3",
        "cases": [
            [f"(\\w+[으]?로|\\w+에게) 흘러 ([가간갈감갑갔]\\w+)", "() 흘러()"]
        ],
        "exception": []
    },
    {
        "name": "sd386684_힘들다",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=386684&searchKeywordTo=3",
        "cases": [
            [f"\\b힘 (드는|드[냐네니]|드시죠|들기만|들[어여][도서]?|들다[고는며면]?|들면|들죠|들지[만]?|듭니다)\\b", "힘()"],
            [f"(\\w+기)[ ]?힘든[ ]?[대데]를\\b", "() 힘든 데를"],
            [f"\\b힘 (드는|[든들])데\\b", "힘()데"]
        ],
        "exception": []
    },
    {
        "name": "sd390272_가로지르다",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=390272&searchKeywordTo=3",
        "cases": [
            [f"\\b가로 질러", "가로질러"]
        ],
        "exception": []
    },
    {
        "name": "sd390853_-게끔",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=390853&searchKeywordTo=3",
        "cases": [
            [f"\\b(맞|살|없|있|지|지나가)게 끔\\b", "()게끔"],
            [f"\\b({KW_NAO})([되하])게 끔\\b", "()()게끔"]
        ],
        "exception": []
    },
    {
        "name": "sd394721_‘-고’(접사)",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=394721&searchKeywordTo=3",
        "cases": [
            [f"(\\w*[를을]) ({KW_NAO})하 ([고곤][는도서선요]?)\\b", "() ()하()"]
        ],
        "exception": []
    },
    {
        "name": "sd401618_그럴듯하다",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=401618&searchKeywordTo=3",
        "cases": [
            [f"\\b그럴 듯[ ]?([하한할함합해했]\\w*)", "그럴듯()"]
        ],
        "exception": []
    },
    {
        "name": "sd411222_너무하다",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=411222&searchKeywordTo=3",
        "cases": [
            [f"\\b(너무) (하[는네다]\\w*|[한할함합해했]\\w*)\\b", "()()"]
        ],
        "exception": []
    },
    {
        "name": "sd414967_더하다",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=414967&searchKeywordTo=3",
        "cases": [
            [f"\\b(\\w+에 .*[가이]) 더 (해[져졌지진질짐집]\\w*)", "() 더()"]
        ],
        "exception": []
    },
    {
        "name": "sd420569_-ㄹ지언정",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=420569&searchKeywordTo=3",
        "cases": [
            [f"(\\w+)([{KL_WFL}]) 지언정\\b", "()()지언정"]
        ],
        "exception": []
    },
    {
        "name": "sd422416_만(滿)",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=4224168&searchKeywordTo=3",
        "cases": [
            [f"\\b만나이(|가|로[는]|를|인|인[가지][요]?)\\b", "만 나이()"]
        ],
        "exception": []
    },
    {
        "name": "sd429547_밤사이",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=429547&searchKeywordTo=3",
        "cases": [
            [f"\\b밤 사이 (내린|눈이|눈 한 번|비가|안녕\\w*)", "밤사이 ()"],
            [f"\\b밤 사이(에)\\b", "밤사이()"]
        ],
        "exception": []
    },
    {
        "name": "sd429331_밤새",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=429331&searchKeywordTo=3",
        "cases": [
            [f"\\b밤 새 (내린|눈이|눈 한 번|비가|안녕\\w*)", "밤사이 ()"]
        ],
        "exception": []
    },
    {
        "name": "sd440506_산속",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=440506&searchKeywordTo=3",
        "cases": [
            [f"\\b산 속(|에[서]?)\\b", "산속()"]
        ],
        "exception": []
    },
    {
        "name": "sd453038_악영향",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=453038&searchKeywordTo=3",
        "cases": [
            [f"\\b악 영향", "악영향"]
        ],
        "exception": []
    },
    {
        "name": "sd462264_왜냐하면",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=462264&searchKeywordTo=3",
        "cases": [
            [f"\\b왜냐 하면", "왜냐하면"]
        ],
        "exception": []
    },
    {
        "name": "sd475183_자기소개",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=475183&searchKeywordTo=3",
        "cases": [
            [f"\\b자기 소개", "자기소개"]
        ],
        "exception": []
    },
    {
        "name": "sd484058_집수리",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=484058&searchKeywordTo=3",
        "cases": [
            [f"\\b(?<!낡은 )집 수리", "집수리"]
        ],
        "exception": []
    },
    {
        "name": "sd488873_차세대",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=488873&searchKeywordTo=3",
        "cases": [
            [f"\\b차 세대 (시스템|전차|전투기)", "차세대 ()"]
        ],
        "exception": []
    },
    {
        "name": "sd499004_한때",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=499004&searchKeywordTo=3",
        "cases": [
            [f"\\b한 때(|는|에)\\b", "한때()"]
        ],
        "exception": []
    },
    {
        "name": "sd499362_파고들다",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=499362&searchKeywordTo=3",
        "cases": [
            [f"\\b파고 들([고다며면었지]\\w*| [것수]\\w*|어|어서[는]?|어[도선야])\\b", "파고들()"],
            [f"\\b파고 들어[ ]?([가간갈감갑갔보본볼봄봅봐봤]\\w*)", "파고들어 ()"],
            [f"\\b파고 드는([걸게]|)\\b", "파고드는 ()"]
        ],
        "exception": []
    },
    {
        "name": "sd501417_현시점",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=501417&searchKeywordTo=3",
        "cases": [
            [f"\\b현 시점[ ]?에(서[는]?|선)\\b", "현시점에()"]
        ],
        "exception": []
    },
    {
        "name": "sd503615_하나하나",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=503615&searchKeywordTo=3",
        "cases": [
            [f"\\b하나 하나(|[가를에])\\b", "하나하나()"]
        ],
        "exception": []
    },
    {
        "name": "sd516024_눈치채다",
        "desc": "https://stdict.korean.go.kr/search/searchView.do?word_no=506024&searchKeywordTo=3",
        "cases": [
            [f"\\b(눈치) ([채챈챌챘]\\w*)", "()()"]
        ],
        "exception": []
    },
    {
        "name": "senfin10_[우리말 길라잡이] (10) 띄어쓰기, 최소한 이 정도는 지키자",
        "desc": "https://m.blog.naver.com/senfin/130183209503",
        "cases": [
            [
                f"내일 부터",
                "내일부터"
            ],
            [
                f"([1-9]?[0-9]+)년동안",
                "()년 동안"
            ],
            [
                f"가을 밤",
                "가을밤"
            ],
            [
                f"같은해",
                "같은 해"
            ],
            [
                f"그 때 까지",
                "그때까지"
            ],
            [
                f"[이윤박최전노김이문윤] 전대통령",
                "() 전 대통령"
            ],
            [
                f"다가 오다",
                "다가오다"
            ],
            [
                f"다시말해",
                "다시 말해"
            ],
            [
                f"다음해",
                "다음 해"
            ],
            [
                f"돌려 받다",
                "돌려받다"
            ],
            [
                f"맞은 편",
                "맞은편"
            ],
            [
                f"맨 눈",
                "맨눈"
            ],
            [
                f"맨 몸",
                "맨몸"
            ],
            [
                f"먹자 마자",
                "먹자마자"
            ],
            [
                f"못가다",
                "못 가다"
            ],
            [
                f"못미치다",
                "못 미치다"
            ],
            [
                f"못지 않다",
                "못지않다"
            ],
            [
                f"방안 조차",
                "방안조차"
            ],
            [
                f"보자 마자",
                "보자마자"
            ],
            [
                f"\\b수 차례",
                "수차례"
            ],
            [
                f"스물 다섯살",
                "스물다섯 살"
            ],
            [
                f"여러차례",
                "여러 차례"
            ],
            [
                f"온 몸",
                "온몸"
            ],
            [
                f"\\b이 참에",
                "이참에"
            ],
            [
                f"이런 저런",
                "이런저런"
            ],
            [
                f"이번 처럼",
                "이번처럼"
            ],
            [
                f"이에대해",
                "이에 대해"
            ],
            [
                f"이에따라",
                "이에 따라"
            ],
            [
                f"이와관련",
                "이와 관련"
            ],
            [
                f"이와함께",
                "이와 함께"
            ],
            [
                f"잘들린다",
                "잘 들린다"
            ],
            [
                f"첫 맛",
                "첫맛"
            ],
            [
                f"첫 발([을이])",
                "첫발()"
            ],
            [
                f"최근들어",
                "최근 들어"
            ],
            [
                f"하지 않은채",
                "하지 않은 채"
            ],
            [
                f"\\b한 가운데",
                "한가운데"
            ],
            [
                f"\\b한 몫",
                "한몫"
            ],
            [
                f"\\b한 복판",
                "한복판"
            ],
            [
                f"\\b한 입에",
                "한입에"
            ],
            [
                f"\\b한치의 양보",
                "한 치의 양보"
            ],
        ],
        "exception": []
    },
    {
        "name": "spacerr1_띄어쓰기 오류",
        "desc": "",
        "cases": [
            [f"({KW_BW})(보[여이]\\w*)", "() ()"],
            [f"\\b각 각\\b", "각각"],
            [f"({KW_NAO})({KC_H})[ ]{{2,}}(\\w+)", "()() ()"],
            [f"(\\w+준)[ ]?(후)[ ]{{2,}}(이)\\b", "() () ()"],
            [f"(\\w+)({KC_H})[ ]{{2,}}([A-Za-z가-힣 ]*)(\\w+[을를])", "()() ()()"],
            [f"\\b호 불호", "호불호"],
            [f"\\맨인 블랙", "맨 인 블랙"],
            [f"\\우 상향", "우상향"],
            [f"\\b({KW_NP}) (끼리\\w*)", "()()"],
            [f"\\b스프레드 시트", "스프레드시트"],
            [f"\\b(\\w+)({KJ})  (값)({KJ})", "()() ()()"],
            [f"\\b인플레 이션", "인플레이션"],
            [f"(\\w+까지[는])[ ]{{2,}}(다) ({KW_NAO})(해[주준줄줌줍줘줬]\\w*)", "() () ()()"],
            [f"(\\w*[갑겁깁납답맙밉빕빱뺍삽습십쌉쏩압옵입잡줍집짭찹칩탑팝합]니) (다[.])", "()()"],
            [f"\\b도 움(|[을이])\\b", "도움()"],
            [f"\\b(않는) 다는[ ]?점", "()다는 점"]
        ],
        "exception": []
    },
    {
        "name": "tw154470_눈 깜짝 할 새",
        "desc": "https://twitter.com/urimal365/status/154470168028917760",
        "cases": [
            [
                f"\\b(눈[ ]?깜짝[ ]?할[ ]?새)",
                "눈 깜짝 할 새"
            ]
        ],
        "exception": [f"눈 깜짝 할 새"]
    },
    {
        "name": "tw191693_두세",
        "desc": "https://twitter.com/urimal365/status/191693160609628160",
        "cases": [
            [f"\\b두 세 ({KW_NU})", "두세 ()"]
        ],
        "exception": [f"눈 깜짝 할 새"]
    },
    {
        "name": "tw196826_앞다투다",
        "desc": "https://twitter.com/urimal365/status/196826972091981825",
        "cases": [
            [f"\\b앞 (다투[고는다며면지]\\w*|다퉈\\w*)", "앞()"]
        ],
        "exception": []
    },
    {
        "name": "tw240691_~인 줄",
        "desc": "https://twitter.com/urimal365/status/240691648537956352",
        "cases": [
            [f"(\\w+인)줄 (알\\w+)", "() 줄 ()"]
        ],
        "exception": []
    },
    {
        "name": "tw258432_수많은",
        "desc": "https://twitter.com/urimal365/status/258432299744505859",
        "cases": [
            [
                f"\\b수 많은",
                "수많은"
            ]
        ],
        "exception": []
    },
    {
        "name": "tw275872_발 빠르다",
        "desc": "https://twitter.com/urimal365/status/275872341442039808",
        "cases": [
            [f"\\b(발)(빠[르른]\\w*)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "tw276189_까지",
        "desc": "https://twitter.com/urimal365/status/276189413980123137",
        "cases": [
            [f"(\\d+[ ]?)(cm|m|km) (까지|까지라면)", "()()()"],
            [f"(\\d+)[ ]?~[ ]?(\\d+) (까지)(|라면)\\b", "(1)~(2)(이)(4)"],
            [f"\\b점 까지", "점까지"]
        ],
        "exception": []
    },
    {
        "name": "tw296148_그런 것",
        "desc": "https://twitter.com/urimal365/status/296148953202827265",
        "cases": [
            [
                f"(그런|이런)(것\\w*)",
                "() ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "tw302313_하지 마",
        "desc": "https://twitter.com/urimal365/status/302313996239900672",
        "cases": [
            [f"(\\w*[가개걸골기꾸놀누눕니달때떼리막먹묻밀받보비빌사싸쓰오우울잡접졸주줍집쫄차치타파팔펴풀하])지(마[라]?|말[거아]?라)\\b", "()지 ()"]
        ],
        "exception": []
    },
    {
        "name": "tw308807_땜에",
        "desc": "https://twitter.com/urimal365/status/308807079404118016",
        "cases": [
            [f"\\b({KW_NT})([ ]?때매|땜에)", "() 땜에"],
            [f"\\b(그|그것|너|당신|무엇|뭐|뭣|저)([ ]?때매|땜에)", "() 땜에"]
        ],
        "exception": []
    },
    {
        "name": "tw321078_될 텐데",
        "desc": "https://twitter.com/urimal365/status/321078665750384641",
        "cases": [
            [f"(\\w*[{KL_WFL}])(텐데[요]?)", "() ()"]
        ],
        "exception": []
    },
    {
        "name": "tw332012_그걸",
        "desc": "https://twitter.com/urimal365/status/332012358945890304",
        "cases": [
            [f"\\b그 걸\\b", "그걸"]
        ],
        "exception": []
    },
    {
        "name": "tw349754_두말하다",
        "desc": "https://twitter.com/urimal365/status/349754585063235585",
        "cases": [
            [f"\\b두 말[ ]?([하한할함합해했]\\w*)", "두말()"]
        ],
        "exception": []
    },
    {
        "name": "tw376953_알아맞히다",
        "desc": "https://twitter.com/urimal365/status/376953104568033280",
        "cases": [
            [f"\\b알아 맞[춰혀][ ]?([보본볼봄봅봐봤]\\w*)", "알아맞혀 ()"]
        ],
        "exception": []
    },
    {
        "name": "tw408870_-지 않다",
        "desc": "https://twitter.com/urimal365/status/408870612610719744",
        "cases": [
            [f"\\b({KW_NAO})([되하]지)(않\\w*)", "()() ()"]
        ],
        "exception": []
    },
    {
        "name": "tw535315_한 방향",
        "desc": "https://twitter.com/urimal365/status/535315977618333696",
        "cases": [
            [
                f"\\b한(방향\\w*)",
                "한 ()"
            ]
        ],
        "exception": []
    },
    {
        "name": "tw535690_-자마자",
        "desc": "https://twitter.com/urimal365/status/535690841025564672",
        "cases": [
            [f"(\\w+)자 마자", "()자마자"]
        ],
        "exception": []
    },
    {
        "name": "kss-add-1",
        "desc": "",
        "cases": [
            [f"우리 나라", "우리나라"]
        ],
        "exception": []
    },
    {
        "name": "kss-add-2",
        "desc": "",
        "cases": [
            ["연구 진", "연구진"]
        ],
        "exception": [],
    }
]

TABLE = []
find_morphs = re.compile(r'<\w+>')
find_good = re.compile(r"(?<=[(])[1-9]*(?=[)])")
for rule in RULES:
    cases = []
    _name = rule['name']
    _desc = rule['desc']
    _exceptions = rule['exception']
    for rc in rule['cases']:
        if len(rc[0]) > 4 and rc[0][:4] in ['~은/는', '~이/가', '~을/를', '~와/과']:
            try:
                cases.append((_name, _desc, '~' + rc[0][1] + rc[0][4:], '~' + rc[1][1] + rc[1][4:], _exceptions))
            except:
                cases.append((_name, _desc, '~' + rc[0][1] + rc[0][4:], rc[1], _exceptions))
            try:
                cases.append((_name, _desc, '~' + rc[0][3] + rc[0][4:], '~' + rc[1][3] + rc[1][4:], _exceptions))
            except:
                cases.append((_name, _desc, '~' + rc[0][3] + rc[0][4:], rc[1], _exceptions))
        else:
            cases.append((_name, _desc, rc[0], rc[1], _exceptions))
    TABLE.append(cases)

for rule_idx, rule in enumerate(TABLE):
    for cs_idx, (_name, _desc, _bad, _good, _exceptions) in enumerate(rule):
        TABLE[rule_idx][cs_idx] = (
            cs_idx,
            _name,
            _desc,
            re.compile(_bad),
            _bad,
            find_good.findall(_good),
            _good,
            tuple(_exceptions),
        )


def pos_processing(cs_idx, name, desc, bad, good, exceptions, text, morphs, target_pos, startswith):
    targets = [w for w, p in morphs if p.startswith(startswith)]
    results = set()
    for t in targets:
        candidate = bad.replace(target_pos, t)
        if candidate in text:
            bad = candidate
            good = good.replace(target_pos, t)
            good = good.replace('()', t)
            results.add((cs_idx, name, desc, bad, good, exceptions))
    return results


def morpheme_processing(cs_idx, name, desc, bad, good, exceptions, text, morphs):
    results = set()
    for a in find_morphs.findall(bad):
        for b in [w for w, p in morphs if f"<{p}>" == a]:
            good = good.replace(a, b)
            bad = bad.replace(a, b)
            if bad in text:
                results.add((cs_idx, name, desc, bad, good, exceptions))
    return results


def postprocess(text, morphs):
    results = set()
    for rule in TABLE:
        for cs_idx, name, desc, bad_compile, bad, good_findall, good, exceptions in rule:
            if any(map(lambda x: x in r'[]\+?|', bad)):
                m = bad_compile.search(text)
                if m:
                    bad = m.group()
                    remain = good
                    buffer = ""
                    k = 1
                    for s in good_findall:
                        n = int(s) if len(s) > 0 else k
                        k += 1
                        if f'({n})' in remain:
                            buffer += remain[:remain.index(f'({n})')] + m.group(n)
                            remain = remain[remain.index(f'({n})') + len(f'({n})'):]
                        elif '()' in remain:
                            try:
                                buffer += remain[:remain.index('()')] + m.group(n)
                                remain = remain[remain.index('()') + len('()'):]
                            except:
                                pass
                        else:
                            pass
                    good = buffer + remain
                    results.add((cs_idx, name, desc, bad, good, exceptions))
                else:
                    continue

            else:
                if "<" in bad:
                    if "<Noun>" in bad:
                        results.update(pos_processing(cs_idx, name, desc, bad, good, exceptions, text, morphs, "<Noun>", "N"))
                    elif "<Adverb>" in bad:
                        results.update(pos_processing(cs_idx, name, desc, bad, good, exceptions, text, morphs, "<Adverb>", "M"))
                    else:
                        results.update(morpheme_processing(cs_idx, name, desc, bad, good, exceptions, text, morphs))

    for _cs_idx, name, desc, bad, good, exceptions in results:
        loc = text.find(bad)
        skip = False
        for ex in exceptions:
            beg, end = 0, -1
            sz = 10
            if loc > sz:
                beg = loc - sz
            if len(text) - loc > 10:
                end = loc + sz
            window = text[beg:end]

            if ex in window:
                skip = True

        if not skip:
            good = good.replace("()", "")
            text = text.replace(bad, good)

    return text


def postprocess_heuristic(text):
    text = text.replace(",", ", ")
    text = text.replace(":", ": ")
    text = re.sub(r"  +", " ", text)
    text = re.sub(r"[\n\t\v\f\r]  {1,}", " ", text)
    text = re.sub(r" {1,}[\n\t\v\f\r]", " ", text)

    text = comma_with_numbers.sub(r"\1,\2", text)
    text = re.sub(r"  +", " ", text)
    return text

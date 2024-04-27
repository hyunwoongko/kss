import re
from functools import partial
from typing import Union, List, Tuple

from kss._utils.logger import highlight_diffs, logger
from kss._utils.multiprocessing import _run_job
from kss._utils.sanity_checks import _check_text, _check_type, _check_num_workers

normalization_open = {
    "< ": "<",
    "〈 ": "<",
    "〈": "<",
    "[ ": "[",
    "( ": "(",
}

normalization_close = {
    " >": ">",
    "〉": ">",
    " 〉": ">",
    " ]": "]",
    " )": ")",
}

normalization_others = {
    "\\n": "\n",
    ". .": "..",
    ". ?": ".?",
    ". !": ".!",
    "! !": "!!",
    "! .": "!.",
    "! ?": "!?",
    "? .": "?.",
    "? !": "?!",
    "? ?": "??",
    ". \" ": ".\" ",
    "! \" ": "!\" ",
    "? \" ": "?\" ",
    "  ": " ",
    "\n ": "\n",
    " \n": "\n",
}

skip_words = [
    "부친상", "모친상", "조부상", "조모상",
    "부고", "별세", "총경 전보", "소방경",
    "인사]",
]

media_list = ['10+Star', 'News1', '21C FA VISION', '365베케이션', '뉴스1', '뉴스핌', '911TV', 'APP저널', 'BBS불교방송', 'BI코리아', 'C3',
              'CARGUY', 'CBS', 'CEO&', 'CEO스코어데일리', 'CIOBIZ+', 'CIOCISO', 'CLO', 'CMC가족오락TV', 'CNB국회방송', 'EBN', 'EPnC',
              'ESCO', 'FAM타임스', 'FA저널', 'FSTV', 'Factiva', 'GIB거제인터넷방송', 'GQ KOREA', 'Groove Korea', 'G밸리', 'HKBC환경방송',
              'HR Insight', 'IP노믹스', 'IT NEWS', 'IT동아', 'IT조선', 'JBC까', 'JTBC', 'K STAR', 'KBS대전', 'KBS미디어', 'KBS춘천',
              'KNN', 'KTV국민방송', 'Kjtimes', 'K모바일', 'MBC경남', 'MBN', 'MBN스타', 'MFG', 'MFIGHT', 'MK스포츠', 'MTN머니투데이방송',
              'Mom대로 키워라', 'M이코노미', 'NBC-1TV', 'NDSOFT', 'NSP통신', 'OBS경인TV', 'OBS플러스', 'OLEDNET', 'OSEN', 'QBS', 'RPM9',
              'RTN부동산TV', 'SBS CNBC', 'SBS Sports', 'SBS funE', 'SEOUL', 'SPACE', 'SPO TV', 'SPOTV NEWS', 'SP투데이',
              'STN SPORTS', 'STYLER', 'TBN한국교통방송', 'TBS교통방송', 'TJB대전방송', 'TK TIMES', 'TV리포트', 'TV조선', 'YTN', 'YTN사이언스',
              'e대학저널', 'e메디코파마', 'e헬스통신', 'icross 교차로', 'jtbc GOLF', '가구저널', '가톨릭평화방송', '건강다이제스트', '건설경제', '건축리포트와이드',
              '건축문화', '게임동아', '게임메카', '게임조선', '게임포커스', '겜툰', '경기시사투데이', '경남매일', '경제풍월', '경제플러스', '경찰방송', '경향게임스',
              '계간 조각', '계장기술', '골닷컴', '골드앤와이즈', '골프가이드', '골프다이제스트', '골프먼스리', '골프세미나', '골프저널', '골프코스 관리정보', '골프포위민',
              '골프한국', '공구사랑', '공구저널', '공무원저널', '공예+디자인', '과학동아', '과학소년', '광주드림', '교육희망', '국방과기술', '국악방송', '국제골프',
              '국토매일', '국토와교통', '국회방송', '군사저널', '귀금속과시계', '그린데일리', '그린투데이', '글로벌이코노믹', '글마루', '금융플러스', '금형기술', '금형저널',
              '기계&자동화', '기술과경영', '기어박스', '까사리빙', '꼬망세', '나라경제', '나우앤티비', '낚시춘추', '난과생활', '내셔널지오그래픽', '내외경제TV',
              '내외전기통신저널', '내외통신', '냉동공조', '네비포유', '네이버 보도자료', '네일홀릭', '넥스트데일리', '넥스트이코노미', '넷퓨', '넷프로', '노동과세계', '노블리안',
              '노트포럼', '녹색경제', '녹색저널', '뉴데일리', '뉴데일리경제', '뉴시스', '뉴트리앤', '다다미디어', '다산저널', '다아라매거진', '다이어트데일리', '닥터W',
              '대덕넷', '대학경제', '대학내일', '대한간호', '대한포커스', '댄스포럼', '더 기어', '더 퍼스트클래스', '더갤러리아', '더게임스', '더골프', '더그아웃', '더닥터',
              '더리더', '더모토', '더뮤지컬', '더바이어', '더바이크', '더불어사는사회', '더셀러브리티', '더스쿠프', '더스포츠', '더아이오토', '더트래블러', '더팩트',
              '더플라워', '데이즈드앤컨퓨즈드', '데이터넷', '데일리 오에스티', '데일리e스포츠', '데일리게임', '데일리경제', '데일리그리드', '데일리대한민국', '데일리로그',
              '데일리머니', '데일리메디', '데일리메디팜', '데일리스포츠한국', '데일리시사닷컴', '데일리시큐', '데일리안', '데일리저널', '데일리중앙', '데일리카', '데일리컬쳐',
              '데일리투머로우', '데일리팜', '데일리펫', '데일리한국', '데일리환경', '데코저널', '덴탈아리랑', '덴탈투데이', '덴탈포커스', '덴포라인', '도시문제', '동아닷컴',
              '동아비즈니스리뷰', '동아사이언스', '동아환경방송', '드림저널', '디바이스마트 매거진', '디스패치', '디아이투데이', '디지털경제', '디지털데일리', '디지털브러시',
              '디지털타임스', '뚜르드몽드', '라움 오', '라이드매거진', '라이브엔', '라펜트', '라포르시안', '랜드데일리', '러브즈뷰티', '럭스맨', '레미콘·아스콘·골재',
              '로드테스트', '로봇기술', '로이슈', '로피시엘옴므', '루어앤플라이피싱', '리빙센스', '리테일매거진', '마니아리포트', '마리끌레르', '마리나스', '마이더스',
              '마이데일리', '마이웨딩', '마이크로소프트웨어', '마케팅투데이', '맘&앙팡', '매거진아트', '매경게임진', '매경닷컴', '매경이코노미', '매경헬스', '매일경제',
              '매일경제TV', '매일투데이', '맥심 코리아', '머니S', '머니위크MNB', '머니투데이', '머니투데이 더벨', '머슬앤맥스큐', '메가오토', '메디칼미디어', '메디칼업저버',
              '메디칼통신', '메디칼트리뷴', '메디컬리포트', '메디컬투데이', '메디컬헤럴드', '메디팜스투데이', '모빌리스타', '모션컨트롤', '모터그래프', '모터리언', '모터매거진',
              '모터스라인', '모터트렌드', '모토야', '무비스트', '무인화기술', '무카스', '문구스타일', '문화관광저널', '문화예술TV21', '문화웹진 나비', '문화저널21',
              '문화투데이', '문화플러스', '문화플러스서울', '미디어광명', '미디어스', '미디어오늘', '미디어펜', '미디어하남', '미래경제', '미래한국', '미술과비평', '미술세계',
              '미즈코치', '미즈호스트', '민중의소리', '바끄로', '바다낚시&SEA LURE', '바스켓코리아', '바앤다이닝', '바이라인 네트워크', '바이오스펙테이터', '바이커즈랩',
              '바이크매거진', '반도체네트워크', '발리볼코리아닷컴', '방송기술저널', '배관기술', '배드민턴매거진', '백세시대', '법률저널', '베네핏 매거진', '베리타스알파',
              '베스트베이비', '베스트일레븐', '베이커리', '벤처스퀘어', '벤치월드', '벨리시마', '보드나라', '보안24', '보험신보', '복지TV', '복지닷컴', '봉제기술',
              '부천포커스', '북데일리', '불교저널', '뷰티경제', '뷰티누리', '뷰티라이프', '뷰티엠', '뷰티투데이', '뷰티패션', '뷰티한국', '브레인박스', '브레인스톰',
              '브릿지경제', '브이알앤', '블랙벨트코리아', '블로터닷넷', '비마이너', '비전시스템', '비즈니스리포트', '비즈니스워치', '비즈니스포스트', '비즈니스플러스',
              '비즈볼프로젝트', '비즈엔터', '비즈트리뷴', '비즈한국', '비트허브', '사건의 내막', '사건의내막', '사람과산', '사이언스엠디', '사이언스올', '사이클TV', '사진예술',
              '사커뱅크', '사회복지동행', '산업데일리', '상용차매거진', '생활성서', '서예문화', '서울21', '서울경제 골프매거진트', '서울경제TV', '서울대동창회보', '서울매일',
              '서울문화투데이', '서울아트가이드', '서울파이낸스', '서울포스트', '설비기술', '세계거리축제', '세계닷컴', '세계파이낸스', '세라믹 코리아', '세미나투데이',
              '세이프투데이', '소년중앙', '소비라이프', '소비자TV', '소비자연합타임스', '솔라투데이', '수상레저', '수학동아', '숙박매거진', '쉬즈라이프', '쉽빌딩',
              '스마트PC사랑', '스카우트', '스카이데일리', '스쿨iTV', '스크랩워치', '스타에이지', '스타일 에이치', '스타저널', '스타투데이', '스타패션', '스타포커스',
              '스틸데일리', '스틸마켓', '스틸프라이스', '스페셜경제', '스포츠Q', '스포츠경향', '스포츠동아', '스포츠서울', '스포츠온', '스포츠월드', '스포츠조선', '스포츠코리아',
              '스포츠타임스', '스포츠투데이', '스포츠한국', '스포탈코리아', '스포티안', '시니어조선', '시사IN', '시사골프', '시사메디in', '시사오늘', '시사위크', '시사저널',
              '시사저널e', '시사주간', '시사코리아', '시사코리아저널', '시사타임', '시사포커스', '시티라이프', '시흥저널', '식품외식경제', '식품저널', '신동아',
              '신재생에너지저널', '신제품신기술', '실버TV', '쎄씨캠퍼스', '씨네21', '씨넷코리아', '아레나 옴므 플러스', '아레나옴므플러스', '아름다운동행', '아리랑TV',
              '아시아경제', '아시아경제TV', '아시아글로브', '아시아에너지경제', '아시아투데이', '아웃도어', '아웃소싱타임스', '아웃스탠딩', '아이가스저널', '아이데일리',
              '아이티데일리', '아이티비즈', '아주경제', '아츠앤컬쳐', '아쿠아인포', '아트앤디자인', '아트앤씨', '아트앤컬렉터', '아트인컬처', '아트저널', '아트코리아방송',
              '아트프라이스', '안전리뷰', '안전저널', '안전정보', '앙쥬', '애니멀매거진', '애슬릿미디어', '애플경제', '약사공론', '어린이과학동아', '어린이동아', '얼루어 코리아',
              '얼리어답터', '업코리아', '에너지데일리', '에너지설비관리', '에너지코리아', '에듀데일리', '에듀동아', '에듀진', '에브리골프', '에스코트서울', '에스콰이어',
              '에이비 로드', '에코데일리', '에코스케이프', '에코저널', '에코타임스', '엔사이드', '엔지니어링데일리', '엔카매거진', '엔터미디어', '엘리베이터·주차설비', '여성동아',
              '여성조선', '여성중앙', '여수투데이', '여행스케치', '연합인포맥스', '열관리시공', '예술TV Arte', '예술세계', '예천저널', '오디오매거진', '오뜨피플',
              '오토다이어리', '오토데일리', '오토레이싱', '오토모닝', '오토모빌썬', '오토모티브 일렉트로닉스', '오토뷰', '오토사운드', '오토카 코리아', '오토캠핑', '오토헤럴드',
              '오픈모바일', '온케이웨더', '올포칩 미디어', '와이드스포츠', '와이드커버리지', '와인리뷰', '요트피아', '용접저널', '우드플래닛', '우등생과학', '우등생논술',
              '우등생학습', '우먼데일리', '우먼라이프', '우먼센스', '우먼컨슈머', '울진마당', '워터저널', '월간 HRD', '월간 가구가이드', '월간 객석', '월간 건축사',
              '월간 낚시21', '월간 도예', '월간 디자인', '월간 문화재', '월간 미대입시', '월간 미술', '월간 붕어', '월간 비디오플러스', '월간 사진', '월간 산',
              '월간 서예', '월간 수퍼마켓', '월간 안과정보', '월간 암', '월간 앱', '월간 외식경영', '월간 윈도어', '월간 전시가이드', '월간 주얼리앤워치', '월간 주유소',
              '월간 중앙', '월간 중장비', '월간 창호기술', '월간 탁구', '월간 포장', '월간 포토닷', '월간 항공', '월간 헌정', '월간 홈쇼핑', '월간CEO', '월간교육',
              '월간에세이', '월간유아', '월간인물', '월간인테리어', '월간전기', '월간조선', '월간커피', '월드얀', '웨딩21', '웰니스투데이', '웰스매니지먼트', '웹브릿지',
              '위기관리경영', '위드레저', '위즈키즈', '위클리서울', '위클리오늘', '위키트리', '유니타스브랜드', '유스라인', '유체제어', '유통데일리', '음식과사람', '음악저널',
              '음악춘추', '의료기기협회보', '의료정보', '이데일리', '이데일리TV', '이버즈', '이슈데일리', '이지경제', '이코노미 인사이트', '이코노미21', '이코노미TV',
              '이코노미스트', '이코노미조선', '이코노믹리뷰', '이코노믹포스트', '이투데이', '익스테리어', '인권하루소식', '인베스트조선', '인사관리', '인사이드저널', '인사이드코리아',
              '인성시대', '인쇄문화', '인스정보기술', '인스타일', '인재경영', '인터넷토마토', '인터풋볼', '일간보사', '일간부동산', '일간스포츠', '일간조선해양', '일간투데이',
              '일간환경', '일렉트릭파워', '일요경제', '일요서울', '일요시사', '자동인식·보안', '자동제어계측', '자동차생활', '자동차와주유소', '자동차제조기술', '자전거생활',
              '작은것이아름답다', '장애인문화방송', '전기기술', '전기설비', '전기저널', '전기평론', '전력경제', '전북포스트', '전원생활', '전원속의 내집', '전원주택라이프',
              '전자과학', '전자기술', '전자부품', '전주교차로', '점프볼', '정읍투데이', '제주저널', '조명과인테리어', '조선닷컴', '조선닷컴 더스타', '조선비즈', '조선에듀',
              '조인스닷컴', '조인스랜드부동산', '좋은교육미디어', '주간 프랜차이즈', '주간경향', '주간동아', '주간무역', '주간조선', '주간코스메틱', '주간한국', '주간현대',
              '주단조와열처리', '주류저널', '주택저널', '중기이코노미', '중부매일', '중앙선데이', '증권플러스', '지디넷 코리아', '참여와혁신', '참좋은환경', '창과문',
              '창업&프랜차이즈', '채널A', '채널프랜차이즈', '철구기술', '첨단환경기술', '청년의사', '초이스경제', '축구저널', '출판문화', '출판저널', '춤과사람들', '춤판춤북',
              '충남투데이', '충청매일', '충청투데이', '치프 이그제큐티브', '카고프레스', '카리포트', '카매거진', '카모드', '카미디어', '카스카미디어', '카앤모델', '카앤스포츠',
              '카오디오', '카조선', '카테크', '카포스', '카포탈넷', '카홀릭', '캐드앤그래픽스', '캠퍼스 잡앤조이', '컨슈머리서치', '컨슈머와이드', '컨슈머치', '컨슈머타임스',
              '컬처오션', '컬처윈도우', '케이벤치', '켐로커스', '코리아닷컴', '코리아데일리', '코리아본드웹', '코리아중앙데일리', '코리아타임스', '코리아트래블', '코리아헤럴드',
              '코메디닷컴', '코스모캠퍼스', '코스모폴리탄', '코어플라넷', '쿠켄', '크레이닷티비', '크리스천투데이', '탑골프', '탑라이더', '테니스코리아', '테니스피플', '테크엠',
              '테크홀릭', '텐아시아', '토마토TV', '토요경제', '토이매거진', '투데이안', '투데이에너지', '투데이코리아', '투어코리아', '트래블데일리', '트래블레저플러스',
              '트래블맵', '트래블아이', '트래블조선', '트랙사이드', '트레블 라이프', '트루스토리', '티매거진', '티몬매거진', '티브이데일리', '파운드매거진', '파워코리아',
              '파워코리아데일리', '파이낸셜투데이', '파이낸스투데이', '파퓰러사이언스', '팍스넷데일리', '팜스탁', '패션리뷰', '패션비즈', '패션서울', '패션웹진 스냅', '패션인사이트',
              '패션저널', '패션채널', '팩트TV', '퍼포먼스텐', '펌프기술', '펫저널', '포모스', '포브스코리아', '포장기계', '포춘코리아', '포커스경제', '포포투', '폴리진',
              '표면실장기술', '표면처리저널', '푸드TV', '푸드트래블', '품질경영', '풋볼리스트', '퓨쳐에코', '프라임경제', '프런티어타임스', '프레시안', '프레지던트', '프로슈머',
              '프리빌리지', '프린팅코리아', '플라스틱사이언스', '플라스틱월드', '플라스틱코리아', '플래텀', '플랜트기술', '하우징헤럴드', '하이닥', '하이맘', '하퍼스 바자',
              '한겨레21', '한경닷컴', '한경닷컴 게임톡', '한경닷컴 스타엔', '한경비즈니스', '한국경제', '한국경제TV', '한국수산경제', '한국스포츠경제', '한국아이닷컴',
              '한국여행업협회', '한국연극', '한국의약통신', '한국종합기술', '한옥문화', '함께걸음', '함께사는길', '항공문화', '해양과조선', '해양한국', '해저여행', '해피CGI',
              '핸드볼코리아', '행복이가득한집', '허핑턴포스트코리아', '헝그리앱', '헤드라이너', '헤럴드POP', '헤럴드경제', '헤렌', '헬스경향', '헬스앤라이프', '헬스조선',
              '현대경영', '현대해양', '호텔&레스토랑', '화이트페이퍼', '화학장치기술', '환경과조경', '환경기술인', '환경데일리', '환경미디어', '환경방송', '환경정보',
              '환경포커스', '효도실버', '후생신보', '히트펌프·공조', '모바일 경향']

media_suffix = [
    "신문", "뉴스", "일보", "타임즈", "타임스"
]

split_words = [
    f"{prefix}{word}" for word in
    ["▶", "▷", "▶", "▷", "▸", "▹", "►", "▻", "◂", "◃", "◄", "◅",
     "■", "□", "▣", "▤", "▥", "▦", "▧", "▨", "▩", "▪", "▫", "☐",
     "◆", "◇", "◈", "◉", "◊", "◐", "◑", "◒", "◓",
     "©", "ⓒ", "☛", "☞", "☚", "☜", "☎", "☏",
     "Copyright", "저작권자", "무단전재", "무단 전재", "(끝)",
     "기사제보", "보도자료", "제보하기", "기사문의", "많이 본 기사", "취재본부",
     "촬영기자", "영상편집", "카카오톡:", "카카오톡 :", "전화:", "전화 :"] + media_list
    for prefix in ["<", "[", "(", ""]
]

split_patterns = [
    re.compile(
        r"(?i)(\b(지금까지|.{2,7}에서)\b)\W+(?:\w+[^\w]+){0,6}?\b(기자|특파원|교통정보|KBS 뉴스|SBS 뉴스|MBC 뉴스|YTN|MBN|뉴스더하기)"
    ),
    re.compile(
        r"(?i)(\b(KBS 뉴스|SBS 뉴스|MBC 뉴스|YTN|MBN|뉴스더하기)\b)\W+(?:\w+){0,3}?(였습니다\.|입니다\.).*"
    ),
    re.compile("|".join([re.escape(p) for p in split_words])),
    re.compile("기자 | 기자| 특파원|특파원 |@"),
]

remove_patterns = {
    re.compile(r'\([^)]*(=| 기자| 특파원|뉴스|뉴스1|신문|일보|타임즈|타임스)[^)]*\)'): "",
    re.compile(r"\s*[\w가-힣·=]*\s*(기자=|기자 =|특파원=|특파원 =)"): "",
    re.compile(r"\s*[\w가-힣·=]*\s*기자|특파원"): "",
    re.compile("(기자 =|특파원 =|기자=|특파원=)|AP=연합뉴스|=연합뉴스|"): "",
    re.compile("=뉴스1"): "",
    re.compile(r"【.*?】|\[.*?]"): "",
    re.compile(r"[a-zA-Z0-9]+@"): "",
}

email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
do_not_split_pattern = re.compile("기자[가-힣]")


def _split_spam(sents, found_media):
    sents_for_use = []
    for sent in sents:
        drop_sent = False
        for check_word, found_word in found_media.items():
            if sent.endswith(found_word):
                drop_sent = True
                break
            elif f"{check_word} " in sent or f"{check_word}\n" in sent:
                drop_sent = True
                break

        if not drop_sent:
            for pattern in split_patterns:
                if pattern.search(sent):
                    do_not_split = False
                    if do_not_split_pattern.search(sent):
                        do_not_split = True

                    if not do_not_split:
                        drop_sent = True
                        break

        if drop_sent:
            continue
        else:
            sents_for_use.append(sent)

    return sents_for_use


def _replace_spam(sents):
    sents_for_use = []
    for sent in sents:
        do_not_split = False
        if do_not_split_pattern.search(sent):
            do_not_split = True

        if not do_not_split:
            for pattern, repl in remove_patterns.items():
                sent = pattern.sub(repl, sent)
        sents_for_use.append(sent)
    return sents_for_use


def _should_skip(text):
    for bad in skip_words:
        if bad in text:
            return True
    return False


def _normalize_text(text, postprocess):
    if not postprocess:
        for before, after in normalization_open.items():
            while before in text:
                text = text.replace(before, after)
        for before, after in normalization_close.items():
            while before in text:
                text = text.replace(before, after)

    for before, after in normalization_others.items():
        while before in text:
            text = text.replace(before, after)
    return text


def _find_media(text):
    words = text.split()
    media_found = {}

    for word in words:
        for media in media_suffix:
            if media in word:
                if media not in media_found:
                    media_found[media] = [word]
                else:
                    media_found[media].append(word)

    return {
        media: f"{prefix}{word}"
        for media, word in media_found.items()
        for prefix in ["<", "[", "(", "< ", "[ ", "( ", ""]
    }


def _split_sentences(text):
    sents = []
    for sent in re.split(r"(?<=[.!?]\s)", text):
        for s in re.split(r"(?<=[다요죠][.!?])(?![\"'\])>])", sent):
            if len(s.strip()) > 0:
                sents.append(s)
    return sents


def _pre_split(text):
    text = text.split("☞")[0]
    text = email_pattern.split(text)[0]
    return text


def clean_news(
    text: Union[str, List[str], Tuple[str]],
    min_sentences: int = 3,
    header_ratio: float = 0.4,
    footer_ratio: float = 0.4,
    num_workers: Union[int, str] = "auto",
    verbose: bool = False,
) -> Union[str, List[str]]:
    """
    This cleans news articles by removing useless headers and footers.

    Args:
        text (Union[str, List[str], Tuple[str]]): Input text or list of texts.
        min_sentences (int): Minimum number of sentences to keep. Defaults to 3.
        header_ratio (float): Ratio of the number of sentences to check in the header. Defaults to 0.4.
        footer_ratio (float): Ratio of the number of sentences to check in the footer. Defaults to 0.4.
        num_workers (Union[int, str]): the number of multiprocessing workers
        verbose (bool): whether to print verbose outputs or not

    Returns:
        Union[str, List[str]]: Cleaned text or list of cleaned texts.

    Examples:
        >>> from kss import Kss
        >>> clean_news = Kss("clean_news")
        >>> text = "[사진]에버랜드, 봄꽃 펼쳐진 '튤립축제' 오픈\\n\\n[ 뉴스1 제공](서울=뉴스1) 이동원 기자 = 에버랜드가 오는 22일부터 봄을 상징하는 튤립 120만 송이와 함께 '튤립축제'를 오픈해 본격적인 봄의 시작을 알린다. 지난 1992년 국내 첫 튤립 축제를 연 이후 올해로 22회째를 맞이한 에버랜드 '튤립축제'는 지난해 첫 선을 보이며 좋은 반응을 얻었던 오감(五感)체험 '시크릿가든'을 리뉴얼하고, 신규 테마 꽃길을 조성하는 등 봄꽃을 활용한 다양한 볼거리를 강화한 것이 특징이다. 또한 4월 28일까지 열리는 '튤립축제'에서는 야간 개장과 함께 손님 참여요소가 늘어난 인기 공연, 퍼레이드가 재오픈하는 등 봄을 맞아 나들이 나온 상춘객들의 눈과 귀를 즐겁게 할 예정이다. (에버랜드 제공)2013.3.10/뉴스1 < 저작권자 뉴스1 코리아, 무단전재 및 재배포 금지 > ☞ 뉴스1 바로가기 [스타뉴스 공식 글로벌 버전 애플리케이션] [증권알리미]국내외 증시핫이슈 및 오늘의 승부주! [머니원]北 리스크로 조정, 매수 기회로 [머니투데이 핫뉴스] ☞ 신입사원 재테크, 5년 안에 '1억 만들기' ☞ '박시후·박준' 고소女, 둘다 '여기'가더니 ☞ 늙으면 '돈이라도' 있어야 하는 진짜 이유 ☞ 손연재 가방 시끌…'신입생은 명품 안돼?' ☞ '바람난 부인 뒷조사' 300만원 줬더니… [book]10년의 선택, 중국에 투자하라 [핫이슈]'멘사' 천재들 뭉쳐 15년 투자했는데... '맙소사' 뉴스1 제공 < 저작권자 ⓒ '돈이 보이는 리얼타임 뉴스' 머니투데이, 무단전재 및 재배포 금지"
        >>> output = clean_news(text)
        >>> print(output)
        '에버랜드, 봄꽃 펼쳐진 '튤립축제' 오픈\\n\\n에버랜드가 오는 22일부터 봄을 상징하는 튤립 120만 송이와 함께 '튤립축제'를 오픈해 본격적인 봄의 시작을 알린다. 지난 1992년 국내 첫 튤립 축제를 연 이후 올해로 22회째를 맞이한 에버랜드 '튤립축제'는 지난해 첫 선을 보이며 좋은 반응을 얻었던 오감(五感)체험 '시크릿가든'을 리뉴얼하고, 신규 테마 꽃길을 조성하는 등 봄꽃을 활용한 다양한 볼거리를 강화한 것이 특징이다. 또한 4월 28일까지 열리는 '튤립축제'에서는 야간 개장과 함께 손님 참여요소가 늘어난 인기 공연, 퍼레이드가 재오픈하는 등 봄을 맞아 나들이 나온 상춘객들의 눈과 귀를 즐겁게 할 예정이다.'
    """
    text, finish = _check_text(text)

    if finish:
        return text

    min_sentences = _check_type(min_sentences, "min_sentences", int)
    header_ratio = _check_type(header_ratio, "header_ratio", float)
    footer_ratio = _check_type(footer_ratio, "footer_ratio", float)
    assert 0 <= header_ratio <= 1, "header_ratio should be in [0, 1]"
    assert 0 <= footer_ratio <= 1, "footer_ratio should be in [0, 1]"
    assert header_ratio + footer_ratio < 1, "header_ratio + footer_ratio should be less than 1"
    verbose = _check_type(verbose, "verbose", bool)
    num_workers = _check_num_workers(text, num_workers)

    if num_workers is not False and verbose:
        verbose = False
        logger.warn(
            "Verbose mode is not supported for multiprocessing. "
            "It will be turned off automatically."
        )

    return _run_job(
        func=partial(
            _clean_news,
            min_sentences=min_sentences,
            header_ratio=header_ratio,
            footer_ratio=footer_ratio,
            verbose=verbose,
        ),
        inputs=text,
        num_workers=num_workers,
    )


def _clean_news(
    text: str,
    min_sentences: int = 3,
    header_ratio: float = 0.4,
    footer_ratio: float = 0.4,
    verbose: bool = False,
):
    input_text = text
    skip_sample = False
    # for debug.

    if _should_skip(text):
        skip_sample = True

    if not skip_sample:
        text = _normalize_text(text, postprocess=False)
        text = _pre_split(text)
        sents = _split_sentences(text)

        if len(sents) <= min_sentences:
            skip_sample = True
        else:
            found_media = _find_media(text)

            if len(sents) <= min_sentences * 2:
                sents = _replace_spam(sents)
                sents = _split_spam(sents, found_media)

                if len([s for s in sents if len(s.strip()) > 0]) == 0:
                    skip_sample = True
                else:
                    text = " ".join(sents)
                    text = _normalize_text(text, postprocess=True).strip()

            else:
                num_header_sent = int(len(sents) * header_ratio)
                num_footer_sent = int(len(sents) * footer_ratio)

                header_sents = sents[:num_header_sent]
                middle_sents = sents[num_header_sent:-num_footer_sent]
                footer_sents = sents[-num_footer_sent:]

                header_sents = _replace_spam(header_sents)
                footer_sents = _split_spam(footer_sents, found_media)
                text = " ".join(header_sents + middle_sents + footer_sents)
                text = _normalize_text(text, postprocess=True).strip()

    if len(text.strip()) == 0:
        skip_sample = True

    if skip_sample:
        output_text = None
    else:
        output_text = text

    if verbose:
        print(highlight_diffs(input_text, output_text).replace("\n", "\\n"))

    return output_text

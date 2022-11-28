# Kss: A Toolkit for Korean sentence segmentation
<a href="https://github.com/hyunwoongko/kss/releases"><img alt="GitHub release" src="https://img.shields.io/github/release/hyunwoongko/kss.svg" /></a> 
<a href="https://github.com/hyunwoongko/kss/issues"><img alt="Issues" src="https://img.shields.io/github/issues/hyunwoongko/kss"/></a>

This repository contains the source code of Kss, a representative Korean sentence segmentation toolkit. I also conduct ongoing research about Korean sentence segmentation algorithms and report the results to this repository.
If you have a good idea about Korean sentence segmentation, please feel free to talk through the [issue](https://github.com/hyunwoongko/kss/issues).

<br>

### What's New:
- May 5, 2022 [Released Kss Fluter](https://github.com/khjde1207/kss_dart).
- August 25, 2021 [Released Kss Java](https://github.com/sangdee/kss-java).
- August 18, 2021 [Released Kss 3.0 Python](https://github.com/hyunwoongko/kss/releases/tag/3.0.1).
- December 21, 2020 [Released Kss 2.0 Python](https://github.com/hyunwoongko/kss/releases/tag/3.0.1).
- August 16, 2019 [Released Kss 1.0 C++](https://github.com/hyunwoongko/kss/releases/tag/3.0.1).

## 1. Installation
### 1.1. Install from pip
Kss can be easily installed using the pip package manager.
```console
pip install kss
```

### 1.2. Install from source code
You can also install Kss from source code.
This can be useful for adding words to user dictionary described in [here](https://github.com/hyunwoongko/kss/blob/main/docs/USERDICT.md).
```console
git clone https://github.com/hyunwoongko/kss
cd kss
pip install -e .
```


## 2. Usage
### 2.1. `split_sentences`
Kss is the sentence segmentation toolkit based on morpheme-aware heuristic algorithms. And `split_sentences` is a key function of this toolkit. 
You can segment input texts to the sentences using this function. Click the triangle button (►) for more detailed information and example code snippets of each paramter.

```python
>>> from kss import split_sentences

>>> split_sentences(
...     text: Union[str, Tuple[str], List[str]],  
...     use_heuristic: bool = True,
...     use_quotes_brackets_processing: bool = False,                             
...     max_recover_step: int = 5,
...     max_recover_length: int = 20000,
...     backend: str = "auto",
...     num_workers: Union[str, int] = "auto",                       
...     disable_gc: Union[str, bool] = "auto",                           
... )
```

<details>
<summary>text (<code>Union[str, tuple, List[str]]</code>) </summary>
<br>

This parameter indicates input texts. You can also input list or tuple for batch processing not only string.

- An example of single text segmentation

  ```python
  >>> from kss import split_sentences

  >>> text = "강남역 맛집으로 소문난 강남 토끼정에 다녀왔습니다 회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요 다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다"
  >>> split_sentences(text)
  ['강남역 맛집으로 소문난 강남 토끼정에 다녀왔습니다', '회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요', '다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다']
  ```

- An example of multiple texts batch segmentation

  ```python
  >>> from kss import split_sentences

  >>> text1 = "오늘 여러분과 함께 리뷰해 볼 영화는 바로 디즈니 픽사의 영화 '업'입니다 저는 이 영화를 고등학교 영어시간에 처음 보게되었는데요, 수능날을 맞이해서 고등학교 추억이 담긴 영화를 오늘 여러분께 소개해드리려고 해요~ㅎㅎㅎ 한방울 눈물과 한바탕 웃음 마음 속에 담고 싶은 단 하나의 걸작 평생 모험을 꿈꿔 왔던 ‘칼’ 할아버지는 수천 개의 풍선을 매달아 집을 통째로 남아메리카로 날려 버리는데, ‘칼’ 할아버지의 이 위대한 모험에 초대 받지 않은 불청객이 있었으니, 바로 황야의 탐험가 ‘러셀’ 지구상에 둘도 없을 이 어색한 커플이 함께 하는 대모험 그들은 과연 남미의 잃어버린 세계에서 사라져 버린 꿈과 희망, 행복을 다시 찾을 수 있을까? 여러분은 디즈니 영화를 좋아하시 나요? 저는 디즈니보다는 픽사를 훨씬 더 좋아하는 편인데요 디즈니와 픽사가 합병한 뒤, 저는 디즈니 픽사 영화가 인생영화 중 대부분을 차지할 정도로 정말 즐겨보고 있어요"
  >>> text2 = "동영상 촬영이 금지되어있어 노홍철 씨의 열정 넘치는 강연을 그대로 보여 드리지 못하는 점 너무 아쉽네요 ㅠㅠ 간단한 행사스케치로나마 참고해주세요~ 노홍철의 열정 Talk 행사는 개그맨 김범용 씨가 맡아주셨고 오프닝 무대는 위대한 탄생3 탑3로 이름을 날린 오병길 씨의 노래로 뜨겁게 달궈졌습니다^^ 이날 초대된 로열블루와 블루 멤버십 고객분들의 환호로 삼성홍보관 딜라이트 안이 가득 차더군요! (오병길 씨의 노래 잘하는 비법은 무엇일까요? 꾸준한 모창연습이라고… ㅋ) 곧이어 이 날 행사의 메인이었던 노홍철씨의 열정 Talk가 본격적으로 시작되었습니다"
  >>> split_sentences([text1, text2])
  [["오늘 여러분과 함께 리뷰해 볼 영화는 바로 디즈니 픽사의 영화 '업'입니다", '저는 이 영화를 고등학교 영어시간에 처음 보게되었는데요,', '수능날을 맞이해서 고등학교 추억이 담긴 영화를 오늘 여러분께 소개해드리려고 해요~ㅎㅎㅎ', '한방울 눈물과 한바탕 웃음 마음 속에 담고 싶은 단 하나의 걸작 평생 모험을 꿈꿔 왔던 ‘칼’ 할아버지는 수천 개의 풍선을 매달아 집을 통째로 남아메리카로 날려 버리는데, ‘칼’ 할아버지의 이 위대한 모험에 초대 받지 않은 불청객이 있었으니, 바로 황야의 탐험가 ‘러셀’ 지구상에 둘도 없을 이 어색한 커플이 함께 하는 대모험 그들은 과연 남미의 잃어버린 세계에서 사라져 버린 꿈과 희망, 행복을 다시 찾을 수 있을까?', '여러분은 디즈니 영화를 좋아하시 나요?', '저는 디즈니보다는 픽사를 훨씬 더 좋아하는 편인데요', '디즈니와 픽사가 합병한 뒤, 저는 디즈니 픽사 영화가 인생영화 중 대부분을 차지할 정도로 정말 즐겨보고 있어요'],
  ['동영상 촬영이 금지되어있어 노홍철 씨의 열정 넘치는 강연을 그대로 보여 드리지 못하는 점 너무 아쉽네요 ㅠㅠ', '간단한 행사스케치로나마 참고해주세요~', '노홍철의 열정 Talk 행사는 개그맨 김범용 씨가 맡아주셨고 오프닝 무대는 위대한 탄생3 탑3로 이름을 날린 오병길 씨의 노래로 뜨겁게 달궈졌습니다^^', '이날 초대된 로열블루와 블루 멤버십 고객분들의 환호로 삼성홍보관 딜라이트 안이 가득 차더군요!', '(오병길 씨의 노래 잘하는 비법은 무엇일까요? 꾸준한 모창연습이라고… ㅋ) 곧이어 이 날 행사의 메인이었던 노홍철씨의 열정 Talk가 본격적으로 시작되었습니다']]
  ```

<br>
</details>

<details>
<summary>use_heuristic (<code>bool</code>)</summary>
<br>

Kss is an open-ended sentence segmentation toolkit, that can segment everywhere in the input texts even if there are no punctuation marks. But, if you want to conduct punctuation-only segmentation, the setting to segment depending only on punctuation, you can modify segmentation setting using this parameter.

This parameter indicates whether to use the heuristic algorithm for the open-ended sentence segmentation. 
If you set it `True`, Kss conduct open-ended segmentation. 
If you set it `False`, Kss conduct punctuation-only segmentation.
I recommend to you set it `False` if input texts follow the punctuation rules relatively well, because Kss can make mistakes sometimes in the parts without punctuation mark.


- Formal articles (wiki, news, essays): recommend to `False`
- Informal articles (sns, blogs, messages): recommend to `True`

<br>

As shown in the [performance analysis](https://github.com/hyunwoongko/kss/blob/main/docs/ANALYSIS.md#1-segmentation-error-rate), if this option is set to `False`, the segmentation error rate will be downed.
However, it does mean Kss will be less sensitive. If your input texts have relatively few punctuation marks, such as messages or blog articles, 
Kss can't split most of the sentences.
Therefore, it must be adjusted according to the type of the input texts.

- An example of `use_heuristic`

  ```python
  >>> from kss import split_sentences
    
  >>> text = "원어민도 흔하게 틀리는 문법오류는 아포스트로피(apostrophe)를 잘못된 사용하는거예요 질문: 아포스트로피(apostrophe)를 왜 쓰나요? 대답: 두 가지 목적으로 사용해요 예를 들어서 do not = don't not의 o를 생략한걸 apostrophe가 보여주는거예요 또 다른 예를 들면 we are = we're are의 a를 생략했죠 생략된 표현에 아포스트로피를 자주 사용해요. 이제 아시겠죠?"
  >>> split_sentences(text, use_heuristic=True)  # can segment without punctuations
  ['원어민도 흔하게 틀리는 문법오류는 아포스트로피(apostrophe)를 잘못된 사용하는거예요', '질문: 아포스트로피(apostrophe)를 왜 쓰나요?', '대답: 두 가지 목적으로 사용해요', "예를 들어서 do not = don't not의 o를 생략한걸 apostrophe가 보여주는거예요", "또 다른 예를 들면 we are = we're are의 a를 생략했죠", '생략된 표현에 아포스트로피를 자주 사용해요.', '이제 아시겠죠?']

  >>> split_sentences(text, use_morpheme=False)  # can't segment without punctuations
  ['원어민도 흔하게 틀리는 문법오류는 아포스트로피(apostrophe)를 잘못된 사용하는거예요 질문: 아포스트로피(apostrophe)를 왜 쓰나요?', "대답: 두 가지 목적으로 사용해요 예를 들어서 do not = don't not의 o를 생략한걸 apostrophe가 보여주는거예요 또 다른 예를 들면 we are = we're are의 a를 생략했죠 생략된 표현에 아포스트로피를 자주 사용해요.", '이제 아시겠죠?']
  ```

<br>
</details>

<details>
<summary>use_quotes_brackets_processing (<code>bool</code>)</summary>
<br>

Kss has the feature that prevents to segment the parts enclosed in brackets (괄호) and quotation marks (따옴표). 
This parameter indicates whether to segment the parts enclosed in brackets or quotations marks. 
If you set it `True`, Kss does not segment these parts, If you set it `False`, Kss segments the even in the parts that are enclosed in brackets and quotations marks. default is `False`. (I set it to `False` because it's too slow. Set to `True` if you need this feature.)

- An example of `use_quotes_brackets_processing`

  ```python
  >>> from kss import split_sentences
    
  >>> text = '"나는 이제 더는 못 먹겠다. 너무 배불러." 그리고 곧장 자리를 떴다. 아마도 화장실에 간 모양이다.'
  >>> split_sentences(text, use_quotes_brackets_processing=True)
  ['"나는 이제 더는 못 먹겠다. 너무 배불러." 그리고 곧장 자리를 떴다.', '아마도 화장실에 간 모양이다.']

  >>> split_sentences(text, use_quotes_brackets_processing=False)
  ['"나는 이제 더는 못 먹겠다.', '너무 배불러.', '" 그리고 곧장 자리를 떴다.', '아마도 화장실에 간 모양이다.']
  ```

<br>
</details>

<details>
<summary>max_recover_step & max_recover_length (<code>int</code>)</summary>
<br>

Kss 2.0 or later can segment sentences even if the pair of brackets and quotation marks do not match. This was a chronic problem in previous Kss C++ (1.0) ([#4](https://github.com/likejazz/korean-sentence-splitter/issues/4), [#8](https://github.com/likejazz/korean-sentence-splitter/issues/8)). 
But it was fixed in 2.0 by calibration feature about quotation marks and brackets mismatch. However, this feature uses the recursive algorithm that has poor time complexity of O(2^n), so it can be very slow in some cases.
Therefore, Kss provides the parameters to adjust the recursive algorithm.

- `max_recover_step` determines the depth of recursion. Kss never go deeper than this when resolving quotes and brackets mismatch.
- `max_recover_length` determines the length of a sentence to which calibration is applied. Kss does not calibrate sentences longer than this value. Because calibrating long sentences takes a very long time.
<br>
  
P.S. From kss 3.0.2, [memoization with LRU cache](https://github.com/hyunwoongko/kss/blob/b4b2b21846b39d8e01da71d761b4033a030505f1/kss/kss.py#L233) was introduced. This can improve performance by saving duplicated segmentation results.


- An example of `max_recover_step` 

  ```python
  >>> from kss import split_sentences
    
  >>> text = 'YOUR_VERY_LONG_TEXT'
  >>> split_sentences(text, max_recover_step=5)
  ```

- An example of `max_recover_length` 
  ```python
  >>> from kss import split_sentences
    
  >>> text = 'YOUR_VERY_LONG_TEXT'
  >>> split_sentences(text, max_recover_length=20000)
  ```

<br>
</details>

<details>
<summary>backend (<code>str</code>)</summary>
<br>

Kss 3.0 or later supports morpheme analysis. This parameter indicates which morpheme analyzer will be used during segmentation. 
If you set it `pynori` or `mecab`, sentence segmentation is possible even at the unspecified [eomi (어미)](https://ko.wikipedia.org/wiki/%EC%96%B4%EB%AF%B8). 
In this case, Kss can segment sentences that use honorifics (경어), dialects (방언), neologisms (신조어) and [eomi transferred from noun (명사형 전성어미)](https://ko.wiktionary.org/wiki/%EC%A0%84%EC%84%B1%EC%96%B4%EB%AF%B8), and can grasped well the parts that are difficult to grasp without morpheme information. 

The followings are summary of the three possible options.

- `auto`: Use mecab backend if mecab can be used else use pynori backend
- `pynori`: Use Pynori analyzer. It works fine even without C++ installed, but is very slow.
- `mecab`: Use Mecab analyzer. It only works in the environment that C++ is installed. However, it is much faster than Pynori.
- `none`: Do not use morpheme analyzer. performance will be decrease.

<br>

Kss use the [Pynori](https://github.com/gritmind/python-nori), the pure python morpheme analyzer by default. However, you can change it to [Mecab-Ko](https://github.com/jonghwanhyeon/python-mecab-ko), the super-fast morpheme analyzer based on C++.
[The performance](https://github.com/hyunwoongko/kss/blob/main/docs/ANALYSIS.md#11-open-ended-segmentation) of two analyzers is almost similar because they were developed based on the same dictionary, [mecab-ko-dic](https://bitbucket.org/eunjeon/mecab-ko-dic). 
However, since there is a lot of difference in speed, we strongly recommend using mecab backend if you can install mecab-ko in your environment.

From kss 3.5.4, `mecab` backend uses `python-mecab-kor` instead of `python-mecab-ko`. 
and `auto` backend added, this backend will select best backend according to your environment

- An example of `backend`

  ```python
  >>> from kss import split_sentences
    
  >>> text = "부디 만수무강 하옵소서 천천히 가세용~ 너 밥을 먹는구나 응 맞아 난 근데 어제 이사했음 그랬구나 이제 마지막임 응응"

   >>> split_sentences(text, backend="auto")
  ['부디 만수무강 하옵소서', '천천히 가세용~', '너 밥을 먹는구나', '응 맞아 난 근데 어제 이사했음', '그랬구나 이제 마지막임', '응응']

  >>> split_sentences(text, backend="pynori")
  ['부디 만수무강 하옵소서', '천천히 가세용~', '너 밥을 먹는구나', '응 맞아 난 근데 어제 이사했음', '그랬구나 이제 마지막임', '응응']

  >>> split_sentences(text, backend="mecab")
  ['부디 만수무강 하옵소서', '천천히 가세용~', '너 밥을 먹는구나', '응 맞아 난 근데 어제 이사했음', '그랬구나 이제 마지막임', '응응']

  >>> split_sentences(text, backend="none")
  ['부디 만수무강 하옵소서 천천히 가세용~', '너 밥을 먹는구나 응 맞아 난 근데 어제 이사했음 그랬구나 이제 마지막임 응응'
  ```

- How to install mecab?  
  ```
  pip install -v python-mecab-kor
  ```

<br>
</details>    

<details>
<summary>num_workers (<code>int</code>)</summary>
<br>

Kss 3.0 or later supports multiprocessing. Therefore, multiple sentences can be segmented at the same time. This parameter indicates the number of workers to use for multiprocessing. If you set this value as 1 or 0, multiprocessing is disabled. If you input -1, Kss uses the maximum workers as many as possible. 
If a different value is entered, the number you entered of workers is allocated.

As shown in the performance evaluation, multiprocessing can lead a very large effect on speed. 
Multiprocessing makes segmentation much faster, especially when using the Pynori backend.

From kss 3.5.4, `auto` is added. this can select the best number of workers for your environment.

- An example of `num_workers`

  ```python
  >>> from kss import split_sentences

  >>> split_sentences(some_text, num_workers="auto")  # kss will select best option for you
  >>> split_sentences(some_text, num_workers=0)  # disable multiprocessing
  >>> split_sentences(some_text, num_workers=1)  # disable multiprocessing
  >>> split_sentences(some_text, num_workers=-1)  # use maximum workers as many as possible
  >>> split_sentences(some_text, num_workers=4)  # use 4 workers
  ```

<br>
</details>

<details>
<summary>disable_gc (<code>bool</code>)</summary>
<br>

This parameter indicates whether to enable the garbage collection during the sentence segmentation. 
The Pynori analyzer is implemented based on the data structure called [Trie](https://en.wikipedia.org/wiki/Trie). 
However, since this uses recursive algorithm, it often wastes a lot of memory, which leads to frequent garbage collection. 
If you set it to `True`, segmentation speed can be improved by disabling garbage collection. 
Of course, when the segmentation process ends, garbage collection will be reactivated.

From kss 3.7.0, `auto` was introduced as a default value. if you set this as `auto`, kss will select best option for you.

- An example of `disable_gc`

  ```python
  >>> from kss import split_sentences

  >>> split_sentences(some_text, disable_gc="auto")  # kss will select best option for you
  >>> split_sentences(some_text, disable_gc=True)  # disable garbage collection
  >>> split_sentences(some_text, disable_gc=False)  # enable garbage collection
  ```

<br>
</details>

### 2.2. `split_chunks`

`split_chunks` is used when you want to segment input texts into paragraphs rather than sentences. 
This function conducts the following two processes:

1) Split sentences using `split_sentences`.
2) Construct a paragraph by concatenating the segmented sentences to the maximum length entered by the user.

Note that this function segments input texts into paragraphs based only on the length, not the contents. 
And it also supports to chunk window level through the `overlap` option.
Click the triangle button (►) for more detailed information and example code snippets of each paramter.

```python
>>> from kss import split_chunks

>>> split_chunks(
...     text: Union[str, List[str], tuple],
...     max_length: int,
...     overlap: bool = False,
...     **kwargs,
... )
```

<details>
<summary>text (<code>Union[str, tuple, List[str]]</code>)</summary>
<br>

This parameter indicates input texts. You can also input list or tuple for batch processing not only string.

- An example of single text segmentation

```python
>>> from kss import split_chunks

>>> text = """강남역 맛집으로 소문난 강남 토끼정에 다녀왔습니다. 회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요 다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다 강남역 맛집 토끼정의 외부 모습. 강남 토끼정은 4층 건물 독채로 이루어져 있습니다.', '역시 토끼정 본 점 답죠?ㅎㅅㅎ 건물은 크지만 간판이 없기 때문에 지나칠 수 있으니 조심하세요 강남 토끼정의 내부 인테리어. 평일 저녁이었지만 강남역 맛집 답게 사람들이 많았어요. 전체적으로 편안하고 아늑한 공간으로 꾸며져 있었습니다ㅎㅎ 한 가지 아쉬웠던 건 조명이 너무 어두워 눈이 침침했던… 저희는 3층에 자리를 잡고 음식을 주문했습니다.', '총 5명이서 먹고 싶은 음식 하나씩 골라 다양하게 주문했어요 첫 번째 준비된 메뉴는 토끼정 고로케와 깻잎 불고기 사라다를 듬뿍 올려 먹는 맛있는 밥입니다. 여러가지 메뉴를 한 번에 시키면 준비되는 메뉴부터 가져다 주더라구요. 토끼정 고로케 금방 튀겨져 나와 겉은 바삭하고 속은 촉촉해 맛있었어요!', '깻잎 불고기 사라다는 불고기, 양배추, 버섯을 볶아 깻잎을 듬뿍 올리고 우엉 튀김을 곁들여 밥이랑 함께 먹는 메뉴입니다. 사실 전 고기를 안 먹어서 무슨 맛인지 모르겠지만.. 다들 엄청 잘 드셨습니다ㅋㅋ 이건 제가 시킨 촉촉한 고로케와 크림스튜우동. 강남 토끼정에서 먹은 음식 중에 이게 제일 맛있었어요!!! 크림소스를 원래 좋아하기도 하지만, 느끼하지 않게 부드럽고 달달한 스튜와 쫄깃한 우동면이 너무 잘 어울려 계속 손이 가더라구요.', '사진을 보니 또 먹고 싶습니다 간사이 풍 연어 지라시입니다. 일본 간사이 지방에서 많이 먹는 떠먹는 초밥(지라시스시)이라고 하네요. 밑에 와사비 마요밥 위에 연어들이 담겨져 있어 코끝이 찡할 수 있다고 적혀 있는데, 난 와사비 맛 1도 모르겠던데…? 와사비를 안 좋아하는 저는 불행인지 다행인지 연어 지라시를 매우 맛있게 먹었습니다ㅋㅋㅋ', '다음 메뉴는 달짝지근한 숯불 갈비 덮밥입니다! 간장 양념에 구운 숯불 갈비에 양파, 깻잎, 달걀 반숙을 터트려 비벼 먹으면 그 맛이 크.. (물론 전 안 먹었지만…다른 분들이 그렇다고 하더라구요ㅋㅋㅋㅋㅋㅋㅋ) 마지막 메인 메뉴 양송이 크림수프와 숯불떡갈비 밥입니다. 크림리조또를 베이스로 위에 그루통과 숯불로 구운 떡갈비가 올라가 있어요!', '크림스튜 우동 만큼이나 대박 맛있습니다…ㅠㅠㅠㅠㅠㅠ (크림 소스면 다 좋아하는 거 절대 아닙니다ㅋㅋㅋㅋㅋㅋ) 강남 토끼정 요리는 다 맛있지만 크림소스 요리를 참 잘하는 거 같네요 요건 물만 마시기 아쉬워 시킨 뉴자몽과 밀키소다 딸기통통! 유자와 자몽의 맛을 함께 느낄 수 있는 뉴자몽은 상큼함 그 자체였어요.', '하치만 저는 딸기통통 밀키소다가 더 맛있었습니다ㅎㅎ 밀키소다는 토끼정에서만 만나볼 수 있는 메뉴라고 하니 한 번 드셔보시길 추천할게요!! 강남 토끼정은 강남역 맛집답게 모든 음식들이 대체적으로 맛있었어요! 건물 위치도 강남 대로변에서 조금 떨어져 있어 내부 인테리어처럼 아늑한 느낌도 있었구요ㅎㅎ', '기회가 되면 다들 꼭 들러보세요~ 🙂"""
>>> split_chunks(text, max_length=128)
['강남역 맛집으로 소문난 강남 토끼정에 다녀왔습니다. 회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요 다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다 강남역 맛집 토끼정의 외부 모습. 강남 토끼정은 4층 건물 독채로 이루어져 있습니다.', '역시 토끼정 본 점 답죠?ㅎㅅㅎ 건물은 크지만 간판이 없기 때문에 지나칠 수 있으니 조심하세요 강남 토끼정의 내부 인테리어. 평일 저녁이었지만 강남역 맛집 답게 사람들이 많았어요. 전체적으로 편안하고 아늑한 공간으로 꾸며져 있었습니다ㅎㅎ 한 가지 아쉬웠던 건 조명이 너무 어두워 눈이 침침했던… 저희는 3층에 자리를 잡고 음식을 주문했습니다.', '총 5명이서 먹고 싶은 음식 하나씩 골라 다양하게 주문했어요 첫 번째 준비된 메뉴는 토끼정 고로케와 깻잎 불고기 사라다를 듬뿍 올려 먹는 맛있는 밥입니다. 여러가지 메뉴를 한 번에 시키면 준비되는 메뉴부터 가져다 주더라구요. 토끼정 고로케 금방 튀겨져 나와 겉은 바삭하고 속은 촉촉해 맛있었어요!', '깻잎 불고기 사라다는 불고기, 양배추, 버섯을 볶아 깻잎을 듬뿍 올리고 우엉 튀김을 곁들여 밥이랑 함께 먹는 메뉴입니다. 사실 전 고기를 안 먹어서 무슨 맛인지 모르겠지만.. 다들 엄청 잘 드셨습니다ㅋㅋ 이건 제가 시킨 촉촉한 고로케와 크림스튜우동. 강남 토끼정에서 먹은 음식 중에 이게 제일 맛있었어요!!! 크림소스를 원래 좋아하기도 하지만, 느끼하지 않게 부드럽고 달달한 스튜와 쫄깃한 우동면이 너무 잘 어울려 계속 손이 가더라구요.', '사진을 보니 또 먹고 싶습니다 간사이 풍 연어 지라시입니다. 일본 간사이 지방에서 많이 먹는 떠먹는 초밥(지라시스시)이라고 하네요. 밑에 와사비 마요밥 위에 연어들이 담겨져 있어 코끝이 찡할 수 있다고 적혀 있는데, 난 와사비 맛 1도 모르겠던데…? 와사비를 안 좋아하는 저는 불행인지 다행인지 연어 지라시를 매우 맛있게 먹었습니다ㅋㅋㅋ', '다음 메뉴는 달짝지근한 숯불 갈비 덮밥입니다! 간장 양념에 구운 숯불 갈비에 양파, 깻잎, 달걀 반숙을 터트려 비벼 먹으면 그 맛이 크.. (물론 전 안 먹었지만…다른 분들이 그렇다고 하더라구요ㅋㅋㅋㅋㅋㅋㅋ) 마지막 메인 메뉴 양송이 크림수프와 숯불떡갈비 밥입니다. 크림리조또를 베이스로 위에 그루통과 숯불로 구운 떡갈비가 올라가 있어요!', '크림스튜 우동 만큼이나 대박 맛있습니다…ㅠㅠㅠㅠㅠㅠ (크림 소스면 다 좋아하는 거 절대 아닙니다ㅋㅋㅋㅋㅋㅋ) 강남 토끼정 요리는 다 맛있지만 크림소스 요리를 참 잘하는 거 같네요 요건 물만 마시기 아쉬워 시킨 뉴자몽과 밀키소다 딸기통통! 유자와 자몽의 맛을 함께 느낄 수 있는 뉴자몽은 상큼함 그 자체였어요.', '하치만 저는 딸기통통 밀키소다가 더 맛있었습니다ㅎㅎ 밀키소다는 토끼정에서만 만나볼 수 있는 메뉴라고 하니 한 번 드셔보시길 추천할게요!! 강남 토끼정은 강남역 맛집답게 모든 음식들이 대체적으로 맛있었어요! 건물 위치도 강남 대로변에서 조금 떨어져 있어 내부 인테리어처럼 아늑한 느낌도 있었구요ㅎㅎ', '기회가 되면 다들 꼭 들러보세요~ 🙂']

```

- An example of multiple texts batch segmentation

```python
>>> from kss import split_chunks

>>> text1 = """강남역 맛집으로 소문난 강남 토끼정에 다녀왔습니다. 회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요 다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다 강남역 맛집 토끼정의 외부 모습. 강남 토끼정은 4층 건물 독채로 이루어져 있습니다.', '역시 토끼정 본 점 답죠?ㅎㅅㅎ 건물은 크지만 간판이 없기 때문에 지나칠 수 있으니 조심하세요 강남 토끼정의 내부 인테리어. 평일 저녁이었지만 강남역 맛집 답게 사람들이 많았어요. 전체적으로 편안하고 아늑한 공간으로 꾸며져 있었습니다ㅎㅎ 한 가지 아쉬웠던 건 조명이 너무 어두워 눈이 침침했던… 저희는 3층에 자리를 잡고 음식을 주문했습니다.', '총 5명이서 먹고 싶은 음식 하나씩 골라 다양하게 주문했어요 첫 번째 준비된 메뉴는 토끼정 고로케와 깻잎 불고기 사라다를 듬뿍 올려 먹는 맛있는 밥입니다. 여러가지 메뉴를 한 번에 시키면 준비되는 메뉴부터 가져다 주더라구요. 토끼정 고로케 금방 튀겨져 나와 겉은 바삭하고 속은 촉촉해 맛있었어요!', '깻잎 불고기 사라다는 불고기, 양배추, 버섯을 볶아 깻잎을 듬뿍 올리고 우엉 튀김을 곁들여 밥이랑 함께 먹는 메뉴입니다. 사실 전 고기를 안 먹어서 무슨 맛인지 모르겠지만.. 다들 엄청 잘 드셨습니다ㅋㅋ 이건 제가 시킨 촉촉한 고로케와 크림스튜우동. 강남 토끼정에서 먹은 음식 중에 이게 제일 맛있었어요!!! 크림소스를 원래 좋아하기도 하지만, 느끼하지 않게 부드럽고 달달한 스튜와 쫄깃한 우동면이 너무 잘 어울려 계속 손이 가더라구요.', '사진을 보니 또 먹고 싶습니다 간사이 풍 연어 지라시입니다. 일본 간사이 지방에서 많이 먹는 떠먹는 초밥(지라시스시)이라고 하네요. 밑에 와사비 마요밥 위에 연어들이 담겨져 있어 코끝이 찡할 수 있다고 적혀 있는데, 난 와사비 맛 1도 모르겠던데…? 와사비를 안 좋아하는 저는 불행인지 다행인지 연어 지라시를 매우 맛있게 먹었습니다ㅋㅋㅋ', '다음 메뉴는 달짝지근한 숯불 갈비 덮밥입니다! 간장 양념에 구운 숯불 갈비에 양파, 깻잎, 달걀 반숙을 터트려 비벼 먹으면 그 맛이 크.. (물론 전 안 먹었지만…다른 분들이 그렇다고 하더라구요ㅋㅋㅋㅋㅋㅋㅋ) 마지막 메인 메뉴 양송이 크림수프와 숯불떡갈비 밥입니다. 크림리조또를 베이스로 위에 그루통과 숯불로 구운 떡갈비가 올라가 있어요!', '크림스튜 우동 만큼이나 대박 맛있습니다…ㅠㅠㅠㅠㅠㅠ (크림 소스면 다 좋아하는 거 절대 아닙니다ㅋㅋㅋㅋㅋㅋ) 강남 토끼정 요리는 다 맛있지만 크림소스 요리를 참 잘하는 거 같네요 요건 물만 마시기 아쉬워 시킨 뉴자몽과 밀키소다 딸기통통! 유자와 자몽의 맛을 함께 느낄 수 있는 뉴자몽은 상큼함 그 자체였어요.', '하치만 저는 딸기통통 밀키소다가 더 맛있었습니다ㅎㅎ 밀키소다는 토끼정에서만 만나볼 수 있는 메뉴라고 하니 한 번 드셔보시길 추천할게요!! 강남 토끼정은 강남역 맛집답게 모든 음식들이 대체적으로 맛있었어요! 건물 위치도 강남 대로변에서 조금 떨어져 있어 내부 인테리어처럼 아늑한 느낌도 있었구요ㅎㅎ', '기회가 되면 다들 꼭 들러보세요~ 🙂"""
>>> text2 = """주말에 가족여행으로 오션월드 다녀왔어요!!! 오션월드는 처음가보는거여서 설렘설렘~~!! 날씨도 끝내주고~! 하늘,구름 너무 이뻤습니다~! 가평휴게소까지 가는데 차가 엄~~~청 막혔습니다(3시간넘게걸림) 와 정말 토나오는줄 알았네요 하필 또 저희가족 늦게 일어나서 늦게 출발했거든요 ㅋㅋㅋ 가평휴게소 사람들이 엄청 많았어요! 호두과자랑 군것질좀 해주구요 ㅋ_ㅋ 오션월드 도착!! 주차장이 다 꽉차서.. 주차할곳이 없더라구요 계속 주차장 돌다가 겨우 한자리 있어서 주차했습니다..ㅠㅠㅠ 그런데 또 주차장에 주차하고 언덕길을 올라가야 하더라구요!?헐~ 오션월드 ..이게뭐람.. 큐알코드로 찍고 간편하게 입장했습니다 오션월드 코인도 넉넉하게 10만원 충전했어요 ㅋㅋㅋ 다들 너무 잘먹기때문에... 넉넉하게..ㅋㅋㅋ 여자 락커실에 에어컨이 얼마나 빵빵한지 오들오들 추웠습니다 캐리비안베이는 습하고 축축한데 오션월드는 완전 정반대 ㅋㅋㅋ 제가 방수팩을 준비못해서 각자 3개 살려고 했는데 헐! 한개에 19000원이에요! 그래서 한개만 샀어요 ㅠㅠ 제 핸드폰은 락커에.. 방수팩 꼭 미리 준비하세요 ㅠ 넘비싸요 ㅠ 오션월드 정말 엉망진창이었어요 ㅠㅠ 사람이 너~~~무많아서 유수풀도 줄서서들어가구요 다른 놀이기구는 엄두도 못났습니다 파도풀도 사람이 너무 많은지 안전상 관리를 빡세게 해서 재미가 없었어요.. 처음으로 먹어본 소떡소떡 물놀이하다가 먹은 간식이어서 그런지 참 맛있게 먹었습니다! 그렇지만 위생은 정말 안좋았어요.. 오션월드 처음이라 기대 많이 했는데 첨부터 끝까지 다 맘에 안들었어요 물론 사람이 너~무 많아서 일수도 있습니다. 캐리비안베이는 위생도 괜찮아 보이고 음식이 비싸지만 다 맛있었거든요! 근데 오션월드 위생도 별로고 비싸고 맛없고!!! 주차장도 좁고 주차장에서 입구까지 걸어서 올라가고.. 캐리비안베이보다 나았던건 락커시설과 유수풀 두개 정도! 오션월드 정말 아쉬웠습니다 개인적으루 캐리비안베이가 훨씬 나은듯!"""
>>> split_chunks([text1, text2], max_length=128)
[['강남역 맛집으로 소문난 강남 토끼정에 다녀왔습니다. 회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요 다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다 강남역 맛집 토끼정의 외부 모습. 강남 토끼정은 4층 건물 독채로 이루어져 있습니다.', '역시 토끼정 본 점 답죠?ㅎㅅㅎ 건물은 크지만 간판이 없기 때문에 지나칠 수 있으니 조심하세요 강남 토끼정의 내부 인테리어. 평일 저녁이었지만 강남역 맛집 답게 사람들이 많았어요. 전체적으로 편안하고 아늑한 공간으로 꾸며져 있었습니다ㅎㅎ 한 가지 아쉬웠던 건 조명이 너무 어두워 눈이 침침했던… 저희는 3층에 자리를 잡고 음식을 주문했습니다.', '총 5명이서 먹고 싶은 음식 하나씩 골라 다양하게 주문했어요 첫 번째 준비된 메뉴는 토끼정 고로케와 깻잎 불고기 사라다를 듬뿍 올려 먹는 맛있는 밥입니다. 여러가지 메뉴를 한 번에 시키면 준비되는 메뉴부터 가져다 주더라구요. 토끼정 고로케 금방 튀겨져 나와 겉은 바삭하고 속은 촉촉해 맛있었어요!', '깻잎 불고기 사라다는 불고기, 양배추, 버섯을 볶아 깻잎을 듬뿍 올리고 우엉 튀김을 곁들여 밥이랑 함께 먹는 메뉴입니다. 사실 전 고기를 안 먹어서 무슨 맛인지 모르겠지만.. 다들 엄청 잘 드셨습니다ㅋㅋ 이건 제가 시킨 촉촉한 고로케와 크림스튜우동. 강남 토끼정에서 먹은 음식 중에 이게 제일 맛있었어요!!! 크림소스를 원래 좋아하기도 하지만, 느끼하지 않게 부드럽고 달달한 스튜와 쫄깃한 우동면이 너무 잘 어울려 계속 손이 가더라구요.', '사진을 보니 또 먹고 싶습니다 간사이 풍 연어 지라시입니다. 일본 간사이 지방에서 많이 먹는 떠먹는 초밥(지라시스시)이라고 하네요. 밑에 와사비 마요밥 위에 연어들이 담겨져 있어 코끝이 찡할 수 있다고 적혀 있는데, 난 와사비 맛 1도 모르겠던데…? 와사비를 안 좋아하는 저는 불행인지 다행인지 연어 지라시를 매우 맛있게 먹었습니다ㅋㅋㅋ', '다음 메뉴는 달짝지근한 숯불 갈비 덮밥입니다! 간장 양념에 구운 숯불 갈비에 양파, 깻잎, 달걀 반숙을 터트려 비벼 먹으면 그 맛이 크.. (물론 전 안 먹었지만…다른 분들이 그렇다고 하더라구요ㅋㅋㅋㅋㅋㅋㅋ) 마지막 메인 메뉴 양송이 크림수프와 숯불떡갈비 밥입니다. 크림리조또를 베이스로 위에 그루통과 숯불로 구운 떡갈비가 올라가 있어요!', '크림스튜 우동 만큼이나 대박 맛있습니다…ㅠㅠㅠㅠㅠㅠ (크림 소스면 다 좋아하는 거 절대 아닙니다ㅋㅋㅋㅋㅋㅋ) 강남 토끼정 요리는 다 맛있지만 크림소스 요리를 참 잘하는 거 같네요 요건 물만 마시기 아쉬워 시킨 뉴자몽과 밀키소다 딸기통통! 유자와 자몽의 맛을 함께 느낄 수 있는 뉴자몽은 상큼함 그 자체였어요.', '하치만 저는 딸기통통 밀키소다가 더 맛있었습니다ㅎㅎ 밀키소다는 토끼정에서만 만나볼 수 있는 메뉴라고 하니 한 번 드셔보시길 추천할게요!! 강남 토끼정은 강남역 맛집답게 모든 음식들이 대체적으로 맛있었어요! 건물 위치도 강남 대로변에서 조금 떨어져 있어 내부 인테리어처럼 아늑한 느낌도 있었구요ㅎㅎ', '기회가 되면 다들 꼭 들러보세요~ 🙂'],
['주말에 가족여행으로 오션월드 다녀왔어요!!! 오션월드는 처음가보는거여서 설렘설렘~~!! 날씨도 끝내주고~! 하늘,구름 너무 이뻤습니다~! 가평휴게소까지 가는데 차가 엄~~~청 막혔습니다(3시간넘게걸림) 와 정말 토나오는줄 알았네요 하필 또 저희가족 늦게 일어나서 늦게 출발했거든요 ㅋㅋㅋ', '가평휴게소 사람들이 엄청 많았어요! 호두과자랑 군것질좀 해주구요 ㅋ_ㅋ 오션월드 도착!! 주차장이 다 꽉차서.. 주차할곳이 없더라구요 계속 주차장 돌다가 겨우 한자리 있어서 주차했습니다..ㅠㅠㅠ 그런데 또 주차장에 주차하고 언덕길을 올라가야 하더라구요!?헐~ 오션월드 ..이게뭐람..', '큐알코드로 찍고 간편하게 입장했습니다 오션월드 코인도 넉넉하게 10만원 충전했어요 ㅋㅋㅋ 다들 너무 잘먹기때문에... 넉넉하게..ㅋㅋㅋ 여자 락커실에 에어컨이 얼마나 빵빵한지 오들오들 추웠습니다 캐리비안베이는 습하고 축축한데 오션월드는 완전 정반대 ㅋㅋㅋ 제가 방수팩을 준비못해서 각자 3개 살려고 했는데 헐! 한개에 19000원이에요!', '그래서 한개만 샀어요 ㅠㅠ 제 핸드폰은 락커에.. 방수팩 꼭 미리 준비하세요 ㅠ 넘비싸요 ㅠ 오션월드 정말 엉망진창이었어요 ㅠㅠ 사람이 너~~~무많아서 유수풀도 줄서서들어가구요 다른 놀이기구는 엄두도 못났습니다 파도풀도 사람이 너무 많은지 안전상 관리를 빡세게 해서 재미가 없었어요..', '처음으로 먹어본 소떡소떡물놀이하다가 먹은 간식이어서 그런지 참 맛있게 먹었습니다! 그렇지만 위생은 정말 안좋았어요.. 오션월드 처음이라 기대 많이 했는데 첨부터 끝까지 다 맘에 안들었어요 물론 사람이 너~무 많아서 일수도 있습니다. 캐리비안베이는 위생도 괜찮아 보이고 음식이 비싸지만 다 맛있었거든요! 근데 오션월드 위생도 별로고 비싸고 맛없고!!! 주차장도 좁고 주차장에서 입구까지 걸어서 올라가고.. 캐리비안베이보다 나았던건 락커시설과 유수풀 두개 정도! 오션월드 정말 아쉬웠습니다', '개인적으루 캐리비안베이가 훨씬 나은듯!']]
```

<br>
</details>

<details>
<summary>max_length (<code>int</code>)</summary>
<br>

This parameter indicates the maximum length of each chunk. The `split_chunks` function creates chunks by concatenating sentences while traversing the list of segmented sentences. 
If the concatenated string is longer than the maximum length, Kss make it into a chunk (paragraph) including previous sentences.

- An example of `max_length`

```python
>>> from kss import split_chunks
>>> text = """주말에 가족여행으로 오션월드 다녀왔어요!!! 오션월드는 처음가보는거여서 설렘설렘~~!! 날씨도 끝내주고~! 하늘,구름 너무 이뻤습니다~! 가평휴게소까지 가는데 차가 엄~~~청 막혔습니다(3시간넘게걸림) 와 정말 토나오는줄 알았네요 하필 또 저희가족 늦게 일어나서 늦게 출발했거든요 ㅋㅋㅋ 가평휴게소 사람들이 엄청 많았어요! 호두과자랑 군것질좀 해주구요 ㅋ_ㅋ 오션월드 도착!! 주차장이 다 꽉차서.. 주차할곳이 없더라구요 계속 주차장 돌다가 겨우 한자리 있어서 주차했습니다..ㅠㅠㅠ 그런데 또 주차장에 주차하고 언덕길을 올라가야 하더라구요!?헐~ 오션월드 ..이게뭐람.. 큐알코드로 찍고 간편하게 입장했습니다 오션월드 코인도 넉넉하게 10만원 충전했어요 ㅋㅋㅋ 다들 너무 잘먹기때문에... 넉넉하게..ㅋㅋㅋ 여자 락커실에 에어컨이 얼마나 빵빵한지 오들오들 추웠습니다 캐리비안베이는 습하고 축축한데 오션월드는 완전 정반대 ㅋㅋㅋ 제가 방수팩을 준비못해서 각자 3개 살려고 했는데 헐! 한개에 19000원이에요! 그래서 한개만 샀어요 ㅠㅠ 제 핸드폰은 락커에.. 방수팩 꼭 미리 준비하세요 ㅠ 넘비싸요 ㅠ 오션월드 정말 엉망진창이었어요 ㅠㅠ 사람이 너~~~무많아서 유수풀도 줄서서들어가구요 다른 놀이기구는 엄두도 못났습니다 파도풀도 사람이 너무 많은지 안전상 관리를 빡세게 해서 재미가 없었어요.. 처음으로 먹어본 소떡소떡 물놀이하다가 먹은 간식이어서 그런지 참 맛있게 먹었습니다! 그렇지만 위생은 정말 안좋았어요.. 오션월드 처음이라 기대 많이 했는데 첨부터 끝까지 다 맘에 안들었어요 물론 사람이 너~무 많아서 일수도 있습니다. 캐리비안베이는 위생도 괜찮아 보이고 음식이 비싸지만 다 맛있었거든요! 근데 오션월드 위생도 별로고 비싸고 맛없고!!! 주차장도 좁고 주차장에서 입구까지 걸어서 올라가고.. 캐리비안베이보다 나았던건 락커시설과 유수풀 두개 정도! 오션월드 정말 아쉬웠습니다 개인적으루 캐리비안베이가 훨씬 나은듯!"""
>>> split_chunks(text, max_length=24)
['주말에 가족여행으로 오션월드 다녀왔어요!!! 오션월드는 처음가보는거여서 설렘설렘~~!! 날씨도 끝내주고~! 하늘,구름 너무 이뻤습니다~! 가평휴게소까지 가는데 차가 엄~~~청 막혔습니다', '(3시간넘게걸림) 와 정말 토나오는줄 알았네요 하필 또 저희가족 늦게 일어나서 늦게 출발했거든요 ㅋㅋㅋ', '가평휴게소 사람들이 엄청 많았어요! 호두과자랑 군것질좀 해주구요 ㅋ_ㅋ 오션월드 도착!! 주차장이 다 꽉차서.. 주차할곳이 없더라구요', '계속 주차장 돌다가 겨우 한자리 있어서 주차했습니다..ㅠㅠㅠ 그런데 또 주차장에 주차하고 언덕길을 올라가야 하더라구요!?', '헐~ 오션월드 ..이게뭐람.. 큐알코드로 찍고 간편하게 입장했습니다 오션월드 코인도 넉넉하게 10만원 충전했어요 ㅋㅋㅋ', '다들 너무 잘먹기때문에... 넉넉하게..ㅋㅋㅋ 여자 락커실에 에어컨이 얼마나 빵빵한지 오들오들 추웠습니다 캐리비안베이는 습하고 축축한데 오션월드는 완전 정반대 ㅋㅋㅋ', '제가 방수팩을 준비못해서 각자 3개 살려고 했는데 헐! 한개에 19000원이에요! 그래서 한개만 샀어요 ㅠㅠ 제 핸드폰은 락커에.. 방수팩 꼭 미리 준비하세요 ㅠ', '넘비싸요 ㅠ 오션월드 정말 엉망진창이었어요 ㅠㅠ 사람이 너~~~무많아서 유수풀도 줄서서들어가구요', '다른 놀이기구는 엄두도 못났습니다 파도풀도 사람이 너무 많은지 안전상 관리를 빡세게 해서 재미가 없었어요..', '처음으로 먹어본 소떡소떡물놀이하다가 먹은 간식이어서 그런지 참 맛있게 먹었습니다! 그렇지만 위생은 정말 안좋았어요.. 오션월드 처음이라 기대 많이 했는데 첨부터 끝까지 다 맘에 안들었어요', '물론 사람이 너~무 많아서 일수도 있습니다. 캐리비안베이는 위생도 괜찮아 보이고 음식이 비싸지만 다 맛있었거든요!', '근데 오션월드 위생도 별로고 비싸고 맛없고!!! 주차장도 좁고 주차장에서 입구까지 걸어서 올라가고.. 캐리비안베이보다 나았던건 락커시설과 유수풀 두개 정도! 오션월드 정말 아쉬웠습니다 개인적으루 캐리비안베이가 훨씬 나은듯!']

>>> split_chunks(text, max_length=128)
['주말에 가족여행으로 오션월드 다녀왔어요!!! 오션월드는 처음가보는거여서 설렘설렘~~!! 날씨도 끝내주고~! 하늘,구름 너무 이뻤습니다~! 가평휴게소까지 가는데 차가 엄~~~청 막혔습니다(3시간넘게걸림) 와 정말 토나오는줄 알았네요 하필 또 저희가족 늦게 일어나서 늦게 출발했거든요 ㅋㅋㅋ', '가평휴게소 사람들이 엄청 많았어요! 호두과자랑 군것질좀 해주구요 ㅋ_ㅋ 오션월드 도착!! 주차장이 다 꽉차서.. 주차할곳이 없더라구요 계속 주차장 돌다가 겨우 한자리 있어서 주차했습니다..ㅠㅠㅠ 그런데 또 주차장에 주차하고 언덕길을 올라가야 하더라구요!?헐~ 오션월드 ..이게뭐람..', '큐알코드로 찍고 간편하게 입장했습니다 오션월드 코인도 넉넉하게 10만원 충전했어요 ㅋㅋㅋ 다들 너무 잘먹기때문에... 넉넉하게..ㅋㅋㅋ 여자 락커실에 에어컨이 얼마나 빵빵한지 오들오들 추웠습니다 캐리비안베이는 습하고 축축한데 오션월드는 완전 정반대 ㅋㅋㅋ 제가 방수팩을 준비못해서 각자 3개 살려고 했는데 헐! 한개에 19000원이에요!', '그래서 한개만 샀어요 ㅠㅠ 제 핸드폰은 락커에.. 방수팩 꼭 미리 준비하세요 ㅠ 넘비싸요 ㅠ 오션월드 정말 엉망진창이었어요 ㅠㅠ 사람이 너~~~무많아서 유수풀도 줄서서들어가구요 다른 놀이기구는 엄두도 못났습니다 파도풀도 사람이 너무 많은지 안전상 관리를 빡세게 해서 재미가 없었어요..', '처음으로 먹어본 소떡소떡물놀이하다가 먹은 간식이어서 그런지 참 맛있게 먹었습니다! 그렇지만 위생은 정말 안좋았어요.. 오션월드 처음이라 기대 많이 했는데 첨부터 끝까지 다 맘에 안들었어요 물론 사람이 너~무 많아서 일수도 있습니다. 캐리비안베이는 위생도 괜찮아 보이고 음식이 비싸지만 다 맛있었거든요! 근데 오션월드 위생도 별로고 비싸고 맛없고!!! 주차장도 좁고 주차장에서 입구까지 걸어서 올라가고.. 캐리비안베이보다 나았던건 락커시설과 유수풀 두개 정도! 오션월드 정말 아쉬웠습니다', '개인적으루 캐리비안베이가 훨씬 나은듯!']
```

<br>
</details>

<details>
<summary>overlap (<code>bool</code>)</summary>
<br>

This parameter indicates whether the sentences can be duplicated across the chunks. 
If you set it to `True`, sentences can be duplicated across the chunks like sliding window.
If you set it to `False`, each sentence is going to unique.

- An example of `overlap`

```python
>>> from kss import split_chunks
>>> text = """주말에 가족여행으로 오션월드 다녀왔어요!!! 오션월드는 처음가보는거여서 설렘설렘~~!! 날씨도 끝내주고~! 하늘,구름 너무 이뻤습니다~! 가평휴게소까지 가는데 차가 엄~~~청 막혔습니다(3시간넘게걸림) 와 정말 토나오는줄 알았네요 하필 또 저희가족 늦게 일어나서 늦게 출발했거든요 ㅋㅋㅋ 가평휴게소 사람들이 엄청 많았어요! 호두과자랑 군것질좀 해주구요 ㅋ_ㅋ 오션월드 도착!! 주차장이 다 꽉차서.. 주차할곳이 없더라구요 계속 주차장 돌다가 겨우 한자리 있어서 주차했습니다..ㅠㅠㅠ 그런데 또 주차장에 주차하고 언덕길을 올라가야 하더라구요!?헐~ 오션월드 ..이게뭐람.. 큐알코드로 찍고 간편하게 입장했습니다 오션월드 코인도 넉넉하게 10만원 충전했어요 ㅋㅋㅋ 다들 너무 잘먹기때문에... 넉넉하게..ㅋㅋㅋ 여자 락커실에 에어컨이 얼마나 빵빵한지 오들오들 추웠습니다 캐리비안베이는 습하고 축축한데 오션월드는 완전 정반대 ㅋㅋㅋ 제가 방수팩을 준비못해서 각자 3개 살려고 했는데 헐! 한개에 19000원이에요! 그래서 한개만 샀어요 ㅠㅠ 제 핸드폰은 락커에.. 방수팩 꼭 미리 준비하세요 ㅠ 넘비싸요 ㅠ 오션월드 정말 엉망진창이었어요 ㅠㅠ 사람이 너~~~무많아서 유수풀도 줄서서들어가구요 다른 놀이기구는 엄두도 못났습니다 파도풀도 사람이 너무 많은지 안전상 관리를 빡세게 해서 재미가 없었어요.. 처음으로 먹어본 소떡소떡 물놀이하다가 먹은 간식이어서 그런지 참 맛있게 먹었습니다! 그렇지만 위생은 정말 안좋았어요.. 오션월드 처음이라 기대 많이 했는데 첨부터 끝까지 다 맘에 안들었어요 물론 사람이 너~무 많아서 일수도 있습니다. 캐리비안베이는 위생도 괜찮아 보이고 음식이 비싸지만 다 맛있었거든요! 근데 오션월드 위생도 별로고 비싸고 맛없고!!! 주차장도 좁고 주차장에서 입구까지 걸어서 올라가고.. 캐리비안베이보다 나았던건 락커시설과 유수풀 두개 정도! 오션월드 정말 아쉬웠습니다 개인적으루 캐리비안베이가 훨씬 나은듯!"""
>>> split_chunks(text, max_length=24, overlap=False)
['주말에 가족여행으로 오션월드 다녀왔어요!!! 오션월드는 처음가보는거여서 설렘설렘~~!! 날씨도 끝내주고~! 하늘,구름 너무 이뻤습니다~! 가평휴게소까지 가는데 차가 엄~~~청 막혔습니다', '(3시간넘게걸림) 와 정말 토나오는줄 알았네요 하필 또 저희가족 늦게 일어나서 늦게 출발했거든요 ㅋㅋㅋ', '가평휴게소 사람들이 엄청 많았어요! 호두과자랑 군것질좀 해주구요 ㅋ_ㅋ 오션월드 도착!! 주차장이 다 꽉차서.. 주차할곳이 없더라구요', '계속 주차장 돌다가 겨우 한자리 있어서 주차했습니다..ㅠㅠㅠ 그런데 또 주차장에 주차하고 언덕길을 올라가야 하더라구요!?', '헐~ 오션월드 ..이게뭐람.. 큐알코드로 찍고 간편하게 입장했습니다 오션월드 코인도 넉넉하게 10만원 충전했어요 ㅋㅋㅋ', '다들 너무 잘먹기때문에... 넉넉하게..ㅋㅋㅋ 여자 락커실에 에어컨이 얼마나 빵빵한지 오들오들 추웠습니다 캐리비안베이는 습하고 축축한데 오션월드는 완전 정반대 ㅋㅋㅋ', '제가 방수팩을 준비못해서 각자 3개 살려고 했는데 헐! 한개에 19000원이에요! 그래서 한개만 샀어요 ㅠㅠ 제 핸드폰은 락커에.. 방수팩 꼭 미리 준비하세요 ㅠ', '넘비싸요 ㅠ 오션월드 정말 엉망진창이었어요 ㅠㅠ 사람이 너~~~무많아서 유수풀도 줄서서들어가구요', '다른 놀이기구는 엄두도 못났습니다 파도풀도 사람이 너무 많은지 안전상 관리를 빡세게 해서 재미가 없었어요..', '처음으로 먹어본 소떡소떡물놀이하다가 먹은 간식이어서 그런지 참 맛있게 먹었습니다! 그렇지만 위생은 정말 안좋았어요.. 오션월드 처음이라 기대 많이 했는데 첨부터 끝까지 다 맘에 안들었어요', '물론 사람이 너~무 많아서 일수도 있습니다. 캐리비안베이는 위생도 괜찮아 보이고 음식이 비싸지만 다 맛있었거든요!', '근데 오션월드 위생도 별로고 비싸고 맛없고!!! 주차장도 좁고 주차장에서 입구까지 걸어서 올라가고.. 캐리비안베이보다 나았던건 락커시설과 유수풀 두개 정도! 오션월드 정말 아쉬웠습니다 개인적으루 캐리비안베이가 훨씬 나은듯!']

>>> split_chunks(text, max_length=24, overlap=True)
['주말에 가족여행으로 오션월드 다녀왔어요!!! 오션월드는 처음가보는거여서 설렘설렘~~!! 날씨도 끝내주고~! 하늘,구름 너무 이뻤습니다~! 가평휴게소까지 가는데 차가 엄~~~청 막혔습니다', '오션월드는 처음가보는거여서 설렘설렘~~!! 날씨도 끝내주고~! 하늘,구름 너무 이뻤습니다~! 가평휴게소까지 가는데 차가 엄~~~청 막혔습니다(3시간넘게걸림) 와 정말 토나오는줄 알았네요', '(3시간넘게걸림) 와 정말 토나오는줄 알았네요 하필 또 저희가족 늦게 일어나서 늦게 출발했거든요 ㅋㅋㅋ', '하필 또 저희가족 늦게 일어나서 늦게 출발했거든요 ㅋㅋㅋ 가평휴게소 사람들이 엄청 많았어요! 호두과자랑 군것질좀 해주구요 ㅋ', '가평휴게소 사람들이 엄청 많았어요! 호두과자랑 군것질좀 해주구요 ㅋ_ㅋ 오션월드 도착!! 주차장이 다 꽉차서.. 주차할곳이 없더라구요', '호두과자랑 군것질좀 해주구요 ㅋ_ㅋ 오션월드 도착!! 주차장이 다 꽉차서.. 주차할곳이 없더라구요 계속 주차장 돌다가 겨우 한자리 있어서 주차했습니다..ㅠㅠㅠ', '_ㅋ 오션월드 도착!! 주차장이 다 꽉차서.. 주차할곳이 없더라구요 계속 주차장 돌다가 겨우 한자리 있어서 주차했습니다..ㅠㅠㅠ 그런데 또 주차장에 주차하고 언덕길을 올라가야 하더라구요!?', '계속 주차장 돌다가 겨우 한자리 있어서 주차했습니다..ㅠㅠㅠ 그런데 또 주차장에 주차하고 언덕길을 올라가야 하더라구요!?헐~ 오션월드 ..이게뭐람..', '그런데 또 주차장에 주차하고 언덕길을 올라가야 하더라구요!?헐~ 오션월드 ..이게뭐람.. 큐알코드로 찍고 간편하게 입장했습니다', '헐~ 오션월드 ..이게뭐람.. 큐알코드로 찍고 간편하게 입장했습니다 오션월드 코인도 넉넉하게 10만원 충전했어요 ㅋㅋㅋ', '큐알코드로 찍고 간편하게 입장했습니다 오션월드 코인도 넉넉하게 10만원 충전했어요 ㅋㅋㅋ 다들 너무 잘먹기때문에... 넉넉하게..ㅋㅋㅋ 여자 락커실에 에어컨이 얼마나 빵빵한지 오들오들 추웠습니다', '오션월드 코인도 넉넉하게 10만원 충전했어요 ㅋㅋㅋ 다들 너무 잘먹기때문에... 넉넉하게..ㅋㅋㅋ 여자 락커실에 에어컨이 얼마나 빵빵한지 오들오들 추웠습니다 캐리비안베이는 습하고 축축한데 오션월드는 완전 정반대 ㅋㅋㅋ', '다들 너무 잘먹기때문에... 넉넉하게..ㅋㅋㅋ 여자 락커실에 에어컨이 얼마나 빵빵한지 오들오들 추웠습니다 캐리비안베이는 습하고 축축한데 오션월드는 완전 정반대 ㅋㅋㅋ 제가 방수팩을 준비못해서 각자 3개 살려고 했는데 헐! 한개에 19000원이에요!', '캐리비안베이는 습하고 축축한데 오션월드는 완전 정반대 ㅋㅋㅋ 제가 방수팩을 준비못해서 각자 3개 살려고 했는데 헐! 한개에 19000원이에요! 그래서 한개만 샀어요 ㅠㅠ', '제가 방수팩을 준비못해서 각자 3개 살려고 했는데 헐! 한개에 19000원이에요! 그래서 한개만 샀어요 ㅠㅠ 제 핸드폰은 락커에.. 방수팩 꼭 미리 준비하세요 ㅠ', '그래서 한개만 샀어요 ㅠㅠ 제 핸드폰은 락커에.. 방수팩 꼭 미리 준비하세요 ㅠ 넘비싸요 ㅠ 오션월드 정말 엉망진창이었어요 ㅠㅠ', '제 핸드폰은 락커에.. 방수팩 꼭 미리 준비하세요 ㅠ 넘비싸요 ㅠ 오션월드 정말 엉망진창이었어요 ㅠㅠ 사람이 너~~~무많아서 유수풀도 줄서서들어가구요', '넘비싸요 ㅠ 오션월드 정말 엉망진창이었어요 ㅠㅠ 사람이 너~~~무많아서 유수풀도 줄서서들어가구요 다른 놀이기구는 엄두도 못났습니다', '사람이 너~~~무많아서 유수풀도 줄서서들어가구요 다른 놀이기구는 엄두도 못났습니다 파도풀도 사람이 너무 많은지 안전상 관리를 빡세게 해서 재미가 없었어요..', '다른 놀이기구는 엄두도 못났습니다 파도풀도 사람이 너무 많은지 안전상 관리를 빡세게 해서 재미가 없었어요.. 처음으로 먹어본 소떡소떡물놀이하다가 먹은 간식이어서 그런지 참 맛있게 먹었습니다!', '파도풀도 사람이 너무 많은지 안전상 관리를 빡세게 해서 재미가 없었어요.. 처음으로 먹어본 소떡소떡물놀이하다가 먹은 간식이어서 그런지 참 맛있게 먹었습니다! 그렇지만 위생은 정말 안좋았어요..', '처음으로 먹어본 소떡소떡물놀이하다가 먹은 간식이어서 그런지 참 맛있게 먹었습니다! 그렇지만 위생은 정말 안좋았어요.. 오션월드 처음이라 기대 많이 했는데 첨부터 끝까지 다 맘에 안들었어요', '그렇지만 위생은 정말 안좋았어요.. 오션월드 처음이라 기대 많이 했는데 첨부터 끝까지 다 맘에 안들었어요 물론 사람이 너~무 많아서 일수도 있습니다.', '오션월드 처음이라 기대 많이 했는데 첨부터 끝까지 다 맘에 안들었어요 물론 사람이 너~무 많아서 일수도 있습니다. 캐리비안베이는 위생도 괜찮아 보이고 음식이 비싸지만 다 맛있었거든요!', '물론 사람이 너~무 많아서 일수도 있습니다. 캐리비안베이는 위생도 괜찮아 보이고 음식이 비싸지만 다 맛있었거든요! 근데 오션월드 위생도 별로고 비싸고 맛없고!!! 주차장도 좁고 주차장에서 입구까지 걸어서 올라가고.. 캐리비안베이보다 나았던건 락커시설과 유수풀 두개 정도! 오션월드 정말 아쉬웠습니다', '캐리비안베이는 위생도 괜찮아 보이고 음식이 비싸지만 다 맛있었거든요! 근데 오션월드 위생도 별로고 비싸고 맛없고!!! 주차장도 좁고 주차장에서 입구까지 걸어서 올라가고.. 캐리비안베이보다 나았던건 락커시설과 유수풀 두개 정도! 오션월드 정말 아쉬웠습니다 개인적으루 캐리비안베이가 훨씬 나은듯!']
```

<br>
</details>

<details>
<summary>kwargs (<code>**dict</code>)</summary>
<br>

`split_chunks` is based on `split_sentences`. 
Therefore, all arguments of `split_sentences` can be used. Check the following examples.

- An example of `kwargs`

```python
>>> from kss import split_chunks
>>> text = """주말에 가족여행으로 오션월드 다녀왔어요!!! 오션월드는 처음가보는거여서 설렘설렘~~!! 날씨도 끝내주고~! 하늘,구름 너무 이뻤습니다~! 가평휴게소까지 가는데 차가 엄~~~청 막혔습니다(3시간넘게걸림) 와 정말 토나오는줄 알았네요 하필 또 저희가족 늦게 일어나서 늦게 출발했거든요 ㅋㅋㅋ 가평휴게소 사람들이 엄청 많았어요! 호두과자랑 군것질좀 해주구요 ㅋ_ㅋ 오션월드 도착!! 주차장이 다 꽉차서.. 주차할곳이 없더라구요 계속 주차장 돌다가 겨우 한자리 있어서 주차했습니다..ㅠㅠㅠ 그런데 또 주차장에 주차하고 언덕길을 올라가야 하더라구요!?헐~ 오션월드 ..이게뭐람.. 큐알코드로 찍고 간편하게 입장했습니다 오션월드 코인도 넉넉하게 10만원 충전했어요 ㅋㅋㅋ 다들 너무 잘먹기때문에... 넉넉하게..ㅋㅋㅋ 여자 락커실에 에어컨이 얼마나 빵빵한지 오들오들 추웠습니다 캐리비안베이는 습하고 축축한데 오션월드는 완전 정반대 ㅋㅋㅋ 제가 방수팩을 준비못해서 각자 3개 살려고 했는데 헐! 한개에 19000원이에요! 그래서 한개만 샀어요 ㅠㅠ 제 핸드폰은 락커에.. 방수팩 꼭 미리 준비하세요 ㅠ 넘비싸요 ㅠ 오션월드 정말 엉망진창이었어요 ㅠㅠ 사람이 너~~~무많아서 유수풀도 줄서서들어가구요 다른 놀이기구는 엄두도 못났습니다 파도풀도 사람이 너무 많은지 안전상 관리를 빡세게 해서 재미가 없었어요.. 처음으로 먹어본 소떡소떡 물놀이하다가 먹은 간식이어서 그런지 참 맛있게 먹었습니다! 그렇지만 위생은 정말 안좋았어요.. 오션월드 처음이라 기대 많이 했는데 첨부터 끝까지 다 맘에 안들었어요 물론 사람이 너~무 많아서 일수도 있습니다. 캐리비안베이는 위생도 괜찮아 보이고 음식이 비싸지만 다 맛있었거든요! 근데 오션월드 위생도 별로고 비싸고 맛없고!!! 주차장도 좁고 주차장에서 입구까지 걸어서 올라가고.. 캐리비안베이보다 나았던건 락커시설과 유수풀 두개 정도! 오션월드 정말 아쉬웠습니다 개인적으루 캐리비안베이가 훨씬 나은듯!"""
>>> split_chunks(text, backend="mecab", max_length=24)
['주말에 가족여행으로 오션월드 다녀왔어요!!! 오션월드는 처음가보는거여서 설렘설렘~~!! 날씨도 끝내주고~! 하늘,구름 너무 이뻤습니다~! 가평휴게소까지 가는데 차가 엄~~~청 막혔습니다', '(3시간넘게걸림) 와 정말 토나오는줄 알았네요 하필 또 저희가족 늦게 일어나서 늦게 출발했거든요 ㅋㅋㅋ', '가평휴게소 사람들이 엄청 많았어요! 호두과자랑 군것질좀 해주구요 ㅋ_ㅋ 오션월드 도착!! 주차장이 다 꽉차서.. 주차할곳이 없더라구요', '계속 주차장 돌다가 겨우 한자리 있어서 주차했습니다..ㅠㅠㅠ 그런데 또 주차장에 주차하고 언덕길을 올라가야 하더라구요!?', '헐~ 오션월드 ..이게뭐람.. 큐알코드로 찍고 간편하게 입장했습니다 오션월드 코인도 넉넉하게 10만원 충전했어요 ㅋㅋㅋ', '다들 너무 잘먹기때문에... 넉넉하게..ㅋㅋㅋ 여자 락커실에 에어컨이 얼마나 빵빵한지 오들오들 추웠습니다 캐리비안베이는 습하고 축축한데 오션월드는 완전 정반대 ㅋㅋㅋ', '제가 방수팩을 준비못해서 각자 3개 살려고 했는데 헐! 한개에 19000원이에요! 그래서 한개만 샀어요 ㅠㅠ 제 핸드폰은 락커에.. 방수팩 꼭 미리 준비하세요 ㅠ', '넘비싸요 ㅠ 오션월드 정말 엉망진창이었어요 ㅠㅠ 사람이 너~~~무많아서 유수풀도 줄서서들어가구요', '다른 놀이기구는 엄두도 못났습니다 파도풀도 사람이 너무 많은지 안전상 관리를 빡세게 해서 재미가 없었어요..', '처음으로 먹어본 소떡소떡물놀이하다가 먹은 간식이어서 그런지 참 맛있게 먹었습니다! 그렇지만 위생은 정말 안좋았어요.. 오션월드 처음이라 기대 많이 했는데 첨부터 끝까지 다 맘에 안들었어요', '물론 사람이 너~무 많아서 일수도 있습니다. 캐리비안베이는 위생도 괜찮아 보이고 음식이 비싸지만 다 맛있었거든요!', '근데 오션월드 위생도 별로고 비싸고 맛없고!!! 주차장도 좁고 주차장에서 입구까지 걸어서 올라가고.. 캐리비안베이보다 나았던건 락커시설과 유수풀 두개 정도! 오션월드 정말 아쉬웠습니다 개인적으루 캐리비안베이가 훨씬 나은듯!']

>>> split_chunks(text, use_heuristic=False, max_length=24)
['주말에 가족여행으로 오션월드 다녀왔어요!!! 오션월드는 처음가보는거여서 설렘설렘~~!! 날씨도 끝내주고~! 하늘,구름 너무 이뻤습니다~! 가평휴게소까지 가는데 차가 엄~~~청 막혔습니다(3시간넘게걸림) 와 정말 토나오는줄 알았네요 하필 또 저희가족 늦게 일어나서 늦게 출발했거든요 ㅋㅋㅋ 가평휴게소 사람들이 엄청 많았어요!', '호두과자랑 군것질좀 해주구요 ㅋ_ㅋ 오션월드 도착!! 주차장이 다 꽉차서.. 주차할곳이 없더라구요 계속 주차장 돌다가 겨우 한자리 있어서 주차했습니다..ㅠㅠㅠ', '그런데 또 주차장에 주차하고 언덕길을 올라가야 하더라구요!?헐~ 오션월드 ..이게뭐람.. 큐알코드로 찍고 간편하게 입장했습니다 오션월드 코인도 넉넉하게 10만원 충전했어요 ㅋㅋㅋ 다들 너무 잘먹기때문에... 넉넉하게..ㅋㅋㅋ 여자 락커실에 에어컨이 얼마나 빵빵한지 오들오들 추웠습니다 캐리비안베이는 습하고 축축한데 오션월드는 완전 정반대 ㅋㅋㅋ 제가 방수팩을 준비못해서 각자 3개 살려고 했는데 헐! 한개에 19000원이에요!', '그래서 한개만 샀어요 ㅠㅠ 제 핸드폰은 락커에.. 방수팩 꼭 미리 준비하세요 ㅠ 넘비싸요 ㅠ 오션월드 정말 엉망진창이었어요 ㅠㅠ 사람이 너~~~무많아서 유수풀도 줄서서들어가구요 다른 놀이기구는 엄두도 못났습니다 파도풀도 사람이 너무 많은지 안전상 관리를 빡세게 해서 재미가 없었어요.. 처음으로 먹어본 소떡소떡물놀이하다가 먹은 간식이어서 그런지 참 맛있게 먹었습니다!', '그렇지만 위생은 정말 안좋았어요.. 오션월드 처음이라 기대 많이 했는데 첨부터 끝까지 다 맘에 안들었어요 물론 사람이 너~무 많아서 일수도 있습니다.', '캐리비안베이는 위생도 괜찮아 보이고 음식이 비싸지만 다 맛있었거든요! 근데 오션월드 위생도 별로고 비싸고 맛없고!!! 주차장도 좁고 주차장에서 입구까지 걸어서 올라가고.. 캐리비안베이보다 나았던건 락커시설과 유수풀 두개 정도! 오션월드 정말 아쉬웠습니다 개인적으루 캐리비안베이가 훨씬 나은듯!']
```

<br>
</details>

## 3. Additional Documents
- [Performance Analysis](https://github.com/hyunwoongko/kss/blob/main/docs/ANALYSIS.md)
- [Contributing Guide](https://github.com/hyunwoongko/kss/blob/main/docs/CONTRIBUTING.md)
- [Adding words to user dictionary](https://github.com/hyunwoongko/kss/blob/main/docs/USERDICT.md)

## 4. References
Kss is available in various programming languages.
- [Python version](https://github.com/hyunwoongko/kss)
- [Java version](https://github.com/sangdee/kss-java)
- [Flutter version](https://github.com/khjde1207/kss_dart)
- [C++ version](https://github.com/likejazz/korean-sentence-splitter)

## 5. Citation
If you find this toolkit useful, please consider citing:
```
@misc{kss,
  author       = {Park, Sang-kil and Ko, Hyunwoong},
  title        = {Kss: A Toolkit for Korean sentence segmentation},
  howpublished = {\url{https://github.com/hyunwoongko/kss}},
  year         = {2020},
}
```

# Korean Sentence Splitter
<a href="https://github.com/hyunwoongko/kss/releases"><img alt="GitHub release" src="https://img.shields.io/github/release/hyunwoongko/kss.svg" /></a>
<a href="https://github.com/hyunwoongko/kss/blob/master/LICENSE"><img alt="BSD 3-Clause" src="https://img.shields.io/badge/license-BSD%203%20Clause-blue.svg"/></a>
<a href="https://github.com/hyunwoongko/kss/issues"><img alt="Issues" src="https://img.shields.io/github/issues/hyunwoongko/kss"/></a>

This repository contains the source code of Kss, a representative Korean sentence segmentation library. I also conduct ongoing research about Korean sentence segmentation algorithms and report the results to this repository.
If you have a good idea about Korean sentence segmentation, please feel free to talk through the [issue](https://github.com/hyunwoongko/kss/issues).
<br><br>

## 1. Installation
### 1.1. Install from pip
Kss can be easily installed using the pip package manager.
```console
pip install kss
```

### 1.2. Install from source codes
You can also install Kss from source codes.
This can be useful for the `Add words to user dictionary` described in [Section 4. Advanced Usage]().
```console
git clone https://github.com/hyunwoongko/kss
cd kss
pip install -e .
```



## 2. Usage
### 2.1. `split_sentences`
Kss is the sentence segmentation library using heuristic algorithms. `split_sentences` is an key function of this library. You can split sentences using this function. Click the triangle button (►) to check the detailed information and example code snippets.

```python
>>> from kss import split_sentences

>>> split_sentences(
...     text: Union[str, tuple, List[str]],  
...     use_heuristic: bool = True,
...     use_morpheme: bool = True,                            
...     use_quotes_brackets_processing: bool = True,                             
...     max_recover_step: int = 5,
...     max_recover_length: int = 20000,
...     backend: str = "pynori",
...     num_workers: int = -1,                       
...     disable_gc: bool = True,                           
... )
```

<ul>
<li>
<details>
<summary>text (<code>Union[str, tuple, List[str]]</code>) </summary>
<br>

This parameter indicates input texts. you can also list or tuple for batch processing not only string.

- An example of single input segmentation

  ```python
  >>> from kss import split_sentences

  >>> text = "강남역 맛집으로 소문난 강남 토끼정에 다녀왔습니다 회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요 다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다"
  >>> split_sentences(text)
  ['강남역 맛집으로 소문난 강남 토끼정에 다녀왔습니다', '회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요', '다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다']
  ```

- An example of multiple inputs batch segmentation

  ```python
  >>> from kss import split_sentences

  >>> text1 = "오늘 여러분과 함께 리뷰해 볼 영화는 바로 디즈니 픽사의 영화 '업'입니다 저는 이 영화를 고등학교 영어시간에 처음 보게되었는데요, 수능날을 맞이해서 고등학교 추억이 담긴 영화를 오늘 여러분께 소개해드리려고 해요~ㅎㅎㅎ 한방울 눈물과 한바탕 웃음 마음 속에 담고 싶은 단 하나의 걸작 평생 모험을 꿈꿔 왔던 ‘칼’ 할아버지는 수천 개의 풍선을 매달아 집을 통째로 남아메리카로 날려 버리는데, ‘칼’ 할아버지의 이 위대한 모험에 초대 받지 않은 불청객이 있었으니, 바로 황야의 탐험가 ‘러셀’ 지구상에 둘도 없을 이 어색한 커플이 함께 하는 대모험 그들은 과연 남미의 잃어버린 세계에서 사라져 버린 꿈과 희망, 행복을 다시 찾을 수 있을까? 여러분은 디즈니 영화를 좋아하시 나요? 저는 디즈니보다는 픽사를 훨씬 더 좋아하는 편인데요 디즈니와 픽사가 합병한 뒤, 저는 디즈니 픽사 영화가 인생영화 중 대부분을 차지할 정도로 정말 즐겨보고 있어요"
  >>> text2 = "동영상 촬영이 금지되어있어 노홍철 씨의 열정 넘치는 강연을 그대로 보여 드리지 못하는 점 너무 아쉽네요 ㅠㅠ 간단한 행사스케치로나마 참고해주세요~ 노홍철의 열정 Talk 행사는 개그맨 김범용 씨가 맡아주셨고 오프닝 무대는 위대한 탄생3 탑3로 이름을 날린 오병길 씨의 노래로 뜨겁게 달궈졌습니다^^ 이날 초대된 로열블루와 블루 멤버십 고객분들의 환호로 삼성홍보관 딜라이트 안이 가득 차더군요! (오병길 씨의 노래 잘하는 비법은 무엇일까요? 꾸준한 모창연습이라고… ㅋ) 곧이어 이 날 행사의 메인이었던 노홍철씨의 열정 Talk가 본격적으로 시작되었습니다"
  >>> split_sentences([text1, text2])
  [["오늘 여러분과 함께 리뷰해 볼 영화는 바로 디즈니 픽사의 영화 '업'입니다", '저는 이 영화를 고등학교 영어시간에 처음 보게되었는데요,', '수능날을 맞이해서 고등학교 추억이 담긴 영화를 오늘 여러분께 소개해드리려고 해요~ㅎㅎㅎ', '한방울 눈물과 한바탕 웃음 마음 속에 담고 싶은 단 하나의 걸작 평생 모험을 꿈꿔 왔던 ‘칼’ 할아버지는 수천 개의 풍선을 매달아 집을 통째로 남아메리카로 날려 버리는데, ‘칼’ 할아버지의 이 위대한 모험에 초대 받지 않은 불청객이 있었으니, 바로 황야의 탐험가 ‘러셀’ 지구상에 둘도 없을 이 어색한 커플이 함께 하는 대모험 그들은 과연 남미의 잃어버린 세계에서 사라져 버린 꿈과 희망, 행복을 다시 찾을 수 있을까?', '여러분은 디즈니 영화를 좋아하시 나요?', '저는 디즈니보다는 픽사를 훨씬 더 좋아하는 편인데요', '디즈니와 픽사가 합병한 뒤, 저는 디즈니 픽사 영화가 인생영화 중 대부분을 차지할 정도로 정말 즐겨보고 있어요'],
  ['동영상 촬영이 금지되어있어 노홍철 씨의 열정 넘치는 강연을 그대로 보여 드리지 못하는 점 너무 아쉽네요 ㅠㅠ', '간단한 행사스케치로나마 참고해주세요~', '노홍철의 열정 Talk 행사는 개그맨 김범용 씨가 맡아주셨고 오프닝 무대는 위대한 탄생3 탑3로 이름을 날린 오병길 씨의 노래로 뜨겁게 달궈졌습니다^^', '이날 초대된 로열블루와 블루 멤버십 고객분들의 환호로 삼성홍보관 딜라이트 안이 가득 차더군요!', '(오병길 씨의 노래 잘하는 비법은 무엇일까요? 꾸준한 모창연습이라고… ㅋ) 곧이어 이 날 행사의 메인이었던 노홍철씨의 열정 Talk가 본격적으로 시작되었습니다']]
  ```
</details>
</li>
<li>    
<details>
<summary>use_heuristic (<code>bool</code>)</summary>
<br>

This parameter indicates whether to use the heuristic algorithm or not. If you set it `True`, sentence segmentation can be performed without punctuation. If you set it `False`, segmentation can be performed depending only on punctuation.
I recommend to you set it `False` if input texts follow the punctuation rules relatively well, because Kss can make mistakes sometimes in the parts that do not have punctuation mark. 

- Formal articles (wiki, news, essays): recommend to `False`
- Informal articles (sns, blogs, messages): recommend to `True`

<br>

As shown in the performance evaluation, if this option is set to `False`, the segmentation error rate will be downed.
However, it does mean Kss will be less sensitive. If there are relatively few punctuation marks, such as messages or blog articles, Kss can't split most of the sentences.
Therefore, it must be adjusted according to the type of the input texts.

- An example of using heuristic algorithms (can segment without punctuations)

  ```python
  >>> from kss import split_sentences
    
  >>> text = "원어민도 흔하게 틀리는 문법오류는 아포스트로피(apostrophe)를 잘못된 사용하는거예요 질문: 아포스트로피(apostrophe)를 왜 쓰나요? 대답: 두 가지 목적으로 사용해요 예를 들어서 do not = don't not의 o를 생략한걸 apostrophe가 보여주는거예요 또 다른 예를 들면 we are = we're are의 a를 생략했죠 생략된 표현에 아포스트로피를 자주 사용해요. 이제 아시겠죠?"
  >>> split_sentences(text, use_heuristic=True)
  ['원어민도 흔하게 틀리는 문법오류는 아포스트로피(apostrophe)를 잘못된 사용하는거예요', '질문: 아포스트로피(apostrophe)를 왜 쓰나요?', '대답: 두 가지 목적으로 사용해요', "예를 들어서 do not = don't not의 o를 생략한걸 apostrophe가 보여주는거예요", "또 다른 예를 들면 we are = we're are의 a를 생략했죠", '생략된 표현에 아포스트로피를 자주 사용해요.', '이제 아시겠죠?']
  ```

- An example of not using heuristic algorithms (can't segment without punctuations)
  ```python
  >>> from kss import split_sentences
    
  >>> text = "원어민도 흔하게 틀리는 문법오류는 아포스트로피(apostrophe)를 잘못된 사용하는거예요 질문: 아포스트로피(apostrophe)를 왜 쓰나요? 대답: 두 가지 목적으로 사용해요 예를 들어서 do not = don't not의 o를 생략한걸 apostrophe가 보여주는거예요 또 다른 예를 들면 we are = we're are의 a를 생략했죠 생략된 표현에 아포스트로피를 자주 사용해요. 이제 아시겠죠?"
  >>> split_sentences(text, use_morpheme=False)
  ['원어민도 흔하게 틀리는 문법오류는 아포스트로피(apostrophe)를 잘못된 사용하는거예요 질문: 아포스트로피(apostrophe)를 왜 쓰나요?', "대답: 두 가지 목적으로 사용해요 예를 들어서 do not = don't not의 o를 생략한걸 apostrophe가 보여주는거예요 또 다른 예를 들면 we are = we're are의 a를 생략했죠 생략된 표현에 아포스트로피를 자주 사용해요.", '이제 아시겠죠?']
  ```
</details>
</li>

<li>
<details>
<summary>use_quotes_brackets_processing (<code>bool</code>)</summary>
<br>

Kss has the feature that does not segment parts enclosed in brackets (괄호) and quotation marks (따옴표). This parameter indicates whether to split the parts enclosed in brackets or quotations marks. If you set it `True`, Kss does not segment parts enclosed in brackets and quotations marks. If you set it `False`, Kss segments all parts even if there are enclosed in brackets and quotations marks.

- An example of using quotes brackets processing

  ```python
  >>> from kss import split_sentences
    
  >>> text = '"나는 이제 더는 못 먹겠다. 너무 배불러." 그리고 곧장 자리를 떴다. 아마도 화장실에 간 모양이다.'
  >>> split_sentences(text, use_quotes_brackets_processing=True)
  ['"나는 이제 더는 못 먹겠다. 너무 배불러." 그리고 곧장 자리를 떴다.', '아마도 화장실에 간 모양이다.']
  ```

- An example of not using quotes brackets processing
  ```python
  >>> from kss import split_sentences
    
  >>> text = '"나는 이제 더는 못 먹겠다. 너무 배불러." 그리고 곧장 자리를 떴다. 아마도 화장실에 간 모양이다.'
  >>> split_sentences(text, use_quotes_brackets_processing=False)
  ['"나는 이제 더는 못 먹겠다.', '너무 배불러.', '" 그리고 곧장 자리를 떴다.', '아마도 화장실에 간 모양이다.']
  ```
</details>
</li>
<li>
<details>
<summary>max_recover_step & max_recover_length (<code>int</code>)</summary>
<br>

Kss 2.0 or later can segment sentences even if the pair of brackets and quotation marks do not match. This was a chronic problem in previous Kss C++ (1.0) ([#4](https://github.com/likejazz/korean-sentence-splitter/issues/4), [#8](https://github.com/likejazz/korean-sentence-splitter/issues/8)). 
But it was fixed in 2.0 by adding calibration feature about quotation marks and brackets mismatch. However, this solution uses the recursive algorithm, so it can be very slow in some cases. Therefore, Kss provides the option to adjust the recursive algorithm.

- `max_recover_step` determines the depth of recursion. Kss never go deeper than this when resolving quotes and brackets mismatch.
- `max_recover_length` determines the length of a sentence to which calibration is applied. Kss does not calibrate sentences longer than this value. Because calibrating long sentences takes a very long time.

<br>

Adjusting the above two options can save your precious time.

- An example of using max recover step

  ```python
  >>> from kss import split_sentences
    
  >>> text = 'YOUR_VERY_LONG_TEXT'
  >>> split_sentences(text, max_recover_step=5)
  ```

- An example of using max recover length
  ```python
  >>> from kss import split_sentences
    
  >>> text = 'YOUR_VERY_LONG_TEXT'
  >>> split_sentences(text, max_recover_length=20000)
  ```
</details>
</li>

<li>    
<details>
<summary>backend (<code>str</code>)</summary>
<br>

Kss 3.0 or later supports morpheme analysis. This parameter indicates which morpheme anlyzer will be used during segmentation. 
If you set it `pynori` or `mecab`, sentence segmentation is possible even at the unspecified [eomi (어미)](https://ko.wikipedia.org/wiki/%EC%96%B4%EB%AF%B8). 
In this case, Kss can segment sentences that use honorifics (경어), dialects (방언), neologisms (신조어) and [eomi transferred from noun (명사형 전성어미)](https://ko.wiktionary.org/wiki/%EC%A0%84%EC%84%B1%EC%96%B4%EB%AF%B8), and can grasped well the parts that are difficult to grasp without morpheme information. 
If you set it `none`, segmentation only can be performed about [final eomi (어말어미)](http://encykorea.aks.ac.kr/Contents/Item/E0066610) `다`, `요`, `죠` that are frequently used in Korean.

The followings are summary of the three possible options.

- `pynori` Use Pynori analyzer. It works fine even without C++ installed, but is very slow.
- `mecab` Use Mecab analyzer. It only works in the environment that C++ is installed. However, it is much faster than Pynori.
- `none`: Do not use morpheme analyzer. Kss segments sentences by relying only on final eomi. (`다`, `요`, `죠`)

<br>

Kss use the [Pynori](https://github.com/gritmind/python-nori), the pure python morpheme anlyzer by default. However, you can change it to [Mecab-Ko](https://github.com/jonghwanhyeon/python-mecab-ko), the super-fast morpheme analyzer based on C++.
[The performance](https://github.com/hyunwoongko/kss/blob/main/UPDATES.md#kss-300) of two analyzers is almost similar because they were developed based on the same dictionary, [mecab-ko-dic](https://bitbucket.org/eunjeon/mecab-ko-dic). 
However, since there is a lot of difference in speed, we strongly recommend using mecab backend if you can install mecab-ko in your environment.
(I didn't set Mecab-Ko as the default because I value compatibility over speed.)

- An example of using morpheme features via `backend` option

  ```python
  >>> from kss import split_sentences
    
  >>> text = "부디 만수무강 하옵소서 천천히 가세용~ 너 밥을 먹는구나 응 맞아 난 근데 어제 이사했음 그랬구나 이제 마지막임 응응"

  >>> split_sentences(text, backend="pynori")
  ['부디 만수무강 하옵소서', '천천히 가세용~', '너 밥을 먹는구나', '응 맞아 난 근데 어제 이사했음', '그랬구나 이제 마지막임', '응응']

  >>> split_sentences(text, backend="pynori")
  ['부디 만수무강 하옵소서', '천천히 가세용~', '너 밥을 먹는구나', '응 맞아 난 근데 어제 이사했음', '그랬구나 이제 마지막임', '응응']

  >>> split_sentences(text, backend="none")
  ['부디 만수무강 하옵소서 천천히 가세용~ 너 밥을 먹는구나 응 맞아 난 근데 어제 이사했음 그랬구나 이제 마지막임 응응']
  ```

</details>    
</li>

<li>    
<details>
<summary>num_workers (<code>int</code>)</summary>
<br>

Kss 3.0 or later supports multiprocessing. Therefore, multiple sentences can be segmented at the same time. This parameter indicates the number of workers to use for multiprocessing. If you set this value as 1 or 0, multiprocessing is disabled. If you input -1, Kss uses the maximum workers as many as possible. 
If a different value is entered, the number you entered of workers is allocated.

As shown in the performance evaluation, multiprocessing can lead a very large effect on speed. 
Multiprocessing makes segmentation much faster, especially when using the Pynori backend.

- An example of using a num_workers option

  ```python
  >>> from kss import split_sentences

  >>> split_sentences(some_text, num_workers=1)  # disable multiprocessing
  >>> split_sentences(some_text, num_workers=-1)  # use maximum workers as many as possible
  >>> split_sentences(some_text, num_workers=4)  # use 4 workers
  ```

</details>
</li>

<li>
<details>
<summary>disable_gc (<code>bool</code>)</summary>
<br>

This parameter indicates whether to enable the garbage collection during the sentence segmentation. The Pynori analyzer is implemented based on the data structure called [Trie](https://en.wikipedia.org/wiki/Trie). 
However, since this uses recursive algorithm, it often wastes a lot of memory, which leads to frequent garbage collection. If you set it to `True`, segmentation speed can be improved by disabling garbage collection. 
Of course, when the segmentation process ends, garbage collection will be reactivated.

- An example of using a num_workers option

  ```python
  >>> from kss import split_sentences

  >>> split_sentences(some_text, disable_gc=True)  # disable garbage collection
  >>> split_sentences(some_text, disable_gc=False)  # enable garbage collection
  ```


</details>
</li>

</ul>
<br>

### 2.2. `split_chunks`
<br>

## 3. Performance Analysis

### 3.1. Segmentation Error Rate
The following table indicates how often each option in Kss leads to mis-segmentation. 
I collected 377 Korean sentences that are difficult to segment and evaluated the error rate based on this data (`/tests/test_uoneway.txt`). 
Since each line of data consists of a complete sentence, it shouldn't be segmented. 
However, Kss often makes mistakes, and the following table shows this as a percentage.
**Note that this is just an error rate, not an accuracy.** (Even if you don't segment any line, you can get an error rate of 0.000%)

|Backend                        |Error rate|
|:------------------------------|:--------:|
|Kss 3.0 (Mecab backend)        |3.1830%   |
|Kss 3.0 (Pynori backend)       |3.7135%   |
|Kss 2.6 (Non-morpheme backend) |7.6923%   |
|Kss 1.3.1 (C++ ver)            |60.3174%  |
|OKT 2.3.1 (Powered by KoalaNLP)|60.3174%  |
|Hannanum (Powered by KoalaNLP) |60.3174%  |


This result shows that more accurate and safe sentence segmentation is possible by using morpheme features. As shown in the table, the error rate is reduced by twice.
If you want to reproduce this, run `/tests/test_kss.py::test_from_uoneway()`.


### 3.2. Segmentation Speed Analysis
I also compared the speed with a combination of morpheme backend and multiprocessing. For the experiment, I used Macbook M1 silicon (8 processes). 
If you use different CPUs and number of cores, there may be a difference in the results.

![](assets/performance-of-mp.png)

|Backend             |Multiprocessing | 5 sample  | 10 samples | 50 samples | 100 samples|
|:-------------------|:--------------:|:---------:|:----------:|:----------:|:----------:|
|Non-morpheme backend|Yes             |0.07581 sec|0.10828 sec |0.33892 sec |0.58824 sec |
|Non-morpheme backend|No              |0.12730 sec|0.25130 sec |1.24873 sec |2.49617 sec |
|Mecab backend       |Yes             |0.07623 sec|0.11040 sec |0.33486 sec |0.58013 sec |
|Mecab backend       |No              |0.12231 sec|0.25161 sec |1.24385 sec |2.47525 sec |
|Pynori backend      |Yes             |0.33854 sec|0.53759 sec |2.03244 sec |3.59298 sec |
|Pynori backend      |No              |0.85390 sec|1.72044 sec |8.56288 sec |16.79657 sec|

Experimental results have shown that using the multiprocessing is the most efficient. With multiprocessing, you can get a huge performance boost because you can process multiple input data at the same time.
I also found the Pynori backend to be very slow. However, it can be supplemented if multiprocessing is used together.
Meanwhile, [Mecab](https://github.com/jonghwanhyeon/python-mecab-ko) has similar speed with non-morpheme backend (backend that is not using morpheme analyzer).
Therefore, If you want to achieve both high speed and performance, it is best to use a combination of mecab and multiprocessing.
If you want to reproduce this, run `/tests/test_mp.py`.

P.s. The reason mecab's graph bounces at the beginning is because it includes the time to load the dictionary. (because it is loaded lazy on first execution)

## 4. Advanced Usage
### 4.1. Add words to user dictionary

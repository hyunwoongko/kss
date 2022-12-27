# Kss: A Toolkit for Korean sentence segmentation
<a href="https://github.com/hyunwoongko/kss/releases"><img alt="GitHub release" src="https://img.shields.io/github/release/hyunwoongko/kss.svg" /></a>
<a href="https://github.com/hyunwoongko/kss/issues"><img alt="Issues" src="https://img.shields.io/github/issues/hyunwoongko/kss"/></a>

This repository contains the source code of Kss, a representative Korean sentence segmentation toolkit. I also conduct ongoing research about Korean sentence segmentation algorithms and report the results to this repository.
If you have some good ideas about Korean sentence segmentation, please feel free to talk through the [issue](https://github.com/hyunwoongko/kss/issues).

<br>

### What's New:
- December 19, 2022 [Released Kss 4.0 Python](https://github.com/hyunwoongko/kss/releases/tag/4.0.0).
- May 5, 2022 [Released Kss Fluter](https://github.com/khjde1207/kss_dart).
- August 25, 2021 [Released Kss Java](https://github.com/sangdee/kss-java).
- August 18, 2021 [Released Kss 3.0 Python](https://github.com/hyunwoongko/kss/releases/tag/3.0.1).
- December 21, 2020 [Released Kss 2.0 Python](https://github.com/hyunwoongko/kss/releases/tag/3.0.1).
- August 16, 2019 [Released Kss 1.0 C++](https://github.com/hyunwoongko/kss/releases/tag/3.0.1).

## Installation
### Install Kss
Kss can be easily installed using the pip package manager.
```console
pip install kss
```

### Install Mecab (Optional)
Please install mecab or konlpy.tag.Mecab to use Kss much faster.
- mecab (Linux/MacOS): https://github.com/hyunwoongko/python-mecab-kor
- mecab (Windows): https://cleancode-ws.tistory.com/97
- konlpy.tag.Mecab (Linux/MacOS): https://konlpy.org/en/latest/api/konlpy.tag/#mecab-class
- konlpy.tag.Mecab (Windows): https://uwgdqo.tistory.com/363

## Features

#### 1) `split_sentences`: split text into sentences

```python
from kss import split_sentences

split_sentences(
    text: Union[str, List[str], Tuple[str]],
    backend: str = "auto",
    num_workers: Union[int, str] = "auto" ,
    strip: bool = True,
)
```

<details>
<summary>Parameters</summary>

- **text: String or List/Tuple of strings**
    - string: single text segmentation
    - list/tuple of strings: batch texts segmentation
- **backend: Morpheme analyzer backend**
    - `backend='auto'`: find `mecab` → `konlpy.tag.Mecab` → `pecab` and use first found analyzer (default)
    - `backend='mecab'`: find `mecab` → `konlpy.tag.Mecab` and use first found analyzer
    - `backend='pecab'`: use `pecab` analyzer
- **num_workers: The number of multiprocessing workers**
    - `num_workers='auto'`: use multiprocessing with the maximum number of workers if possible (default)
    - `num_workers=1`: don't use multiprocessing
    - `num_workers=2~N`: use multiprocessing with the specified number of workers
- **strip: Whether it does `strip()` for all output sentences or not**
  - `strip=True`: do `strip()` for all output sentences (default)
  - `strip=False`: do not `strip()` for all output sentences

</details>

<details>
<summary>Usages</summary>

- Single text segmentation
  ```python
  import kss

  text = "회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요 다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다 강남역 맛집 토끼정의 외부 모습."

  kss.split_sentences(text)
  # ['회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요', '다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다', '강남역 맛집 토끼정의 외부 모습.']
  ```

- Batch texts segmentation
  ```python
  import kss

  texts = [
      "회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요 다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다",
      "강남역 맛집 토끼정의 외부 모습. 강남 토끼정은 4층 건물 독채로 이루어져 있습니다.",
      "역시 토끼정 본 점 답죠?ㅎㅅㅎ 건물은 크지만 간판이 없기 때문에 지나칠 수 있으니 조심하세요 강남 토끼정의 내부 인테리어.",
  ]

  kss.split_sentences(texts)
  # [['회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요', '다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다']
  # ['강남역 맛집 토끼정의 외부 모습.', '강남 토끼정은 4층 건물 독채로 이루어져 있습니다.']
  # ['역시 토끼정 본 점 답죠?ㅎㅅㅎ', '건물은 크지만 간판이 없기 때문에 지나칠 수 있으니 조심하세요', '강남 토끼정의 내부 인테리어.']]
  ```

- Remain all prefixes/suffixes space characters for original text recoverability
  ```python
  import kss
  
  text = "회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요\n다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다 강남역 맛집 토끼정의 외부 모습."

  kss.split_sentences(text)
  # ['회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요\n', '다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다 ', '강남역 맛집 토끼정의 외부 모습.']
  ```

</details>

<details>
<summary>Performance Analysis</summary>

#### 1) Test Commands
You can reproduce all the following analyses using source code and datasets in `./bench/` directory and the source code was copied from [here](https://github.com/bab2min/kiwipiepy/tree/main/benchmark/sentence_split).
Note that the `Baseline` is regex based segmentation method (`re.split(r"(?<=[.!?])\s", text)`).

| Name                                             | Command (in root directory)                                                                               |
|--------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| Baseline                                         | `python3 ./bench/test_baseline.py ./bench/testset/*.txt`                                                  |
| [Kiwi](https://github.com/bab2min/kiwipiepy)     | `python3 ./bench/test_kiwi.py ./bench/testset/*.txt`                                                      |
| [Koalanlp](https://github.com/koalanlp/koalanlp) | `python3 ./bench/test_koalanlp.py ./bench/testset/*.txt --backend=OKT/HNN/KMR/RHINO/EUNJEON/ARIRANG/KKMA` |
| [Kss](https://github.com/hyunwoongko/kss) (ours) | `python3 ./bench/test_kss.py ./bench/testset/*.txt --backend=mecab/pecab`                                 |

<br>

#### 2) Evaluation datasets:

I used the following 6 evaluation datasets for analyses. Thanks to [Minchul Lee](https://github.com/bab2min) for creating various sentence segmentation datasets.

| Name                                                                                  | Descriptions                                                                              | The number of sentences | Creator                                                                                                                                                                                                                                                            |
|---------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [blogs_lee](https://github.com/hyunwoongko/kss/blob/main/bench/testset/blogs_lee.txt) | Dataset for testing blog style text segmentation                                          | 170                     | [Minchul Lee](https://github.com/bab2min/kiwipiepy/tree/main/benchmark/sentence_split)                                                                                                                                                                             |
| [blogs_ko](https://github.com/hyunwoongko/kss/blob/main/bench/testset/blogs_ko.txt)   | Dataset for testing blog style text segmentation, which is harder than Lee's blog dataset | 336                     | [Hyunwoong Ko](https://github.com/hyunwoongko)                                                                                                                                                                                                                     |
| [tweets](https://github.com/hyunwoongko/kss/blob/main/bench/testset/tweets.txt)       | Dataset for testing tweeter style text segmentation                                       | 178                     | [Minchul Lee](https://github.com/bab2min/kiwipiepy/tree/main/benchmark/sentence_split)                                                                                                                                                                             |
| [nested](https://github.com/hyunwoongko/kss/blob/main/bench/testset/nested.txt)       | Dataset for testing text which have parentheses and quotation marks segmentation          | 91                      | [Minchul Lee](https://github.com/bab2min/kiwipiepy/tree/main/benchmark/sentence_split)                                                                                                                                                                             |
| [v_ending](https://github.com/hyunwoongko/kss/blob/main/bench/testset/v_ending.txt)   | Dataset for testing difficult eomi segmentation, it contains various dialect sentences    | 30                      | [Minchul Lee](https://github.com/bab2min/kiwipiepy/tree/main/benchmark/sentence_split)                                                                                                                                                                             |
| [sample](https://github.com/hyunwoongko/kss/blob/main/bench/testset/sample.txt)       | An example used in README.md (강남 토끼정)                                                     | 41                      | [Isaac](http://semantics.kr/%ed%95%9c%ea%b5%ad%ec%96%b4-%ed%98%95%ed%83%9c%ec%86%8c-%eb%b6%84%ec%84%9d%ea%b8%b0-%eb%b3%84-%eb%ac%b8%ec%9e%a5-%eb%b6%84%eb%a6%ac-%ec%84%b1%eb%8a%a5%eb%b9%84%ea%b5%90/), modified by [Hyunwoong Ko](https://github.com/hyunwoongko) |

Note that I modified labels of two sentences in `sample.txt` made by [Issac](http://semantics.kr/%ed%95%9c%ea%b5%ad%ec%96%b4-%ed%98%95%ed%83%9c%ec%86%8c-%eb%b6%84%ec%84%9d%ea%b8%b0-%eb%b3%84-%eb%ac%b8%ec%9e%a5-%eb%b6%84%eb%a6%ac-%ec%84%b1%eb%8a%a5%eb%b9%84%ea%b5%90/)
because the [original blog post](https://blog.naver.com/jully1211/221437777873) was written like the following:

<img width=1000px src="https://github.com/hyunwoongko/kss/blob/main/assets/rabbit_1.png">

<img width=1000px src="https://github.com/hyunwoongko/kss/blob/main/assets/rabbit_2.png">

But Issac's labels were:

<img width=500px src="https://github.com/hyunwoongko/kss/blob/main/assets/issac.png">

In fact, `사실 전 고기를 안 먹어서 무슨 맛인지 모르겠지만..` and `(물론 전 안 먹었지만` are embraced sentences (안긴문장), not independent sentences. So sentence segmentation tools should do not split that parts.
    
<br>

#### 3) Sentence segmentation performance (Quantitative Analysis)
 
The following table shows the segmentation performance based on **exact match (EM)**.
If you are unfamilar with EM score and F1 score, please refer to [this](https://qa.fastforwardlabs.com/no%20answer/null%20threshold/bert/distilbert/exact%20match/f1/robust%20predictions/2020/06/09/Evaluating_BERT_on_SQuAD.html#Metrics-for-QA).
Kss performed best in most cases, and Kiwi performed well. Both baseline and koalanlp performed poorly.

| Name           | Library version | Backend | blogs_lee   | blogs_ko    | tweets      | nested      | v_ending    | sample      | Average     |
|----------------|-----------------|---------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| Baseline       | N/A             | N/A     | 0.53529     | 0.44940     | 0.51124     | 0.68132     | 0.00000     | 0.34146     | 0.41987     |
| Koalanlp       | 2.1.7           | OKT     | 0.53529     | 0.44940     | 0.53371     | 0.79121     | 0.00000     | 0.36585     | 0.44591     |
| Koalanlp       | 2.1.7           | HNN     | 0.54118     | 0.44345     | 0.54494     | 0.78022     | 0.00000     | 0.34146     | 0.44187     |
| Koalanlp       | 2.1.7           | KMR     | 0.51176     | 0.39583     | 0.42135     | 0.79121     | 0.00000     | 0.26829     | 0.39807     |
| Koalanlp       | 2.1.7           | RHINO   | 0.52941     | 0.40774     | 0.39326     | 0.79121     | 0.00000     | 0.29268     | 0.40238     |
| Koalanlp       | 2.1.7           | EUNJEON | 0.51176     | 0.37500     | 0.38202     | 0.70330     | 0.00000     | 0.21951     | 0.36526     |
| Koalanlp       | 2.1.7           | ARIRANG | 0.51176     | 0.41071     | 0.44382     | 0.79121     | 0.00000     | 0.29268     | 0.40836     |
| Koalanlp       | 2.1.7           | KKMA    | 0.52941     | 0.45238     | 0.38202     | 0.58242     | 0.06667     | 0.31707     | 0.38832     |
| Kiwi           | 0.14.0          | N/A     | 0.78235     | 0.60714     | 0.66292     | 0.83516     | 0.20000     | 0.90244     | 0.66500     |
| **Kss (ours)** | 4.0.0           | pecab   | **0.86471** | **0.82440** | 0.71910     | **0.87912** | **0.36667** | **0.95122** | 0.76753     |
| **Kss (ours)** | 4.0.0           | mecab   | **0.86471** | **0.82440** | **0.73034** | **0.87912** | **0.36667** | **0.95122** | **0.76941** |

You can also compare the performance with the following graphs.

![](https://github.com/hyunwoongko/kss/blob/main/assets/tasks_performance.png)

![](https://github.com/hyunwoongko/kss/blob/main/assets/average_score.png)

<br>

#### 4) Why don't I trust F1 score in sentence segmentation domain?
The evaluation source code which I copied from [kiwipiepy](https://github.com/bab2min/kiwipiepy/tree/main/benchmark/sentence_split) provides both EM score and F1 score  (dice similarity). I measured both scores, but I didn't upload F1 score based results. Actually, F1 scores of Kss are also best among the segmentation tools. **But I don't believe this is proper metric to measure sentence segmentation performance.** For example, EM score of `text.split(" ")` on `tweets.txt` is 0.06742. This means it's terrible sentence segmentation method on tweeter style text. However, F1 score of it on `tweets.txt` is 0.54083, and it is similar with the F1 score of Koalanlp KKMA backend (0.56832).

What I want to say is the actual performance of segmentation could be vastly different even if the F1 scores were similar.
You can reproduce this with `python3 ./bench/test_word_split.py ./bench/testset/tweets.txt`, and here is one of the segmentation example of both method.

```
Input:

기억해. 넌 그 애의 친구야. 네가 죽으면 마 들레 느가 펑펑 울 거야. 비 체는 슬퍼하겠지. 이 안은 화를 낼 거야. 메이 시는 어쩌면 조금은 생각 해 주지 않을까. 중요한 건 그건 네가 지키고 싶어 했던 사람들이잖아. 어서 가.
```
```
Method: Koalanlp KKMA backend
EM score: 0.38202
F1 score: 0.56832

Output:
기억해. 넌 그 애의 친구야.
네가 죽으면 마 들레 느가 펑펑 울 거야.
비 체는 슬퍼하겠지.
이 안은 화를 낼 거야.
메이 시는 어쩌면 조금은 생각 해 주지 않을까.
중요한 건 그건 네가 지키고 싶어 했던 사람들이잖아.
어서 가.
```

```
Method: text.split(" ")
EM score: 0.06742
F1 score: 0.54083

Output:
기억해.
넌
그
애의
친구야.
네가
죽으면
마들레느가
펑펑
울거야.
비체는
슬퍼하겠지.
이안은
화를
낼거야.
메이시는
어쩌면
조금은
생각
해주지
않을까.
중요한건
그건
네가
지키고
싶어했던
사람들이잖아.
어서
가.
```

This means that the F1 score has the huge advantages for method that cut sentences too finely.
Of course, measuring the performance of the sentence segmentation algorithm is difficult, and we need to think more about metrics. 
However, the character level F1 score may cause **users to misunderstand the tool's real performance**. 
So I have more confidence in the EM score, which is a somewhat clunky but safe metric.

<br>

#### 5) Where does the difference in performance come from? (Qualitative Analysis)
It is meaningless to simply compare them by number. I definitely want you to see the segmentation results.
Let's take `blogs_ko` samples as examples, and compare performance of each library.
For this, I will take the best backend of each library (Kss=mecab, Koalanlp=KKMA), because looking results of all backends may make you tired.

#### Example 1
- Input text
```
거제 내려가는 길에 휴게소를 들렸는데 새로 생겼나보더라구요!? 남편과 저, 둘 다 빵러버라 지나칠 수 없어 구매해 먹어봤답니당😊 보성녹차휴게소 안으로 들어오시면 딱 가운데 위치해 있어요ㅎㅎ 그래서 어느 문으로라도 들어오셔도 가깝답니다😉 메뉴판을 이렇고, 가격은 2000원~3000원 사이에 형성 되어 있어요! 이런거 하나하나 맛보는거 너무 좋아하는데... 진정하고 소미미 단팥빵 하나, 옥수수 치즈빵 하나, 구리볼 하나 골랐습니다! 다음에 가면 강낭콩이랑 밤 꼭 먹어봐야겠어요😙
```
- Label
```
거제 내려가는 길에 휴게소를 들렸는데 새로 생겼나보더라구요!?
남편과 저, 둘 다 빵러버라 지나칠 수 없어 구매해 먹어봤답니당😊
보성녹차휴게소 안으로 들어오시면 딱 가운데 위치해 있어요ㅎㅎ
그래서 어느 문으로라도 들어오셔도 가깝답니다😉
메뉴판을 이렇고, 가격은 2000원~3000원 사이에 형성 되어 있어요!
이런거 하나하나 맛보는거 너무 좋아하는데... 진정하고 소미미 단팥빵 하나, 옥수수 치즈빵 하나, 구리볼 하나 골랐습니다!
다음에 가면 강낭콩이랑 밤 꼭 먹어봐야겠어요😙
```
- Source

[https://hi-e2e2.tistory.com/193](https://hi-e2e2.tistory.com/193)

- Output texts
```
Baseline:

거제 내려가는 길에 휴게소를 들렸는데 새로 생겼나보더라구요!?
남편과 저, 둘 다 빵러버라 지나칠 수 없어 구매해 먹어봤답니당😊 보성녹차휴게소 안으로 들어오시면 딱 가운데 위치해 있어요ㅎㅎ 그래서 어느 문으로라도 들어오셔도 가깝답니다😉 메뉴판을 이렇고, 가격은 2000원~3000원 사이에 형성 되어 있어요!
이런거 하나하나 맛보는거 너무 좋아하는데...
진정하고 소미미 단팥빵 하나, 옥수수 치즈빵 하나, 구리볼 하나 골랐습니다!
다음에 가면 강낭콩이랑 밤 꼭 먹어봐야겠어요😙
```

Baseline separates input text into 5 sentences. First of all, the first sentence was separated well because it has final symbols. However, since these final symbols don't appear from the second sentence, you can see that these sentences were not separated well.

```
Koalanlp (KKMA):

거제 내려가는 길에 휴게 소를 들렸는데 새로 생겼나
보더라구요!?
남편과 저, 둘 다 빵 러버라 지나칠 수 없어 구매해 먹어 봤답니당
😊 보성 녹차 휴게소 안으로 들어오시면 딱 가운데 위치해 있어요
ㅎㅎ 그래서 어느 문으로 라도 들어오셔도 가깝답니다
😉 메뉴판을 이렇고, 가격은 2000원 ~3000 원 사이에 형성 되어 있어요!
이런 거 하나하나 맛보는 거 너무 좋아하는데... 진정하고 소미 미 단팥빵 하나, 옥수수 치즈 빵 하나, 구리 볼 하나 골랐습니다!
다음에 가면 강낭콩이랑 밤 꼭 먹어봐야겠어요😙
```

Koalanlp splits sentences better than baseline because it uses morphological information. It splits input text into 8 sentences in total.
But many mispartitions still exist. The first thing that catches your eye is the immature emoji handling.
People usually put emojis at the end of a sentence, and in this case, the emojis should be included in the sentence.
The second thing is the mispartition between `생겼나` and `보더라구요!?`. 
Probably this is because the KKMA morpheme analyzer recognized `생겼나` as a final eomi (종결어미). but it's a connecting eomi (연결어미).
This is because the performance of the morpheme analyzer. Rather, the baseline is a little safer in this area.

```
Kiwi:

거제 내려가는 길에 휴게소를 들렸는데 새로 생겼나보더라구요!?
남편과 저, 둘 다 빵러버라 지나칠 수 없어 구매해 먹어봤답니당😊
보성녹차휴게소 안으로 들어오시면 딱 가운데 위치해 있어요ㅎㅎ
그래서 어느 문으로라도 들어오셔도 가깝답니다😉 메뉴판을 이렇고, 가격은 2000원~3000원 사이에 형성 되어 있어요!
이런거 하나하나 맛보는거 너무 좋아하는데...
진정하고 소미미 단팥빵 하나, 옥수수 치즈빵 하나, 구리볼 하나 골랐습니다!
다음에 가면 강낭콩이랑 밤 꼭 먹어봐야겠어요😙
```
Kiwi shows better performance than Koalanlp. It splits input text into 7 sentences. 
Most sentences are pretty good, but it doesn't split `가깝답니다😉` and `메뉴판을`.
The second thing is it separates `좋아하는데...` and `진정하고`.
This part may be recognized as an independent sentence depending on the viewer, 
but the author of the original article didn't write this as an independent sentence, but an embraced sentence (안긴문장).

The [original article](https://hi-e2e2.tistory.com/193) was written like:
    
![](https://github.com/hyunwoongko/kss/blob/main/assets/example_1_1.png)

```
Kss (mecab):

거제 내려가는 길에 휴게소를 들렸는데 새로 생겼나보더라구요!?
남편과 저, 둘 다 빵러버라 지나칠 수 없어 구매해 먹어봤답니당😊
보성녹차휴게소 안으로 들어오시면 딱 가운데 위치해 있어요ㅎㅎ
그래서 어느 문으로라도 들어오셔도 가깝답니다😉
메뉴판을 이렇고, 가격은 2000원~3000원 사이에 형성 되어 있어요!
이런거 하나하나 맛보는거 너무 좋아하는데... 진정하고 소미미 단팥빵 하나, 옥수수 치즈빵 하나, 구리볼 하나 골랐습니다!
다음에 가면 강낭콩이랑 밤 꼭 먹어봐야겠어요😙
```
The result of Kss is same with gold label. Especially it succesfully separates `가깝답니다😉` and `메뉴판을`. In fact, this part is the final eomi (종결어미), but many morpheme analyzers confuse the final eomi (종결어미) with the connecting eomi (연결어미). Actually, mecab and pecab morpheme analyzers which are backend of Kss also recognizes that part as a connecting eomi (연결어미). For this reason, Kss has a feature to recognize wrongly recognized connecting eomi (연결어미) and to correct those eomis. Thus, it is able to separate this part effectively. Next, Kss doesn't split `좋아하는데...` and `진정하고` becuase `좋아하는데...` is not an independent sentence, but an embraced sentence (안긴문장). This means Kss doesn't split sentences simply because `. ` appears, unlike baseline. In most cases, `. ` could be the delimiter of sentences, actually there are many exceptions about this.

#### Example 2
- Input text
```
어느화창한날 출근전에 너무일찍일어나 버렸음 (출근시간 19시) 할꺼도없고해서 카페를 찾아 시내로 나갔음 새로생긴곳에 사장님이 커피선수인지 커피박사라고 해서 갔음 오픈한지 얼마안되서 그런지 손님이 얼마없었음 조용하고 좋다며 좋아하는걸시켜서 테라스에 앉음 근데 조용하던 카페가 산만해짐 소리의 출처는 카운터였음(테라스가 카운터 바로옆) 들을라고 들은게 아니라 귀는 열려있으니 듣게된 대사.
```
- Label
```
어느화창한날 출근전에 너무일찍일어나 버렸음 (출근시간 19시)
할꺼도없고해서 카페를 찾아 시내로 나갔음
새로생긴곳에 사장님이 커피선수인지 커피박사라고 해서 갔음
오픈한지 얼마안되서 그런지 손님이 얼마없었음
조용하고 좋다며 좋아하는걸시켜서 테라스에 앉음
근데 조용하던 카페가 산만해짐
소리의 출처는 카운터였음(테라스가 카운터 바로옆)
들을라고 들은게 아니라 귀는 열려있으니 듣게된 대사.
```
- Source

[https://mrsign92.tistory.com/6099371](https://mrsign92.tistory.com/6099371)

- Output texts
```
Baseline:

어느화창한날 출근전에 너무일찍일어나 버렸음 (출근시간 19시) 할꺼도없고해서 카페를 찾아 시내로 나갔음 새로생긴곳에 사장님이 커피선수인지 커피박사라고 해서 갔음 오픈한지 얼마안되서 그런지 손님이 얼마없었음 조용하고 좋다며 좋아하는걸시켜서 테라스에 앉음 근데 조용하던 카페가 산만해짐 소리의 출처는 카운터였음(테라스가 카운터 바로옆) 들을라고 들은게 아니라 귀는 열려있으니 듣게된 대사.
```

Baseline doesn't split any sentences because there's no `.!? ` in the input text.

```
Koalanlp (KKMA)

어느 화창한 날 출근 전에 너무 일찍 일어나 버렸음 ( 출근시간 19시) 할 꺼도 없고 해서 카페를 찾아 시내로 나갔음 새로 생긴 곳에 사장님이 커피선수인지 커피박사라고 해서 갔음 오픈한지 얼마 안 되 서 그런지 손님이 얼마 없었음 조용하고 좋다며 좋아하는 걸 시켜서 테라스에 앉음 근데 조용하던 카페가 산만 해짐 소리의 출처는 카운터였음( 테라스가 카운터 바로 옆) 들을라고
들은 게 아니라 귀는 열려 있으니 듣게 된 대사.
```

Koalanlp separates `들을라고` and `들은` but it is not correct split point.
And I think it doesn't consider predicative use of eomi transferred from noun (명사형 전성어미의 서술적 용법).

```
Kiwi

어느화창한날 출근전에 너무일찍일어나 버렸음 (출근시간 19시) 할꺼도없고해서 카페를 찾아 시내로 나갔음 새로생긴곳에 사장님이 커피선수인지 커피박사라고 해서 갔음 오픈한지 얼마안되서 그런지 손님이 얼마없었음 조용하고 좋다며 좋아하는걸시켜서 테라스에 앉음 근데 조용하던 카페가 산만해짐 소리의 출처는 카운터였음(테라스가 카운터 바로옆) 들을라고 들은게 아니라 귀는 열려있으니 듣게된 대사.
```
Kiwi doesn't separate any sentence, similar with baseline.
Similarly, it doesn't consider predicative use of eomi transferred from noun (명사형 전성어미의 서술적 용법).

```
Kss (Mecab)

어느화창한날 출근전에 너무일찍일어나 버렸음 (출근시간 19시)
할꺼도없고해서 카페를 찾아 시내로 나갔음
새로생긴곳에 사장님이 커피선수인지 커피박사라고 해서 갔음
오픈한지 얼마안되서 그런지 손님이 얼마없었음
조용하고 좋다며 좋아하는걸시켜서 테라스에 앉음
근데 조용하던 카페가 산만해짐 소리의 출처는 카운터였음(테라스가 카운터 바로옆)
들을라고 들은게 아니라 귀는 열려있으니 듣게된 대사.
```
The result of Kss is very similar with gold label, Kss considers predicative use of eomi transferred from noun (명사형 전성어미의 서술적 용법).
But Kss couldn't split `산만해짐` and `소리의`. That part is a correct split point, but it was blocked by one of the exceptions which I built to prevent wrong segmentation. Splitting eomi transferred from noun (명사형 전성어미) is one of the unsafe and difficult tasks, so Kss has many exceptions to prevent wrong segmentation.

#### Example 3
- Input text
```
책소개에 이건 소설인가 실제인가라는 문구를 보고 재밌겠다 싶어 보게 되었다. '바카라'라는 도박은 2장의 카드 합이 높은 사람이 이기는 게임으로 아주 단순한 게임이다. 이런게 중독이 되나? 싶었는데 이 책이 바카라와 비슷한 매력이 있다 생각들었다. 내용이 스피드하게 진행되고 막히는 구간없이 읽히는게 나도 모르게 페이지를 슥슥 넘기고 있었다. 물론 읽음으로써 큰 돈을 벌진 않지만 이런 스피드함에 나도 모르게 계속 게임에 참여하게 되고 나오는 타이밍을 잡지 못해 빠지지 않았을까? 라는 생각을 하게 됐다. 이 책에서 현지의 꿈은 가격표를 보지 않는 삶이라 한다. 이 부분을 읽고 나돈데! 라는 생각하면서 순간 도박이라는걸로라도 돈을 많이 벌었던 현지가 부러웠다. 그러면서 내가 도박을 했다면?라는 상상을 해봤다. 그리고 이런 상상을 할 수 있게 만들어줘서 이 책이 더 재밌게 다가왔다. 일상에 지루함을 느껴 도박같은 삶을 살고싶다면 도박하지말고 차라리 이 책을 보길^^ㅋ 
```
- Label
```
책소개에 이건 소설인가 실제인가라는 문구를 보고 재밌겠다 싶어 보게 되었다.
'바카라'라는 도박은 2장의 카드 합이 높은 사람이 이기는 게임으로 아주 단순한 게임이다.
이런게 중독이 되나? 싶었는데 이 책이 바카라와 비슷한 매력이 있다 생각들었다.
내용이 스피드하게 진행되고 막히는 구간없이 읽히는게 나도 모르게 페이지를 슥슥 넘기고 있었다.
물론 읽음으로써 큰 돈을 벌진 않지만 이런 스피드함에 나도 모르게 계속 게임에 참여하게 되고 나오는 타이밍을 잡지 못해 빠지지 않았을까? 라는 생각을 하게 됐다.
이 책에서 현지의 꿈은 가격표를 보지 않는 삶이라 한다.
이 부분을 읽고 나돈데! 라는 생각하면서 순간 도박이라는걸로라도 돈을 많이 벌었던 현지가 부러웠다.
그러면서 내가 도박을 했다면?라는 상상을 해봤다.
그리고 이런 상상을 할 수 있게 만들어줘서 이 책이 더 재밌게 다가왔다.
일상에 지루함을 느껴 도박같은 삶을 살고싶다면 도박하지말고 차라리 이 책을 보길^^ㅋ 
```
- Source

[https://hi-e2e2.tistory.com/63](https://hi-e2e2.tistory.com/63)

- Output texts
```
Baseline:

책소개에 이건 소설인가 실제인가라는 문구를 보고 재밌겠다 싶어 보게 되었다.
'바카라'라는 도박은 2장의 카드 합이 높은 사람이 이기는 게임으로 아주 단순한 게임이다.
이런게 중독이 되나?
싶었는데 이 책이 바카라와 비슷한 매력이 있다 생각들었다.
내용이 스피드하게 진행되고 막히는 구간없이 읽히는게 나도 모르게 페이지를 슥슥 넘기고 있었다.
물론 읽음으로써 큰 돈을 벌진 않지만 이런 스피드함에 나도 모르게 계속 게임에 참여하게 되고 나오는 타이밍을 잡지 못해 빠지지 않았을까?
라는 생각을 하게 됐다.
이 책에서 현지의 꿈은 가격표를 보지 않는 삶이라 한다.
이 부분을 읽고 나돈데!
라는 생각하면서 순간 도박이라는걸로라도 돈을 많이 벌었던 현지가 부러웠다.
그러면서 내가 도박을 했다면?라는 상상을 해봤다.
그리고 이런 상상을 할 수 있게 만들어줘서 이 책이 더 재밌게 다가왔다.
일상에 지루함을 느껴 도박같은 삶을 살고싶다면 도박하지말고 차라리 이 책을 보길^^ㅋ 
```

Baseline separates input text into 13 sentences. You can see it can't distinguish final eomi(종결어미) and connecting eomi(연결어미), for example it splits `이런게 중독이 되나?` and `싶었는데`. But `되나?` is connecting eomi (연결어미). And here's one more problem. It doesn't recognize embraced sentences (안긴문장). For example it splits `못해 빠지지 않았을까?` and `라는 생각을 하게 됐다.`.
```
Koalanlp (KKMA)

책 소개에 이건 소설인가 실제 인가라는 문구를 보고 재밌겠다 싶어 보게 되었다.
' 바카라' 라는 도박은 2 장의 카드 합이 높은 사람이 이기는 게임으로 아주 단순한 게임이다.
이런 게 중독이 되나?
싶었는데 이 책이 바카라와 비슷한 매력이 있다 생각 들었다.
내용이 스피드하게 진행되고 막히는 구간 없이 읽히는 게 나도 모르게 페이지를 슥슥 넘기고 있었다.
물론 읽음으로써 큰 돈을 벌진 않지만 이런 스피드함에 나도 모르게 계속 게임에 참여하게 되고 나오는 타이밍을 잡지 못해 빠지지 않았을까?
라는 생각을 하게 됐다.
이 책에서 현지의 꿈은 가격표를 보지 않는 삶이라 한다.
이 부분을 읽고 나돈데!
라는 생각하면서 순간 도박이라는 걸로라도 돈을 많이 벌었던 현지가 부러웠다.
그러면서 내가 도박을 했다면? 라는 상상을 해봤다.
그리고 이런 상상을 할 수 있게 만들어 줘서 이 책이 더 재밌게 다가왔다.
일상에 지루함을 느껴 도박 같은 삶을 살고 싶다면 도박하지 말고 차라리 이 책을 보길 ^^ ㅋ
```

The result of Koalanlp was really similar with baseline, the two problems (final-connecting eomi distinction, embracing sentences recognization) still exist.
```
Kiwi

책소개에 이건 소설인가 실제인가
라는 문구를 보고 재밌겠다 싶어 보게 되었다.
'바카라'라는 도박은 2장의 카드 합이 높은 사람이 이기는 게임으로 아주 단순한 게임이다.
이런게 중독이 되나?
싶었는데 이 책이 바카라와 비슷한 매력이 있다 생각들었다.
내용이 스피드하게 진행되고 막히는 구간없이 읽히는게 나도 모르게 페이지를 슥슥 넘기고 있었다.
물론 읽음으로써 큰 돈을 벌진 않지만 이런 스피드함에 나도 모르게 계속 게임에 참여하게 되고 나오는 타이밍을 잡지 못해 빠지지 않았을까?
라는 생각을 하게 됐다.
이 책에서 현지의 꿈은 가격표를 보지 않는 삶이라 한다.
이 부분을 읽고 나돈데!
라는 생각하면서 순간 도박이라는걸로라도 돈을 많이 벌었던 현지가 부러웠다.
그러면서 내가 도박을 했다면?
라는 상상을 해봤다.
그리고 이런 상상을 할 수 있게 만들어줘서 이 책이 더 재밌게 다가왔다.
일상에 지루함을 느껴 도박같은 삶을 살고싶다면 도박하지말고 차라리 이 책을 보길^^ㅋ
```
The two problems are also shown in result of Kiwi. And it additionally splits `실제인가` and `라는`, but `이건 소설인가 실제인가` is not an independent sentence, but an embraced sentence (안긴문장).

```
Kss (Mecab)

책소개에 이건 소설인가 실제인가라는 문구를 보고 재밌겠다 싶어 보게 되었다.
'바카라'라는 도박은 2장의 카드 합이 높은 사람이 이기는 게임으로 아주 단순한 게임이다.
이런게 중독이 되나? 싶었는데 이 책이 바카라와 비슷한 매력이 있다 생각들었다.
내용이 스피드하게 진행되고 막히는 구간없이 읽히는게 나도 모르게 페이지를 슥슥 넘기고 있었다.
물론 읽음으로써 큰 돈을 벌진 않지만 이런 스피드함에 나도 모르게 계속 게임에 참여하게 되고 나오는 타이밍을 잡지 못해 빠지지 않았을까? 라는 생각을 하게 됐다.
이 책에서 현지의 꿈은 가격표를 보지 않는 삶이라 한다.
이 부분을 읽고 나돈데! 라는 생각하면서 순간 도박이라는걸로라도 돈을 많이 벌었던 현지가 부러웠다.
그러면서 내가 도박을 했다면?라는 상상을 해봤다.
그리고 이런 상상을 할 수 있게 만들어줘서 이 책이 더 재밌게 다가왔다.
일상에 지루함을 느껴 도박같은 삶을 살고싶다면 도박하지말고 차라리 이 책을 보길^^ㅋ
```
The result of Kss is same with gold label. This means that Kss considers the two problems. Of course, it's not easy to detect that parts while splitting sentences, so Kss has one more step after splitting sentences. It's postprocessing step which corrects some problems in segmenration results. For example, Korean sentence doesn't start from josa (조사) in general. Therefore if segmented results (sentences) started from josa (조사), Kss recognizes them as embraced sentences (안긴문장), and attaches them to their previous sentence. For your information, Kss has many more powerful postprocessing algorithms which correct wrong segmentation results like this.

In conclusion, Kss considers more than other libraries in Korean sentences. And these considerations led to difference in performance.

#### 6) Speed analysis
I also measured speed of tools to compare their computation efficiency. The following table shows computation time of each tool when it splits `sample.txt` (41 sentences).
It is a single blog post, so you can expect the following time when you split a blog post into sentences.
Since the computation time may vary depending on the current CPU status, so I measured 5 times and calculated the average.
Note that every experiment was conducted on single thread / process environment with my M1 macbook pro (2021, 13'inch).

| Name           | Library version | Backend | Average time (msec) |
|----------------|-----------------|---------|---------------------|
| Baseline       | N/A             | N/A     | **0.22**            |
| koalanlp       | 2.1.7           | OKT     | 27.37               |
| koalanlp       | 2.1.7           | HNN     | 50.39               |
| koalanlp       | 2.1.7           | KMR     | 757.08              |
| koalanlp       | 2.1.7           | RHINO   | 978.53              |
| koalanlp       | 2.1.7           | EUNJEON | 881.24              |
| koalanlp       | 2.1.7           | ARIRANG | 1415.53             |
| koalanlp       | 2.1.7           | KKMA    | 1971.31             |
| Kiwi           | 0.14.0          | N/A     | 36.41               |
| **Kss (ours)** | 4.0.0           | pecab   | 6929.27             |
| **Kss (ours)** | 4.0.0           | mecab   | 43.80               |

You can also compare the speed of tools with the following graphs.

![](https://github.com/hyunwoongko/kss/blob/main/assets/average_computation_time.png)

You can also compare the speed of faster tools the following graphs (under 100 msec).

![](https://github.com/hyunwoongko/kss/blob/main/assets/average_computation_time_under_100.png)

The baseline was fastest (because it's a just regex function), and Koalanlp (OKT backend), Kiwi, Kss (mecab backend) followed.
The slowest library was Kss (pecab backend) and it was about 160 times slower than its mecab backend.
Mecab and Kiwi were written in C++, All Koalanlp backends were written in Java and Pecab was written in pure python.
I think this difference was caused by speed of each language. Therefore, if you can install mecab, it makes most sense to use Kss Mecab backend.

- For Linux/MacOS users: Kss tries to install [`python-mecab-kor`](https://github.com/hyunwoongko/python-mecab-kor) when you install kss. so you can use mecab backend very easily.
But if it was failed, please install mecab yourself to use mecab backend.


- For Windows users: Kss supports [`mecab-ko-msvc`](https://github.com/Pusnow/mecab-ko-msvc) (mecab for Microsoft Visual C++), and its konlpy wrapper.
To use mecab backend, you need to install one of mecab and konlpy.tag.Mecab on your machine.
There are much information about mecab installing on Windows machine in internet like the following.
  - mecab: https://cleancode-ws.tistory.com/97
  - konlpy.tag.Mecab: https://uwgdqo.tistory.com/363

<br>

#### 7) Conclusion
I've measured the performance of Kss and other libraries using 6 evaluation datasets, and also measured their speed.
In terms of segmentation performance, Kss performed best on most datasets. In terms of speed, baseline was the fastest, and Koalanlp (OKT backend) and Kiwi followed. 
but Kss (mecab backend) also showed a speed that could compete with others.

Although much progress has been made by Kiwi and Kss, there are still many difficulties and limitations in Korean sentence segmentation libraries. In fact, it's also because very few people attack this task. If anyone wants to discuss Korean sentence segmentation algorithms with me or contribute to my work, feel free to send an email to kevin.ko@tunib.ai or let me know on the Github [issue](https://github.com/hyunwoongko/kss/issues) page.

</details>

<br>

#### 2) `split_morphemes`: split text into morphemes

```python
from kss import split_morphemes

split_morphemes(
    text: Union[str, List[str], Tuple[str]],
    backend: str = "auto",
    num_workers: Union[int, str] = "auto",
    drop_space: bool = True,
)
```

<details>
<summary>Parameters</summary>

- **text: String or List/Tuple of strings**
    - string: single text segmentation
    - list/tuple of strings: batch texts segmentation
- **backend: Morpheme analyzer backend.**
    - `backend='auto'`: find `mecab` → `konlpy.tag.Mecab` → `pecab` and use first found analyzer (default)
    - `backend='mecab'`: find `mecab` → `konlpy.tag.Mecab` and use first found analyzer
    - `backend='pecab'`: use `pecab` analyzer
- **num_workers: The number of multiprocessing workers**
    - `num_workers='auto'`: use multiprocessing with the maximum number of workers if possible (default)
    - `num_workers=1`: don't use multiprocessing
    - `num_workers=2~N`: use multiprocessing with the specified number of workers
- **drop_space: Whether it drops all space characters or not**
    - `drop_space=True`: drop all space characters in output (default)
    - `drop_space=False`: remain all space characters in output

</details>

<details>
<summary>Usages</summary>

- Single text segmentation
  ```python
  import kss

  text = "회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요 다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다 강남역 맛집 토끼정의 외부 모습."

  kss.split_morphemes(text)
  # [('회사', 'NNG'), ('동료', 'NNG'), ('분', 'NNB'), ('들', 'XSN'), ('과', 'JKB'), ('다녀왔', 'VV+EP'), ('는데', 'EC'), ('분위기', 'NNG'), ('도', 'JX'), ('좋', 'VA'), ('고', 'EC'), ('음식', 'NNG'), ('도', 'JX'), ('맛있', 'VA'), ('었', 'EP'), ('어요', 'EF'), ('다만', 'MAJ'), (',', 'SC'), ('강남', 'NNP'), ('토끼', 'NNG'), ('정', 'NNG'), ('이', 'JKS'), ('강남', 'NNP'), ('쉑쉑', 'MAG'), ('버거', 'NNG'), ('골목길', 'NNG'), ('로', 'JKB'), ('쭉', 'MAG'), ('올라가', 'VV'), ('야', 'EC'), ('하', 'VV'), ('는데', 'EC'), ('다', 'MAG'), ('들', 'XSN'), ('쉑쉑', 'MAG'), ('버거', 'NNG'), ('의', 'JKG'), ('유혹', 'NNG'), ('에', 'JKB'), ('넘어갈', 'VV+ETM'), ('뻔', 'NNB'), ('했', 'VV+EP'), ('답니다', 'EC'), ('강남역', 'NNP'), ('맛집', 'NNG'), ('토끼', 'NNG'), ('정의', 'NNG'), ('외부', 'NNG'), ('모습', 'NNG'), ('.', 'SF')]
  ```

- Batch texts segmentation
  ```python
  import kss

  texts = [
      "회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요 다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다",
      "강남역 맛집 토끼정의 외부 모습. 강남 토끼정은 4층 건물 독채로 이루어져 있습니다.",
      "역시 토끼정 본 점 답죠?ㅎㅅㅎ 건물은 크지만 간판이 없기 때문에 지나칠 수 있으니 조심하세요 강남 토끼정의 내부 인테리어.",
  ]

  kss.split_morphemes(texts)
  # [[('회사', 'NNG'), ('동료', 'NNG'), ('분', 'NNB'), ('들', 'XSN'), ('과', 'JKB'), ('다녀왔', 'VV+EP'), ('는데', 'EC'), ('분위기', 'NNG'), ('도', 'JX'), ('좋', 'VA'), ('고', 'EC'), ('음식', 'NNG'), ('도', 'JX'), ('맛있', 'VA'), ('었', 'EP'), ('어요', 'EF'), ('다만', 'MAJ'), (',', 'SC'), ('강남', 'NNP'), ('토끼', 'NNG'), ('정', 'NNG'), ('이', 'JKS'), ('강남', 'NNP'), ('쉑쉑', 'MAG'), ('버거', 'NNG'), ('골목길', 'NNG'), ('로', 'JKB'), ('쭉', 'MAG'), ('올라가', 'VV'), ('야', 'EC'), ('하', 'VV'), ('는데', 'EC'), ('다', 'MAG'), ('들', 'XSN'), ('쉑쉑', 'MAG'), ('버거', 'NNG'), ('의', 'JKG'), ('유혹', 'NNG'), ('에', 'JKB'), ('넘어갈', 'VV+ETM'), ('뻔', 'NNB'), ('했', 'VV+EP'), ('답니다', 'EC')], 
  # [('강남역', 'NNP'), ('맛집', 'NNG'), ('토끼', 'NNG'), ('정의', 'NNG'), ('외부', 'NNG'), ('모습', 'NNG'), ('.', 'SF'), ('강남', 'NNP'), ('토끼', 'NNG'), ('정은', 'NNP'), ('4', 'SN'), ('층', 'NNG'), ('건물', 'NNG'), ('독채', 'NNG'), ('로', 'JKB'), ('이루어져', 'VV+EC'), ('있', 'VX'), ('습니다', 'EF'), ('.', 'SF')], 
  # [('역시', 'MAJ'), ('토끼', 'NNG'), ('정', 'NNG'), ('본', 'VV+ETM'), ('점', 'NNB'), ('답', 'MAG+VCP'), ('죠', 'EF'), ('?', 'SF'), ('ㅎ', 'IC'), ('ㅅ', 'NNG'), ('ㅎ', 'IC'), ('건물', 'NNG'), ('은', 'JX'), ('크', 'VA'), ('지만', 'EC'), ('간판', 'NNG'), ('이', 'JKS'), ('없', 'VA'), ('기', 'ETN'), ('때문', 'NNB'), ('에', 'JKB'), ('지나칠', 'VV+ETM'), ('수', 'NNB'), ('있', 'VV'), ('으니', 'EC'), ('조심', 'NNG'), ('하', 'XSV'), ('세요', 'EP+EF'), ('강남', 'NNP'), ('토끼', 'NNG'), ('정의', 'NNG'), ('내부', 'NNG'), ('인테리어', 'NNG'), ('.', 'SF')]]
  ```

- Remain space characters for original text recoverability
  ```python
  import kss
  
  text = "회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요\n다만,\t강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다 강남역 맛집 토끼정의 외부 모습."

  kss.split_morphemes(text, drop_space=False)
  # [('회사', 'NNG'), (' ', 'SP'), ('동료', 'NNG'), (' ', 'SP'), ('분', 'NNB'), ('들', 'XSN'), ('과', 'JKB'), (' ', 'SP'), ('다녀왔', 'VV+EP'), ('는데', 'EC'), (' ', 'SP'), ('분위기', 'NNG'), ('도', 'JX'), (' ', 'SP'), ('좋', 'VA'), ('고', 'EC'), (' ', 'SP'), ('음식', 'NNG'), ('도', 'JX'), (' ', 'SP'), ('맛있', 'VA'), ('었', 'EP'), ('어요', 'EF'), ('\n', 'SP'), ('다만', 'MAJ'), (',', 'SC'), ('\t', 'SP'), ('강남', 'NNP'), (' ', 'SP'), ('토끼', 'NNG'), ('정', 'NNG'), ('이', 'JKS'), (' ', 'SP'), ('강남', 'NNP'), (' ', 'SP'), ('쉑쉑', 'MAG'), ('버거', 'NNG'), (' ', 'SP'), ('골목길', 'NNG'), ('로', 'JKB'), (' ', 'SP'), ('쭉', 'MAG'), (' ', 'SP'), ('올라가', 'VV'), ('야', 'EC'), (' ', 'SP'), ('하', 'VV'), ('는데', 'EC'), (' ', 'SP'), ('다', 'MAG'), ('들', 'XSN'), (' ', 'SP'), ('쉑쉑', 'MAG'), ('버거', 'NNG'), ('의', 'JKG'), (' ', 'SP'), ('유혹', 'NNG'), ('에', 'JKB'), (' ', 'SP'), ('넘어갈', 'VV+ETM'), (' ', 'SP'), ('뻔', 'NNB'), (' ', 'SP'), ('했', 'VV+EP'), ('답니다', 'EC'), (' ', 'SP'), ('강남역', 'NNP'), (' ', 'SP'), ('맛집', 'NNG'), (' ', 'SP'), ('토끼', 'NNG'), ('정의', 'NNG'), (' ', 'SP'), ('외부', 'NNG'), (' ', 'SP'), ('모습', 'NNG'), ('.', 'SF')]
  ```

</details>

<br>

## Kss in various programming languages
Kss is available in various programming languages.
- [Kss Python version](https://github.com/hyunwoongko/kss)
- [Kss Java version](https://github.com/sangdee/kss-java)
- [Kss Flutter version](https://github.com/khjde1207/kss_dart)
- [Kss C++ version](https://github.com/likejazz/korean-sentence-splitter)

## Citation
If you find this toolkit useful, please consider citing:
```
@misc{kss,
  author       = {Ko, Hyunwoong and Park, Sang-kil},
  title        = {Kss: A Toolkit for Korean sentence segmentation},
  howpublished = {\url{https://github.com/hyunwoongko/kss}},
  year         = {2021},
}
```

## License
Kss project is licensed under the terms of the BSD 3-Clause "New" or "Revised" License.

Copyright 2021 [Hyunwoong Ko](https://github.com/hyunwoongko) and [Sang-kil Park](https://github.com/likejazz). All Rights Reserved.

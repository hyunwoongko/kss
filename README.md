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
You can reproduce all the following results using source code and datasets in `./bench/` directory and the source code was copied from [here](https://github.com/bab2min/kiwipiepy/tree/main/benchmark/sentence_split).
Note that the `Baseline` is regex based segmentation method (`re.split(r"(?<=[.!?])\s", text)`).

| Name                                             | Command (in root directory)                                                                               |
|--------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| Baseline                                         | `python3 ./bench/test_baseline.py ./bench/testset/*.txt`                                                  |
| [Kiwi](https://github.com/bab2min/kiwipiepy)     | `python3 ./bench/test_kiwi.py ./bench/testset/*.txt`                                                      |
| [Koalanlp](https://github.com/koalanlp/koalanlp) | `python3 ./bench/test_koalanlp.py ./bench/testset/*.txt --backend=OKT/HNN/KMR/RHINO/EUNJEON/ARIRANG/KKMA` |
| [Kss](https://github.com/hyunwoongko/kss) (ours) | `python3 ./bench/test_kss.py ./bench/testset/*.txt --backend=mecab/pecab`                                 |

<br>

#### 2) Evaluation datasets:

I used the following 7 evaluation datasets for the follwing experiments. Thanks to [Minchul Lee](https://github.com/bab2min) for creating various sentence segmentation datasets.

| Name                                                                                  | Descriptions                                                                              | The number of sentences | Creator                                                                                                                                                                                                                                                            |
|---------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [blogs_lee](https://github.com/hyunwoongko/kss/blob/main/bench/testset/blogs_lee.txt) | Dataset for testing blog style text segmentation                                          | 170                     | [Minchul Lee](https://github.com/bab2min/kiwipiepy/tree/main/benchmark/sentence_split)                                                                                                                                                                             |
| [blogs_ko](https://github.com/hyunwoongko/kss/blob/main/bench/testset/blogs_ko.txt)   | Dataset for testing blog style text segmentation, which is harder than Lee's blog dataset | 346                     | [Hyunwoong Ko](https://github.com/hyunwoongko)                                                                                                                                                                                                                     |
| [sample](https://github.com/hyunwoongko/kss/blob/main/bench/testset/sample.txt)       | An example used in README.md (강남 토끼정)                                                     | 41                      | [Isaac](http://semantics.kr/%ed%95%9c%ea%b5%ad%ec%96%b4-%ed%98%95%ed%83%9c%ec%86%8c-%eb%b6%84%ec%84%9d%ea%b8%b0-%eb%b3%84-%eb%ac%b8%ec%9e%a5-%eb%b6%84%eb%a6%ac-%ec%84%b1%eb%8a%a5%eb%b9%84%ea%b5%90/), modified by [Hyunwoong Ko](https://github.com/hyunwoongko) |
| [tweets](https://github.com/hyunwoongko/kss/blob/main/bench/testset/tweets.txt)       | Dataset for testing tweeter style text segmentation                                       | 178                     | [Minchul Lee](https://github.com/bab2min/kiwipiepy/tree/main/benchmark/sentence_split)                                                                                                                                                                             |
| [wikipedia](https://github.com/hyunwoongko/kss/blob/main/bench/testset/wikipedia.txt) | Dataset for testing wikipedia style text segmentation                                     | 326                     | [Hyunwoong Ko](https://github.com/hyunwoongko)                                                                                                                                                                                                                     |
| [nested](https://github.com/hyunwoongko/kss/blob/main/bench/testset/nested.txt)       | Dataset for testing text which have parentheses and quotation marks segmentation          | 91                      | [Minchul Lee](https://github.com/bab2min/kiwipiepy/tree/main/benchmark/sentence_split)                                                                                                                                                                             |
| [v_ending](https://github.com/hyunwoongko/kss/blob/main/bench/testset/v_ending.txt)   | Dataset for testing difficult eomi segmentation, it contains various dialect sentences    | 30                      | [Minchul Lee](https://github.com/bab2min/kiwipiepy/tree/main/benchmark/sentence_split)                                                                                                                                                                             |

Note that I modified labels of two sentences in `sample.txt` made by [Issac](http://semantics.kr/%ed%95%9c%ea%b5%ad%ec%96%b4-%ed%98%95%ed%83%9c%ec%86%8c-%eb%b6%84%ec%84%9d%ea%b8%b0-%eb%b3%84-%eb%ac%b8%ec%9e%a5-%eb%b6%84%eb%a6%ac-%ec%84%b1%eb%8a%a5%eb%b9%84%ea%b5%90/)
because the [original blog post](https://blog.naver.com/jully1211/221437777873) was written like the following:

<img width=1000px src="https://github.com/hyunwoongko/kss/blob/main/assets/rabbit_1.png">

<img width=1000px src="https://github.com/hyunwoongko/kss/blob/main/assets/rabbit_2.png">

But Issac's labels were:

<img width=500px src="https://github.com/hyunwoongko/kss/blob/main/assets/issac.png">

In fact, `사실 전 고기를 안 먹어서 무슨 맛인지 모르겠지만..` and `(물론 전 안 먹었지만` are embraced sentences (안긴문장), not independent sentences. So sentence segmentation tools should do not split that parts.
    
<br>

#### 3) Sentence segmentation performance (Quantitative Analysis)
 
The following tables show the segmentation performance based on **Exact Match (EM)**, **F1 score (F1)** and **Normalized F1 score (NF1)**.

- **EM score**: This only gives score when the output predictions are exactly the same with gold labels. This could be useful, but too harsh and clunky.

| Name           | Library version | Backend | blogs_lee (EM) | blogs_ko (EM) | sample (EM) | tweets (EM) | wikipedia (EM) | nested (EM) | v_ending (EM) | Average (EM) |
|----------------|-----------------|---------|----------------|---------------|-------------|-------------|----------------|-------------|---------------|--------------|
| Baseline       | N/A             | N/A     | 0.53529        | 0.43642       | 0.34146     | 0.51124     | 0.66258        | 0.68132     | 0.00000       | 0.45261      |
| Koalanlp       | 2.1.7           | OKT     | 0.53529        | 0.43642       | 0.36585     | 0.53371     | 0.65951        | 0.79121     | 0.00000       | 0.47457      |
| Koalanlp       | 2.1.7           | HNN     | 0.54118        | 0.44220       | 0.34146     | 0.54494     | 0.67791        | 0.78022     | 0.00000       | 0.47541      |
| Koalanlp       | 2.1.7           | KMR     | 0.51176        | 0.38439       | 0.26829     | 0.42135     | 0.45706        | 0.79121     | 0.00000       | 0.40486      |
| Koalanlp       | 2.1.7           | RHINO   | 0.52941        | 0.41329       | 0.29268     | 0.39326     | 0.67791        | 0.79121     | 0.00000       | 0.44253      |
| Koalanlp       | 2.1.7           | EUNJEON | 0.51176        | 0.38728       | 0.21951     | 0.38202     | 0.59816        | 0.70330     | 0.00000       | 0.40029      |
| Koalanlp       | 2.1.7           | ARIRANG | 0.51176        | 0.41618       | 0.29268     | 0.44382     | 0.66564        | 0.79121     | 0.00000       | 0.44589      |
| Koalanlp       | 2.1.7           | KKMA    | 0.52941        | 0.45954       | 0.31707     | 0.38202     | 0.57669        | 0.58242     | 0.06667       | 0.41626      |
| Kiwi           | 0.14.1          | N/A     | 0.78235        | 0.61272       | 0.90244     | 0.66292     | 0.63804        | 0.83516     | 0.20000       | 0.66194      |
| **Kss (ours)** | 4.2.0           | pecab   | **0.87059**    | **0.82659**   | **0.95122** | 0.74157     | 0.98160        | **0.86813** | **0.36667**   | 0.80091      |
| **Kss (ours)** | 4.2.0           | mecab   | **0.87059**    | **0.82659**   | **0.95122** | **0.75281** | **1.00000**    | **0.86813** | **0.36667**   | **0.80514**  |

![](https://github.com/hyunwoongko/kss/blob/main/assets/tasks_em.png)

![](https://github.com/hyunwoongko/kss/blob/main/assets/avg_em.png)

- **F1 score (dice similarity)**: This calculates the overlap between the output predictions and gold labels. It means this gives score even if the output predictions are not exactly same with gold labels. This is less reliable because this gives huge advantages to splitters which separate sentences too finely.

| Name           | Library version | Backend | blogs_lee (F1) | blogs_ko (F1) | sample (F1) | tweets (F1) | wikipedia (F1) | nested (F1) | v_ending (F1) | Average (F1) |
|----------------|-----------------|---------|----------------|---------------|-------------|-------------|----------------|-------------|---------------|--------------|
| Baseline       | N/A             | N/A     | 0.66847        | 0.55724       | 0.54732     | 0.65446     | 0.76664        | 0.85438     | 0.11359       | 0.59458      |
| Koalanlp       | 2.1.7           | OKT     | 0.66847        | 0.55724       | 0.58642     | 0.69434     | 0.76639        | 0.93010     | 0.11359       | 0.61665      |
| Koalanlp       | 2.1.7           | HNN     | 0.69341        | 0.59185       | 0.57092     | 0.70350     | 0.98116        | 0.94163     | 0.11359       | 0.65658      |
| Koalanlp       | 2.1.7           | KMR     | 0.63506        | 0.48661       | 0.49026     | 0.56364     | 0.54806        | 0.85426     | 0.11359       | 0.52735      |
| Koalanlp       | 2.1.7           | RHINO   | 0.68313        | 0.53548       | 0.52258     | 0.57900     | 0.96743        | 0.85426     | 0.11359       | 0.60792      |
| Koalanlp       | 2.1.7           | EUNJEON | 0.67063        | 0.54010       | 0.48446     | 0.65018     | 0.91846        | 0.80233     | 0.11359       | 0.59710      |
| Koalanlp       | 2.1.7           | ARIRANG | 0.69407        | 0.57230       | 0.56872     | 0.67882     | 0.97884        | 0.85426     | 0.11359       | 0.63722      |
| Koalanlp       | 2.1.7           | KKMA    | 0.78127        | 0.66599       | 0.78335     | 0.56832     | 0.92527        | 0.89952     | 0.30797       | 0.70457      |
| Kiwi           | 0.14.1          | N/A     | 0.91323        | 0.76214       | 0.96003     | **0.84503** | 0.97740        | **0.98447** | 0.38535       | 0.83252      |
| **Kss (ours)** | 4.2.0           | pecab   | **0.92162**    | **0.90335**   | **0.96826** | 0.82720     | 0.98801        | 0.93012     | **0.48153**   | 0.86001      |
| **Kss (ours)** | 4.2.0           | mecab   | **0.92162**    | **0.90335**   | **0.96826** | 0.83329     | **1.00000**    | 0.93012     | **0.48153**   | **0.86259**  |

![](https://github.com/hyunwoongko/kss/blob/main/assets/tasks_f1.png)

![](https://github.com/hyunwoongko/kss/blob/main/assets/avg_f1.png)

- **Normalized F1 score**: This is the most reliable metric made by the Kss project. It makes up for the downside of the F1 score by penalizing splitters which separate too finely.

| Name           | Library version | Backend | blogs_lee (NF1) | blogs_ko (NF1) | sample (NF1) | tweets (NF1) | wikipedia (NF1) | nested (NF1) | v_ending (NF1) | Average (NF1) |
|----------------|-----------------|---------|-----------------|----------------|--------------|--------------|-----------------|--------------|----------------|---------------|
| Baseline       | N/A             | N/A     | 0.59884         | 0.52607        | 0.54732      | 0.61806      | 0.76379         | 0.75991      | 0.11359        | 0.56108       |
| Koalanlp       | 2.1.7           | OKT     | 0.62168         | 0.55724        | 0.58642      | 0.66198      | 0.76354         | 0.83832      | 0.11359        | 0.59182       |
| Koalanlp       | 2.1.7           | HNN     | 0.62515         | 0.57098        | 0.57092      | 0.66922      | 0.97286         | 0.82031      | 0.11359        | 0.62043       |
| Koalanlp       | 2.1.7           | KMR     | 0.61636         | 0.48412        | 0.49026      | 0.55535      | 0.54806         | 0.85426      | 0.11359        | 0.52314       |
| Koalanlp       | 2.1.7           | RHINO   | 0.63619         | 0.51835        | 0.52258      | 0.55140      | 0.95886         | 0.85426      | 0.11359        | 0.59360       |
| Koalanlp       | 2.1.7           | EUNJEON | 0.62104         | 0.52132        | 0.48446      | 0.57766      | 0.91307         | 0.80233      | 0.11359        | 0.57261       |
| Koalanlp       | 2.1.7           | ARIRANG | 0.58979         | 0.51149        | 0.56872      | 0.53500      | 0.94617         | 0.85426      | 0.11359        | 0.58843       |
| Koalanlp       | 2.1.7           | KKMA    | 0.73972         | 0.64048        | 0.78335      | 0.56408      | 0.89218         | 0.75068      | 0.30797        | 0.66835       |
| Kiwi           | 0.14.1          | N/A     | 0.84378         | 0.72367        | 0.93717      | 0.79056      | 0.91031         | **0.92687**  | 0.34179        | 0.78202       |
| **Kss (ours)** | 4.2.0           | pecab   | **0.88878**     | **0.88605**    | **0.96826**  | 0.80771      | 0.98160         | 0.92063      | **0.48153**    | 0.84957       |
| **Kss (ours)** | 4.2.0           | mecab   | **0.88878**     | **0.88605**    | **0.96826**  | **0.81379**  | **1.00000**     | 0.92063      | **0.48153**    | **0.85129**   |

![](https://github.com/hyunwoongko/kss/blob/main/assets/tasks_nf1.png)

![](https://github.com/hyunwoongko/kss/blob/main/assets/avg_nf1.png)

Kss performed best in most metrics and datasets, and Kiwi performed well. Both baseline and koalanlp performed poorly.

<br>

#### 4) Consideration of metrics and Normalized F1 score
The evaluation source code which was copied from [kiwipiepy](https://github.com/bab2min/kiwipiepy/tree/main/benchmark/sentence_split) provides both EM score and F1 score (dice similarity). 
**But I don't believe both are good metrics to measure sentence segmentation performance.**
In this section, I will show you the problems of both EM score and F1 score, and propose a new metric, Normalized F1 score to solve these problems.
For these experiments, I used Kiwi (0.14.1) and Word Split, and the Word Split is equivalent to `text.split(" ")`.

#### 4.1) Problem of EM score

Firstly, the EM score has a problem like the following. Let's look at an example like this:

- Input text:
  ```
  델포이 섬에 있는 아폴론 신전은 앞일을 예언하는 신탁으로 유명하다.[3] 아폴론이 아직 태어나기 이전에 레토는, 자신이 임신한 쌍둥이들이, 아버지인 제우스 다음가는 권력을 누리게 될 것이라는 예언을 받았다고 한다. 
  ```

- Label:
  ```
  델포이 섬에 있는 아폴론 신전은 앞일을 예언하는 신탁으로 유명하다.[3] 
  아폴론이 아직 태어나기 이전에 레토는, 자신이 임신한 쌍둥이들이, 아버지인 제우스 다음가는 권력을 누리게 될 것이라는 예언을 받았다고 한다. 
  ```

And the two splitters split input text like the following:

-  Output of Kiwi (0.14.1):
   ```
   # EM score: 0.0

   델포이 섬에 있는 아폴론 신전은 앞일을 예언하는 신탁으로 유명하다.
   [3] 아폴론이 아직 태어나기 이전에 레토는, 자신이 임신한 쌍둥이들이, 아버지인 제우스 다음가는 권력을 누리게 될 것이라는 예언을 받았다고 한다. 
   ```

- Output of Word Split:
   ```
   # EM score: 0.0

   델포이
   섬에
   있는
   아폴론
   신전은
   앞일을
   예언하는
   신탁으로
   유명하다.[3]
   아폴론이
   아직
   태어나기
   이전에
   레토는,
   자신이
   임신한
   쌍둥이들이,
   아버지인
   제우스
   다음가는
   권력을
   누리게
   될
   것이라는
   예언을
   받았다고
   한다. 
   ```

The Kiwi separated sentences well excluding the footnote (`[3]`).
Even if it didn't split sentences exactly accurate, it split somewhat well.
On the contrary, the Word Split separated sentences completely wrong.
However, since none of these outputs are the same with label, both are rated as 0.0 with EM score. 
It's too harsh evaluation for Kiwi.
As such, the EM score does not properly evaluate the performance in the case of the sentence segmentation is not exactly accurate.

You can reproduce this result using the following commands:
- Kiwi: `python3 ./bench/test_kiwi.py ./bench/metrics/em_problem.txt`
- Word Split: `python3 ./bench/test_word_split.py ./bench/metrics/em_problem.txt`

#### 4.2) Problem of F1 score

We can utilize the F1 score to solve the problem of EM score. 
But F1 score has another problem. Let's look at an example like this:

- Input text:
  ```
  기억해 넌 그 애의 친구야. 네가 죽으면 마 들레 느가 펑펑 울 거야 비 체는 슬퍼하겠지 이 안은 화를 낼 거야. 메이 시는 어쩌면 조금은 생각 해 주지 않을까 중요한 건 그건 네가 지키고 싶어 했던 사람들이잖아 어서 가.
  ```
 
- Label:
  ```
  기억해 
  넌 그 애의 친구야.
  네가 죽으면 마 들레 느가 펑펑 울 거야
  비 체는 슬퍼하겠지
  이 안은 화를 낼 거야.
  메이 시는 어쩌면 조금은 생각 해 주지 않을까
  중요한 건 그건 네가 지키고 싶어 했던 사람들이잖아
  어서 가.
  ```

And the two splitters split this input like the following:

- Output of Kiwi (0.14.1):
  ```
  F1 score: 0.56229
  
  Output:
  기억해 넌 그 애의 친구야.
  네가 죽으면 마 들레 느가 펑펑 울 거야
  비 체는 슬퍼하겠지
  이 안은 화를 낼 거야.
  메이 시는 어쩌면 조금은 생각 해 주지 않을까 중요한 건 그건 네가 지키고 싶어 했던 사람들이잖아 어서 가.
  ```

- Output of Word Split:
  ```
  F1 score: 0.58326
  
  Output:
  기억해
  넌
  그
  애의
  친구야.
  네가
  죽으면
  마
  들레
  느가
  펑펑
  울
  거야
  비
  체는
  슬퍼하겠지
  이
  안은
  화를
  낼
  거야.
  메이
  시는
  어쩌면
  조금은
  생각
  해
  주지
  않을까
  중요한
  건
  그건
  네가
  지키고
  싶어
  했던
  사람들이잖아
  어서
  가.
  ```

Neither two splitters split the sentence perfectly, but Kiwi split sentences pretty well.
On the contrary, the Word Split separated sentences completely wrong.
Interestingly, Word Split's F1 score is 0.58326, which is higher than Kiwi's 0.56229.
This means that the F1 score (dice similarity) gives a huge advantage to splitters which separate sentences too finely.

You can reproduce this result using the following commands:
- Kiwi: `python3 ./bench/test_kiwi.py ./bench/metrics/f1_problem.txt`
- Word Split: `python3 ./bench/test_word_split.py ./bench/metrics/f1_problem.txt`

#### 4.3) Normalized F1 score

To overcome the problems of both EM score and F1 score, I propose a new metric named `Normalized F1 score`.
This can be obtained by the following formula.

```
Normalized_F1_score = F1_score * min(1, len(golds)/len(preds))
```

This inherits the advantages of the F1 score, but penalizes splitters which separate sentences too finely.
If we re-evaluate the above two cases with the Normalized F1 score, the scores change as follows.

| Splitter   | Library version | Input sentences    | EM score | Normalized F1 score |
|------------|-----------------|--------------------|----------|---------------------|
| Kiwi       | 0.14.1          | `델포이 섬에 있는 아폴론...` | **0.0**  | **0.96341**         |
| Word Split | N/A             | `델포이 섬에 있는 아폴론...` | **0.0**  | 0.02145             |

| Splitter   | Library version | Input sentences    | F1 score    | Normalized F1 score |
|------------|-----------------|--------------------|-------------|---------------------|
| Kiwi       | 0.14.1          | `기억해 넌 그 애의 친구...` | 0.56229     | **0.56229**         |
| Word Split | N/A             | `기억해 넌 그 애의 친구...` | **0.58326** | 0.11964             |

In both cases, Word Split scores significantly lower than Kiwi. 
This means that the Normalized F1 score can complement the EM score and F1 score.
That's why I'm introducing this new metric, Normalized F1 to sentence segmentation evaluation.

<br>

#### 5) Where does the difference in performance come from? (Qualitative Analysis)
So far, I've conducted quantitative analysis and have been considering evaluation metrics. 
However, it is meaningless to simply compare them by number. I definitely want you to see the segmentation results.
Let's take `blogs_ko` samples as examples, and compare performance of each library.
For this, I will take the best backend of each library (Kss=mecab, Koalanlp=KKMA) on the `blogs_ko` dataset, because looking results of all backends may make you tired.

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
This is a single blog post, so you can expect the following time when you split a blog post into sentences.
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
| Kiwi           | 0.14.1          | N/A     | 36.26               |
| **Kss (ours)** | 4.2.0           | pecab   | 7050.50             |
| **Kss (ours)** | 4.2.0           | mecab   | 46.81               |

![](https://github.com/hyunwoongko/kss/blob/main/assets/average_computation_time.png)

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
I've measured the performance of Kss and other libraries using 7 evaluation datasets, and also measured their speed.
And I proposed a new metric named 'Normalized F1 score'. In terms of segmentation performance, Kss performed best on most datasets. 
In terms of speed, baseline was the fastest, and Koalanlp (OKT backend) and Kiwi followed. 
but Kss (mecab backend) also showed a speed that could compete with others.

Although much progress has been made by Kiwi and Kss, there are still many difficulties and limitations in Korean sentence segmentation libraries. 
In fact, it's also because very few people attack this task. If anyone wants to discuss Korean sentence segmentation algorithms with me or contribute to my work, feel free to send an email to kevin.ko@tunib.ai or let me know on the Github [issue](https://github.com/hyunwoongko/kss/issues) page.

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


#### 2) `summarize_sentences`: summarize text into important sentences

```python
from kss import summarize_sentences

summarize_sentences(
    text: Union[str, List[str], Tuple[str]],
    backend: str = "auto",
    num_workers: Union[int, str] = "auto",
    num_sentences: int = 3,
    tolerance: float: 0.05,
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
- **max_sentences: The maximum number of output sentences**
  - `max_sentences=1~N`: return 1~N sentences by sentence importance
- **tolerance: Threshold for omitting edge weights.**

</details>

<details>
<summary>Usages</summary>


- Single text summarization
  ```python
  import kss

  text = """개그맨 겸 가수 ‘개가수’ UV 유세윤이 신곡 발매 이후 많은 남편들의 응원을 받고 있다. 유세윤은 지난 3일 오후 6시 새 싱글 ‘마더 사커(Mother Soccer)(Feat. 수퍼비)’를 발매했다. ‘마더 사커’는 아내에 대한 서운한 마음을 위트 있고 강한 어조로 디스 하는 남편 유세윤의 마음을 담은 곡이다. 발매 후 소셜 미디어 상에서 화제를 모으고 있는 가운데, 가수 하동균은 “유세유니 괜찮겠어”라는 반응을 보이기도 했다. 누리꾼들은 ‘두 분의 원만한 합의가 있기를 바랍니다’, ‘집에는 들어갈 수 있겠나’ 등 유세윤의 귀가를 걱정하는 모습을 보였다. 유세윤은 점입가경으로 ‘마더 사커’ 챌린지를 시작, 자신의 SNS를 통해 “부부 싸움이 좀 커졌네요”라며 배우 송진우와 함께 촬영한 영상을 게재했다. 해당 영상에서는 양말을 신고 침대에 들어간 뒤 환호를 지르거나 화장실 불을 끄지 않고 도망가는 등 아내의 잔소리 유발 포인트를 살려 재치 있는 영상을 완성했다. 유세윤은 ‘마더 사커’를 통해 남편들의 마음을 대변해 주고 있는 한편 아내의 반응은 어떨지 궁금증을 모은다."""

  kss.summarize_sentences(text)
  # ['개그맨 겸 가수 ‘개가수’ UV 유세윤이 신곡 발매 이후 많은 남편들의 응원을 받고 있다.', '‘마더 사커’는 아내에 대한 서운한 마음을 위트 있고 강한 어조로 디스 하는 남편 유세윤의 마음을 담은 곡이다.', '유세윤은 ‘마더 사커’를 통해 남편들의 마음을 대변해 주고 있는 한편 아내의 반응은 어떨지 궁금증을 모은다.']
  ```

- Batch texts summarization
  ```python
  import kss

  texts = [
      """개그맨 겸 가수 ‘개가수’ UV 유세윤이 신곡 발매 이후 많은 남편들의 응원을 받고 있다. 유세윤은 지난 3일 오후 6시 새 싱글 ‘마더 사커(Mother Soccer)(Feat. 수퍼비)’를 발매했다. ‘마더 사커’는 아내에 대한 서운한 마음을 위트 있고 강한 어조로 디스 하는 남편 유세윤의 마음을 담은 곡이다. 발매 후 소셜 미디어 상에서 화제를 모으고 있는 가운데, 가수 하동균은 “유세유니 괜찮겠어”라는 반응을 보이기도 했다. 누리꾼들은 ‘두 분의 원만한 합의가 있기를 바랍니다’, ‘집에는 들어갈 수 있겠나’ 등 유세윤의 귀가를 걱정하는 모습을 보였다. 유세윤은 점입가경으로 ‘마더 사커’ 챌린지를 시작, 자신의 SNS를 통해 “부부 싸움이 좀 커졌네요”라며 배우 송진우와 함께 촬영한 영상을 게재했다. 해당 영상에서는 양말을 신고 침대에 들어간 뒤 환호를 지르거나 화장실 불을 끄지 않고 도망가는 등 아내의 잔소리 유발 포인트를 살려 재치 있는 영상을 완성했다. 유세윤은 ‘마더 사커’를 통해 남편들의 마음을 대변해 주고 있는 한편 아내의 반응은 어떨지 궁금증을 모은다.""",
      """제임스 카메론 감독의 영화 ‘아바타: 물의 길’(아바타2)이 개봉 21일 만에 전국 누적 관객 800만명을 달성했다. 올해 국내 첫 ‘천만 영화’가 될지 주목된다. 4일 영화진흥위원회(영진위)에 따르면 지난달 14일 개봉한 ‘아바타2’는 전날 11만3902명의 관객을 모았다. 누적 관객 800만1930명으로 전편 ‘아바타’보다 4일 빠른 기록이다. 이는 한국의 신종 코로나바이러스 감염증(코로나19) 팬데믹 이후 세 번째 기록이다. 지난해 개봉한 ‘범죄도시2’와 ‘탑건: 매버릭’에 이어 관객 800만명을 넘어선 것이다. 2021년 12월 개봉한 ‘스파이더맨: 노 웨이 홈’도 800만명을 넘지 못했다. 이번에 ‘아바타2’가 1000만명을 돌파한다면 2019년 개봉한 ‘어벤져스: 엔드게임’ 이후 5년 만에 첫 1000만 국내 개봉 외국 영화가 된다. 영진위의 통합전산망에 따르면 ‘아바타2’의 국내 실시간 예매율은 53.9%(4일 오전 10시 기준)로 이날 개봉한 일본 영화 ‘더 퍼스트 슬램덩크’(12.9%)보다 약 4배 이상 높은 예매율을 기록했다. 박스오피스 2위는 정성화 주연의 한국 뮤지컬 영화 ‘영웅’으로, 누적 관객 180만명을 기록했다. 이어 작년 11월 말 개봉한 일본 영화 ‘오늘 밤, 세계에서 이 사랑이 사라진다 해도’가 누적 관객 72만명으로 3위를 유지하고 있다.""",
  ]

  kss.summarize_sentences(texts)
  # [['개그맨 겸 가수 ‘개가수’ UV 유세윤이 신곡 발매 이후 많은 남편들의 응원을 받고 있다.', '‘마더 사커’는 아내에 대한 서운한 마음을 위트 있고 강한 어조로 디스 하는 남편 유세윤의 마음을 담은 곡이다.', '유세윤은 ‘마더 사커’를 통해 남편들의 마음을 대변해 주고 있는 한편 아내의 반응은 어떨지 궁금증을 모은다.'], 
  # ['제임스 카메론 감독의 영화 ‘아바타: 물의 길’(아바타2)이 개봉 21일 만에 전국 누적 관객 800만명을 달성했다.', '4일 영화진흥위원회(영진위)에 따르면 지난달 14일 개봉한 ‘아바타2’는 전날 11만3902명의 관객을 모았다.', '박스오피스 2위는 정성화 주연의 한국 뮤지컬 영화 ‘영웅’으로, 누적 관객 180만명을 기록했다.']]
  ```

- Set `max_sentences` if you want get more or less three sentences from text
  ```python
  import kss

  text = """개그맨 겸 가수 ‘개가수’ UV 유세윤이 신곡 발매 이후 많은 남편들의 응원을 받고 있다. 유세윤은 지난 3일 오후 6시 새 싱글 ‘마더 사커(Mother Soccer)(Feat. 수퍼비)’를 발매했다. ‘마더 사커’는 아내에 대한 서운한 마음을 위트 있고 강한 어조로 디스 하는 남편 유세윤의 마음을 담은 곡이다. 발매 후 소셜 미디어 상에서 화제를 모으고 있는 가운데, 가수 하동균은 “유세유니 괜찮겠어”라는 반응을 보이기도 했다. 누리꾼들은 ‘두 분의 원만한 합의가 있기를 바랍니다’, ‘집에는 들어갈 수 있겠나’ 등 유세윤의 귀가를 걱정하는 모습을 보였다. 유세윤은 점입가경으로 ‘마더 사커’ 챌린지를 시작, 자신의 SNS를 통해 “부부 싸움이 좀 커졌네요”라며 배우 송진우와 함께 촬영한 영상을 게재했다. 해당 영상에서는 양말을 신고 침대에 들어간 뒤 환호를 지르거나 화장실 불을 끄지 않고 도망가는 등 아내의 잔소리 유발 포인트를 살려 재치 있는 영상을 완성했다. 유세윤은 ‘마더 사커’를 통해 남편들의 마음을 대변해 주고 있는 한편 아내의 반응은 어떨지 궁금증을 모은다."""

  kss.summarize_sentences(text, max_sentences=4)
  # ['개그맨 겸 가수 ‘개가수’ UV 유세윤이 신곡 발매 이후 많은 남편들의 응원을 받고 있다.', '‘마더 사커’는 아내에 대한 서운한 마음을 위트 있고 강한 어조로 디스 하는 남편 유세윤의 마음을 담은 곡이다.', '유세윤은 점입가경으로 ‘마더 사커’ 챌린지를 시작, 자신의 SNS를 통해 “부부 싸움이 좀 커졌네요”라며 배우 송진우와 함께 촬영한 영상을 게재했다.', '유세윤은 ‘마더 사커’를 통해 남편들의 마음을 대변해 주고 있는 한편 아내의 반응은 어떨지 궁금증을 모은다.']
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

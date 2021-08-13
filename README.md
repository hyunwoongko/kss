# Korean Sentence Splitter
Split Korean text into sentences using heuristic algorithm.

<br><br>

## 1. Installation
```console
pip install kss
```

<br><br>

## 2. Performance Evaluation
- Kss is a Korean sentence segmentation toolkit with the best performance ever.
- You can check [simple performance evaluation](https://github.com/hyunwoongko/kss/blob/main/EVALUATION.md) comparison with OKT and Hannanum.

<br><br>

## 3. Usage of `split_sentences`
### 3.1. Split sentences with heuristics and punctuations.
```python
>>> from kss import split_sentences
>>> text = "미리 예약을 할 수 있는 시스템으로 합리적인 가격에 여러 종류의 생선, 그리고 다양한 부위를 즐길 수 있기 때문이다 계절에 따라 모둠회의 종류는 조금씩 달라지지만 자주 올려주는 참돔 마스까와는 특히 맛이 매우 좋다 제철 생선 5~6가지 구성에 평소 접하지 못했던 부위까지 색다르게 즐길 수 있다"
>>> split_sentences(text)
```
```python
['미리 예약을 할 수 있는 시스템으로 합리적인 가격에 여러 종류의 생선, 그리고 다양한 부위를 즐길 수 있기 때문이다', 
'계절에 따라 모둠회의 종류는 조금씩 달라지지만 자주 올려주는 참돔 마스까와는 특히 맛이 매우 좋다', 
'제철 생선 5~6가지 구성에 평소 접하지 못했던 부위까지 색다르게 즐길 수 있다']
```

### 3.2. Split sentences without heuristics.
- If your article follows the punctuation rules well, we recommend to you set the `use_heuristic=False`. (default is `True`)
- In that cases, splitting sentence without heuristic is better than using heuristic algorithms.
    - Formal articles (Wiki, News, Essay, ...) : `use_heuristic=False`
    - Informal articles (SNS, Blogs, Messages, ...) : `use_heuristic=True`
```python
>>> from kss import split_sentences
>>> text = "미리 예약을 할 수 있는 시스템으로 합리적인 가격에 여러 종류의 생선, 그리고 다양한 부위를 즐길 수 있기 때문이다. 계절에 따라 모둠회의 종류는 조금씩 달라지지만 자주 올려주는 참돔 마스까와는 특히 맛이 매우 좋다. 일반 모둠회도 좋지만 좀 더 특별한 맛을 즐기고 싶다면 특수 부위 모둠회를 추천한다 제철 생선 5~6가지 구성에 평소 접하지 못했던 부위까지 색다르게 즐길 수 있다."
>>> split_sentences(text, use_heuristic=False)  # split sentence without heuristic
```
```python
['미리 예약을 할 수 있는 시스템으로 합리적인 가격에 여러 종류의 생선, 그리고 다양한 부위를 즐길 수 있기 때문이다.', 
'계절에 따라 모둠회의 종류는 조금씩 달라지지만 자주 올려주는 참돔 마스까와는 특히 맛이 매우 좋다.', 
'제철 생선 5~6가지 구성에 평소 접하지 못했던 부위까지 색다르게 즐길 수 있다.']
```

### 3.3. Brackets and quotation marks processing
- We provide a technique for not splitting sentences enclosed in brackets or quotation marks.
- However, these features can cause problems when brackets and quotation marks are misaligned.
- This was a chronic problem in previous Kss C++. So we provide two solutions to solve these problems.
  
#### 3.3.1. Turn off brackets and quotation marks processing
- You can turn off processing related to parentheses or quotes if you want.
- Set `ignore_quotes_or_brackets` to `True` option to turn off processing. (default is `False`)
```python
>>> from kss import split_sentences
>>> text = "그가 말했다. (거기는 가지 마세요. 위험하니까요. 알겠죠?) 그러자 그가 말했다. 알겠어요."

>>> kss.split_sentences(text)  # turn on 
['그가 말했다.', '(거기는 가지 마세요. 위험하니까요. 알겠죠?) 그러자 그가 말했다.', '알겠어요.']

>>> kss.split_sentences(text, ignore_quotes_or_brackets=True)
['그가 말했다.', '(거기는 가지 마세요.', '위험하니까요.', '알겠죠?', ') 그러자 그가 말했다.', '알겠어요.']
```

#### 3.3.2. Calibration brackets and quotation marks misalignment
- If brackets and quotation marks processing is turned on, we provide a calibration feature by default.
```python
>>> from kss import split_sentences
>>> text = "그가 말했다. '거기는 가지 마세요. 위험하니까요.'' 알겠죠? 그러자 그가 말했다. 알겠어요."

>>> kss.split_sentences(text)  # 1.3.1
# 1.3.1 (C++ version) can't split misaligned sentence
['그가 말했다.', "'거기는 가지 마세요. 위험하니까요.'' 알겠죠? 그러자 그가 말했다. 알겠어요."]

>>> kss.split_sentences(text)  # 2.6.0
# 2.6.0 (Python version) can split misaligned sentence via calibration
['그가 말했다.', "'거기는 가지 마세요. 위험하니까요.'", "'알겠죠?", '그러자 그가 말했다.', '알겠어요.']

```

- However, this feature uses recursion, so it works very slowly on very long text. 
- So, you can optimize calibration by changing parameters about the recursion.  
    - The depth of the recursion can be modified through a parameter `max_recover_step`. (default is 5)
    - In addition, applying calibration to very long text significantly reduces the speed, so you can turn it off using the `max_recover_length` parameter. (default is 30,000)
```python
>>> from kss import split_sentences
>>> text = "VERY_LONG_TEXT"

>>> split_sentences(text, max_recover_step=5)
>>> # you can adjust recursion depth using `max_recover_step` (default is 5)
>>> split_sentences(text, max_recover_length=30000)
>>> # you can turn it off when you input very long text using `max_recover_length` (default is 30000)
```

<br><br>

## 4.Usage of `split_sentences`
### 4.1. Set maximum length of chunks via `max_length`
- `split_chunks` combine sentences into chunks of a certain length or less.
- You can set the maximum length of one chunk to `max_length`.
```python
>>> from kss import split_chunks
>>> text = "NoSQL이라고 하는 말은 No 'English'라고 하는 말과 마찬가지다. 세상에는 영어 말고도 수많은 언어가 존재한다. MongoDB에서 사용하는 쿼리 언어와 CouchDB에서 사용하는 쿼리 언어는 서로 전혀 다르다. 그럼에도 이 두 쿼리 언어는 같은 NoSQL 카테고리에 속한다. 어쨌거나 SQL이 아니기 때문이다. 또한 NoSQL이 No RDBMS를 의미하지는 않는다. BerkleyDB같은 예외가 있기 때문이다. 그리고 No RDBMS가 NoSQL인 것도 아니다. SQL호환 레이어를 제공하는 KV-store라는 예외가 역시 존재한다. 물론 KV-store의 특징상 range query를 where절에 넣을 수 없으므로 완전한 SQL은 못 되고 SQL의 부분집합 정도를 제공한다."
>>> split_chunks(text, max_length=128)
```
```python
[ChunkWithIndex(start=0, text="NoSQL이라고 하는 말은 No 'English'라고 하는 말과 마찬가지다. 세상에는 영어 말고도 수많은 언어가 존재한다. MongoDB에서 사용하는 쿼리 언어와 CouchDB에서 사용하는 쿼리 언어는 서로 전혀 다르다."),
ChunkWithIndex(start=124, text='그럼에도 이 두 쿼리 언어는 같은 NoSQL 카테고리에 속한다. 어쨌거나 SQL이 아니기 때문이다. 또한 NoSQL이 No RDBMS를 의미하지는 않는다. BerkleyDB같은 예외가 있기 때문이다.'),
ChunkWithIndex(start=236, text='그리고 No RDBMS가 NoSQL인 것도 아니다. SQL호환 레이어를 제공하는 KV-store라는 예외가 역 시 존재한다.'),
ChunkWithIndex(start=305, text='물론 KV-store의 특징상 range query를 where절에 넣을 수 없으므로 완전한 SQL은 못 되고 SQL의 부분집합 정도를 제공한다.')]
```

### 4.2. Use every options used in `split_sentences`
- You can use the EVERY options used in `split_sentences`.
- For example, if you want to turn off the processing about quotation marks, you can set `ignore_quotes_or_brackets` the same as split_sentences.
```python
>>> from kss import split_chunks
>>> text = "NoSQL이라고 하는 말은 No 'English'라고 하는 말과 마찬가지다. 세상에는 영어 말고도 수많은 언어가 존재한다. MongoDB에서 사용하는 쿼리 언어와 CouchDB에서 사용하는 쿼리 언어는 서로 전혀 다르다. 그럼에도 이 두 쿼리 언어는 같은 NoSQL 카테고리에 속한다. 어쨌거나 SQL이 아니기 때문이다. 또한 NoSQL이 No RDBMS를 의미하지는 않는다. BerkleyDB같은 예외가 있기 때문이다. 그리고 No RDBMS가 NoSQL인 것도 아니다. SQL호환 레이어를 제공하는 KV-store라는 예외가 역시 존재한다. 물론 KV-store의 특징상 range query를 where절에 넣을 수 없으므로 완전한 SQL은 못 되고 SQL의 부분집합 정도를 제공한다."
>>> split_chunks(text, max_length=128, ignore_quotes_or_brackets=True)
```

### 4.3. Overlap sentences across chunks
- If `overlap` is `True`, text will be chunked similar with sliding window.
- So, when you turn this feature on, each chunk allows for duplicate sentences.
```python
>>> from kss import split_chunks
>>> text = "NoSQL이라고 하는 말은 No 'English'라고 하는 말과 마찬가지다. 세상에는 영어 말고도 수많은 언어가 존재한다. MongoDB에서 사용하는 쿼리 언어와 CouchDB에서 사용하는 쿼리 언어는 서로 전혀 다르다. 그럼에도 이 두 쿼리 언어는 같은 NoSQL 카테고리에 속한다. 어쨌거나 SQL이 아니기 때문이다. 또한 NoSQL이 No RDBMS를 의미하지는 않는다. BerkleyDB같은 예외가 있기 때문이다. 그리고 No RDBMS가 NoSQL인 것도 아니다. SQL호환 레이어를 제공하는 KV-store라는 예외가 역시 존재한다. 물론 KV-store의 특징상 range query를 where절에 넣을 수 없으므로 완전한 SQL은 못 되고 SQL의 부분집합 정도를 제공한다."
>>> split_chunks(text, max_length=128, overlap=True)
```
```python
[ChunkWithIndex(start=0, text="NoSQL이라고 하는 말은 No 'English'라고 하는 말과 마찬가지다. 세상에는 영어 말고도 수많은 언어가 존재한다. MongoDB에서 사용하는 쿼리 언어와 CouchDB에서 사용하는 쿼리 언어는 서로 전혀 다르다."),
ChunkWithIndex(start=43, text='세상에는 영어 말고도 수많은 언어가 존재한다. MongoDB에서 사용하는 쿼리 언어와 CouchDB에서 사용하는 쿼리 언어는 서로 전혀 다르다. 그럼에도 이 두 쿼리 언어는 같은 NoSQL 카테고리에 속한다.'),
ChunkWithIndex(start=69, text='MongoDB에서 사용하는 쿼리 언어와 CouchDB에서 사용하는 쿼리 언어는 서로 전혀 다르다. 그럼 에도 이 두 쿼리 언어는 같은 NoSQL 카테고리에 속한다. 어쨌거나 SQL이 아니기 때문이다.'),
ChunkWithIndex(start=124, text='그럼에도 이 두 쿼리 언어는 같은 NoSQL 카테고리에 속한다. 어쨌거나 SQL이 아니기 때문이다. 또한 NoSQL이 No RDBMS를 의미하지는 않는다. BerkleyDB같은 예외가 있기 때문이다.'),
ChunkWithIndex(start=180, text='또한 NoSQL이 No RDBMS를 의미하지는 않는다. BerkleyDB같은 예외가 있기 때문이다. 그리고 No RDBMS가 NoSQL인 것도 아니다. SQL호환 레이어를 제공하는 KV-store라는 예외가 역시 존재한다.'),
ChunkWithIndex(start=236, text='그리고 No RDBMS가 NoSQL인 것도 아니다. SQL호환 레이어를 제공하는 KV-store라는 예외가 역 시 존재한다. 물론 KV-store의 특징상 range query를 where절에 넣을 수 없으므로 완전한 SQL은 못 되고 SQL의 부분집합 정도를 제공한다.')]
```

<br><br>

## 5. Updates
- you can upgrade library by `pip install kss --upgrade` 
- you can also check update notes [here](https://github.com/hyunwoongko/kss/blob/main/UPDATES.md).
```consol
test: twine upload --repository-url https://test.pypi.org/legacy/ dist/*
realse: twine upload dist/*
```

<br><br>

## 6. References
- [KSS Java version (Coming soon...)](#)
- [KSS C++ version](https://github.com/likejazz/korean-sentence-splitter)
- [Docs of C++ version](http://docs.likejazz.com/kss/)
- [PyPI repository](https://pypi.org/project/kss/)

<br><br>

## 7. Citation
If you find this library useful, please consider citing:
```
@misc{kss,
  author       = {Park, Sangkil and Ko, Hyunwoong},
  title        = {Korean sentence splitter},
  howpublished = {\url{https://github.com/hyunwoongko/kss}},
  year         = {2020},
}
```
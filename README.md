# Korean Sentence Splitter
Split Korean text into sentences using heuristic algorithm.
<br><br><br>

## Install
```console
pip install kss
```
<br><br>

## Performance Evaluation
- You can check simple performance evaluation [here](https://github.com/hyunwoongko/kss/blob/main/EVALUATION.md).
- There are 6 difficult example documents for a sentence segmentation.
<br><br>

## Usage
### 1. `split_sentences`
- Split sentences from text
```python
>>> from kss import split_sentences

>>> s = "회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요 다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다 강남역 맛집 토끼정의 외부 모습."
>>> for sent in split_sentences(s):
...    print(sent)
...
```
```
회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요
다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다
강남역 맛집 토끼정의 외부 모습.
```
<br>

- if you want more safe segmentation, set the argument `safe = True`
```python
>>> from kss import split_sentences
>>> text = """
... 미리 예약을 할 수 있는 시스템으로 합리적인 가격에 여러 종류의 생선, 그리고 다양한 부위를 즐길 수 있기 때문이다 계절에 따라 모둠회의 종류는 조금씩 달라지지만 자주 올려주는 참돔 마스까와(껍질만 끓는 물에 익힌 것)는 특히 맛이 매우 좋다 일반 모둠회도 좋지만 좀 더 특별한 맛을 즐기고 싶다면 특수 부위 모둠회를 추천한다 제철 생선 5~6가지 구성에 평소 접하지 못했던 부위까지 색다르게 즐길 수 있다
... """

>>> for i in split_sentences(text):
...     print(i)
...
```
```
미리 예약을 할 수 있는 시스템으로 합리적인 가격에 여러 종류의 생선, 그리고 다양한 부위를 즐길 수 있기 때문이다
계절에 따라 모둠회의 종류는 조금씩 달라지지만 자주 올려주는 참돔 마스까와(껍질만 끓는 물에 익힌 것)는 특히 맛이 매우 좋다
일반 모둠회도 좋지만 좀 더 특별한 맛을 즐기고 싶다면 특수 부위 모둠회를 추천한다
제철 생선 5~6가지 구성에 평소 접하지 못했던 부위까지 색다르게 즐길 수 있다
```
```python
>>> from kss import split_sentences
>>> text = """
... 미리 예약을 할 수 있는 시스템으로 합리적인 가격에 여러 종류의 생선, 그리고 다양한 부위를 즐길 수 있기 때문이다 계절에 따라 모둠회의 종류는 조금씩 달라지지만 자주 올려주는 참돔 마스까와(껍질만 끓는 물에 익힌 것)는 특히 맛이 매우 좋다 일반 모둠회도 좋지만 좀 더 특별한 맛을 즐기고 싶다면 특수 부위 모둠회를 추천한다 제철 생선 5~6가지 구성에 평소 접하지 못했던 부위까지 색다르게 즐길 수 있다
... """

>>> for i in split_sentences(text, safe=True):
...     print(i)
...
```
```
미리 예약을 할 수 있는 시스템으로 합리적인 가격에 여러 종류의 생선, 그리고 다양한 부위를 즐길 수 있기 때문이다
계절에 따라 모둠회의 종류는 조금씩 달라지지만 자주 올려주는 참돔 마스까와(껍질만 끓는 물에 익힌 것)는 특히 맛이 매우 좋다 일반 모둠회도 좋지만 좀 더 특별한 맛을 즐기고 싶다면 특수 부위 모둠회를 추천한다
제철 생선 5~6가지 구성에 평소 접하지 못했던 부위까지 색다르게 즐길 수 있다
```
<br>

### 2. `split_chunks`
- Collects the sentences and creates chunks of `max_length` or less.
```python
>>> from kss import split_chunks

>>> s = "NoSQL이라고 하는 말은 No 'English'라고 하는 말과 마찬가지다. 세상에는 영어 말고도 수많은 언어가 존재한다. MongoDB에서 사용하는 쿼리 언어와 CouchDB에서 사용하는 쿼리 언어는 서로 전혀 다르다. 그럼에도 이 두 쿼리 언어는 같은 NoSQL 카테고리에 속한다. 어쨌거나 SQL이 아니기 때문이다. 또한 NoSQL이 No RDBMS를 의미하지는 않는다. BerkleyDB같은 예외가 있기 때문이다. 그리고 No RDBMS가 NoSQL인 것도 아니다. SQL호환 레이어를 제공하는 KV-store라는 예외가 역시 존재한다. 물론 KV-store의 특징상 range query를 where절에 넣을 수 없으므로 완전한 SQL은 못 되고 SQL의 부분집합 정도를 제공한다."
>>> for chunk in split_chunks(s, max_length=128):
...    print(chunk)
```
```python
ChunkWithIndex(start=0, text="NoSQL이라고 하는 말은 No 'English'라고 하는 말과 마찬가지다. 세상에는 영어 말고도 수많은  언어가 존재한다. MongoDB에서 사용하는 쿼리 언어와 CouchDB에서 사용하는 쿼리 언어는 서로 전혀 다르다.")
ChunkWithIndex(start=124, text='그럼에도 이 두 쿼리 언어는 같은 NoSQL 카테고리에 속한다. 어쨌거나 SQL이 아니기 때문이다. 또한 NoSQL이 No RDBMS를 의미하지는 않는다. BerkleyDB같은 예외가 있기 때문이다.')
ChunkWithIndex(start=236, text='그리고 No RDBMS가 NoSQL인 것도 아니다. SQL호환 레이어를 제공하는 KV-store라는 예외가 역 시 존재한다.')
ChunkWithIndex(start=305, text='물론 KV-store의 특징상 range query를 where절에 넣을 수 없으므로 완전한 SQL은 못 되고 SQL의 부분집합 정도를 제공한다.')
```
<br>

- If `overlap` is `True`, it will be chunked similar with sliding window.
```python
>>> from kss import split_chunks

>>> s = "NoSQL이라고 하는 말은 No 'English'라고 하는 말과 마찬가지다. 세상에는 영어 말고도 수많은 언어가 존재한다. MongoDB에서 사용하는 쿼리 언어와 CouchDB에서 사용하는 쿼리 언어는 서로 전혀 다르다. 그럼에도 이 두 쿼리 언어는 같은 NoSQL 카테고리에 속한다. 어쨌거나 SQL이 아니기 때문이다. 또한 NoSQL이 No RDBMS를 의미하지는 않는다. BerkleyDB같은 예외가 있기 때문이다. 그리고 No RDBMS가 NoSQL인 것도 아니다. SQL호환 레이어를 제공하는 KV-store라는 예외가 역시 존재한다. 물론 KV-store의 특징상 range query를 where절에 넣을 수 없으므로 완전한 SQL은 못 되고 SQL의 부분집합 정도를 제공한다."
>>> for chunk in split_chunks(s, max_length=128, overlap=True):
...    print(chunk)
```
```python
ChunkWithIndex(start=0, text="NoSQL이라고 하는 말은 No 'English'라고 하는 말과 마찬가지다. 세상에는 영어 말고도 수많은  언어가 존재한다. MongoDB에서 사용하는 쿼리 언어와 CouchDB에서 사용하는 쿼리 언어는 서로 전혀 다르다.")
ChunkWithIndex(start=43, text='세상에는 영어 말고도 수많은 언어가 존재한다. MongoDB에서 사용하는 쿼리 언어와 CouchDB에서 사용하는 쿼리 언어는 서로 전혀 다르다. 그럼에도 이 두 쿼리 언어는 같은 NoSQL 카테고리에 속한다.')
ChunkWithIndex(start=69, text='MongoDB에서 사용하는 쿼리 언어와 CouchDB에서 사용하는 쿼리 언어는 서로 전혀 다르다. 그럼 에도 이 두 쿼리 언어는 같은 NoSQL 카테고리에 속한다. 어쨌거나 SQL이 아니기 때문이다.')
ChunkWithIndex(start=124, text='그럼에도 이 두 쿼리 언어는 같은 NoSQL 카테고리에 속한다. 어쨌거나 SQL이 아니기 때문이다. 또한 NoSQL이 No RDBMS를 의미하지는 않는다. BerkleyDB같은 예외가 있기 때문이다.')
ChunkWithIndex(start=180, text='또한 NoSQL이 No RDBMS를 의미하지는 않는다. BerkleyDB같은 예외가 있기 때문이다. 그리고 No RDBMS가 NoSQL인 것도 아니다. SQL호환 레이어를 제공하는 KV-store라는 예외가 역시 존재한다.')
ChunkWithIndex(start=236, text='그리고 No RDBMS가 NoSQL인 것도 아니다. SQL호환 레이어를 제공하는 KV-store라는 예외가 역 시 존재한다. 물론 KV-store의 특징상 range query를 where절에 넣을 수 없으므로 완전한 SQL은 못 되고 SQL의 부분집합 정도를 제공한다.')
```
<br><br>

## Updates
- upgrade : `pip install kss --upgrade` 
- you can check update notes [here](https://github.com/hyunwoongko/kss/blob/main/UPDATES.md).
```consol
PyPI upload instructions

1. test upload
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

2. pypi upload
twine upload dist/*
```
<br><br>

## Reference
- [KSS C++](https://github.com/likejazz/korean-sentence-splitter)
- [KSS Docs](http://docs.likejazz.com/kss/)
- [PyPI](https://pypi.org/project/kss/)

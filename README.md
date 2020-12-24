# Korean Sentence Splitter
Split Korean text into sentences using heuristic algorithm.
<br><br>

## Install
```console
pip install kss
```
<br><br>

## Usage
### 1. `split_sentences`
- Split sentences from text
```python
from kss import split_sentences

s = "회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요 다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다 강남역 맛집 토끼정의 외부 모습."
for sent in split_sentences(s):
    print(sent)
```
```
회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요
다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다
강남역 맛집 토끼정의 외부 모습.
```
<br>

### 2. `split_chunks`
- Collects the sentences and creates chunks of `max_length` or less.
```python
from kss import split_chunks

s = "NoSQL이라고 하는 말은 No 'English'라고 하는 말과 마찬가지다. 세상에는 영어 말고도 수많은 언어가 존재한다. MongoDB에서 사용하는 쿼리 언어와 CouchDB에서 사용하는 쿼리 언어는 서로 전혀 다르다. 그럼에도 이 두 쿼리 언어는 같은 NoSQL 카테고리에 속한다. 어쨌거나 SQL이 아니기 때문이다. 또한 NoSQL이 No RDBMS를 의미하지는 않는다. BerkleyDB같은 예외가 있기 때문이다. 그리고 No RDBMS가 NoSQL인 것도 아니다. SQL호환 레이어를 제공하는 KV-store라는 예외가 역시 존재한다. 물론 KV-store의 특징상 range query를 where절에 넣을 수 없으므로 완전한 SQL은 못 되고 SQL의 부분집합 정도를 제공한다."
for chunk in split_chunks(s, max_length=128):
    print(chunk)
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
from kss import split_chunks

s = "NoSQL이라고 하는 말은 No 'English'라고 하는 말과 마찬가지다. 세상에는 영어 말고도 수많은 언어가 존재한다. MongoDB에서 사용하는 쿼리 언어와 CouchDB에서 사용하는 쿼리 언어는 서로 전혀 다르다. 그럼에도 이 두 쿼리 언어는 같은 NoSQL 카테고리에 속한다. 어쨌거나 SQL이 아니기 때문이다. 또한 NoSQL이 No RDBMS를 의미하지는 않는다. BerkleyDB같은 예외가 있기 때문이다. 그리고 No RDBMS가 NoSQL인 것도 아니다. SQL호환 레이어를 제공하는 KV-store라는 예외가 역시 존재한다. 물론 KV-store의 특징상 range query를 where절에 넣을 수 없으므로 완전한 SQL은 못 되고 SQL의 부분집합 정도를 제공한다."
for chunk in split_chunks(s, max_length=128, overlap=True):
    print(chunk)
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
### version 0.0.2
- Fixed a bug in a sentence with single quotes.
- Related test : `test_single_quotes` in `tests/test_kss.py`
### version 0.0.3
- Fixed a bug about quotation marks misalignment.
  - https://github.com/likejazz/korean-sentence-splitter/issues/4
  - https://github.com/likejazz/korean-sentence-splitter/issues/8
- Related test : `test_quote_misalignment` in `tests/test_kss.py`
### version 2.0.0
- python-kss became the official version of kss.
- From now on, you can install python-kss using `pip install kss`.
- Add `split_chunks` function that create chunks from text.
### version 2.0.1
- Fix quote realignment bugs (list out of range)
- Related test : `test_realignment` in `tests/test_kss.py`
### version 2.1
- Add exception cases about prime and apostrophe
    - number + ' or " : [1900's, 5'30, 60" inch]
    - alphabet + ' + s : [He's, Jimmy's, KAKAO's]
    - any other frequent cases : I'm, I'd, I'll, ...
- Add new eomi "죠"
  - input : "그땐 그랬죠 이젠 괜찮아요"
  - output : ["그땐 그랬죠", "이젠 괜찮아요"]
- And new spliting cases
  - 볐다 (후볐다)
  - 몄다 (꾸몄다)
  - 폈다 (종이 등을 폈다)
  - 셨다 (높힘말)
- Fix `split_chunks` bug
  - Problems with getting location information correctly if duplicate sentences are found during the chunking

<br><br>

## Reference
- [KSS C++](https://github.com/likejazz/korean-sentence-splitter)
- [KSS Docs](http://docs.likejazz.com/kss/)
- [PyPI](https://pypi.org/project/kss/)

# Korean Sentence Splitter-fix
기 kss library의 사용성 및 일부 성능 개선을 위한 수정 repo입니다.
<br>

## Update points from kss
기본적으로 kss는 형태소분석과정 없이 종결형에 사용되는 음절(다/요/.!?)을 골라내어 이전/이후 음절을 매칭하여 문장을 구분합니다.   
이로 kss는 처리속도가 아주 빠른 반면, 문장 종결 부호(".", "!", "?")가 잘 들어가 있는 뉴스와 같은 한글 텍스트에서는 분리하지 않아야 하는 곳 까지 분리하는 문제가 있습니다.

이에 따라 다음을 수정하였습니다.

1. 사용자가 알고리즘 적용 정도를 선택할 수 있도록 `safe` parameter 추가(3단계로 확장)

- 기 kss 문제 예시

  ```
  '국내에 판매하는 OEM 수입차의 판매량이 2017년까지 하락세를 보이다 지난해 반등했으며 수입차 대비 비중도 높아질 전망이다.'
  -> ['국내에 판매하는 OEM 수입차의 판매량이 2017년까지 하락세를 보이다', '지난해 반등했으며 수입차 대비 비중도 높아질 전망이다.']
  '전과 8범 A씨는 지난 17일 전자발찌를 끊고 도주하다 붙잡혀 전자발찌 부착기간이 2020년 8월14일까지 늘었다.'
  -> ['전과 8범 A씨는 지난 17일 전자발찌를 끊고 도주하다', '붙잡혀 전자발찌 부착기간이 2020년 8월14일까지 늘었다.']
  ```

- 변경사항

  - 문장 종결 부호(".", "!", "?")가 존재하는 경우에만 한정하여 kss 알고리즘을 적용하는 `safe=2` 옵션 추가

  ```
  >>> kss.split_sentences(text, safe=2)
  ['국내에 판매하는 OEM 수입차의 판매량이 2017년까지 하락세를 보이다 지난해 반등했으며 수입차 대비 비중도 높아질 전망이다.']
  ```

  - kss.split_sentences(text, safe=0)은 기 kss.split_sentences(text)와,
    kss.split_sentences(text, safe=1)은 기 kss.split_sentences(text, safe=True)와 동일

2. QuoteException 조건 수정

   - 기 kss 문제 예시

     `quote+숫자` 형태의 경우,  time 또는 inch로 인식

   ```
   >>> text= """한 시민은 "코로나로 인해 '2020년'이란 시간은 멈춘 듯 하다"고 말했다."""
   >>> kss.split_sentences(text)
   ["한 시민은 \"코로나로 인해 \'2020년\'이란 시간은 멈춘 듯 하다", "고 말했다.\""]
   ```

   - 수정사항

     time 및 inch를 위한 조건에서 해당 기호 앞이 공백인 경우는 제외

3. 기타 수정사항

   - 각 사항에 대한 test case 추가
   
- corpus에 대한 테스트 시행 및 결과 추가
   
     <br>
   

------

# Korean Sentence Splitter

Split Korean text into sentences using heuristic algorithm.

<br>

## Install
```console
pip install kss
```
<br><br>

## Performance Evaluation
- You can check simple performance evaluation [here](https://github.com/hyunwoongko/kss/blob/main/EVALUATION.md).
- There are 6 difficult example documents for a sentence segmentation.
<br><br><br>

## Usage
### 1. `split_sentences`
- Split sentences from text
```python
>>> from kss import split_sentences
>>> text = "미리 예약을 할 수 있는 시스템으로 합리적인 가격에 여러 종류의 생선, 그리고 다양한 부위를 즐길 수 있기 때문이다 계절에 따라 모둠회의 종류는 조금씩 달라지지만 자주 올려주는 참돔 마스까와(껍질만 끓는 물에 익힌 것)는 특히 맛이 매우 좋다 일반 모둠회도 좋지만 좀 더 특별한 맛을 즐기고 싶다면 특수 부위 모둠회를 추천한다 제철 생선 5~6가지 구성에 평소 접하지 못했던 부위까지 색다르게 즐길 수 있다"
>>> split_sentences(text)
```
```python
['미리 예약을 할 수 있는 시스템으로 합리적인 가격에 여러 종류의 생선, 그리고 다양한 부위를 즐길 수 있기 때문이다', 
'계절에 따라 모둠회의 종류는 조금씩 달라지지만 자주 올려주는 참돔 마스까와(껍질만 끓는 물에 익힌 것)는 특히 맛이 매우 좋다', 
'일반 모둠회도 좋지만 좀 더 특별한 맛을 즐기고 싶다면 특수 부위 모둠회를 추천한다', 
'제철 생선 5~6가지 구성에 평소 접하지 못했던 부위까지 색다르게 즐길 수 있다']
```
<br>

- If you want more safe segmentation, set the argument `safe = True`
```python
>>> from kss import split_sentences
>>> text = "미리 예약을 할 수 있는 시스템으로 합리적인 가격에 여러 종류의 생선, 그리고 다양한 부위를 즐길 수 있기 때문이다 계절에 따라 모둠회의 종류는 조금씩 달라지지만 자주 올려주는 참돔 마스까와(껍질만 끓는 물에 익힌 것)는 특히 맛이 매우 좋다 일반 모둠회도 좋지만 좀 더 특별한 맛을 즐기고 싶다면 특수 부위 모둠회를 추천한다 제철 생선 5~6가지 구성에 평소 접하지 못했던 부위까지 색다르게 즐길 수 있다"
>>> split_sentences(text, safe=True)
```
```python
['미리 예약을 할 수 있는 시스템으로 합리적인 가격에 여러 종류의 생선, 그리고 다양한 부위를 즐길 수 있기 때문이다', 
'계절에 따라 모둠회의 종류는 조금씩 달라지지만 자주 올려주는 참돔 마스까와(껍질만 끓는 물에 익힌 것)는 특히 맛이 매우 좋다 일반 모둠회도 좋지만 좀 더 특별한 맛을 즐기고 싶다면 특수 부위 모둠회를 추천한다', 
'제철 생선 5~6가지 구성에 평소 접하지 못했던 부위까지 색다르게 즐길 수 있다']
```
<br>

### 2. `split_chunks`
- Collects the sentences and creates chunks of `max_length` or less.
```python
>>> from kss import split_chunks
>>> text = "NoSQL이라고 하는 말은 No 'English'라고 하는 말과 마찬가지다. 세상에는 영어 말고도 수많은 언어가 존재한다. MongoDB에서 사용하는 쿼리 언어와 CouchDB에서 사용하는 쿼리 언어는 서로 전혀 다르다. 그럼에도 이 두 쿼리 언어는 같은 NoSQL 카테고리에 속한다. 어쨌거나 SQL이 아니기 때문이다. 또한 NoSQL이 No RDBMS를 의미하지는 않는다. BerkleyDB같은 예외가 있기 때문이다. 그리고 No RDBMS가 NoSQL인 것도 아니다. SQL호환 레이어를 제공하는 KV-store라는 예외가 역시 존재한다. 물론 KV-store의 특징상 range query를 where절에 넣을 수 없으므로 완전한 SQL은 못 되고 SQL의 부분집합 정도를 제공한다."
>>> split_chunks(text, max_length=128)
```
```python
[ChunkWithIndex(start=0, text="NoSQL이라고 하는 말은 No 'English'라고 하는 말과 마찬가지다. 세상에는 영어 말고도 수많은  언어가 존재한다. MongoDB에서 사용하는 쿼리 언어와 CouchDB에서 사용하는 쿼리 언어는 서로 전혀 다르다."),
ChunkWithIndex(start=124, text='그럼에도 이 두 쿼리 언어는 같은 NoSQL 카테고리에 속한다. 어쨌거나 SQL이 아니기 때문이다. 또한 NoSQL이 No RDBMS를 의미하지는 않는다. BerkleyDB같은 예외가 있기 때문이다.'),
ChunkWithIndex(start=236, text='그리고 No RDBMS가 NoSQL인 것도 아니다. SQL호환 레이어를 제공하는 KV-store라는 예외가 역 시 존재한다.'),
ChunkWithIndex(start=305, text='물론 KV-store의 특징상 range query를 where절에 넣을 수 없으므로 완전한 SQL은 못 되고 SQL의 부분집합 정도를 제공한다.')]
```
<br>

- If `overlap` is `True`, it will be chunked similar with sliding window.
```python
>>> from kss import split_chunks
>>> text = "NoSQL이라고 하는 말은 No 'English'라고 하는 말과 마찬가지다. 세상에는 영어 말고도 수많은 언어가 존재한다. MongoDB에서 사용하는 쿼리 언어와 CouchDB에서 사용하는 쿼리 언어는 서로 전혀 다르다. 그럼에도 이 두 쿼리 언어는 같은 NoSQL 카테고리에 속한다. 어쨌거나 SQL이 아니기 때문이다. 또한 NoSQL이 No RDBMS를 의미하지는 않는다. BerkleyDB같은 예외가 있기 때문이다. 그리고 No RDBMS가 NoSQL인 것도 아니다. SQL호환 레이어를 제공하는 KV-store라는 예외가 역시 존재한다. 물론 KV-store의 특징상 range query를 where절에 넣을 수 없으므로 완전한 SQL은 못 되고 SQL의 부분집합 정도를 제공한다."
>>> split_chunks(text, max_length=128, overlap=True):
```
```python
[ChunkWithIndex(start=0, text="NoSQL이라고 하는 말은 No 'English'라고 하는 말과 마찬가지다. 세상에는 영어 말고도 수많은  언어가 존재한다. MongoDB에서 사용하는 쿼리 언어와 CouchDB에서 사용하는 쿼리 언어는 서로 전혀 다르다."),
ChunkWithIndex(start=43, text='세상에는 영어 말고도 수많은 언어가 존재한다. MongoDB에서 사용하는 쿼리 언어와 CouchDB에서 사용하는 쿼리 언어는 서로 전혀 다르다. 그럼에도 이 두 쿼리 언어는 같은 NoSQL 카테고리에 속한다.'),
ChunkWithIndex(start=69, text='MongoDB에서 사용하는 쿼리 언어와 CouchDB에서 사용하는 쿼리 언어는 서로 전혀 다르다. 그럼 에도 이 두 쿼리 언어는 같은 NoSQL 카테고리에 속한다. 어쨌거나 SQL이 아니기 때문이다.'),
ChunkWithIndex(start=124, text='그럼에도 이 두 쿼리 언어는 같은 NoSQL 카테고리에 속한다. 어쨌거나 SQL이 아니기 때문이다. 또한 NoSQL이 No RDBMS를 의미하지는 않는다. BerkleyDB같은 예외가 있기 때문이다.'),
ChunkWithIndex(start=180, text='또한 NoSQL이 No RDBMS를 의미하지는 않는다. BerkleyDB같은 예외가 있기 때문이다. 그리고 No RDBMS가 NoSQL인 것도 아니다. SQL호환 레이어를 제공하는 KV-store라는 예외가 역시 존재한다.'),
ChunkWithIndex(start=236, text='그리고 No RDBMS가 NoSQL인 것도 아니다. SQL호환 레이어를 제공하는 KV-store라는 예외가 역 시 존재한다. 물론 KV-store의 특징상 range query를 where절에 넣을 수 없으므로 완전한 SQL은 못 되고 SQL의 부분집합 정도를 제공한다.')]
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

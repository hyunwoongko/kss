# Korean Sentence Splitter
Split Korean text into sentences using heuristic algorithm.
<br><br>

## Install
```console
pip install kss
```
<br><br>

## Usage
```python
import kss

s = "회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요 다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다 강남역 맛집 토끼정의 외부 모습."
for sent in kss.split_sentences(s):
    print(sent)
```
```
회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요
다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다
강남역 맛집 토끼정의 외부 모습.
```
<br><br>

## Bugfix Notes
### version 0.0.2
- 작은 따옴표가 들어간 문장에서 생기는 버그를 해결했습니다.
- 관련 테스트 : `tests/test_kss.py`의 `test_single_quotes`
### version 0.0.3
- 따옴표가 misalign되는 경우 문장 분절이 되지 않는 이슈를 해결하였습니다.
  - https://github.com/likejazz/korean-sentence-splitter/issues/4
  - https://github.com/likejazz/korean-sentence-splitter/issues/8
- 관련 테스트 : `tests/test_kss.py`의 `test_quote_misalignment`
<br><br>

## Reference
- [KSS C++](https://github.com/likejazz/korean-sentence-splitter)
- [KSS Docs](http://docs.likejazz.com/kss/)


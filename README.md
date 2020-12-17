# python-kss

## Objective
- 박상길님의 KSS(Korean Sentence Splitter)는 cython으로 구현되어있습니다.
- Cython의 빠른 속도는 장점이지만 `cythonize`때문에 cython이 설치된 환경에서만 설치 가능합니다.
- 이 때문에 현재의 KSS는 프로젝트 디펜던시에 추가하기 까다롭습니다.
- 이러한 문제를 해결하기 위해 순수 파이썬만 이용하여 KSS를 재구현합니다.
<br><br>

## Install
- pip를 이용하여 설치할 수 있습니다.
```console
pip install python-kss
```
<br><br>

## Usage
- 기존 KSS 사용법과 100% 동일합니다.
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
- 따옴표가 misalign되는 경우 문장 분절이 되지 않는 이슈가 있었습니다.
  - https://github.com/likejazz/korean-sentence-splitter/issues/4
  - https://github.com/likejazz/korean-sentence-splitter/issues/8
- 기존 kss 레포에서는 특정 케이스(n't, e's 등)에 대한 예외처리만 수행하는데, 이 방식으로는 모든 misalignment를 처리할 수 없습니다.
- 따라서 misalignment가 발생 할 경우 문제가 발생한 부분을 제외한 나머지 부분을 재귀적으로 처리하여 최종적으로 병합하는 방식을 도입했습니다.
- 관련 테스트 : `tests/test_kss.py`의 `test_quote_misalignment`
<br><br>

## Reference
- [KSS 깃허브 레포](https://github.com/likejazz/korean-sentence-splitter)
- [KSS 도큐먼트](http://docs.likejazz.com/kss/)
- [형태소분석기에 탑재된 문장 분리기 분석](http://semantics.kr/%ed%95%9c%ea%b5%ad%ec%96%b4-%ed%98%95%ed%83%9c%ec%86%8c-%eb%b6%84%ec%84%9d%ea%b8%b0-%eb%b3%84-%eb%ac%b8%ec%9e%a5-%eb%b6%84%eb%a6%ac-%ec%84%b1%eb%8a%a5%eb%b9%84%ea%b5%90/)


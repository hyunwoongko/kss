## Update Notes
#### python-kss 0.0.2
- Fixed a bug in a sentence with single quotes.
- Related test : `test_single_quotes` in `tests/test_kss.py`
#### python-kss 0.0.3
- Fixed a bug about quotation marks misalignment.
  - https://github.com/likejazz/korean-sentence-splitter/issues/4
  - https://github.com/likejazz/korean-sentence-splitter/issues/8
- Related test : `test_quote_misalignment` in `tests/test_kss.py`
#### kss 2.0.0
- python-kss became the official version of kss.
- From now on, you can install python-kss using `pip install kss`.
- Add `split_chunks` function that create chunks from text.
#### kss 2.0.1
- Fix quote realignment bugs (list out of range)
- Related test : `test_realignment` in `tests/test_kss.py`
#### kss 2.1.0
- Add exception cases about prime and apostrophe
    - number + ' or " : [1900's, 5'30, 60" inch]
    - alphabet + ' + s : [He's, Jimmy's, KAKAO's]
    - any other frequent cases : I'm, I'd, I'll, ...
- Add new eomi (죠)
  - input : "그땐 그랬죠 이젠 괜찮아요"
  - output : ["그땐 그랬죠", "이젠 괜찮아요"]
- And new splitting cases
  - 볐다 (후볐다)
  - 몄다 (꾸몄다)
  - 폈다 (종이 등을 폈다)
  - 셨다 (높힘말)
  - 켰다 (불 등을 켰다)
- Fix `split_chunks` bug
  - Problems with getting location information correctly if duplicate sentences are found during the chunking
#### kss 2.1.1
- And new splitting cases
  - 려요 (드려요)
  - 거요 (이거요)
  - 겨요 (이겨요)
  - 니요 (아니요), 니죠 (아니죠)
  - ㄱ, ㄴ, ㄷ, ㄹ, ㅂ, ㅅ, ㅇ, ㅈ, ㅊ, ㅋ, ㅌ, ㅎ (punctuation)
  - ㅜ, ㅠ, ㅡ, ㅗ (punctuation)
  - ）, ], ］, 〕, 】, }, ｝, 〕, 〉, >, 》, 」, 』 (punctuation)

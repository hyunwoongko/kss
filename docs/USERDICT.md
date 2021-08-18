# Adding words to user dictionary
Kss 3.0 and later, you can add words to prevent segmentation errors.
Follow the appropriate method for each morpheme backend.

## 1. Pynori Backend
### 1.1. Find path of dictionary
If you are using the Pynori backend, you can add user words to `/kss/pynori/resources/userdict.txt` in the kss installation path.
The Python library is installed in the `site-package` path when installed with pip. If it is difficult to access this path, 
it can be helpful [to install from the source code.](https://github.com/hyunwoongko/kss#12-install-from-source-codes).

### 1.2. Syntax of user dictionary
Please refer to following syntax to use user dictionary.

- You can use comment line by `#` like Python language.
- [The single word (단일어)](https://ko.wikipedia.org/wiki/%EB%8B%A8%EC%9D%BC%EC%96%B4]) must be written one per line.
- [The compound words (복합어)](https://namu.wiki/w/%EB%B3%B5%ED%95%A9%EC%96%B4) must be listed the original word and sub-words by whitespace.
```
# 1. EXAMPLE OF SINGLE WORDS
대한민국
라이브러리
Kss

# 2. EXAMPLE OF COMPOUND WORDS
자연어처리 자연어 처리
서울시 서울 시
```

## 2. Mecab Backend

Refer to [mecab-ko-dict](https://bitbucket.org/eunjeon/mecab-ko-dic/src/df15a487444d88565ea18f8250330276497cc9b9/final/user-dic/README.md).

## 3. Non-morpheme Backend

Unfortunately, Kss only provides the user dictionary feature for the Morpheme backend. If you want to use this feature, please use the Morpheme backend.
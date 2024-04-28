<h1 align="center">
KSS: Korean String processing Suite
</h1>

<p align="center">
    <a href="https://github.com/hyunwoongko/kss/releases"><img alt="GitHub release" src="https://img.shields.io/github/release/hyunwoongko/kss.svg"></a> <a href="https://github.com/hyunwoongko/kss/issues"><img alt="Issues" src="https://img.shields.io/github/issues/hyunwoongko/kss"></a> <a href="https://github.com/hyunwoongko/kss/actions"><img alt="Tests on Ubuntu" src="https://github.com/hyunwoongko/kss/actions/workflows/test_ubuntu.yaml/badge.svg"></a> <a href="https://github.com/hyunwoongko/kss/actions"><img alt="Tests on MacOS" src="https://github.com/hyunwoongko/kss/actions/workflows/test_macos.yaml/badge.svg"></a> <a href="https://github.com/hyunwoongko/kss/actions"><img alt="Tests on Windows" src="https://github.com/hyunwoongko/kss/actions/workflows/test_windows.yaml/badge.svg"></a>
</p>


KSS is a Korean string processing suite that provides various functions for processing Korean strings. It is designed to be simple and easy to use, and it is designed to be used in various fields such as natural language processing, data preprocessing, and data analysis.

### What's New:
- April 27, 2024 [Released Kss 6.0 Python](https://github.com/hyunwoongko/kss/releases/tag/6.0.0).
- March 31, 2024 [Released Kss 5.0 Python](https://github.com/hyunwoongko/kss/releases/tag/5.1.0).
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

## Usage
### 1. Basic Usage
All functions can be used by creating an instance of the Kss class and calling the instance with the inputs.
```python
from kss import Kss

module = Kss("MODULE_NAME")
output = module("YOUR_INPUT_STRING", **kwargs)
```

### 2. Available Modules

If you want to check the available modules, you can use the `available()` function.
```python
from kss import Kss

Kss.available()
```
```python
['augment', 'collocate', 'g2p', 'hangulize', 'split_hanja', 'is_hanja', 'hanja2hangul', 'h2j', 'h2hcj', 'j2h', 'j2hcj', 'hcj2h', 'hcj2j', 'is_jamo', 'is_jamo_modern', 'is_hcj', 'is_hcj_modern', 'is_hangul_char', 'select_josa', 'combine_josa', 'extract_keywords', 'split_morphemes', 'paradigm', 'anonymize', 'clean_news', 'is_completed_form', 'get_all_completed_form_hangul_chars', 'get_all_incompleted_form_hangul_chars', 'filter_out', 'half2full', 'reduce_char_repeats', 'reduce_emoticon_repeats', 'remove_invisible_chars', 'normalize', 'preprocess', 'qwerty', 'romanize', 'is_unsafe', 'split_sentences', 'correct_spacing', 'summarize_sentences']
```

### 3. Checking the usage of each module
If you want to check the usage of each module, you can use the `help()` function.
```python
from kss import Kss

module = Kss("split_sentences")
module.help()
```

```text
Split texts into sentences.

Args:
    text (Union[str, List[str], Tuple[str]]): single text or list/tuple of texts
    backend (str): morpheme analyzer backend. 'mecab', 'pecab', 'punct' are supported
    num_workers (Union[int, str]): the number of multiprocessing workers
    strip (bool): strip all sentences or not
    return_morphemes (bool): whether to return morphemes or not
    ignores (List[str]): list of strings to ignore

Returns:
    Union[List[str], List[List[str]]]: outputs of sentence splitting

Examples:
    >>> from kss import Kss
    >>> split_sentences = Kss("split_sentences")
    >>> text = "회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요 다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다 강남역 맛집 토끼정의 외부 모습."
    >>> split_sentences(text)
    ['회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요', '다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다', '강남역 맛집 토끼정의 외부 모습.']
```
### 4. Multiprocessing
If you input a list of strings, Kss will automatically use multiprocessing to process the strings in parallel.
And you can set the number of processes to use by setting the `num_workers` parameter.
If you input `num_workers < 2`, Kss will not use multiprocessing.

```python
from kss import Kss

module = Kss("MODULE_NAME")

# using all cores
output = module(["YOUR_INPUT_STRING1", "YOUR_INPUT_STRING2", ...], **kwargs)
# using 4 cores
output = module(["YOUR_INPUT_STRING1", "YOUR_INPUT_STRING2", ...], num_workers=4, **kwargs)
# using 1 core (no multiprocessing)
output = module(["YOUR_INPUT_STRING1", "YOUR_INPUT_STRING2", ...], num_workers=1, **kwargs)
``` 

### 5. Backward Compatibility
The old version of Kss used functional usage. KSS also supports this for backward compatibility.
```python
from kss import split_sentences

output = split_sentences("YOUR_INPUT_STRING", **kwargs)
```

### 6. Alias of module names
Because there are so many modules in Kss, user may have difficulty remembering the names of each module.
Kss provides aliases for some modules to make it easier to use them.
```python
from kss import Kss

module_1 = Kss("split_morphemes")
module_2 = Kss("tokenize")
# For example, 'split_morphemes' module can be loaded by using the alias named 'tokenize'.
```

You can check the alias of each module by using the `alias()` function.
```python
from kss import Kss

Kss.alias()
```

```python
{'aug': 'augment', 'augmentation': 'augment', 'collocation': 'collocate', 'hangulization': 'hangulize', 'hangulisation': 'hangulize', 'hangulise': 'hangulize', 'hanja': 'hanja2hangul', 'hangul2jamo': 'h2j', 'hangul2hcj': 'h2hcj', 'jamo2hangul': 'j2h', 'jamo2hcj': 'j2hcj', 'hcj2hangul': 'hcj2h', 'hcj2jamo': 'hcj2j', 'josa': 'select_josa', 'keyword': 'extract_keywords', 'keywords': 'extract_keywords', 'morpheme': 'split_morphemes', 'morphemes': 'split_morphemes', 'annonymization': 'anonymize', 'news_cleaning': 'clean_news', 'news': 'clean_news', 'completed_form': 'is_completed_form', 'completed': 'is_completed_form', 'filter': 'filter_out', 'reduce_repeats': 'reduce_char_repeats', 'reduce_char': 'reduce_char_repeats', 'reduce_chars': 'reduce_char_repeats', 'reduce_emoticon': 'reduce_emoticon_repeats', 'reduce_emoticons': 'reduce_emoticon_repeats', 'reduce_emo': 'reduce_emoticon_repeats', 'remove_invisible': 'remove_invisible_chars', 'invisible_chars': 'remove_invisible_chars', 'invisible': 'remove_invisible_chars', 'normalization': 'normalize', 'normalisation': 'normalize', 'normalise': 'normalize', 'preprocessing': 'preprocess', 'prep': 'preprocess', 'romanization': 'romanize', 'romanisation': 'romanize', 'romanise': 'romanize', 'safety': 'is_unsafe', 'check_safety': 'is_unsafe', 'sentence': 'split_sentences', 'sentences': 'split_sentences', 'sent_split': 'split_sentences', 'sent_splits': 'split_sentences', 'sents_split': 'split_sentences', 'split_sent': 'split_sentences', 'split_sents': 'split_sentences', 'spacing': 'correct_spacing', 'space': 'correct_spacing', 'spaces': 'correct_spacing', 'summarization': 'summarize_sentences', 'summarize': 'summarize_sentences', 'summ': 'summarize_sentences', 'morph': 'split_morphemes', 'morphs': 'split_morphemes', 'tokenize': 'split_morphemes', 'tokenization': 'split_morphemes', 'split_morph': 'split_morphemes', 'split_morphs': 'split_morphemes', 'morph_split': 'split_morphemes', 'morph_splits': 'split_morphemes', 'morphs_split': 'split_morphemes'}
```

## Supported Modules
Kss supports the following modules and there are the simple usages of each module in the following sections.

Because there are so many modules, I apologize for not being able to explain each one in detail.

<details>
<summary>1. augment</summary>

This augments text with synonym replacement method and, 
optionally it postprocesses the text by correcting josa.
For this, Kss uses the Korean wordnet from KAIST.

Args:
- text (`Union[str, List[str], Tuple[str]]`): single text or list of texts
- replacement_ratio (`float`): ratio of words to be replaced
- josa_correction (`bool`): whether to correct josa or not
- num_workers (`Union[int, str]`): the number of multiprocessing workers
- backend (`str`): morpheme analyzer backend. 'mecab', 'pecab' are supported
- verbose (`bool`): whether to print verbose outputs or not

Returns:
- `Union[str, List[str]]`: augmented text or list of augmented texts

Examples:
```python
>>> from kss import Kss
>>> augment = Kss("augment")
>>> text = "앞서 지난해 11월, 보이저 1호는 명령을 수신하고 수행하는 데엔 문제가 없었지만 통신 장치에 문제가 생겨 과학·엔지니어링 데이터가 지구로 전송되지 않았던 바 있다. 당시 그들은 컴퓨터 시스템을 재시작하고 문제의 근본적인 원인을 파악하기 위해 명령을 보내려고 시도했고, 이달 1일 '포크'라는 명령을 보냈다."
>>> output = augment(text)
>>> print(output)
"앞서 지난해 11월, 보이저 1호는 명령을 수신하고 시행하는 데엔 문제가 없었지만 송신 장비에 문제가 생겨 과학·엔지니어링 데이터가 지구로 전송되지 않았던 바 있다. 당시 그들은 컴퓨터 시스템을 재시작하고 문제의 근본적인 원인을 파악하기 위해 명령을 보내려고 시도했고, 이달 1일 '포크'라는 명령을 보냈다."
```

References:
- This was copied from [KoEDA](https://github.com/toriving/KoEDA) and modified by Kss
</details>

<details>
<summary>2. collocate</summary>

This returns collocation (연어) of given words.
The collocation is a set of words that frequently appear together.

Args:
- text (`Union[str, List[str], Tuple[str]]`): single word or list of words
- num_workers (`Union[int, str]`): the number of multiprocessing workers
- verbose (`bool`): whether to print verbose outputs or not

Returns:
- `Union[dict, List[dict]]`: collocations and frequencies of words in text or list of collocations and frequencies

Examples:
```python
>>> from kss import Kss
>>> collocate = Kss("collocate")
>>> text = "먹"
>>> output = collocate(text)
>>> print(output)
{'verb': {'noun': [('것', 39), ('수', 29), ('음식', 23), ('등', 16), ('고기', 14), ('먹이', 14), ('때', 12), ('식물', 12), ('개고기', 9), ('젖', 9), ('겁', 7), ('시작', 7), ('후', 7), ('밥', 7), ('요리', 7), ('경우', 6), ('풀', 6), ('사람', 5), ('자살', 5), ('과일', 4), ('늑대', 4), ('마음', 4), ('나이', 4), ('애', 4), ('생선', 3), ('개', 3), ('죽', 3), ('양', 3), ('나무', 3), ('만큼', 3), ('물', 3), ('방법', 3), ('알', 3), ('떡볶이', 3), ('식사', 3), ('아침', 3), ('사과', 3), ('라면', 3), ('자기', 3), ('약', 3), ('점심', 3), ('때문', 3), ('조리', 3), ('떡', 2), ('접시', 2), ('국수', 2), ('일반적', 2), ('무엇', 2), ('파이', 2), ('만', 2), ('다음', 2), ('이후', 2), ('무리', 2), ('기록', 2), ('풍습', 2), ('동물', 2), ('식물질', 2), ('곤충', 2), ('이', 2), ('유제류', 2), ('새끼', 2), ('불고기', 2), ('한국', 2), ('한국식', 2), ('동안', 2), ('몸', 2), ('돼지고기', 2), ('잡식성', 2), ('기관', 2), ('제사장', 2), ('끼', 2), ('운동', 2), ('곡식', 2), ('궁중', 2), ('젖소', 2), ('우유', 2), ('고', 2), ('이야기', 2), ('정도', 2), ('일', 2), ('자리', 2), ('지역', 2), ('소화', 2), ('도중', 2), ('쓰레기', 2), ('저녁', 2), ('그', 2), ('뒤', 2), ('조', 2), ('고구마', 1), ('가지', 1), ('가시', 1), ('가지도', 1), ('아이', 1), ('쌈', 1), ('노출', 1), ('그다음', 1), ('근육', 1), ('아침상', 1), ('대로', 1), ('솔잎', 1), ('생', 1), ('중세', 1), ('어른', 1), ('성소', 1), ('집중적', 1), ('한번', 1), ('멜론', 1), ('입', 1), ('나뭇가지', 1), ('혀', 1), ('무시', 1), ('발견', 1), ('전후', 1), ('운반', 1), ('찬밥', 1), ('벌레', 1), ('남편', 1), ('하', 1), ('부인', 1), ('플랑크톤', 1), ('4', 1), ('미역국', 1), ('벨', 1), ('잔가지', 1), ('그중', 1), ('말', 1), ('소시지', 1), ('사냥', 1), ('카스', 1), ('따위', 1), ('레', 1), ('새', 1), ('내서', 1), ('인류', 1), ('소문', 1), ('수라', 1), ('곳', 1), ('항원', 1), ('구지가', 1), ('되새김', 1), ('사료', 1), ('하루', 1), ('문제', 1), ('큰곰', 1), ('비율', 1), ('6', 1), ('보리', 1), ('메조', 1), ('광', 1), ('물냉면', 1), ('살', 1), ('여공', 1), ('수영', 1), ('주변', 1), ('파리', 1), ('체액', 1), ('가운데', 1), ('시체', 1), ('구기', 1), ('해초', 1), ('호두', 1), ('엽전', 1), ('고추장', 1), ('300', 1), ('배설', 1), ('곰국', 1), ('노루', 1), ('대나무', 1), ('초식성', 1), ('부육', 1), ('종류', 1), ('남', 1), ('포장마차', 1), ('어묵', 1), ('특효', 1), ('약물', 1), ('노래', 1), ('어미', 1), ('맥', 1), ('털가죽', 1), ('뇌', 1), ('돌', 1), ('방식', 1), ('비빔밥', 1), ('진화', 1), ('콩', 1), ('탈', 1), ('신의주', 1), ('뜰', 1), ('하느님', 1), ('공화제', 1), ('물질', 1), ('초식', 1), ('간', 1), ('흑', 1), ('식품', 1), ('덮밥', 1), ('탐사선', 1), ('해산물', 1), ('내부', 1), ('3', 1), ('공격', 1), ('정', 1), ('대부분', 1), ('데', 1), ('연습', 1), ('오이', 1), ('성장', 1), ('볶음', 1), ('설', 1), ('스탈린', 1), ('형식', 1), ('골목', 1), ('나뭇잎', 1), ('주간', 1), ('잎', 1), ('된장찌개', 1), ('자매', 1), ('시간당', 1), ('말복', 1), ('구어', 1), ('말고기', 1), ('당나귀', 1), ('모습', 1), ('박테리아', 1), ('영양분', 1), ('부분', 1), ('가축', 1), ('그것', 1), ('가공품', 1), ('구이', 1), ('목', 1), ('기름', 1), ('휴식', 1), ('소스', 1), ('나무껍질', 1), ('쇠고기', 1), ('고착', 1), ('밝기', 1), ('짜장면', 1), ('날', 1), ('수액', 1), ('배달', 1), ('장면', 1), ('단어', 1), ('떡국', 1), ('찜', 1), ('문화권', 1), ('소형', 1), ('이전', 1), ('로', 1), ('노년', 1), ('난자', 1), ('돼지', 1), ('채집', 1), ('나라', 1), ('전', 1), ('육식성', 1), ('격려', 1), ('반복', 1), ('유협', 1), ('디저트', 1), ('분위기', 1), ('일과', 1), ('쌀', 1), ('고관', 1), ('밑반찬', 1), ('떼', 1), ('개월', 1), ('다양', 1), ('본격적', 1), ('생각', 1), ('수면제', 1), ('학교', 1), ('칭', 1), ('고깃국', 1), ('충격', 1), ('복사본', 1), ('미', 1), ('감로', 1), ('비', 1), ('독약', 1), ('우두', 1), ('도', 1), ('농작물', 1), ('자장면', 1), ('인터넷', 1), ('술', 1), ('기회', 1), ('풀뿌리', 1), ('게걸', 1), ('외상술', 1), ('약밥', 1), ('풍속', 1), ('한방', 1), ('치질', 1), ('나', 1), ('허기', 1), ('어린이', 1), ('나물밥', 1), ('사약', 1), ('가죽', 1), ('서부', 1), ('명', 1), ('이승만', 1), ('가래떡', 1), ('절대', 1), ('숲', 1), ('깨', 1), ('봄맞이', 1), ('곡', 1), ('계속', 1), ('자연', 1), ('목축', 1), ('시간', 1), ('서로', 1), ('얼', 1), ('가능성', 1), ('빵', 1), ('뿌리', 1), ('독립', 1), ('혼자', 1), ('잠', 1), ('덴푸라', 1), ('둥', 1), ('성', 1), ('가열', 1), ('전자', 1), ('창신', 1), ('탈진', 1), ('맘', 1), ('자신', 1)], 'verb': [('하', 33), ('않', 21), ('살', 17), ('즐기', 11), ('굽', 9), ('곁들이', 7), ('썰', 6), ('찍', 5), ('섞', 5), ('있', 5), ('치우', 4), ('잡', 4), ('나누', 4), ('비비', 4), ('되', 3), ('싸', 3), ('어', 3), ('익히', 3), ('버리', 3), ('만들', 3), ('집', 3), ('보', 3), ('죽', 3), ('들', 2), ('튀기', 2), ('삭히', 2), ('마시', 2), ('말', 2), ('달이', 2), ('끓이', 2), ('뜯', 2), ('사', 2), ('자라', 2), ('뿌리', 2), ('넣', 2), ('시키', 2), ('위하', 2), ('찌', 1), ('씹', 1), ('뒤집', 1), ('바꾸', 1), ('부르', 1), ('다니', 1), ('담구', 1), ('도망치', 1), ('재우', 1), ('파', 1), ('오', 1), ('덜', 1), ('발르', 1), ('늘', 1), ('자르', 1), ('얹', 1), ('묻히', 1), ('볶', 1), ('담그', 1), ('태어나', 1), ('죽이', 1), ('줍', 1), ('갉', 1), ('생겨나', 1), ('찾', 1), ('아', 1), ('부숴뜨리', 1), ('짜', 1), ('부리', 1), ('훔치', 1), ('쓰', 1), ('나르', 1), ('베', 1), ('대', 1), ('둘러앉', 1), ('걸르', 1), ('맞', 1), ('넘', 1), ('부', 1), ('두들기', 1), ('팔', 1), ('따', 1)], 'adverb': [('많이', 10), ('주로', 7), ('다', 5), ('같이', 4), ('잘', 4), ('함께', 3), ('못', 3), ('가장', 3), ('우연히', 1), ('자주', 1), ('하지만', 1), ('그냥', 1), ('씩', 1), ('또한', 1), ('너무', 1), ('채', 1), ('내내', 1), ('어찌', 1), ('적당히', 1), ('대체로', 1), ('가끔', 1), ('특히', 1), ('흥청망청', 1), ('적이', 1), ('흔히', 1), ('상관없이', 1), ('또', 1), ('통째로', 1), ('날로', 1), ('빨리', 1), ('때로', 1), ('전혀', 1), ('배불리', 1), ('겨우', 1), ('안', 1), ('간단히', 1), ('달리', 1)], 'determiner': [('다른', 5), ('그', 2), ('여러', 1), ('세', 1), ('몇몇', 1), ('새', 1)], 'adjective': [('싶', 5), ('어리', 1), ('편하', 1), ('작', 1), ('좋', 1), ('손쉽', 1), ('못하', 1)]}, 'noun': {'noun': [('붓', 3), ('종이', 2), ('묘선', 1), ('청자', 1), ('은장도', 1), ('제조', 1), ('벼루', 1), ('농담', 1), ('윤', 1)], 'verb': [('의하', 1), ('그리', 1), ('찍', 1), ('차', 1), ('늘어놓', 1)], 'adverb': [('하지만', 1)]}}
```

References:
- This was copied from [Kollocate](https://github.com/Kyubyong/kollocate) and modified by Kss
</details>

<details>
<summary>3. g2p</summary>

This function provides a way to convert Korean graphemes to phonemes.
The 'grapheme' means a letter or a character, and the 'phoneme' means a sound.

Args:
- text (`Union[str, List[str], Tuple[str]]`): single text or list of texts
- descriptive (`bool`): return descriptive pronunciation, the 'descriptive' means a real-life pronunciation
- group_vowels (`bool`): If True, the vowels of the identical sound are normalized. (e.g. ㅒ -> ㅖ)
- to_syllable (`bool`): If True, hangul letters or jamo are assembled to form syllables.
- convert_english_to_hangul_phonemes (`bool`): If True, convert English to Hangul phonemes
- convert_numbers_to_hangul_phonemes (`bool`): If True, convert numbers to Hangul phonemes
- num_workers (`Union[int, str]`): the number of multiprocessing workers
- backend (`str`): morpheme analyzer backend. 'mecab', 'pecab' are supported
- verbose (`bool`): whether to print verbose outputs or not

Returns:
- `Union[str, List[str]]`: phoneme string or list of phoneme strings from the given text

Examples:
```python
>>> from kss import Kss
>>> g2p = Kss("g2p")
>>> text = "어제는 맑았는데 오늘은 흐리다."
>>> output = g2p(text)
>>> print(output)
"어제는 말간는데 오느른 흐리다."
```

References:
- This was copied from [g2pk](https://github.com/Kyubyong/g2pk) and modified by Kss
</details>

<details>
<summary>4. hangulize</summary>

This converts the given text to Hangul pronunciation.

Args:
- text (`Union[str, List[str], Tuple[str]`): single text or list of texts
- lang (`str`): source language code
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[str, List[str]]`: Hangul pronunciation of the given text

Examples:
```python
>>> from kss import Kss
>>> hangulize = Kss("hangulize")
>>> text = "Giro d'Italia"
>>> output = hangulize(text, lang="ita")
>>> print(output)
"지로 디탈리아"
```

References:
- This was copied from [hangulize](https://github.com/sublee/hangulize) and modified by Kss
</details>

<details>
<summary>5. split_hanja</summary>

This splits the given text into hanja string and non-hanja string.

Args:
- text (`Union[str, List[str], Tuple[str]`): single text or list of texts
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[str, List[str]]`: hanja string and non-hanja string of the given text

Examples:
```python
>>> from kss import Kss
>>> split_hanja = Kss("split_hanja")
>>> text = "大韓民國은 民主共和國이다."
>>> output = split_hanja(text)
>>> print(output)
["大韓民國", "은 ", "民主共和國", "이다."]
```

References:
This was copied from [hanja](https://github.com/suminb/hanja) and modified by Kss
</details>

<details>
<summary>6. is_hanja</summary>

This checks if the given character is a hanja character.

Args:
- text (`Union[str, List[str], Tuple[str]`): single character or list of characters
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[bool, List[bool]]`: whether the given character is a hanja character or not

Examples:
```python
>>> from kss import Kss
>>> is_hanja = Kss("is_hanja")
>>> text = "大"
>>> output = is_hanja(text)
>>> print(output)
True
>>> text = "대"
>>> output = is_hanja(text)
>>> print(output)
False
```

References:
This was copied from [hanja](https://github.com/suminb/hanja) and modified by Kss
</details>

<details>
<summary>7. hanja2hangul</summary>

This converts hanja to hangul.

Args:
- text (`Union[str, List[str], Tuple[str]`): single text or list of texts
- combination (`bool`): whether to return hanja and hangul together or not
- reverse (`bool`): whether to reverse the order of hanja and hangul or not
- html (`bool`): whether to return html format or not
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[str, List[str]]`: hanja to hangul converted text or list of texts

Examples:
```python
>>> from kss import Kss
>>> hanja2hangul = Kss("hanja2hangul")
>>> text = "大韓民國은 民主共和國이다."
>>> output = hanja2hangul(text)
>>> print(output)
"대한민국은 민주공화국이다."
```

References:
- This was copied from [hanja](https://github.com/suminb/hanja) and modified by Kss
</details>

<details>
<summary>8. h2j</summary>

This converts a string of Hangul to jamo.

Args:
- text (`Union[str, List[str], Tuple[str]`): single text or list of texts
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[str, List[str]]`: jamo string of the given text

Examples:
```python

>>> from kss import Kss
>>> h2j = Kss("h2j")
>>> text = "안녕하세요"
>>> output = h2j(text)
>>> print(output)
'안녕하세요'
```

References:
- This was copied from [jamo](https://github.com/JDongian/python-jamo) and modified by Kss
</details>

<details>
<summary>9. h2hcj</summary>

This converts a string of Hangul to Hangul Compatibility Jamo.

Args:
- text (`Union[str, List[str], Tuple[str]`): single text or list of texts
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[str, List[str]]`: Hangul Compatibility Jamo string of the given text

Examples:
```python
>>> from kss import Kss
>>> h2hcj = Kss("h2hcj")
>>> text = "안녕하세요"
>>> output = h2hcj(text)
>>> print(output)
'ㅇㅏㄴㄴㅕㅇㅎㅏㅅㅔㅇㅛ'
```

References:
- This was copied from [hangul-jamo](https://github.com/jonghwanhyeon/hangul-jamo) and modified by Kss
</details>

<details>
<summary>10. j2h</summary>

This converts a string of jamo to Hangul.

Args:
- text (`Union[str, List[str], Tuple[str]`): single text or list of texts
- add_placeholder_for_leading_vowels (`bool`): add 'ㅇ' for leading vowels (e.g. 'ㅐ플' -> '애플')
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[str, List[str]]`: Hangul string of the given text

Examples:
```python
>>> from kss import Kss
>>> j2h = Kss("j2h")
>>> text = '안녕하세요'
>>> output = j2h(text)
>>> print(output)
'안녕하세요'
```

References:
- This was copied from [jamo](https://github.com/JDongian/python-jamo) and modified by Kss
    
</details>

<details>
<summary>11. j2hcj</summary>

This converts a string of jamo to Hangul Compatibility Jamo.

Args:
- text (`Union[str, List[str], Tuple[str]`): single text or list of texts
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[str, List[str]]`: Hangul Compatibility Jamo string of the given text

Examples:
```python
>>> from kss import Kss
>>> j2hcj = Kss("j2hcj")
>>> text = '안녕하세요'
>>> output = j2hcj(text)
>>> print(output)
'ㅇㅏㄴㄴㅕㅇㅎㅏㅅㅔㅇㅛ'
```

References:
- This was copied from [jamo](https://github.com/JDongian/python-jamo) and modified by Kss
    
</details>

<details>
<summary>12. hcj2h</summary>

This converts a string of Hangul Compatibility Jamo to Hangul.

Args:
- text (`Union[str, List[str], Tuple[str]`): single text or list of texts
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[str, List[str]]`: Hangul string of the given text

Examples:
```python
>>> from kss import Kss
>>> hcj2h = Kss("hcj2h")
>>> text = 'ㅇㅏㄴㄴㅕㅇㅎㅏㅅㅔㅇㅛ'
>>> output = hcj2h(text)
>>> print(output)
'안녕하세요'
```

References:
- This was copied from [hangul-jamo](https://github.com/jonghwanhyeon/hangul-jamo) and modified by Kss
    
</details>

<details>
<summary>13. hcj2j</summary>

This converts a string of Hangul Compatibility Jamo to jamo.

Args:
- text (`Union[str, List[str], Tuple[str]`): single text or list of texts
- position (`str`): the position of the HCJ character to convert to jamo character, one of 'lead', 'vowel', 'tail'
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[str, List[str]]`: jamo string of the given text

Examples:
```python
>>> from kss import Kss
>>> hcj2j = Kss("hcj2j")
>>> text = 'ㅇ'
>>> output = hcj2j(text)
>>> print(output)
'ᄋ'
```

References:
- This was copied from [jamo](https://github.com/JDongian/python-jamo) and modified by Kss
    
</details>

<details>
<summary>14. is_jamo</summary>

This checks if a character is a jamo character.

Args:
- text (`Union[str, List[str], Tuple[str]`): single text or list of texts
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[bool, List[bool]]`: whether the given character is a jamo character or not

Examples:
```python
>>> from kss import Kss
>>> is_jamo = Kss("is_jamo")
>>> text = 'ᄋ'
>>> output = is_jamo(text)
>>> print(output)
True
```

References:
- This was copied from [jamo](https://github.com/JDongian/python-jamo) and modified by Kss
    
</details>

<details>
<summary>15. is_jamo_modern</summary>

This checks if a character is a modern jamo character.

Args:
- text (`Union[str, List[str], Tuple[str]`): single text or list of texts
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[bool, List[bool]]`: whether the given character is a modern jamo character or not

Examples:
```python
>>> from kss import Kss
>>> is_jamo_modern = Kss("is_jamo_modern")
>>> text = 'ᄋ'
>>> output = is_jamo_modern(text)
>>> print(output)
True
```

References:
- This was copied from [jamo](https://github.com/JDongian/python-jamo) and modified by Kss
    
</details>

<details>
<summary>16. is_hcj</summary>

This checks if a character is a Hangul Compatibility Jamo character.

Args:
- text (`Union[str, List[str], Tuple[str]`): single text or list of texts
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[bool, List[bool]]`: whether the given character is a Hangul Compatibility Jamo character or not

Examples:
```python
>>> from kss import Kss
>>> is_hcj = Kss("is_hcj")
>>> text = 'ㅇ'
>>> output = is_hcj(text)
>>> print(output)
True
```

References:
- This was copied from [jamo](https://github.com/JDongian/python-jamo) and modified by Kss
    
</details>

<details>
<summary>17. is_hcj_modern</summary>

This checks if a character is a modern Hangul Compatibility Jamo character.

Args:
- text (`Union[str, List[str], Tuple[str]`): single text or list of texts
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[bool, List[bool]]`: whether the given character is a modern Hangul Compatibility Jamo character or not

Examples:
```python
>>> from kss import Kss
>>> is_hcj_modern = Kss("is_hcj_modern")
>>> text = 'ㅇ'
>>> output = is_hcj_modern(text)
>>> print(output)
True
```

References:
- This was copied from [jamo](https://github.com/JDongian/python-jamo) and modified by Kss
    
</details>

<details>
<summary>18. is_hangul_char</summary>

This checks if a character is a Hangul character.

Args:
- text (`Union[str, List[str], Tuple[str]`): single text or list of texts
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[bool, List[bool]]`: whether the given character is a Hangul character or not

Examples:
```python
>>> from kss import Kss
>>> is_hangul_char = Kss("is_hangul_char")
>>> text = '안'
>>> output = is_hangul_char(text)
>>> print(output)
True
```

References:
- This was copied from [jamo](https://github.com/JDongian/python-jamo) and modified by Kss
</details>

<details>
<summary>19. select_josa</summary>

This selects the correct josa for the given prefix.

Args:
- prefix (`Union[str, List[str]`): single prefix or list of prefixes
- josa (`Union[str, List[str]`): single josa or list of josas
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[str, List[str]]`: the correct josa for the given prefix

Examples:
```python
>>> from kss import Kss
>>> select_josa = Kss("select_josa")
>>> prefix = "철수"
>>> josa = "은"
>>> output = select_josa(prefix, josa)
>>> print(output)
"는"
```

References:
- This was copied from [tossi](https://github.com/what-studio/tossi) and modified by Kss
</details>

<details>
<summary>20. combine_josa</summary>

This combines the given prefix and josa.

Args:
- prefix (`Union[str, List[str]`): single prefix or list of prefixes
- josa (`Union[str, List[str]`): single josa or list of josas
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[str, List[str]]`: the combined prefix and josa

Examples:
```python
>>> from kss import Kss
>>> combine_josa = Kss("combine_josa")
>>> prefix = "철수"
>>> josa = "은"
>>> output = combine_josa(prefix, josa)
>>> print(output)
"철수는"
```

References:
- This was copied from [tossi](https://github.com/what-studio/tossi) and modified by Kss
</details>

<details>
<summary>21. extract_keywords</summary>

This extracts keywords from the given text.
This uses TextRank algorithm to extract keywords.

Args:
- text (`Union[str, List[str]`): single text or list of texts
- num_keywords (`int`): the number of keywords to extract
- min_word_count (`int`): the minimum count of words
- max_word_length (`int`): the maximum length of words
- return_scores (`bool`): whether to return scores or not
- backend (`str`): morpheme analyzer backend. 'mecab', 'pecab' are supported
- noun_only (`bool`): whether to extract only nouns or not
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[List[str], List[Tuple[str, float]]]`: list of keywords or list of tuples of keywords and scores

Examples:
```python
>>> from kss import Kss
>>> extract_keywords = Kss("extract_keywords")
>>> text = ['여운이 크게남는영화 엠마스톤 너무 사랑스럽고 라이언고슬링 남자가봐도 정말 매력적인 배우인듯 영상미 음악 연기 구성 전부 좋았고 마지막 엔딩까지 신선하면서 애틋하구요 30중반에 감정이 많이 메말라있었는데 오랜만에 가슴이 촉촉해지네요',
...         '영상미도 너무 아름답고 신나는 음악도 좋았다 마지막 세바스찬과 미아의 눈빛교환은 정말 마음 아팠음 영화관에 고딩들이 엄청 많던데 고딩들은 영화 내용 이해를 못하더라ㅡㅡ사랑을 깊게 해본 사람이라면 누구나 느껴볼수있는 먹먹함이 있다',
...         '정말 영상미랑 음악은 최고였다 그리고 신선했다 음악이 너무 멋있어서 연기를 봐야 할지 노래를 들어야 할지 모를 정도로 그리고 보고 나서 생각 좀 많아진 영화 정말 이 연말에 보기 좋은 영화 인 것 같다',
...         '무언의 마지막 피아노연주 완전 슬픔ㅠ보는이들에게 꿈을 상기시켜줄듯 또 보고 싶은 내생에 최고의 뮤지컬영화였음 단순할수 있는 내용에 뮤지컬을 가미시켜째즈음악과 춤으로 지루할틈없이 빠져서봄 ost너무좋았음',
...         '처음엔 초딩들 보는 그냥 그런영화인줄 알았는데 정말로 눈과 귀가 즐거운 영화였습니다 어찌보면 뻔한 스토리일지 몰라도 그냥 보고 듣는게 즐거운 그러다가 정말 마지막엔 너무 아름답고 슬픈 음악이 되어버린',
...         '정말 멋진 노래와 음악과 영상미까지 정말 너무 멋있는 영화 눈물을 흘리면서 봤습니다 영화가 끝난 순간 감탄과 동시에 여운이 길게 남아 또 눈물을 흘렸던내 인생 최고의 뮤지컬 영화',
...         '평소 뮤지컬 영화 좋아하는 편인데도 평점에 비해 너무나 별로였던 영화 재즈음악이나 영상미 같은 건 좋았지만 줄거리도 글쎄 결말은 정말 별로 6 7점 정도 주는게 맞다고 생각하지만 개인적으로 후반부가 너무 별로여서',
...         '오랜만에 좋은 영화봤다는 생각들었구요 음악도 영상도 스토리도 너무나좋았고 무엇보다 진한 여운이 남는 영화는 정말 오랜만이었어요 연인끼리 가서 보기 정말 좋은영화 너뮤너뮤너뮤 재밌게 잘 봤습니다',
...         '음악 미술 연기 등 모든 것이 좋았지만 마지막 결말이 너무 현실에 뒤떨어진 꿈만 같다 꿈을 이야기하는 영화지만 과정과 결과에 있어 예술가들의 현실을 너무 반영하지 못한 것이 아닌가하는 생각이든다 그래서 보고 난 뒤 나는 꿈을 꿔야하는데 허탈했다',
...         '마지막 회상씬의 감동이 잊혀지질않는다마지막 십분만으로 티켓값이 아깝지않은 영화 음악들도 너무 아름다웠다옛날 뮤지컬 같은 빈티지영상미도 최고']
>>> output = extract_keywords(text, noun_only=True)
>>> print(output)
['마지막', '영화', '음악', '라이언고슬링', '뮤지컬']
>>> output = extract_keywords(text, noun_only=False)
>>> print(output)
['너무', '정말', '마지막', '영화', '음악']
```

References:
- This was copied from [KR-WordRank](https://github.com/lovit/KR-WordRank) and modified by Kss
</details>

<details>
<summary>22. split_morphemes</summary>

This splits texts into morphemes.

Args:
- text (`Union[str, List[str], Tuple[str]]`): single text or list/tuple of texts
- backend (`str`): morpheme analyzer backend. 'mecab', 'pecab' are supported.
- num_workers (`Union[int, str]`): the number of multiprocessing workers
- drop_space (`bool`): drop all spaces in output or not

Returns:
- `Union[List[Tuple[str, str]], List[List[Tuple[str, str]]], Union[List, Tuple]]`: outputs of morpheme analysis.

Examples:
```python
>>> from kss import Kss
>>> split_morphemes = Kss("split_morphemes")
>>> text = "아버지가방에들어오시다."
>>> output = split_morphemes(text)
>>> print(output)
[('아버지', 'NNG'), ('가', 'JKS'), ('방', 'NNG'), ('에', 'JKB'), ('들어오', 'VV'), ('시', 'EP'), ('다', 'EF'), ('.', 'SF')]
```    
</details>

<details>
<summary>23. paradigm</summary>

This searches paradigms of the given text.

Args:
- text (`Union[str, List[str], Tuple[str]`): single text or list of texts
- num_workers (`Union[int, str]`): the number of multiprocessing workers
- verbose (`bool`): whether to print the results or not

Returns:
- `Union[Dict[str, str], List[Dict[str, str]]]`: paradigms of the given text

Examples:
```python
>>> from kss import Kss
>>> paradigm = Kss("paradigm")
>>> text = "곱"
>>> output = paradigm(text)
>>> print(output)
{'Action Verb': [('거나', '곱거나'), ('거늘', '곱거늘'), ('거니', '곱거니'), ('거니와', '곱거니와'), ('거드면', '곱거드면'), ('거든', '곱거든'), ('건', '곱건'), ('건마는', '곱건마는'), ('것다', '곱것다'), ('게', '곱게'), ('겠', '곱겠'), ('고', '곱고'), ('고도', '곱고도'), ('고말고', '곱고말고'), ('관데', '곱관데'), ('기', '곱기'), ('기로', '곱기로'), ('기로니', '곱기로니'), ('기로서', '곱기로서'), ('기로서니', '곱기로서니'), ('기로선들', '곱기로선들'), ('기에', '곱기에'), ('네', '곱네'), ('니', '곱니'), ('다', '곱다'), ('다가', '곱다가'), ('다가는', '곱다가는'), ('다간', '곱다간'), ('다니', '곱다니'), ('다마다', '곱다마다'), ('더', '곱더'), ('더구나', '곱더구나'), ('더구려', '곱더구려'), ('더군', '곱더군'), ('더냐', '곱더냐'), ('더뇨', '곱더뇨'), ('더니', '곱더니'), ('더니라', '곱더니라'), ('더니마는', '곱더니마는'), ('더니만', '곱더니만'), ('더니이까', '곱더니이까'), ('더니이다', '곱더니이다'), ('더라', '곱더라'), ('더라나', '곱더라나'), ('더라니', '곱더라니'), ('더라니까', '곱더라니까'), ('더라도', '곱더라도'), ('더라며', '곱더라며'), ('더라면', '곱더라면'), ('더라면서', '곱더라면서'), ('더라손', '곱더라손'), ('더라지', '곱더라지'), ('더람', '곱더람'), ('더이까', '곱더이까'), ('더이다', '곱더이다'), ('던', '곱던'), ('던가', '곱던가'), ('던감', '곱던감'), ('던걸', '곱던걸'), ('던고', '곱던고'), ('던데', '곱던데'), ('던바', '곱던바'), ('던지', '곱던지'), ('데', '곱데'), ('데요', '곱데요'), ('도다', '곱도다'), ('되', '곱되'), ('든', '곱든'), ('든가', '곱든가'), ('든지', '곱든지'), ('듯', '곱듯'), ('듯이', '곱듯이'), ('소이까', '곱소이까'), ('죠', '곱죠'), ('지마는', '곱지마는'), ('지만', '곱지만'), ('지요', '곱지요'), ('게', '곱게'), ('고는', '곱고는'), ('누', '곱누'), ('디', '곱디'), ('소', '곱소'), ('지', '곱지'), ('아', '곱아'), ('아도', '곱아도'), ('아라', '곱아라'), ('아서', '곱아서'), ('아야', '곱아야'), ('아야만', '곱아야만'), ('아야지', '곱아야지'), ('아요', '곱아요'), ('아지이다', '곱아지이다'), ('았', '곱았'), ('았었', '곱았었'), ('았자', '곱았자'), ('으나', '곱으나'), ('으나마', '곱으나마'), ('으니', '곱으니'), ('으니까', '곱으니까'), ('으니까는', '곱으니까는'), ('으니만치', '곱으니만치'), ('으니만큼', '곱으니만큼'), ('으려니와', '곱으려니와'), ('으려면', '곱으려면'), ('으련마는', '곱으련마는'), ('으렷다', '곱으렷다'), ('으리', '곱으리'), ('으리까', '곱으리까'), ('으리니', '곱으리니'), ('으리니라', '곱으리니라'), ('으리다', '곱으리다'), ('으리라', '곱으리라'), ('으리로다', '곱으리로다'), ('으리만치', '곱으리만치'), ('으리만큼', '곱으리만큼'), ('으리오', '곱으리오'), ('으매', '곱으매'), ('으며', '곱으며'), ('으면', '곱으면'), ('으면서', '곱으면서'), ('으므로', '곱으므로'), ('으사', '곱으사'), ('으세요', '곱으세요'), ('으셔요', '곱으셔요'), ('으소서', '곱으소서'), ('으시', '곱으시'), ('으시어요', '곱으시어요'), ('으오', '곱으오'), ('으오니까', '곱으오니까'), ('으오리까', '곱으오리까'), ('으오리다', '곱으오리다'), ('으오리이까', '곱으오리이까'), ('으오리이다', '곱으오리이다'), ('으오이다', '곱으오이다'), ('으옵', '곱으옵'), ('으옵나이까', '곱으옵나이까'), ('으옵나이다', '곱으옵나이다'), ('으옵니까', '곱으옵니까'), ('으옵니다', '곱으옵니다'), ('으옵디까', '곱으옵디까'), ('으옵디다', '곱으옵디다'), ('으옵소서', '곱으옵소서'), ('으옵시', '곱으옵시'), ('으와', '곱으와'), ('으우', '곱으우'), ('은', '곱은'), ('은걸', '곱은걸'), ('은들', '곱은들'), ('은즉', '곱은즉'), ('은즉슨', '곱은즉슨'), ('을', '곱을'), ('을걸', '곱을걸'), ('을까', '곱을까'), ('을는지', '곱을는지'), ('을라', '곱을라'), ('을라고', '곱을라고'), ('을러니', '곱을러니'), ('을러라', '곱을러라'), ('을런가', '곱을런가'), ('을런고', '곱을런고'), ('을레', '곱을레'), ('을레라', '곱을레라'), ('을망정', '곱을망정'), ('을밖에', '곱을밖에'), ('을뿐더러', '곱을뿐더러'), ('을새', '곱을새'), ('을세', '곱을세'), ('을세라', '곱을세라'), ('을세말이지', '곱을세말이지'), ('을수록', '곱을수록'), ('을시', '곱을시'), ('을쏘냐', '곱을쏘냐'), ('을쏜가', '곱을쏜가'), ('을지', '곱을지'), ('을지나', '곱을지나'), ('을지니', '곱을지니'), ('을지니라', '곱을지니라'), ('을지라', '곱을지라'), ('을지라도', '곱을지라도'), ('을지로다', '곱을지로다'), ('을지며', '곱을지며'), ('을지어다', '곱을지어다'), ('을지언정', '곱을지언정'), ('을진대', '곱을진대'), ('을진대는', '곱을진대는'), ('을진저', '곱을진저'), ('음', '곱음'), ('음에도', '곱음에도'), ('음에랴', '곱음에랴'), ('읍시오', '곱읍시오'), ('습네', '곱습네'), ('습늰다', '곱습늰다'), ('습니까', '곱습니까'), ('습니다', '곱습니다'), ('습디까', '곱습디까'), ('습디다', '곱습디다'), ('습딘다', '곱습딘다'), ('습죠', '곱습죠'), ('습지요', '곱습지요'), ('거라', '곱거라'), ('건대', '곱건대'), ('게', '곱게'), ('게끔', '곱게끔'), ('게나', '곱게나'), ('고는', '곱고는'), ('고서', '곱고서'), ('고야', '곱고야'), ('곤', '곱곤'), ('구려', '곱구려'), ('구먼', '곱구먼'), ('나', '곱나'), ('나니', '곱나니'), ('남', '곱남'), ('노니', '곱노니'), ('노라', '곱노라'), ('노라고', '곱노라고'), ('누나', '곱누나'), ('누먼', '곱누먼'), ('느라', '곱느라'), ('느라고', '곱느라고'), ('는구나', '곱는구나'), ('는구려', '곱는구려'), ('는군', '곱는군'), ('도록', '곱도록'), ('세나', '곱세나'), ('자', '곱자'), ('자고', '곱자고'), ('자꾸나', '곱자꾸나'), ('자느니', '곱자느니'), ('자니까', '곱자니까'), ('자마자', '곱자마자'), ('자며', '곱자며'), ('자면', '곱자면'), ('자면서', '곱자면서'), ('자손', '곱자손'), ('아다', '곱아다'), ('아다가', '곱아다가'), ('고자', '곱고자'), ('나이까', '곱나이까'), ('나이다', '곱나이다'), ('노라니', '곱노라니'), ('노라니까', '곱노라니까'), ('노라면', '곱노라면'), ('느냐', '곱느냐'), ('느냐고', '곱느냐고'), ('느뇨', '곱느뇨'), ('느니', '곱느니'), ('느니라', '곱느니라'), ('느니만', '곱느니만'), ('느니만치', '곱느니만치'), ('느니만큼', '곱느니만큼'), ('는', '곱는'), ('는가', '곱는가'), ('는감', '곱는감'), ('는걸', '곱는걸'), ('는고', '곱는고'), ('는데', '곱는데'), ('는뎁쇼', '곱는뎁쇼'), ('는바', '곱는바'), ('는지', '곱는지'), ('는지고', '곱는지고'), ('는지라', '곱는지라'), ('으라', '곱으라'), ('으라고', '곱으라고'), ('으라나', '곱으라나'), ('으라느니', '곱으라느니'), ('으라니까', '곱으라니까'), ('으라며', '곱으라며'), ('으라면서', '곱으라면서'), ('으라손', '곱으라손'), ('으락', '곱으락'), ('으란', '곱으란'), ('으람', '곱으람'), ('으랴', '곱으랴'), ('으러', '곱으러'), ('으려', '곱으려'), ('으려거든', '곱으려거든'), ('으려고', '곱으려고'), ('으려나', '곱으려나'), ('으려니', '곱으려니'), ('으려든', '곱으려든'), ('으려무나', '곱으려무나'), ('으련', '곱으련'), ('으렴', '곱으렴'), ('으렵니까', '곱으렵니까'), ('으렵니다', '곱으렵니다'), ('으마', '곱으마'), ('으사이다', '곱으사이다'), ('으세', '곱으세'), ('으시라', '곱으시라'), ('으시압', '곱으시압'), ('으십사', '곱으십사'), ('으십시다', '곱으십시다'), ('으십시오', '곱으십시오'), ('을거나', '곱을거나'), ('을게', '곱을게'), ('을깝쇼', '곱을깝쇼'), ('을라치면', '곱을라치면'), ('을락', '곱을락'), ('을래', '곱을래'), ('을작시면', '곱을작시면'), ('음세', '곱음세'), ('읍시다', '곱읍시다'), ('읍시사', '곱읍시사'), ('는다', '곱는다'), ('는다고', '곱는다고'), ('는다나', '곱는다나'), ('는다네', '곱는다네'), ('는다느니', '곱는다느니'), ('는다니', '곱는다니'), ('는다니까', '곱는다니까'), ('는다더라', '곱는다더라'), ('는다마는', '곱는다마는'), ('는다며', '곱는다며'), ('는다면', '곱는다면'), ('는다면서', '곱는다면서'), ('는다손', '곱는다손'), ('는다오', '곱는다오'), ('는다지', '곱는다지'), ('는단다', '곱는단다'), ('는담', '곱는담'), ('는답니까', '곱는답니까'), ('는답니다', '곱는답니다'), ('는답시고', '곱는답시고'), ('는대', '곱는대'), ('는대요', '곱는대요')], 'Descriptive Verb': [('거나', '곱거나'), ('거늘', '곱거늘'), ('거니', '곱거니'), ('거니와', '곱거니와'), ('거드면', '곱거드면'), ('거든', '곱거든'), ('건', '곱건'), ('건마는', '곱건마는'), ('것다', '곱것다'), ('게', '곱게'), ('겠', '곱겠'), ('고', '곱고'), ('고도', '곱고도'), ('고말고', '곱고말고'), ('관데', '곱관데'), ('기', '곱기'), ('기로', '곱기로'), ('기로니', '곱기로니'), ('기로서', '곱기로서'), ('기로서니', '곱기로서니'), ('기로선들', '곱기로선들'), ('기에', '곱기에'), ('네', '곱네'), ('니', '곱니'), ('다', '곱다'), ('다가', '곱다가'), ('다가는', '곱다가는'), ('다간', '곱다간'), ('다니', '곱다니'), ('다마다', '곱다마다'), ('더', '곱더'), ('더구나', '곱더구나'), ('더구려', '곱더구려'), ('더군', '곱더군'), ('더냐', '곱더냐'), ('더뇨', '곱더뇨'), ('더니', '곱더니'), ('더니라', '곱더니라'), ('더니마는', '곱더니마는'), ('더니만', '곱더니만'), ('더니이까', '곱더니이까'), ('더니이다', '곱더니이다'), ('더라', '곱더라'), ('더라나', '곱더라나'), ('더라니', '곱더라니'), ('더라니까', '곱더라니까'), ('더라도', '곱더라도'), ('더라며', '곱더라며'), ('더라면', '곱더라면'), ('더라면서', '곱더라면서'), ('더라손', '곱더라손'), ('더라지', '곱더라지'), ('더람', '곱더람'), ('더이까', '곱더이까'), ('더이다', '곱더이다'), ('던', '곱던'), ('던가', '곱던가'), ('던감', '곱던감'), ('던걸', '곱던걸'), ('던고', '곱던고'), ('던데', '곱던데'), ('던바', '곱던바'), ('던지', '곱던지'), ('데', '곱데'), ('데요', '곱데요'), ('도다', '곱도다'), ('되', '곱되'), ('든', '곱든'), ('든가', '곱든가'), ('든지', '곱든지'), ('듯', '곱듯'), ('듯이', '곱듯이'), ('소이까', '곱소이까'), ('죠', '곱죠'), ('지마는', '곱지마는'), ('지만', '곱지만'), ('지요', '곱지요'), ('게', '곱게'), ('고는', '곱고는'), ('누', '곱누'), ('디', '곱디'), ('소', '곱소'), ('지', '곱지'), ('아', '고와'), ('아도', '고와도'), ('아라', '고와라'), ('아서', '고와서'), ('아야', '고와야'), ('아야만', '고와야만'), ('아야지', '고와야지'), ('아요', '고와요'), ('아지이다', '고와지이다'), ('았', '고왔'), ('았었', '고왔었'), ('았자', '고왔자'), ('으나', '고우나'), ('으나마', '고우나마'), ('으니', '고우니'), ('으니까', '고우니까'), ('으니까는', '고우니까는'), ('으니만치', '고우니만치'), ('으니만큼', '고우니만큼'), ('으려니와', '고우려니와'), ('으려면', '고우려면'), ('으련마는', '고우련마는'), ('으렷다', '고우렷다'), ('으리', '고우리'), ('으리까', '고우리까'), ('으리니', '고우리니'), ('으리니라', '고우리니라'), ('으리다', '고우리다'), ('으리라', '고우리라'), ('으리로다', '고우리로다'), ('으리만치', '고우리만치'), ('으리만큼', '고우리만큼'), ('으리오', '고우리오'), ('으매', '고우매'), ('으며', '고우며'), ('으면', '고우면'), ('으면서', '고우면서'), ('으므로', '고우므로'), ('으사', '고우사'), ('으세요', '고우세요'), ('으셔요', '고우셔요'), ('으소서', '고우소서'), ('으시', '고우시'), ('으시어요', '고우시어요'), ('으오', '고우오'), ('으오니까', '고우오니까'), ('으오리까', '고우오리까'), ('으오리다', '고우오리다'), ('으오리이까', '고우오리이까'), ('으오리이다', '고우오리이다'), ('으오이다', '고우오이다'), ('으옵', '고우옵'), ('으옵나이까', '고우옵나이까'), ('으옵나이다', '고우옵나이다'), ('으옵니까', '고우옵니까'), ('으옵니다', '고우옵니다'), ('으옵디까', '고우옵디까'), ('으옵디다', '고우옵디다'), ('으옵소서', '고우옵소서'), ('으옵시', '고우옵시'), ('으와', '고우와'), ('으우', '고우우'), ('은', '고운'), ('은걸', '고운걸'), ('은들', '고운들'), ('은즉', '고운즉'), ('은즉슨', '고운즉슨'), ('을', '고울'), ('을걸', '고울걸'), ('을까', '고울까'), ('을는지', '고울는지'), ('을라', '고울라'), ('을라고', '고울라고'), ('을러니', '고울러니'), ('을러라', '고울러라'), ('을런가', '고울런가'), ('을런고', '고울런고'), ('을레', '고울레'), ('을레라', '고울레라'), ('을망정', '고울망정'), ('을밖에', '고울밖에'), ('을뿐더러', '고울뿐더러'), ('을새', '고울새'), ('을세', '고울세'), ('을세라', '고울세라'), ('을세말이지', '고울세말이지'), ('을수록', '고울수록'), ('을시', '고울시'), ('을쏘냐', '고울쏘냐'), ('을쏜가', '고울쏜가'), ('을지', '고울지'), ('을지나', '고울지나'), ('을지니', '고울지니'), ('을지니라', '고울지니라'), ('을지라', '고울지라'), ('을지라도', '고울지라도'), ('을지로다', '고울지로다'), ('을지며', '고울지며'), ('을지어다', '고울지어다'), ('을지언정', '고울지언정'), ('을진대', '고울진대'), ('을진대는', '고울진대는'), ('을진저', '고울진저'), ('음', '고움'), ('음에도', '고움에도'), ('음에랴', '고움에랴'), ('읍시오', '고웁시오'), ('습네', '곱습네'), ('습늰다', '곱습늰다'), ('습니까', '곱습니까'), ('습니다', '곱습니다'), ('습디까', '곱습디까'), ('습디다', '곱습디다'), ('습딘다', '곱습딘다'), ('습죠', '곱습죠'), ('습지요', '곱습지요'), ('구나', '곱구나'), ('구려', '곱구려'), ('군', '곱군'), ('다고', '곱다고'), ('다나', '곱다나'), ('다네', '곱다네'), ('다느니', '곱다느니'), ('다니', '곱다니'), ('다니까', '곱다니까'), ('다더라', '곱다더라'), ('다마는', '곱다마는'), ('다며', '곱다며'), ('다면', '곱다면'), ('다면서', '곱다면서'), ('다손', '곱다손'), ('다지', '곱다지'), ('단다', '곱단다'), ('담', '곱담'), ('답니까', '곱답니까'), ('답니다', '곱답니다'), ('답시고', '곱답시고'), ('대', '곱대'), ('대요', '곱대요'), ('디', '곱디'), ('우', '곱우'), ('으냐', '고우냐'), ('으냐고', '고우냐고'), ('으뇨', '고우뇨'), ('으니', '고우니'), ('으니라', '고우니라'), ('으이', '고우이'), ('은가', '고운가'), ('은감', '고운감'), ('은고', '고운고'), ('은데', '고운데'), ('은뎁쇼', '고운뎁쇼'), ('은지', '고운지'), ('을데라니', '고울데라니'), ('을시고', '고울시고')]}
```

References:
- This was copied from [KoParadigm](https://github.com/Kyubyong/KoParadigm) and modified by Kss
</details>

<details>
<summary>24. anonymize</summary>

This anonymizes sensitive information in the given text.

Args:
- text (`Union[str, List[str], Tuple[str]`): single text or list of texts
- phone_number_anonymization (`bool`): whether to anonymize phone numbers or not
- rrn_anonymization (`bool`): whether to anonymize resident registration numbers or not
- card_anonymization (`bool`): whether to anonymize card numbers or not
- email_anonymization (`bool`): whether to anonymize email addresses or not
- back_account_anonymization (`bool`): whether to anonymize bank account numbers or not
- credit_card_anonymization (`bool`): whether to anonymize credit card numbers or not
- zip_anonymization (`bool`): whether to anonymize zip codes or not
- bitcoin_anonymization (`bool`): whether to anonymize bitcoin addresses or not
- url_anonymization (`bool`): whether to anonymize URLs or not
- ip_v6_anonymization (`bool`): whether to anonymize IPv6 addresses or not
- ip_v4_anonymization (`bool`): whether to anonymize IPv4 addresses or not
- phone_number_replacement (`str`): the replacement string for phone numbers, default is "<PHONE_NUMBER>"
- rrn_replacement (`str`): the replacement string for resident registration numbers, default is "<RRN>"
- card_replacement (`str`): the replacement string for card numbers, default is "<CARD>"
- email_replacement (`str`): the replacement string for email addresses, default is "<EMAIL>"
- back_account_replacement (`str`): the replacement string for bank account numbers, default is "<BANK_ACCOUNT>"
- credit_card_replacement (`str`): the replacement string for credit card numbers, default is "<CREDIT_CARD>"
- zip_replacement (`str`): the replacement string for zip codes, default is "<ZIP>"
- bitcoin_replacement (`str`): the replacement string for bitcoin addresses, default is "<BITCOIN>"
- url_replacement (`str`): the replacement string for URLs, default is "<URL>"
- ip_v6_replacement (`str`): the replacement string for IPv6 addresses, default is "<IPV6>"
- ip_v4_replacement (`str`): the replacement string for IPv4 addresses, default is "<IPV4>"
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[str, List[str], Tuple[str]]`: anonymized text or list of anonymized texts

Examples:
```python
>>> from kss import Kss
>>> anonymize = Kss("anonymize")
>>> text = "제 전화번호는 010-1234-5678, 이메일 주소는 kevin.brain@kakaobrain.com입니다."
>>> output = anonymize(text)
>>> print(output)
"제 전화번호는 <PHONE_NUMBER>, 이메일 주소는 <EMAIL>입니다."
```
</details>

<details>
<summary>25. clean_news</summary>

This cleans news articles by removing useless headers and footers.

Args:
- text (`Union[str, List[str], Tuple[str]]`): Input text or list of texts.
- min_sentences (`int`): Minimum number of sentences to keep. Defaults to 3.
- header_ratio (`float`): Ratio of the number of sentences to check in the header. Defaults to 0.4.
- footer_ratio (`float`): Ratio of the number of sentences to check in the footer. Defaults to 0.4.
- num_workers (`Union[int, str]`): the number of multiprocessing workers
- verbose (`bool`): whether to print verbose outputs or not

Returns:
- `Union[str, List[str]]`: Cleaned text or list of cleaned texts.

Examples:
```python
>>> from kss import Kss
>>> clean_news = Kss("clean_news")
>>> text = "[사진]에버랜드, 봄꽃 펼쳐진 '튤립축제' 오픈\n\n[ 뉴스1 제공](서울=뉴스1) 이동원 기자 = 에버랜드가 오는 22일부터 봄을 상징하는 튤립 120만 송이와 함께 '튤립축제'를 오픈해 본격적인 봄의 시작을 알린다. 지난 1992년 국내 첫 튤립 축제를 연 이후 올해로 22회째를 맞이한 에버랜드 '튤립축제'는 지난해 첫 선을 보이며 좋은 반응을 얻었던 오감(五感)체험 '시크릿가든'을 리뉴얼하고, 신규 테마 꽃길을 조성하는 등 봄꽃을 활용한 다양한 볼거리를 강화한 것이 특징이다. 또한 4월 28일까지 열리는 '튤립축제'에서는 야간 개장과 함께 손님 참여요소가 늘어난 인기 공연, 퍼레이드가 재오픈하는 등 봄을 맞아 나들이 나온 상춘객들의 눈과 귀를 즐겁게 할 예정이다. (에버랜드 제공)2013.3.10/뉴스1 < 저작권자 뉴스1 코리아, 무단전재 및 재배포 금지 > ☞ 뉴스1 바로가기 [스타뉴스 공식 글로벌 버전 애플리케이션] [증권알리미]국내외 증시핫이슈 및 오늘의 승부주! [머니원]北 리스크로 조정, 매수 기회로 [머니투데이 핫뉴스] ☞ 신입사원 재테크, 5년 안에 '1억 만들기' ☞ '박시후·박준' 고소女, 둘다 '여기'가더니 ☞ 늙으면 '돈이라도' 있어야 하는 진짜 이유 ☞ 손연재 가방 시끌…'신입생은 명품 안돼?' ☞ '바람난 부인 뒷조사' 300만원 줬더니… [book]10년의 선택, 중국에 투자하라 [핫이슈]'멘사' 천재들 뭉쳐 15년 투자했는데... '맙소사' 뉴스1 제공 < 저작권자 ⓒ '돈이 보이는 리얼타임 뉴스' 머니투데이, 무단전재 및 재배포 금지"
>>> output = clean_news(text)
>>> print(output)
'에버랜드, 봄꽃 펼쳐진 '튤립축제' 오픈\n\n에버랜드가 오는 22일부터 봄을 상징하는 튤립 120만 송이와 함께 '튤립축제'를 오픈해 본격적인 봄의 시작을 알린다. 지난 1992년 국내 첫 튤립 축제를 연 이후 올해로 22회째를 맞이한 에버랜드 '튤립축제'는 지난해 첫 선을 보이며 좋은 반응을 얻었던 오감(五感)체험 '시크릿가든'을 리뉴얼하고, 신규 테마 꽃길을 조성하는 등 봄꽃을 활용한 다양한 볼거리를 강화한 것이 특징이다. 또한 4월 28일까지 열리는 '튤립축제'에서는 야간 개장과 함께 손님 참여요소가 늘어난 인기 공연, 퍼레이드가 재오픈하는 등 봄을 맞아 나들이 나온 상춘객들의 눈과 귀를 즐겁게 할 예정이다.'
```
</details>

<details>
<summary>26. is_completed_form</summary>

This checks if the given text is in completed form.

Args:
- text (`Union[str, List[str], Tuple[str]`): single text or list of texts
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[bool, List[bool]]`: whether the given text is in completed form or not

Examples:
```python
>>> from kss import Kss
>>> is_completed_form = Kss("is_completed_form")
>>> text = "백"
>>> output = is_completed_form(text)
>>> print(output)
True
>>> text = "봯"
>>> output = is_completed_form(text)
>>> print(output)
False
```
</details>

<details>
<summary>27. get_all_completed_form_hangul_chars</summary>

This returns all completed form Hangul characters.

Returns:
- `List[str]`: all completed form Hangul characters

Examples:
```python
>>> from kss import Kss
>>> get_all_completed_form_hangul_chars = Kss("get_all_completed_form_hangul_chars")
>>> output = get_all_completed_form_hangul_chars()
>>> print(output)
['가', '각', '간', '갇', '갈', '갉', '갊', '감', '갑', '값', '갓', '갔', '강', '갖', '갗', '같', '갚', '갛', '개', '객', '갠', '갤', '갬', '갭', '갯', '갰', '갱', '갸', '갹', '갼', '걀', '걋', '걍', '걔', '걘', '걜', '거', '걱', '건', '걷', '걸', '걺', '검', '겁', '것', '겄', '겅', '겆', '겉', '겊', '겋', '게', '겐', '겔', '겜', '겝', '겟', '겠', '겡', '겨', '격', '겪', '견', '겯', '결', '겸', '겹', '겻', '겼', '경', '곁', '계', '곈', '곌', '곕', '곗', '고', '곡', '곤', '곧', '골', '곪', '곬', '곯', '곰', '곱', '곳', '공', '곶', '과', '곽', '관', '괄', '괆', '괌', '괍', '괏', '광', '괘', '괜', '괠', '괩', '괬', '괭', '괴', '괵', '괸', '괼', '굄', '굅', '굇', '굉', '교', '굔', '굘', '굡', '굣', '구', '국', '군', '굳', '굴', '굵', '굶', '굻', '굼', '굽', '굿', '궁', '궂', '궈', '궉', '권', '궐', '궜', '궝', '궤', '궷', '귀', '귁', '귄', '귈', '귐', '귑', '귓', '규', '균', '귤', '그', '극', '근', '귿', '글', '긁', '금', '급', '긋', '긍', '긔', '기', '긱', '긴', '긷', '길', '긺', '김', '깁', '깃', '깅', '깆', '깊', '까', '깍', '깎', '깐', '깔', '깖', '깜', '깝', '깟', '깠', '깡', '깥', '깨', '깩', '깬', '깰', '깸', '깹', '깻', '깼', '깽', '꺄', '꺅', '꺌', '꺼', '꺽', '꺾', '껀', '껄', '껌', '껍', '껏', '껐', '껑', '께', '껙', '껜', '껨', '껫', '껭', '껴', '껸', '껼', '꼇', '꼈', '꼍', '꼐', '꼬', '꼭', '꼰', '꼲', '꼴', '꼼', '꼽', '꼿', '꽁', '꽂', '꽃', '꽈', '꽉', '꽐', '꽜', '꽝', '꽤', '꽥', '꽹', '꾀', '꾄', '꾈', '꾐', '꾑', '꾕', '꾜', '꾸', '꾹', '꾼', '꿀', '꿇', '꿈', '꿉', '꿋', '꿍', '꿎', '꿔', '꿜', '꿨', '꿩', '꿰', '꿱', '꿴', '꿸', '뀀', '뀁', '뀄', '뀌', '뀐', '뀔', '뀜', '뀝', '뀨', '끄', '끅', '끈', '끊', '끌', '끎', '끓', '끔', '끕', '끗', '끙', '끝', '끼', '끽', '낀', '낄', '낌', '낍', '낏', '낑', '나', '낙', '낚', '난', '낟', '날', '낡', '낢', '남', '납', '낫', '났', '낭', '낮', '낯', '낱', '낳', '내', '낵', '낸', '낼', '냄', '냅', '냇', '냈', '냉', '냐', '냑', '냔', '냘', '냠', '냥', '너', '넉', '넋', '넌', '널', '넒', '넓', '넘', '넙', '넛', '넜', '넝', '넣', '네', '넥', '넨', '넬', '넴', '넵', '넷', '넸', '넹', '녀', '녁', '년', '녈', '념', '녑', '녔', '녕', '녘', '녜', '녠', '노', '녹', '논', '놀', '놂', '놈', '놉', '놋', '농', '높', '놓', '놔', '놘', '놜', '놨', '뇌', '뇐', '뇔', '뇜', '뇝', '뇟', '뇨', '뇩', '뇬', '뇰', '뇹', '뇻', '뇽', '누', '눅', '눈', '눋', '눌', '눔', '눕', '눗', '눙', '눠', '눴', '눼', '뉘', '뉜', '뉠', '뉨', '뉩', '뉴', '뉵', '뉼', '늄', '늅', '늉', '느', '늑', '는', '늘', '늙', '늚', '늠', '늡', '늣', '능', '늦', '늪', '늬', '늰', '늴', '니', '닉', '닌', '닐', '닒', '님', '닙', '닛', '닝', '닢', '다', '닥', '닦', '단', '닫', '달', '닭', '닮', '닯', '닳', '담', '답', '닷', '닸', '당', '닺', '닻', '닿', '대', '댁', '댄', '댈', '댐', '댑', '댓', '댔', '댕', '댜', '더', '덕', '덖', '던', '덛', '덜', '덞', '덟', '덤', '덥', '덧', '덩', '덫', '덮', '데', '덱', '덴', '델', '뎀', '뎁', '뎃', '뎄', '뎅', '뎌', '뎐', '뎔', '뎠', '뎡', '뎨', '뎬', '도', '독', '돈', '돋', '돌', '돎', '돐', '돔', '돕', '돗', '동', '돛', '돝', '돠', '돤', '돨', '돼', '됐', '되', '된', '될', '됨', '됩', '됫', '됴', '두', '둑', '둔', '둘', '둠', '둡', '둣', '둥', '둬', '뒀', '뒈', '뒝', '뒤', '뒨', '뒬', '뒵', '뒷', '뒹', '듀', '듄', '듈', '듐', '듕', '드', '득', '든', '듣', '들', '듦', '듬', '듭', '듯', '등', '듸', '디', '딕', '딘', '딛', '딜', '딤', '딥', '딧', '딨', '딩', '딪', '따', '딱', '딴', '딸', '땀', '땁', '땃', '땄', '땅', '땋', '때', '땍', '땐', '땔', '땜', '땝', '땟', '땠', '땡', '떠', '떡', '떤', '떨', '떪', '떫', '떰', '떱', '떳', '떴', '떵', '떻', '떼', '떽', '뗀', '뗄', '뗌', '뗍', '뗏', '뗐', '뗑', '뗘', '뗬', '또', '똑', '똔', '똘', '똥', '똬', '똴', '뙈', '뙤', '뙨', '뚜', '뚝', '뚠', '뚤', '뚫', '뚬', '뚱', '뛔', '뛰', '뛴', '뛸', '뜀', '뜁', '뜅', '뜨', '뜩', '뜬', '뜯', '뜰', '뜸', '뜹', '뜻', '띄', '띈', '띌', '띔', '띕', '띠', '띤', '띨', '띰', '띱', '띳', '띵', '라', '락', '란', '랄', '람', '랍', '랏', '랐', '랑', '랒', '랖', '랗', '래', '랙', '랜', '랠', '램', '랩', '랫', '랬', '랭', '랴', '략', '랸', '럇', '량', '러', '럭', '런', '럴', '럼', '럽', '럿', '렀', '렁', '렇', '레', '렉', '렌', '렐', '렘', '렙', '렛', '렝', '려', '력', '련', '렬', '렴', '렵', '렷', '렸', '령', '례', '롄', '롑', '롓', '로', '록', '론', '롤', '롬', '롭', '롯', '롱', '롸', '롼', '뢍', '뢨', '뢰', '뢴', '뢸', '룀', '룁', '룃', '룅', '료', '룐', '룔', '룝', '룟', '룡', '루', '룩', '룬', '룰', '룸', '룹', '룻', '룽', '뤄', '뤘', '뤠', '뤼', '뤽', '륀', '륄', '륌', '륏', '륑', '류', '륙', '륜', '률', '륨', '륩', '륫', '륭', '르', '륵', '른', '를', '름', '릅', '릇', '릉', '릊', '릍', '릎', '리', '릭', '린', '릴', '림', '립', '릿', '링', '마', '막', '만', '많', '맏', '말', '맑', '맒', '맘', '맙', '맛', '망', '맞', '맡', '맣', '매', '맥', '맨', '맬', '맴', '맵', '맷', '맸', '맹', '맺', '먀', '먁', '먈', '먕', '머', '먹', '먼', '멀', '멂', '멈', '멉', '멋', '멍', '멎', '멓', '메', '멕', '멘', '멜', '멤', '멥', '멧', '멨', '멩', '며', '멱', '면', '멸', '몃', '몄', '명', '몇', '몌', '모', '목', '몫', '몬', '몰', '몲', '몸', '몹', '못', '몽', '뫄', '뫈', '뫘', '뫙', '뫼', '묀', '묄', '묍', '묏', '묑', '묘', '묜', '묠', '묩', '묫', '무', '묵', '묶', '문', '묻', '물', '묽', '묾', '뭄', '뭅', '뭇', '뭉', '뭍', '뭏', '뭐', '뭔', '뭘', '뭡', '뭣', '뭬', '뮈', '뮌', '뮐', '뮤', '뮨', '뮬', '뮴', '뮷', '므', '믄', '믈', '믐', '믓', '미', '믹', '민', '믿', '밀', '밂', '밈', '밉', '밋', '밌', '밍', '및', '밑', '바', '박', '밖', '밗', '반', '받', '발', '밝', '밞', '밟', '밤', '밥', '밧', '방', '밭', '배', '백', '밴', '밸', '뱀', '뱁', '뱃', '뱄', '뱅', '뱉', '뱌', '뱍', '뱐', '뱝', '버', '벅', '번', '벋', '벌', '벎', '범', '법', '벗', '벙', '벚', '베', '벡', '벤', '벧', '벨', '벰', '벱', '벳', '벴', '벵', '벼', '벽', '변', '별', '볍', '볏', '볐', '병', '볕', '볘', '볜', '보', '복', '볶', '본', '볼', '봄', '봅', '봇', '봉', '봐', '봔', '봤', '봬', '뵀', '뵈', '뵉', '뵌', '뵐', '뵘', '뵙', '뵤', '뵨', '부', '북', '분', '붇', '불', '붉', '붊', '붐', '붑', '붓', '붕', '붙', '붚', '붜', '붤', '붰', '붸', '뷔', '뷕', '뷘', '뷜', '뷩', '뷰', '뷴', '뷸', '븀', '븃', '븅', '브', '븍', '븐', '블', '븜', '븝', '븟', '비', '빅', '빈', '빌', '빎', '빔', '빕', '빗', '빙', '빚', '빛', '빠', '빡', '빤', '빨', '빪', '빰', '빱', '빳', '빴', '빵', '빻', '빼', '빽', '뺀', '뺄', '뺌', '뺍', '뺏', '뺐', '뺑', '뺘', '뺙', '뺨', '뻐', '뻑', '뻔', '뻗', '뻘', '뻠', '뻣', '뻤', '뻥', '뻬', '뼁', '뼈', '뼉', '뼘', '뼙', '뼛', '뼜', '뼝', '뽀', '뽁', '뽄', '뽈', '뽐', '뽑', '뽕', '뾔', '뾰', '뿅', '뿌', '뿍', '뿐', '뿔', '뿜', '뿟', '뿡', '쀼', '쁑', '쁘', '쁜', '쁠', '쁨', '쁩', '삐', '삑', '삔', '삘', '삠', '삡', '삣', '삥', '사', '삭', '삯', '산', '삳', '살', '삵', '삶', '삼', '삽', '삿', '샀', '상', '샅', '새', '색', '샌', '샐', '샘', '샙', '샛', '샜', '생', '샤', '샥', '샨', '샬', '샴', '샵', '샷', '샹', '섀', '섄', '섈', '섐', '섕', '서', '석', '섞', '섟', '선', '섣', '설', '섦', '섧', '섬', '섭', '섯', '섰', '성', '섶', '세', '섹', '센', '셀', '셈', '셉', '셋', '셌', '셍', '셔', '셕', '션', '셜', '셤', '셥', '셧', '셨', '셩', '셰', '셴', '셸', '솅', '소', '속', '솎', '손', '솔', '솖', '솜', '솝', '솟', '송', '솥', '솨', '솩', '솬', '솰', '솽', '쇄', '쇈', '쇌', '쇔', '쇗', '쇘', '쇠', '쇤', '쇨', '쇰', '쇱', '쇳', '쇼', '쇽', '숀', '숄', '숌', '숍', '숏', '숑', '수', '숙', '순', '숟', '술', '숨', '숩', '숫', '숭', '숯', '숱', '숲', '숴', '쉈', '쉐', '쉑', '쉔', '쉘', '쉠', '쉥', '쉬', '쉭', '쉰', '쉴', '쉼', '쉽', '쉿', '슁', '슈', '슉', '슐', '슘', '슛', '슝', '스', '슥', '슨', '슬', '슭', '슴', '습', '슷', '승', '시', '식', '신', '싣', '실', '싫', '심', '십', '싯', '싱', '싶', '싸', '싹', '싻', '싼', '쌀', '쌈', '쌉', '쌌', '쌍', '쌓', '쌔', '쌕', '쌘', '쌜', '쌤', '쌥', '쌨', '쌩', '썅', '써', '썩', '썬', '썰', '썲', '썸', '썹', '썼', '썽', '쎄', '쎈', '쎌', '쏀', '쏘', '쏙', '쏜', '쏟', '쏠', '쏢', '쏨', '쏩', '쏭', '쏴', '쏵', '쏸', '쐈', '쐐', '쐤', '쐬', '쐰', '쐴', '쐼', '쐽', '쑈', '쑤', '쑥', '쑨', '쑬', '쑴', '쑵', '쑹', '쒀', '쒔', '쒜', '쒸', '쒼', '쓩', '쓰', '쓱', '쓴', '쓸', '쓺', '쓿', '씀', '씁', '씌', '씐', '씔', '씜', '씨', '씩', '씬', '씰', '씸', '씹', '씻', '씽', '아', '악', '안', '앉', '않', '알', '앍', '앎', '앓', '암', '압', '앗', '았', '앙', '앝', '앞', '애', '액', '앤', '앨', '앰', '앱', '앳', '앴', '앵', '야', '약', '얀', '얄', '얇', '얌', '얍', '얏', '양', '얕', '얗', '얘', '얜', '얠', '얩', '어', '억', '언', '얹', '얻', '얼', '얽', '얾', '엄', '업', '없', '엇', '었', '엉', '엊', '엌', '엎', '에', '엑', '엔', '엘', '엠', '엡', '엣', '엥', '여', '역', '엮', '연', '열', '엶', '엷', '염', '엽', '엾', '엿', '였', '영', '옅', '옆', '옇', '예', '옌', '옐', '옘', '옙', '옛', '옜', '오', '옥', '온', '올', '옭', '옮', '옰', '옳', '옴', '옵', '옷', '옹', '옻', '와', '왁', '완', '왈', '왐', '왑', '왓', '왔', '왕', '왜', '왝', '왠', '왬', '왯', '왱', '외', '왹', '왼', '욀', '욈', '욉', '욋', '욍', '요', '욕', '욘', '욜', '욤', '욥', '욧', '용', '우', '욱', '운', '울', '욹', '욺', '움', '웁', '웃', '웅', '워', '웍', '원', '월', '웜', '웝', '웠', '웡', '웨', '웩', '웬', '웰', '웸', '웹', '웽', '위', '윅', '윈', '윌', '윔', '윕', '윗', '윙', '유', '육', '윤', '율', '윰', '윱', '윳', '융', '윷', '으', '윽', '은', '을', '읊', '음', '읍', '읏', '응', '읒', '읓', '읔', '읕', '읖', '읗', '의', '읜', '읠', '읨', '읫', '이', '익', '인', '일', '읽', '읾', '잃', '임', '입', '잇', '있', '잉', '잊', '잎', '자', '작', '잔', '잖', '잗', '잘', '잚', '잠', '잡', '잣', '잤', '장', '잦', '재', '잭', '잰', '잴', '잼', '잽', '잿', '쟀', '쟁', '쟈', '쟉', '쟌', '쟎', '쟐', '쟘', '쟝', '쟤', '쟨', '쟬', '저', '적', '전', '절', '젊', '점', '접', '젓', '정', '젖', '제', '젝', '젠', '젤', '젬', '젭', '젯', '젱', '져', '젼', '졀', '졈', '졉', '졌', '졍', '졔', '조', '족', '존', '졸', '졺', '좀', '좁', '좃', '종', '좆', '좇', '좋', '좌', '좍', '좔', '좝', '좟', '좡', '좨', '좼', '좽', '죄', '죈', '죌', '죔', '죕', '죗', '죙', '죠', '죡', '죤', '죵', '주', '죽', '준', '줄', '줅', '줆', '줌', '줍', '줏', '중', '줘', '줬', '줴', '쥐', '쥑', '쥔', '쥘', '쥠', '쥡', '쥣', '쥬', '쥰', '쥴', '쥼', '즈', '즉', '즌', '즐', '즘', '즙', '즛', '증', '지', '직', '진', '짇', '질', '짊', '짐', '집', '짓', '징', '짖', '짙', '짚', '짜', '짝', '짠', '짢', '짤', '짧', '짬', '짭', '짯', '짰', '짱', '째', '짹', '짼', '쨀', '쨈', '쨉', '쨋', '쨌', '쨍', '쨔', '쨘', '쨩', '쩌', '쩍', '쩐', '쩔', '쩜', '쩝', '쩟', '쩠', '쩡', '쩨', '쩽', '쪄', '쪘', '쪼', '쪽', '쫀', '쫄', '쫌', '쫍', '쫏', '쫑', '쫓', '쫘', '쫙', '쫠', '쫬', '쫴', '쬈', '쬐', '쬔', '쬘', '쬠', '쬡', '쭁', '쭈', '쭉', '쭌', '쭐', '쭘', '쭙', '쭝', '쭤', '쭸', '쭹', '쮜', '쮸', '쯔', '쯤', '쯧', '쯩', '찌', '찍', '찐', '찔', '찜', '찝', '찡', '찢', '찧', '차', '착', '찬', '찮', '찰', '참', '찹', '찻', '찼', '창', '찾', '채', '책', '챈', '챌', '챔', '챕', '챗', '챘', '챙', '챠', '챤', '챦', '챨', '챰', '챵', '처', '척', '천', '철', '첨', '첩', '첫', '첬', '청', '체', '첵', '첸', '첼', '쳄', '쳅', '쳇', '쳉', '쳐', '쳔', '쳤', '쳬', '쳰', '촁', '초', '촉', '촌', '촐', '촘', '촙', '촛', '총', '촤', '촨', '촬', '촹', '최', '쵠', '쵤', '쵬', '쵭', '쵯', '쵱', '쵸', '춈', '추', '축', '춘', '출', '춤', '춥', '춧', '충', '춰', '췄', '췌', '췐', '취', '췬', '췰', '췸', '췹', '췻', '췽', '츄', '츈', '츌', '츔', '츙', '츠', '측', '츤', '츨', '츰', '츱', '츳', '층', '치', '칙', '친', '칟', '칠', '칡', '침', '칩', '칫', '칭', '카', '칵', '칸', '칼', '캄', '캅', '캇', '캉', '캐', '캑', '캔', '캘', '캠', '캡', '캣', '캤', '캥', '캬', '캭', '컁', '커', '컥', '컨', '컫', '컬', '컴', '컵', '컷', '컸', '컹', '케', '켁', '켄', '켈', '켐', '켑', '켓', '켕', '켜', '켠', '켤', '켬', '켭', '켯', '켰', '켱', '켸', '코', '콕', '콘', '콜', '콤', '콥', '콧', '콩', '콰', '콱', '콴', '콸', '쾀', '쾅', '쾌', '쾡', '쾨', '쾰', '쿄', '쿠', '쿡', '쿤', '쿨', '쿰', '쿱', '쿳', '쿵', '쿼', '퀀', '퀄', '퀑', '퀘', '퀭', '퀴', '퀵', '퀸', '퀼', '큄', '큅', '큇', '큉', '큐', '큔', '큘', '큠', '크', '큭', '큰', '클', '큼', '큽', '킁', '키', '킥', '킨', '킬', '킴', '킵', '킷', '킹', '타', '탁', '탄', '탈', '탉', '탐', '탑', '탓', '탔', '탕', '태', '택', '탠', '탤', '탬', '탭', '탯', '탰', '탱', '탸', '턍', '터', '턱', '턴', '털', '턺', '텀', '텁', '텃', '텄', '텅', '테', '텍', '텐', '텔', '템', '텝', '텟', '텡', '텨', '텬', '텼', '톄', '톈', '토', '톡', '톤', '톨', '톰', '톱', '톳', '통', '톺', '톼', '퇀', '퇘', '퇴', '퇸', '툇', '툉', '툐', '투', '툭', '툰', '툴', '툼', '툽', '툿', '퉁', '퉈', '퉜', '퉤', '튀', '튁', '튄', '튈', '튐', '튑', '튕', '튜', '튠', '튤', '튬', '튱', '트', '특', '튼', '튿', '틀', '틂', '틈', '틉', '틋', '틔', '틘', '틜', '틤', '틥', '티', '틱', '틴', '틸', '팀', '팁', '팃', '팅', '파', '팍', '팎', '판', '팔', '팖', '팜', '팝', '팟', '팠', '팡', '팥', '패', '팩', '팬', '팰', '팸', '팹', '팻', '팼', '팽', '퍄', '퍅', '퍼', '퍽', '펀', '펄', '펌', '펍', '펏', '펐', '펑', '페', '펙', '펜', '펠', '펨', '펩', '펫', '펭', '펴', '편', '펼', '폄', '폅', '폈', '평', '폐', '폘', '폡', '폣', '포', '폭', '폰', '폴', '폼', '폽', '폿', '퐁', '퐈', '퐝', '푀', '푄', '표', '푠', '푤', '푭', '푯', '푸', '푹', '푼', '푿', '풀', '풂', '품', '풉', '풋', '풍', '풔', '풩', '퓌', '퓐', '퓔', '퓜', '퓟', '퓨', '퓬', '퓰', '퓸', '퓻', '퓽', '프', '픈', '플', '픔', '픕', '픗', '피', '픽', '핀', '필', '핌', '핍', '핏', '핑', '하', '학', '한', '할', '핥', '함', '합', '핫', '항', '해', '핵', '핸', '핼', '햄', '햅', '햇', '했', '행', '햐', '향', '허', '헉', '헌', '헐', '헒', '험', '헙', '헛', '헝', '헤', '헥', '헨', '헬', '헴', '헵', '헷', '헹', '혀', '혁', '현', '혈', '혐', '협', '혓', '혔', '형', '혜', '혠', '혤', '혭', '호', '혹', '혼', '홀', '홅', '홈', '홉', '홋', '홍', '홑', '화', '확', '환', '활', '홧', '황', '홰', '홱', '홴', '횃', '횅', '회', '획', '횐', '횔', '횝', '횟', '횡', '효', '횬', '횰', '횹', '횻', '후', '훅', '훈', '훌', '훑', '훔', '훗', '훙', '훠', '훤', '훨', '훰', '훵', '훼', '훽', '휀', '휄', '휑', '휘', '휙', '휜', '휠', '휨', '휩', '휫', '휭', '휴', '휵', '휸', '휼', '흄', '흇', '흉', '흐', '흑', '흔', '흖', '흗', '흘', '흙', '흠', '흡', '흣', '흥', '흩', '희', '흰', '흴', '흼', '흽', '힁', '히', '힉', '힌', '힐', '힘', '힙', '힛', '힝']
```
</details>

<details>
<summary>28. get_all_incompleted_form_hangul_chars</summary>

This returns all incompleted form Hangul characters.

Returns:
- `List[str]`: all incompleted form Hangul characters

Examples:
```python
>>> from kss import Kss
>>> get_all_incompleted_form_hangul_chars = Kss("get_all_incompleted_form_hangul_chars")
>>> output = get_all_incompleted_form_hangul_chars()
>>> print(output)
['갂', '갃', '갅', '갆', '갋', '갌', '갍', '갎', '갏', '갘', '갞', '갟', '갡', '갢', '갣', '갥', '갦', '갧', '갨', '갩', '갪', '갫', '갮', '갲', '갳', '갴', '갵', '갶', '갷', '갺', '갻', '갽', '갾', '갿', '걁', '걂', '걃', '걄', '걅', '걆', '걇', '걈', '걉', '걊', '걌', '걎', '걏', '걐', '걑', '걒', '걓', '걕', '걖', '걗', '걙', '걚', '걛', '걝', '걞', '걟', '걠', '걡', '걢', '걣', '걤', '걥', '걦', '걧', '걨', '걩', '걪', '걫', '걬', '걭', '걮', '걯', '걲', '걳', '걵', '걶', '걹', '걻', '걼', '걽', '걾', '걿', '겂', '겇', '겈', '겍', '겎', '겏', '겑', '겒', '겓', '겕', '겖', '겗', '겘', '겙', '겚', '겛', '겞', '겢', '겣', '겤', '겥', '겦', '겧', '겫', '겭', '겮', '겱', '겲', '겳', '겴', '겵', '겶', '겷', '겺', '겾', '겿', '곀', '곂', '곃', '곅', '곆', '곇', '곉', '곊', '곋', '곍', '곎', '곏', '곐', '곑', '곒', '곓', '곔', '곖', '곘', '곙', '곚', '곛', '곜', '곝', '곞', '곟', '곢', '곣', '곥', '곦', '곩', '곫', '곭', '곮', '곲', '곴', '곷', '곸', '곹', '곺', '곻', '곾', '곿', '괁', '괂', '괃', '괅', '괇', '괈', '괉', '괊', '괋', '괎', '괐', '괒', '괓', '괔', '괕', '괖', '괗', '괙', '괚', '괛', '괝', '괞', '괟', '괡', '괢', '괣', '괤', '괥', '괦', '괧', '괨', '괪', '괫', '괮', '괯', '괰', '괱', '괲', '괳', '괶', '괷', '괹', '괺', '괻', '괽', '괾', '괿', '굀', '굁', '굂', '굃', '굆', '굈', '굊', '굋', '굌', '굍', '굎', '굏', '굑', '굒', '굓', '굕', '굖', '굗', '굙', '굚', '굛', '굜', '굝', '굞', '굟', '굠', '굢', '굤', '굥', '굦', '굧', '굨', '굩', '굪', '굫', '굮', '굯', '굱', '굲', '굷', '굸', '굹', '굺', '굾', '궀', '궃', '궄', '궅', '궆', '궇', '궊', '궋', '궍', '궎', '궏', '궑', '궒', '궓', '궔', '궕', '궖', '궗', '궘', '궙', '궚', '궛', '궞', '궟', '궠', '궡', '궢', '궣', '궥', '궦', '궧', '궨', '궩', '궪', '궫', '궬', '궭', '궮', '궯', '궰', '궱', '궲', '궳', '궴', '궵', '궶', '궸', '궹', '궺', '궻', '궼', '궽', '궾', '궿', '귂', '귃', '귅', '귆', '귇', '귉', '귊', '귋', '귌', '귍', '귎', '귏', '귒', '귔', '귕', '귖', '귗', '귘', '귙', '귚', '귛', '귝', '귞', '귟', '귡', '귢', '귣', '귥', '귦', '귧', '귨', '귩', '귪', '귫', '귬', '귭', '귮', '귯', '귰', '귱', '귲', '귳', '귴', '귵', '귶', '귷', '귺', '귻', '귽', '귾', '긂', '긃', '긄', '긅', '긆', '긇', '긊', '긌', '긎', '긏', '긐', '긑', '긒', '긓', '긕', '긖', '긗', '긘', '긙', '긚', '긛', '긜', '긝', '긞', '긟', '긠', '긡', '긢', '긣', '긤', '긥', '긦', '긧', '긨', '긩', '긪', '긫', '긬', '긭', '긮', '긯', '긲', '긳', '긵', '긶', '긹', '긻', '긼', '긽', '긾', '긿', '깂', '깄', '깇', '깈', '깉', '깋', '깏', '깑', '깒', '깓', '깕', '깗', '깘', '깙', '깚', '깛', '깞', '깢', '깣', '깤', '깦', '깧', '깪', '깫', '깭', '깮', '깯', '깱', '깲', '깳', '깴', '깵', '깶', '깷', '깺', '깾', '깿', '꺀', '꺁', '꺂', '꺃', '꺆', '꺇', '꺈', '꺉', '꺊', '꺋', '꺍', '꺎', '꺏', '꺐', '꺑', '꺒', '꺓', '꺔', '꺕', '꺖', '꺗', '꺘', '꺙', '꺚', '꺛', '꺜', '꺝', '꺞', '꺟', '꺠', '꺡', '꺢', '꺣', '꺤', '꺥', '꺦', '꺧', '꺨', '꺩', '꺪', '꺫', '꺬', '꺭', '꺮', '꺯', '꺰', '꺱', '꺲', '꺳', '꺴', '꺵', '꺶', '꺷', '꺸', '꺹', '꺺', '꺻', '꺿', '껁', '껂', '껃', '껅', '껆', '껇', '껈', '껉', '껊', '껋', '껎', '껒', '껓', '껔', '껕', '껖', '껗', '껚', '껛', '껝', '껞', '껟', '껠', '껡', '껢', '껣', '껤', '껥', '껦', '껧', '껩', '껪', '껬', '껮', '껯', '껰', '껱', '껲', '껳', '껵', '껶', '껷', '껹', '껺', '껻', '껽', '껾', '껿', '꼀', '꼁', '꼂', '꼃', '꼄', '꼅', '꼆', '꼉', '꼊', '꼋', '꼌', '꼎', '꼏', '꼑', '꼒', '꼓', '꼔', '꼕', '꼖', '꼗', '꼘', '꼙', '꼚', '꼛', '꼜', '꼝', '꼞', '꼟', '꼠', '꼡', '꼢', '꼣', '꼤', '꼥', '꼦', '꼧', '꼨', '꼩', '꼪', '꼫', '꼮', '꼯', '꼱', '꼳', '꼵', '꼶', '꼷', '꼸', '꼹', '꼺', '꼻', '꼾', '꽀', '꽄', '꽅', '꽆', '꽇', '꽊', '꽋', '꽌', '꽍', '꽎', '꽏', '꽑', '꽒', '꽓', '꽔', '꽕', '꽖', '꽗', '꽘', '꽙', '꽚', '꽛', '꽞', '꽟', '꽠', '꽡', '꽢', '꽣', '꽦', '꽧', '꽨', '꽩', '꽪', '꽫', '꽬', '꽭', '꽮', '꽯', '꽰', '꽱', '꽲', '꽳', '꽴', '꽵', '꽶', '꽷', '꽸', '꽺', '꽻', '꽼', '꽽', '꽾', '꽿', '꾁', '꾂', '꾃', '꾅', '꾆', '꾇', '꾉', '꾊', '꾋', '꾌', '꾍', '꾎', '꾏', '꾒', '꾓', '꾔', '꾖', '꾗', '꾘', '꾙', '꾚', '꾛', '꾝', '꾞', '꾟', '꾠', '꾡', '꾢', '꾣', '꾤', '꾥', '꾦', '꾧', '꾨', '꾩', '꾪', '꾫', '꾬', '꾭', '꾮', '꾯', '꾰', '꾱', '꾲', '꾳', '꾴', '꾵', '꾶', '꾷', '꾺', '꾻', '꾽', '꾾', '꾿', '꿁', '꿂', '꿃', '꿄', '꿅', '꿆', '꿊', '꿌', '꿏', '꿐', '꿑', '꿒', '꿓', '꿕', '꿖', '꿗', '꿘', '꿙', '꿚', '꿛', '꿝', '꿞', '꿟', '꿠', '꿡', '꿢', '꿣', '꿤', '꿥', '꿦', '꿧', '꿪', '꿫', '꿬', '꿭', '꿮', '꿯', '꿲', '꿳', '꿵', '꿶', '꿷', '꿹', '꿺', '꿻', '꿼', '꿽', '꿾', '꿿', '뀂', '뀃', '뀅', '뀆', '뀇', '뀈', '뀉', '뀊', '뀋', '뀍', '뀎', '뀏', '뀑', '뀒', '뀓', '뀕', '뀖', '뀗', '뀘', '뀙', '뀚', '뀛', '뀞', '뀟', '뀠', '뀡', '뀢', '뀣', '뀤', '뀥', '뀦', '뀧', '뀩', '뀪', '뀫', '뀬', '뀭', '뀮', '뀯', '뀰', '뀱', '뀲', '뀳', '뀴', '뀵', '뀶', '뀷', '뀸', '뀹', '뀺', '뀻', '뀼', '뀽', '뀾', '뀿', '끀', '끁', '끂', '끃', '끆', '끇', '끉', '끋', '끍', '끏', '끐', '끑', '끒', '끖', '끘', '끚', '끛', '끜', '끞', '끟', '끠', '끡', '끢', '끣', '끤', '끥', '끦', '끧', '끨', '끩', '끪', '끫', '끬', '끭', '끮', '끯', '끰', '끱', '끲', '끳', '끴', '끵', '끶', '끷', '끸', '끹', '끺', '끻', '끾', '끿', '낁', '낂', '낃', '낅', '낆', '낇', '낈', '낉', '낊', '낋', '낎', '낐', '낒', '낓', '낔', '낕', '낖', '낗', '낛', '낝', '낞', '낣', '낤', '낥', '낦', '낧', '낪', '낰', '낲', '낶', '낷', '낹', '낺', '낻', '낽', '낾', '낿', '냀', '냁', '냂', '냃', '냆', '냊', '냋', '냌', '냍', '냎', '냏', '냒', '냓', '냕', '냖', '냗', '냙', '냚', '냛', '냜', '냝', '냞', '냟', '냡', '냢', '냣', '냤', '냦', '냧', '냨', '냩', '냪', '냫', '냬', '냭', '냮', '냯', '냰', '냱', '냲', '냳', '냴', '냵', '냶', '냷', '냸', '냹', '냺', '냻', '냼', '냽', '냾', '냿', '넀', '넁', '넂', '넃', '넄', '넅', '넆', '넇', '넊', '넍', '넎', '넏', '넑', '넔', '넕', '넖', '넗', '넚', '넞', '넟', '넠', '넡', '넢', '넦', '넧', '넩', '넪', '넫', '넭', '넮', '넯', '넰', '넱', '넲', '넳', '넶', '넺', '넻', '넼', '넽', '넾', '넿', '녂', '녃', '녅', '녆', '녇', '녉', '녊', '녋', '녌', '녍', '녎', '녏', '녒', '녓', '녖', '녗', '녙', '녚', '녛', '녝', '녞', '녟', '녡', '녢', '녣', '녤', '녥', '녦', '녧', '녨', '녩', '녪', '녫', '녬', '녭', '녮', '녯', '녰', '녱', '녲', '녳', '녴', '녵', '녶', '녷', '녺', '녻', '녽', '녾', '녿', '놁', '놃', '놄', '놅', '놆', '놇', '놊', '놌', '놎', '놏', '놐', '놑', '놕', '놖', '놗', '놙', '놚', '놛', '놝', '놞', '놟', '놠', '놡', '놢', '놣', '놤', '놥', '놦', '놧', '놩', '놪', '놫', '놬', '놭', '놮', '놯', '놰', '놱', '놲', '놳', '놴', '놵', '놶', '놷', '놸', '놹', '놺', '놻', '놼', '놽', '놾', '놿', '뇀', '뇁', '뇂', '뇃', '뇄', '뇅', '뇆', '뇇', '뇈', '뇉', '뇊', '뇋', '뇍', '뇎', '뇏', '뇑', '뇒', '뇓', '뇕', '뇖', '뇗', '뇘', '뇙', '뇚', '뇛', '뇞', '뇠', '뇡', '뇢', '뇣', '뇤', '뇥', '뇦', '뇧', '뇪', '뇫', '뇭', '뇮', '뇯', '뇱', '뇲', '뇳', '뇴', '뇵', '뇶', '뇷', '뇸', '뇺', '뇼', '뇾', '뇿', '눀', '눁', '눂', '눃', '눆', '눇', '눉', '눊', '눍', '눎', '눏', '눐', '눑', '눒', '눓', '눖', '눘', '눚', '눛', '눜', '눝', '눞', '눟', '눡', '눢', '눣', '눤', '눥', '눦', '눧', '눨', '눩', '눪', '눫', '눬', '눭', '눮', '눯', '눰', '눱', '눲', '눳', '눵', '눶', '눷', '눸', '눹', '눺', '눻', '눽', '눾', '눿', '뉀', '뉁', '뉂', '뉃', '뉄', '뉅', '뉆', '뉇', '뉈', '뉉', '뉊', '뉋', '뉌', '뉍', '뉎', '뉏', '뉐', '뉑', '뉒', '뉓', '뉔', '뉕', '뉖', '뉗', '뉙', '뉚', '뉛', '뉝', '뉞', '뉟', '뉡', '뉢', '뉣', '뉤', '뉥', '뉦', '뉧', '뉪', '뉫', '뉬', '뉭', '뉮', '뉯', '뉰', '뉱', '뉲', '뉳', '뉶', '뉷', '뉸', '뉹', '뉺', '뉻', '뉽', '뉾', '뉿', '늀', '늁', '늂', '늃', '늆', '늇', '늈', '늊', '늋', '늌', '늍', '늎', '늏', '늒', '늓', '늕', '늖', '늗', '늛', '늜', '늝', '늞', '늟', '늢', '늤', '늧', '늨', '늩', '늫', '늭', '늮', '늯', '늱', '늲', '늳', '늵', '늶', '늷', '늸', '늹', '늺', '늻', '늼', '늽', '늾', '늿', '닀', '닁', '닂', '닃', '닄', '닅', '닆', '닇', '닊', '닋', '닍', '닎', '닏', '닑', '닓', '닔', '닕', '닖', '닗', '닚', '닜', '닞', '닟', '닠', '닡', '닣', '닧', '닩', '닪', '닰', '닱', '닲', '닶', '닼', '닽', '닾', '댂', '댃', '댅', '댆', '댇', '댉', '댊', '댋', '댌', '댍', '댎', '댏', '댒', '댖', '댗', '댘', '댙', '댚', '댛', '댝', '댞', '댟', '댠', '댡', '댢', '댣', '댤', '댥', '댦', '댧', '댨', '댩', '댪', '댫', '댬', '댭', '댮', '댯', '댰', '댱', '댲', '댳', '댴', '댵', '댶', '댷', '댸', '댹', '댺', '댻', '댼', '댽', '댾', '댿', '덀', '덁', '덂', '덃', '덄', '덅', '덆', '덇', '덈', '덉', '덊', '덋', '덌', '덍', '덎', '덏', '덐', '덑', '덒', '덓', '덗', '덙', '덚', '덝', '덠', '덡', '덢', '덣', '덦', '덨', '덪', '덬', '덭', '덯', '덲', '덳', '덵', '덶', '덷', '덹', '덺', '덻', '덼', '덽', '덾', '덿', '뎂', '뎆', '뎇', '뎈', '뎉', '뎊', '뎋', '뎍', '뎎', '뎏', '뎑', '뎒', '뎓', '뎕', '뎖', '뎗', '뎘', '뎙', '뎚', '뎛', '뎜', '뎝', '뎞', '뎟', '뎢', '뎣', '뎤', '뎥', '뎦', '뎧', '뎩', '뎪', '뎫', '뎭', '뎮', '뎯', '뎰', '뎱', '뎲', '뎳', '뎴', '뎵', '뎶', '뎷', '뎸', '뎹', '뎺', '뎻', '뎼', '뎽', '뎾', '뎿', '돀', '돁', '돂', '돃', '돆', '돇', '돉', '돊', '돍', '돏', '돑', '돒', '돓', '돖', '돘', '돚', '돜', '돞', '돟', '돡', '돢', '돣', '돥', '돦', '돧', '돩', '돪', '돫', '돬', '돭', '돮', '돯', '돰', '돱', '돲', '돳', '돴', '돵', '돶', '돷', '돸', '돹', '돺', '돻', '돽', '돾', '돿', '됀', '됁', '됂', '됃', '됄', '됅', '됆', '됇', '됈', '됉', '됊', '됋', '됌', '됍', '됎', '됏', '됑', '됒', '됓', '됔', '됕', '됖', '됗', '됙', '됚', '됛', '됝', '됞', '됟', '됡', '됢', '됣', '됤', '됥', '됦', '됧', '됪', '됬', '됭', '됮', '됯', '됰', '됱', '됲', '됳', '됵', '됶', '됷', '됸', '됹', '됺', '됻', '됼', '됽', '됾', '됿', '둀', '둁', '둂', '둃', '둄', '둅', '둆', '둇', '둈', '둉', '둊', '둋', '둌', '둍', '둎', '둏', '둒', '둓', '둕', '둖', '둗', '둙', '둚', '둛', '둜', '둝', '둞', '둟', '둢', '둤', '둦', '둧', '둨', '둩', '둪', '둫', '둭', '둮', '둯', '둰', '둱', '둲', '둳', '둴', '둵', '둶', '둷', '둸', '둹', '둺', '둻', '둼', '둽', '둾', '둿', '뒁', '뒂', '뒃', '뒄', '뒅', '뒆', '뒇', '뒉', '뒊', '뒋', '뒌', '뒍', '뒎', '뒏', '뒐', '뒑', '뒒', '뒓', '뒔', '뒕', '뒖', '뒗', '뒘', '뒙', '뒚', '뒛', '뒜', '뒞', '뒟', '뒠', '뒡', '뒢', '뒣', '뒥', '뒦', '뒧', '뒩', '뒪', '뒫', '뒭', '뒮', '뒯', '뒰', '뒱', '뒲', '뒳', '뒴', '뒶', '뒸', '뒺', '뒻', '뒼', '뒽', '뒾', '뒿', '듁', '듂', '듃', '듅', '듆', '듇', '듉', '듊', '듋', '듌', '듍', '듎', '듏', '듑', '듒', '듓', '듔', '듖', '듗', '듘', '듙', '듚', '듛', '듞', '듟', '듡', '듢', '듥', '듧', '듨', '듩', '듪', '듫', '듮', '듰', '듲', '듳', '듴', '듵', '듶', '듷', '듹', '듺', '듻', '듼', '듽', '듾', '듿', '딀', '딁', '딂', '딃', '딄', '딅', '딆', '딇', '딈', '딉', '딊', '딋', '딌', '딍', '딎', '딏', '딐', '딑', '딒', '딓', '딖', '딗', '딙', '딚', '딝', '딞', '딟', '딠', '딡', '딢', '딣', '딦', '딫', '딬', '딭', '딮', '딯', '딲', '딳', '딵', '딶', '딷', '딹', '딺', '딻', '딼', '딽', '딾', '딿', '땂', '땆', '땇', '땈', '땉', '땊', '땎', '땏', '땑', '땒', '땓', '땕', '땖', '땗', '땘', '땙', '땚', '땛', '땞', '땢', '땣', '땤', '땥', '땦', '땧', '땨', '땩', '땪', '땫', '땬', '땭', '땮', '땯', '땰', '땱', '땲', '땳', '땴', '땵', '땶', '땷', '땸', '땹', '땺', '땻', '땼', '땽', '땾', '땿', '떀', '떁', '떂', '떃', '떄', '떅', '떆', '떇', '떈', '떉', '떊', '떋', '떌', '떍', '떎', '떏', '떐', '떑', '떒', '떓', '떔', '떕', '떖', '떗', '떘', '떙', '떚', '떛', '떜', '떝', '떞', '떟', '떢', '떣', '떥', '떦', '떧', '떩', '떬', '떭', '떮', '떯', '떲', '떶', '떷', '떸', '떹', '떺', '떾', '떿', '뗁', '뗂', '뗃', '뗅', '뗆', '뗇', '뗈', '뗉', '뗊', '뗋', '뗎', '뗒', '뗓', '뗔', '뗕', '뗖', '뗗', '뗙', '뗚', '뗛', '뗜', '뗝', '뗞', '뗟', '뗠', '뗡', '뗢', '뗣', '뗤', '뗥', '뗦', '뗧', '뗨', '뗩', '뗪', '뗫', '뗭', '뗮', '뗯', '뗰', '뗱', '뗲', '뗳', '뗴', '뗵', '뗶', '뗷', '뗸', '뗹', '뗺', '뗻', '뗼', '뗽', '뗾', '뗿', '똀', '똁', '똂', '똃', '똄', '똅', '똆', '똇', '똈', '똉', '똊', '똋', '똌', '똍', '똎', '똏', '똒', '똓', '똕', '똖', '똗', '똙', '똚', '똛', '똜', '똝', '똞', '똟', '똠', '똡', '똢', '똣', '똤', '똦', '똧', '똨', '똩', '똪', '똫', '똭', '똮', '똯', '똰', '똱', '똲', '똳', '똵', '똶', '똷', '똸', '똹', '똺', '똻', '똼', '똽', '똾', '똿', '뙀', '뙁', '뙂', '뙃', '뙄', '뙅', '뙆', '뙇', '뙉', '뙊', '뙋', '뙌', '뙍', '뙎', '뙏', '뙐', '뙑', '뙒', '뙓', '뙔', '뙕', '뙖', '뙗', '뙘', '뙙', '뙚', '뙛', '뙜', '뙝', '뙞', '뙟', '뙠', '뙡', '뙢', '뙣', '뙥', '뙦', '뙧', '뙩', '뙪', '뙫', '뙬', '뙭', '뙮', '뙯', '뙰', '뙱', '뙲', '뙳', '뙴', '뙵', '뙶', '뙷', '뙸', '뙹', '뙺', '뙻', '뙼', '뙽', '뙾', '뙿', '뚀', '뚁', '뚂', '뚃', '뚄', '뚅', '뚆', '뚇', '뚈', '뚉', '뚊', '뚋', '뚌', '뚍', '뚎', '뚏', '뚐', '뚑', '뚒', '뚓', '뚔', '뚕', '뚖', '뚗', '뚘', '뚙', '뚚', '뚛', '뚞', '뚟', '뚡', '뚢', '뚣', '뚥', '뚦', '뚧', '뚨', '뚩', '뚪', '뚭', '뚮', '뚯', '뚰', '뚲', '뚳', '뚴', '뚵', '뚶', '뚷', '뚸', '뚹', '뚺', '뚻', '뚼', '뚽', '뚾', '뚿', '뛀', '뛁', '뛂', '뛃', '뛄', '뛅', '뛆', '뛇', '뛈', '뛉', '뛊', '뛋', '뛌', '뛍', '뛎', '뛏', '뛐', '뛑', '뛒', '뛓', '뛕', '뛖', '뛗', '뛘', '뛙', '뛚', '뛛', '뛜', '뛝', '뛞', '뛟', '뛠', '뛡', '뛢', '뛣', '뛤', '뛥', '뛦', '뛧', '뛨', '뛩', '뛪', '뛫', '뛬', '뛭', '뛮', '뛯', '뛱', '뛲', '뛳', '뛵', '뛶', '뛷', '뛹', '뛺', '뛻', '뛼', '뛽', '뛾', '뛿', '뜂', '뜃', '뜄', '뜆', '뜇', '뜈', '뜉', '뜊', '뜋', '뜌', '뜍', '뜎', '뜏', '뜐', '뜑', '뜒', '뜓', '뜔', '뜕', '뜖', '뜗', '뜘', '뜙', '뜚', '뜛', '뜜', '뜝', '뜞', '뜟', '뜠', '뜡', '뜢', '뜣', '뜤', '뜥', '뜦', '뜧', '뜪', '뜫', '뜭', '뜮', '뜱', '뜲', '뜳', '뜴', '뜵', '뜶', '뜷', '뜺', '뜼', '뜽', '뜾', '뜿', '띀', '띁', '띂', '띃', '띅', '띆', '띇', '띉', '띊', '띋', '띍', '띎', '띏', '띐', '띑', '띒', '띓', '띖', '띗', '띘', '띙', '띚', '띛', '띜', '띝', '띞', '띟', '띡', '띢', '띣', '띥', '띦', '띧', '띩', '띪', '띫', '띬', '띭', '띮', '띯', '띲', '띴', '띶', '띷', '띸', '띹', '띺', '띻', '띾', '띿', '랁', '랂', '랃', '랅', '랆', '랇', '랈', '랉', '랊', '랋', '랎', '랓', '랔', '랕', '랚', '랛', '랝', '랞', '랟', '랡', '랢', '랣', '랤', '랥', '랦', '랧', '랪', '랮', '랯', '랰', '랱', '랲', '랳', '랶', '랷', '랹', '랺', '랻', '랼', '랽', '랾', '랿', '럀', '럁', '럂', '럃', '럄', '럅', '럆', '럈', '럊', '럋', '럌', '럍', '럎', '럏', '럐', '럑', '럒', '럓', '럔', '럕', '럖', '럗', '럘', '럙', '럚', '럛', '럜', '럝', '럞', '럟', '럠', '럡', '럢', '럣', '럤', '럥', '럦', '럧', '럨', '럩', '럪', '럫', '럮', '럯', '럱', '럲', '럳', '럵', '럶', '럷', '럸', '럹', '럺', '럻', '럾', '렂', '렃', '렄', '렅', '렆', '렊', '렋', '렍', '렎', '렏', '렑', '렒', '렓', '렔', '렕', '렖', '렗', '렚', '렜', '렞', '렟', '렠', '렡', '렢', '렣', '렦', '렧', '렩', '렪', '렫', '렭', '렮', '렯', '렰', '렱', '렲', '렳', '렶', '렺', '렻', '렼', '렽', '렾', '렿', '롁', '롂', '롃', '롅', '롆', '롇', '롈', '롉', '롊', '롋', '롌', '롍', '롎', '롏', '롐', '롒', '롔', '롕', '롖', '롗', '롘', '롙', '롚', '롛', '롞', '롟', '롡', '롢', '롣', '롥', '롦', '롧', '롨', '롩', '롪', '롫', '롮', '롰', '롲', '롳', '롴', '롵', '롶', '롷', '롹', '롺', '롻', '롽', '롾', '롿', '뢀', '뢁', '뢂', '뢃', '뢄', '뢅', '뢆', '뢇', '뢈', '뢉', '뢊', '뢋', '뢌', '뢎', '뢏', '뢐', '뢑', '뢒', '뢓', '뢔', '뢕', '뢖', '뢗', '뢘', '뢙', '뢚', '뢛', '뢜', '뢝', '뢞', '뢟', '뢠', '뢡', '뢢', '뢣', '뢤', '뢥', '뢦', '뢧', '뢩', '뢪', '뢫', '뢬', '뢭', '뢮', '뢯', '뢱', '뢲', '뢳', '뢵', '뢶', '뢷', '뢹', '뢺', '뢻', '뢼', '뢽', '뢾', '뢿', '룂', '룄', '룆', '룇', '룈', '룉', '룊', '룋', '룍', '룎', '룏', '룑', '룒', '룓', '룕', '룖', '룗', '룘', '룙', '룚', '룛', '룜', '룞', '룠', '룢', '룣', '룤', '룥', '룦', '룧', '룪', '룫', '룭', '룮', '룯', '룱', '룲', '룳', '룴', '룵', '룶', '룷', '룺', '룼', '룾', '룿', '뤀', '뤁', '뤂', '뤃', '뤅', '뤆', '뤇', '뤈', '뤉', '뤊', '뤋', '뤌', '뤍', '뤎', '뤏', '뤐', '뤑', '뤒', '뤓', '뤔', '뤕', '뤖', '뤗', '뤙', '뤚', '뤛', '뤜', '뤝', '뤞', '뤟', '뤡', '뤢', '뤣', '뤤', '뤥', '뤦', '뤧', '뤨', '뤩', '뤪', '뤫', '뤬', '뤭', '뤮', '뤯', '뤰', '뤱', '뤲', '뤳', '뤴', '뤵', '뤶', '뤷', '뤸', '뤹', '뤺', '뤻', '뤾', '뤿', '륁', '륂', '륃', '륅', '륆', '륇', '륈', '륉', '륊', '륋', '륍', '륎', '륐', '륒', '륓', '륔', '륕', '륖', '륗', '륚', '륛', '륝', '륞', '륟', '륡', '륢', '륣', '륤', '륥', '륦', '륧', '륪', '륬', '륮', '륯', '륰', '륱', '륲', '륳', '륶', '륷', '륹', '륺', '륻', '륽', '륾', '륿', '릀', '릁', '릂', '릃', '릆', '릈', '릋', '릌', '릏', '릐', '릑', '릒', '릓', '릔', '릕', '릖', '릗', '릘', '릙', '릚', '릛', '릜', '릝', '릞', '릟', '릠', '릡', '릢', '릣', '릤', '릥', '릦', '릧', '릨', '릩', '릪', '릫', '릮', '릯', '릱', '릲', '릳', '릵', '릶', '릷', '릸', '릹', '릺', '릻', '릾', '맀', '맂', '맃', '맄', '맅', '맆', '맇', '맊', '맋', '맍', '맓', '맔', '맕', '맖', '맗', '맚', '맜', '맟', '맠', '맢', '맦', '맧', '맩', '맪', '맫', '맭', '맮', '맯', '맰', '맱', '맲', '맳', '맶', '맻', '맼', '맽', '맾', '맿', '먂', '먃', '먄', '먅', '먆', '먇', '먉', '먊', '먋', '먌', '먍', '먎', '먏', '먐', '먑', '먒', '먓', '먔', '먖', '먗', '먘', '먙', '먚', '먛', '먜', '먝', '먞', '먟', '먠', '먡', '먢', '먣', '먤', '먥', '먦', '먧', '먨', '먩', '먪', '먫', '먬', '먭', '먮', '먯', '먰', '먱', '먲', '먳', '먴', '먵', '먶', '먷', '먺', '먻', '먽', '먾', '먿', '멁', '멃', '멄', '멅', '멆', '멇', '멊', '멌', '멏', '멐', '멑', '멒', '멖', '멗', '멙', '멚', '멛', '멝', '멞', '멟', '멠', '멡', '멢', '멣', '멦', '멪', '멫', '멬', '멭', '멮', '멯', '멲', '멳', '멵', '멶', '멷', '멹', '멺', '멻', '멼', '멽', '멾', '멿', '몀', '몁', '몂', '몆', '몈', '몉', '몊', '몋', '몍', '몎', '몏', '몐', '몑', '몒', '몓', '몔', '몕', '몖', '몗', '몘', '몙', '몚', '몛', '몜', '몝', '몞', '몟', '몠', '몡', '몢', '몣', '몤', '몥', '몦', '몧', '몪', '몭', '몮', '몯', '몱', '몳', '몴', '몵', '몶', '몷', '몺', '몼', '몾', '몿', '뫀', '뫁', '뫂', '뫃', '뫅', '뫆', '뫇', '뫉', '뫊', '뫋', '뫌', '뫍', '뫎', '뫏', '뫐', '뫑', '뫒', '뫓', '뫔', '뫕', '뫖', '뫗', '뫚', '뫛', '뫜', '뫝', '뫞', '뫟', '뫠', '뫡', '뫢', '뫣', '뫤', '뫥', '뫦', '뫧', '뫨', '뫩', '뫪', '뫫', '뫬', '뫭', '뫮', '뫯', '뫰', '뫱', '뫲', '뫳', '뫴', '뫵', '뫶', '뫷', '뫸', '뫹', '뫺', '뫻', '뫽', '뫾', '뫿', '묁', '묂', '묃', '묅', '묆', '묇', '묈', '묉', '묊', '묋', '묌', '묎', '묐', '묒', '묓', '묔', '묕', '묖', '묗', '묙', '묚', '묛', '묝', '묞', '묟', '묡', '묢', '묣', '묤', '묥', '묦', '묧', '묨', '묪', '묬', '묭', '묮', '묯', '묰', '묱', '묲', '묳', '묷', '묹', '묺', '묿', '뭀', '뭁', '뭂', '뭃', '뭆', '뭈', '뭊', '뭋', '뭌', '뭎', '뭑', '뭒', '뭓', '뭕', '뭖', '뭗', '뭙', '뭚', '뭛', '뭜', '뭝', '뭞', '뭟', '뭠', '뭢', '뭤', '뭥', '뭦', '뭧', '뭨', '뭩', '뭪', '뭫', '뭭', '뭮', '뭯', '뭰', '뭱', '뭲', '뭳', '뭴', '뭵', '뭶', '뭷', '뭸', '뭹', '뭺', '뭻', '뭼', '뭽', '뭾', '뭿', '뮀', '뮁', '뮂', '뮃', '뮄', '뮅', '뮆', '뮇', '뮉', '뮊', '뮋', '뮍', '뮎', '뮏', '뮑', '뮒', '뮓', '뮔', '뮕', '뮖', '뮗', '뮘', '뮙', '뮚', '뮛', '뮜', '뮝', '뮞', '뮟', '뮠', '뮡', '뮢', '뮣', '뮥', '뮦', '뮧', '뮩', '뮪', '뮫', '뮭', '뮮', '뮯', '뮰', '뮱', '뮲', '뮳', '뮵', '뮶', '뮸', '뮹', '뮺', '뮻', '뮼', '뮽', '뮾', '뮿', '믁', '믂', '믃', '믅', '믆', '믇', '믉', '믊', '믋', '믌', '믍', '믎', '믏', '믑', '믒', '믔', '믕', '믖', '믗', '믘', '믙', '믚', '믛', '믜', '믝', '믞', '믟', '믠', '믡', '믢', '믣', '믤', '믥', '믦', '믧', '믨', '믩', '믪', '믫', '믬', '믭', '믮', '믯', '믰', '믱', '믲', '믳', '믴', '믵', '믶', '믷', '믺', '믻', '믽', '믾', '밁', '밃', '밄', '밅', '밆', '밇', '밊', '밎', '밐', '밒', '밓', '밙', '밚', '밠', '밡', '밢', '밣', '밦', '밨', '밪', '밫', '밬', '밮', '밯', '밲', '밳', '밵', '밶', '밷', '밹', '밺', '밻', '밼', '밽', '밾', '밿', '뱂', '뱆', '뱇', '뱈', '뱊', '뱋', '뱎', '뱏', '뱑', '뱒', '뱓', '뱔', '뱕', '뱖', '뱗', '뱘', '뱙', '뱚', '뱛', '뱜', '뱞', '뱟', '뱠', '뱡', '뱢', '뱣', '뱤', '뱥', '뱦', '뱧', '뱨', '뱩', '뱪', '뱫', '뱬', '뱭', '뱮', '뱯', '뱰', '뱱', '뱲', '뱳', '뱴', '뱵', '뱶', '뱷', '뱸', '뱹', '뱺', '뱻', '뱼', '뱽', '뱾', '뱿', '벀', '벁', '벂', '벃', '벆', '벇', '벉', '벊', '벍', '벏', '벐', '벑', '벒', '벓', '벖', '벘', '벛', '벜', '벝', '벞', '벟', '벢', '벣', '벥', '벦', '벩', '벪', '벫', '벬', '벭', '벮', '벯', '벲', '벶', '벷', '벸', '벹', '벺', '벻', '벾', '벿', '볁', '볂', '볃', '볅', '볆', '볇', '볈', '볉', '볊', '볋', '볌', '볎', '볒', '볓', '볔', '볖', '볗', '볙', '볚', '볛', '볝', '볞', '볟', '볠', '볡', '볢', '볣', '볤', '볥', '볦', '볧', '볨', '볩', '볪', '볫', '볬', '볭', '볮', '볯', '볰', '볱', '볲', '볳', '볷', '볹', '볺', '볻', '볽', '볾', '볿', '봀', '봁', '봂', '봃', '봆', '봈', '봊', '봋', '봌', '봍', '봎', '봏', '봑', '봒', '봓', '봕', '봖', '봗', '봘', '봙', '봚', '봛', '봜', '봝', '봞', '봟', '봠', '봡', '봢', '봣', '봥', '봦', '봧', '봨', '봩', '봪', '봫', '봭', '봮', '봯', '봰', '봱', '봲', '봳', '봴', '봵', '봶', '봷', '봸', '봹', '봺', '봻', '봼', '봽', '봾', '봿', '뵁', '뵂', '뵃', '뵄', '뵅', '뵆', '뵇', '뵊', '뵋', '뵍', '뵎', '뵏', '뵑', '뵒', '뵓', '뵔', '뵕', '뵖', '뵗', '뵚', '뵛', '뵜', '뵝', '뵞', '뵟', '뵠', '뵡', '뵢', '뵣', '뵥', '뵦', '뵧', '뵩', '뵪', '뵫', '뵬', '뵭', '뵮', '뵯', '뵰', '뵱', '뵲', '뵳', '뵴', '뵵', '뵶', '뵷', '뵸', '뵹', '뵺', '뵻', '뵼', '뵽', '뵾', '뵿', '붂', '붃', '붅', '붆', '붋', '붌', '붍', '붎', '붏', '붒', '붔', '붖', '붗', '붘', '붛', '붝', '붞', '붟', '붠', '붡', '붢', '붣', '붥', '붦', '붧', '붨', '붩', '붪', '붫', '붬', '붭', '붮', '붯', '붱', '붲', '붳', '붴', '붵', '붶', '붷', '붹', '붺', '붻', '붼', '붽', '붾', '붿', '뷀', '뷁', '뷂', '뷃', '뷄', '뷅', '뷆', '뷇', '뷈', '뷉', '뷊', '뷋', '뷌', '뷍', '뷎', '뷏', '뷐', '뷑', '뷒', '뷓', '뷖', '뷗', '뷙', '뷚', '뷛', '뷝', '뷞', '뷟', '뷠', '뷡', '뷢', '뷣', '뷤', '뷥', '뷦', '뷧', '뷨', '뷪', '뷫', '뷬', '뷭', '뷮', '뷯', '뷱', '뷲', '뷳', '뷵', '뷶', '뷷', '뷹', '뷺', '뷻', '뷼', '뷽', '뷾', '뷿', '븁', '븂', '븄', '븆', '븇', '븈', '븉', '븊', '븋', '븎', '븏', '븑', '븒', '븓', '븕', '븖', '븗', '븘', '븙', '븚', '븛', '븞', '븠', '븡', '븢', '븣', '븤', '븥', '븦', '븧', '븨', '븩', '븪', '븫', '븬', '븭', '븮', '븯', '븰', '븱', '븲', '븳', '븴', '븵', '븶', '븷', '븸', '븹', '븺', '븻', '븼', '븽', '븾', '븿', '빀', '빁', '빂', '빃', '빆', '빇', '빉', '빊', '빋', '빍', '빏', '빐', '빑', '빒', '빓', '빖', '빘', '빜', '빝', '빞', '빟', '빢', '빣', '빥', '빦', '빧', '빩', '빫', '빬', '빭', '빮', '빯', '빲', '빶', '빷', '빸', '빹', '빺', '빾', '빿', '뺁', '뺂', '뺃', '뺅', '뺆', '뺇', '뺈', '뺉', '뺊', '뺋', '뺎', '뺒', '뺓', '뺔', '뺕', '뺖', '뺗', '뺚', '뺛', '뺜', '뺝', '뺞', '뺟', '뺠', '뺡', '뺢', '뺣', '뺤', '뺥', '뺦', '뺧', '뺩', '뺪', '뺫', '뺬', '뺭', '뺮', '뺯', '뺰', '뺱', '뺲', '뺳', '뺴', '뺵', '뺶', '뺷', '뺸', '뺹', '뺺', '뺻', '뺼', '뺽', '뺾', '뺿', '뻀', '뻁', '뻂', '뻃', '뻄', '뻅', '뻆', '뻇', '뻈', '뻉', '뻊', '뻋', '뻌', '뻍', '뻎', '뻏', '뻒', '뻓', '뻕', '뻖', '뻙', '뻚', '뻛', '뻜', '뻝', '뻞', '뻟', '뻡', '뻢', '뻦', '뻧', '뻨', '뻩', '뻪', '뻫', '뻭', '뻮', '뻯', '뻰', '뻱', '뻲', '뻳', '뻴', '뻵', '뻶', '뻷', '뻸', '뻹', '뻺', '뻻', '뻼', '뻽', '뻾', '뻿', '뼀', '뼂', '뼃', '뼄', '뼅', '뼆', '뼇', '뼊', '뼋', '뼌', '뼍', '뼎', '뼏', '뼐', '뼑', '뼒', '뼓', '뼔', '뼕', '뼖', '뼗', '뼚', '뼞', '뼟', '뼠', '뼡', '뼢', '뼣', '뼤', '뼥', '뼦', '뼧', '뼨', '뼩', '뼪', '뼫', '뼬', '뼭', '뼮', '뼯', '뼰', '뼱', '뼲', '뼳', '뼴', '뼵', '뼶', '뼷', '뼸', '뼹', '뼺', '뼻', '뼼', '뼽', '뼾', '뼿', '뽂', '뽃', '뽅', '뽆', '뽇', '뽉', '뽊', '뽋', '뽌', '뽍', '뽎', '뽏', '뽒', '뽓', '뽔', '뽖', '뽗', '뽘', '뽙', '뽚', '뽛', '뽜', '뽝', '뽞', '뽟', '뽠', '뽡', '뽢', '뽣', '뽤', '뽥', '뽦', '뽧', '뽨', '뽩', '뽪', '뽫', '뽬', '뽭', '뽮', '뽯', '뽰', '뽱', '뽲', '뽳', '뽴', '뽵', '뽶', '뽷', '뽸', '뽹', '뽺', '뽻', '뽼', '뽽', '뽾', '뽿', '뾀', '뾁', '뾂', '뾃', '뾄', '뾅', '뾆', '뾇', '뾈', '뾉', '뾊', '뾋', '뾌', '뾍', '뾎', '뾏', '뾐', '뾑', '뾒', '뾓', '뾕', '뾖', '뾗', '뾘', '뾙', '뾚', '뾛', '뾜', '뾝', '뾞', '뾟', '뾠', '뾡', '뾢', '뾣', '뾤', '뾥', '뾦', '뾧', '뾨', '뾩', '뾪', '뾫', '뾬', '뾭', '뾮', '뾯', '뾱', '뾲', '뾳', '뾴', '뾵', '뾶', '뾷', '뾸', '뾹', '뾺', '뾻', '뾼', '뾽', '뾾', '뾿', '뿀', '뿁', '뿂', '뿃', '뿄', '뿆', '뿇', '뿈', '뿉', '뿊', '뿋', '뿎', '뿏', '뿑', '뿒', '뿓', '뿕', '뿖', '뿗', '뿘', '뿙', '뿚', '뿛', '뿝', '뿞', '뿠', '뿢', '뿣', '뿤', '뿥', '뿦', '뿧', '뿨', '뿩', '뿪', '뿫', '뿬', '뿭', '뿮', '뿯', '뿰', '뿱', '뿲', '뿳', '뿴', '뿵', '뿶', '뿷', '뿸', '뿹', '뿺', '뿻', '뿼', '뿽', '뿾', '뿿', '쀀', '쀁', '쀂', '쀃', '쀄', '쀅', '쀆', '쀇', '쀈', '쀉', '쀊', '쀋', '쀌', '쀍', '쀎', '쀏', '쀐', '쀑', '쀒', '쀓', '쀔', '쀕', '쀖', '쀗', '쀘', '쀙', '쀚', '쀛', '쀜', '쀝', '쀞', '쀟', '쀠', '쀡', '쀢', '쀣', '쀤', '쀥', '쀦', '쀧', '쀨', '쀩', '쀪', '쀫', '쀬', '쀭', '쀮', '쀯', '쀰', '쀱', '쀲', '쀳', '쀴', '쀵', '쀶', '쀷', '쀸', '쀹', '쀺', '쀻', '쀽', '쀾', '쀿', '쁀', '쁁', '쁂', '쁃', '쁄', '쁅', '쁆', '쁇', '쁈', '쁉', '쁊', '쁋', '쁌', '쁍', '쁎', '쁏', '쁐', '쁒', '쁓', '쁔', '쁕', '쁖', '쁗', '쁙', '쁚', '쁛', '쁝', '쁞', '쁟', '쁡', '쁢', '쁣', '쁤', '쁥', '쁦', '쁧', '쁪', '쁫', '쁬', '쁭', '쁮', '쁯', '쁰', '쁱', '쁲', '쁳', '쁴', '쁵', '쁶', '쁷', '쁸', '쁹', '쁺', '쁻', '쁼', '쁽', '쁾', '쁿', '삀', '삁', '삂', '삃', '삄', '삅', '삆', '삇', '삈', '삉', '삊', '삋', '삌', '삍', '삎', '삏', '삒', '삓', '삕', '삖', '삗', '삙', '삚', '삛', '삜', '삝', '삞', '삟', '삢', '삤', '삦', '삧', '삨', '삩', '삪', '삫', '삮', '삱', '삲', '삷', '삸', '삹', '삺', '삻', '삾', '샂', '샃', '샄', '샆', '샇', '샊', '샋', '샍', '샎', '샏', '샑', '샒', '샓', '샔', '샕', '샖', '샗', '샚', '샞', '샟', '샠', '샡', '샢', '샣', '샦', '샧', '샩', '샪', '샫', '샭', '샮', '샯', '샰', '샱', '샲', '샳', '샶', '샸', '샺', '샻', '샼', '샽', '샾', '샿', '섁', '섂', '섃', '섅', '섆', '섇', '섉', '섊', '섋', '섌', '섍', '섎', '섏', '섑', '섒', '섓', '섔', '섖', '섗', '섘', '섙', '섚', '섛', '섡', '섢', '섥', '섨', '섩', '섪', '섫', '섮', '섲', '섳', '섴', '섵', '섷', '섺', '섻', '섽', '섾', '섿', '셁', '셂', '셃', '셄', '셅', '셆', '셇', '셊', '셎', '셏', '셐', '셑', '셒', '셓', '셖', '셗', '셙', '셚', '셛', '셝', '셞', '셟', '셠', '셡', '셢', '셣', '셦', '셪', '셫', '셬', '셭', '셮', '셯', '셱', '셲', '셳', '셵', '셶', '셷', '셹', '셺', '셻', '셼', '셽', '셾', '셿', '솀', '솁', '솂', '솃', '솄', '솆', '솇', '솈', '솉', '솊', '솋', '솏', '솑', '솒', '솓', '솕', '솗', '솘', '솙', '솚', '솛', '솞', '솠', '솢', '솣', '솤', '솦', '솧', '솪', '솫', '솭', '솮', '솯', '솱', '솲', '솳', '솴', '솵', '솶', '솷', '솸', '솹', '솺', '솻', '솼', '솾', '솿', '쇀', '쇁', '쇂', '쇃', '쇅', '쇆', '쇇', '쇉', '쇊', '쇋', '쇍', '쇎', '쇏', '쇐', '쇑', '쇒', '쇓', '쇕', '쇖', '쇙', '쇚', '쇛', '쇜', '쇝', '쇞', '쇟', '쇡', '쇢', '쇣', '쇥', '쇦', '쇧', '쇩', '쇪', '쇫', '쇬', '쇭', '쇮', '쇯', '쇲', '쇴', '쇵', '쇶', '쇷', '쇸', '쇹', '쇺', '쇻', '쇾', '쇿', '숁', '숂', '숃', '숅', '숆', '숇', '숈', '숉', '숊', '숋', '숎', '숐', '숒', '숓', '숔', '숕', '숖', '숗', '숚', '숛', '숝', '숞', '숡', '숢', '숣', '숤', '숥', '숦', '숧', '숪', '숬', '숮', '숰', '숳', '숵', '숶', '숷', '숸', '숹', '숺', '숻', '숼', '숽', '숾', '숿', '쉀', '쉁', '쉂', '쉃', '쉄', '쉅', '쉆', '쉇', '쉉', '쉊', '쉋', '쉌', '쉍', '쉎', '쉏', '쉒', '쉓', '쉕', '쉖', '쉗', '쉙', '쉚', '쉛', '쉜', '쉝', '쉞', '쉟', '쉡', '쉢', '쉣', '쉤', '쉦', '쉧', '쉨', '쉩', '쉪', '쉫', '쉮', '쉯', '쉱', '쉲', '쉳', '쉵', '쉶', '쉷', '쉸', '쉹', '쉺', '쉻', '쉾', '슀', '슂', '슃', '슄', '슅', '슆', '슇', '슊', '슋', '슌', '슍', '슎', '슏', '슑', '슒', '슓', '슔', '슕', '슖', '슗', '슙', '슚', '슜', '슞', '슟', '슠', '슡', '슢', '슣', '슦', '슧', '슩', '슪', '슫', '슮', '슯', '슰', '슱', '슲', '슳', '슶', '슸', '슺', '슻', '슼', '슽', '슾', '슿', '싀', '싁', '싂', '싃', '싄', '싅', '싆', '싇', '싈', '싉', '싊', '싋', '싌', '싍', '싎', '싏', '싐', '싑', '싒', '싓', '싔', '싕', '싖', '싗', '싘', '싙', '싚', '싛', '싞', '싟', '싡', '싢', '싥', '싦', '싧', '싨', '싩', '싪', '싮', '싰', '싲', '싳', '싴', '싵', '싷', '싺', '싽', '싾', '싿', '쌁', '쌂', '쌃', '쌄', '쌅', '쌆', '쌇', '쌊', '쌋', '쌎', '쌏', '쌐', '쌑', '쌒', '쌖', '쌗', '쌙', '쌚', '쌛', '쌝', '쌞', '쌟', '쌠', '쌡', '쌢', '쌣', '쌦', '쌧', '쌪', '쌫', '쌬', '쌭', '쌮', '쌯', '쌰', '쌱', '쌲', '쌳', '쌴', '쌵', '쌶', '쌷', '쌸', '쌹', '쌺', '쌻', '쌼', '쌽', '쌾', '쌿', '썀', '썁', '썂', '썃', '썄', '썆', '썇', '썈', '썉', '썊', '썋', '썌', '썍', '썎', '썏', '썐', '썑', '썒', '썓', '썔', '썕', '썖', '썗', '썘', '썙', '썚', '썛', '썜', '썝', '썞', '썟', '썠', '썡', '썢', '썣', '썤', '썥', '썦', '썧', '썪', '썫', '썭', '썮', '썯', '썱', '썳', '썴', '썵', '썶', '썷', '썺', '썻', '썾', '썿', '쎀', '쎁', '쎂', '쎃', '쎅', '쎆', '쎇', '쎉', '쎊', '쎋', '쎍', '쎎', '쎏', '쎐', '쎑', '쎒', '쎓', '쎔', '쎕', '쎖', '쎗', '쎘', '쎙', '쎚', '쎛', '쎜', '쎝', '쎞', '쎟', '쎠', '쎡', '쎢', '쎣', '쎤', '쎥', '쎦', '쎧', '쎨', '쎩', '쎪', '쎫', '쎬', '쎭', '쎮', '쎯', '쎰', '쎱', '쎲', '쎳', '쎴', '쎵', '쎶', '쎷', '쎸', '쎹', '쎺', '쎻', '쎼', '쎽', '쎾', '쎿', '쏁', '쏂', '쏃', '쏄', '쏅', '쏆', '쏇', '쏈', '쏉', '쏊', '쏋', '쏌', '쏍', '쏎', '쏏', '쏐', '쏑', '쏒', '쏓', '쏔', '쏕', '쏖', '쏗', '쏚', '쏛', '쏝', '쏞', '쏡', '쏣', '쏤', '쏥', '쏦', '쏧', '쏪', '쏫', '쏬', '쏮', '쏯', '쏰', '쏱', '쏲', '쏳', '쏶', '쏷', '쏹', '쏺', '쏻', '쏼', '쏽', '쏾', '쏿', '쐀', '쐁', '쐂', '쐃', '쐄', '쐅', '쐆', '쐇', '쐉', '쐊', '쐋', '쐌', '쐍', '쐎', '쐏', '쐑', '쐒', '쐓', '쐔', '쐕', '쐖', '쐗', '쐘', '쐙', '쐚', '쐛', '쐜', '쐝', '쐞', '쐟', '쐠', '쐡', '쐢', '쐣', '쐥', '쐦', '쐧', '쐨', '쐩', '쐪', '쐫', '쐭', '쐮', '쐯', '쐱', '쐲', '쐳', '쐵', '쐶', '쐷', '쐸', '쐹', '쐺', '쐻', '쐾', '쐿', '쑀', '쑁', '쑂', '쑃', '쑄', '쑅', '쑆', '쑇', '쑉', '쑊', '쑋', '쑌', '쑍', '쑎', '쑏', '쑐', '쑑', '쑒', '쑓', '쑔', '쑕', '쑖', '쑗', '쑘', '쑙', '쑚', '쑛', '쑜', '쑝', '쑞', '쑟', '쑠', '쑡', '쑢', '쑣', '쑦', '쑧', '쑩', '쑪', '쑫', '쑭', '쑮', '쑯', '쑰', '쑱', '쑲', '쑳', '쑶', '쑷', '쑸', '쑺', '쑻', '쑼', '쑽', '쑾', '쑿', '쒁', '쒂', '쒃', '쒄', '쒅', '쒆', '쒇', '쒈', '쒉', '쒊', '쒋', '쒌', '쒍', '쒎', '쒏', '쒐', '쒑', '쒒', '쒓', '쒕', '쒖', '쒗', '쒘', '쒙', '쒚', '쒛', '쒝', '쒞', '쒟', '쒠', '쒡', '쒢', '쒣', '쒤', '쒥', '쒦', '쒧', '쒨', '쒩', '쒪', '쒫', '쒬', '쒭', '쒮', '쒯', '쒰', '쒱', '쒲', '쒳', '쒴', '쒵', '쒶', '쒷', '쒹', '쒺', '쒻', '쒽', '쒾', '쒿', '쓀', '쓁', '쓂', '쓃', '쓄', '쓅', '쓆', '쓇', '쓈', '쓉', '쓊', '쓋', '쓌', '쓍', '쓎', '쓏', '쓐', '쓑', '쓒', '쓓', '쓔', '쓕', '쓖', '쓗', '쓘', '쓙', '쓚', '쓛', '쓜', '쓝', '쓞', '쓟', '쓠', '쓡', '쓢', '쓣', '쓤', '쓥', '쓦', '쓧', '쓨', '쓪', '쓫', '쓬', '쓭', '쓮', '쓯', '쓲', '쓳', '쓵', '쓶', '쓷', '쓹', '쓻', '쓼', '쓽', '쓾', '씂', '씃', '씄', '씅', '씆', '씇', '씈', '씉', '씊', '씋', '씍', '씎', '씏', '씑', '씒', '씓', '씕', '씖', '씗', '씘', '씙', '씚', '씛', '씝', '씞', '씟', '씠', '씡', '씢', '씣', '씤', '씥', '씦', '씧', '씪', '씫', '씭', '씮', '씯', '씱', '씲', '씳', '씴', '씵', '씶', '씷', '씺', '씼', '씾', '씿', '앀', '앁', '앂', '앃', '앆', '앇', '앋', '앏', '앐', '앑', '앒', '앖', '앚', '앛', '앜', '앟', '앢', '앣', '앥', '앦', '앧', '앩', '앪', '앫', '앬', '앭', '앮', '앯', '앲', '앶', '앷', '앸', '앹', '앺', '앻', '앾', '앿', '얁', '얂', '얃', '얅', '얆', '얈', '얉', '얊', '얋', '얎', '얐', '얒', '얓', '얔', '얖', '얙', '얚', '얛', '얝', '얞', '얟', '얡', '얢', '얣', '얤', '얥', '얦', '얧', '얨', '얪', '얫', '얬', '얭', '얮', '얯', '얰', '얱', '얲', '얳', '얶', '얷', '얺', '얿', '엀', '엁', '엂', '엃', '엋', '엍', '엏', '엒', '엓', '엕', '엖', '엗', '엙', '엚', '엛', '엜', '엝', '엞', '엟', '엢', '엤', '엦', '엧', '엨', '엩', '엪', '엫', '엯', '엱', '엲', '엳', '엵', '엸', '엹', '엺', '엻', '옂', '옃', '옄', '옉', '옊', '옋', '옍', '옎', '옏', '옑', '옒', '옓', '옔', '옕', '옖', '옗', '옚', '옝', '옞', '옟', '옠', '옡', '옢', '옣', '옦', '옧', '옩', '옪', '옫', '옯', '옱', '옲', '옶', '옸', '옺', '옼', '옽', '옾', '옿', '왂', '왃', '왅', '왆', '왇', '왉', '왊', '왋', '왌', '왍', '왎', '왏', '왒', '왖', '왗', '왘', '왙', '왚', '왛', '왞', '왟', '왡', '왢', '왣', '왤', '왥', '왦', '왧', '왨', '왩', '왪', '왫', '왭', '왮', '왰', '왲', '왳', '왴', '왵', '왶', '왷', '왺', '왻', '왽', '왾', '왿', '욁', '욂', '욃', '욄', '욅', '욆', '욇', '욊', '욌', '욎', '욏', '욐', '욑', '욒', '욓', '욖', '욗', '욙', '욚', '욛', '욝', '욞', '욟', '욠', '욡', '욢', '욣', '욦', '욨', '욪', '욫', '욬', '욭', '욮', '욯', '욲', '욳', '욵', '욶', '욷', '욻', '욼', '욽', '욾', '욿', '웂', '웄', '웆', '웇', '웈', '웉', '웊', '웋', '웎', '웏', '웑', '웒', '웓', '웕', '웖', '웗', '웘', '웙', '웚', '웛', '웞', '웟', '웢', '웣', '웤', '웥', '웦', '웧', '웪', '웫', '웭', '웮', '웯', '웱', '웲', '웳', '웴', '웵', '웶', '웷', '웺', '웻', '웼', '웾', '웿', '윀', '윁', '윂', '윃', '윆', '윇', '윉', '윊', '윋', '윍', '윎', '윏', '윐', '윑', '윒', '윓', '윖', '윘', '윚', '윛', '윜', '윝', '윞', '윟', '윢', '윣', '윥', '윦', '윧', '윩', '윪', '윫', '윬', '윭', '윮', '윯', '윲', '윴', '윶', '윸', '윹', '윺', '윻', '윾', '윿', '읁', '읂', '읃', '읅', '읆', '읇', '읈', '읉', '읋', '읎', '읐', '읙', '읚', '읛', '읝', '읞', '읟', '읡', '읢', '읣', '읤', '읥', '읦', '읧', '읩', '읪', '읬', '읭', '읮', '읯', '읰', '읱', '읲', '읳', '읶', '읷', '읹', '읺', '읻', '읿', '잀', '잁', '잂', '잆', '잋', '잌', '잍', '잏', '잒', '잓', '잕', '잙', '잛', '잜', '잝', '잞', '잟', '잢', '잧', '잨', '잩', '잪', '잫', '잮', '잯', '잱', '잲', '잳', '잵', '잶', '잷', '잸', '잹', '잺', '잻', '잾', '쟂', '쟃', '쟄', '쟅', '쟆', '쟇', '쟊', '쟋', '쟍', '쟏', '쟑', '쟒', '쟓', '쟔', '쟕', '쟖', '쟗', '쟙', '쟚', '쟛', '쟜', '쟞', '쟟', '쟠', '쟡', '쟢', '쟣', '쟥', '쟦', '쟧', '쟩', '쟪', '쟫', '쟭', '쟮', '쟯', '쟰', '쟱', '쟲', '쟳', '쟴', '쟵', '쟶', '쟷', '쟸', '쟹', '쟺', '쟻', '쟼', '쟽', '쟾', '쟿', '젂', '젃', '젅', '젆', '젇', '젉', '젋', '젌', '젍', '젎', '젏', '젒', '젔', '젗', '젘', '젙', '젚', '젛', '젞', '젟', '젡', '젢', '젣', '젥', '젦', '젧', '젨', '젩', '젪', '젫', '젮', '젰', '젲', '젳', '젴', '젵', '젶', '젷', '젹', '젺', '젻', '젽', '젾', '젿', '졁', '졂', '졃', '졄', '졅', '졆', '졇', '졊', '졋', '졎', '졏', '졐', '졑', '졒', '졓', '졕', '졖', '졗', '졘', '졙', '졚', '졛', '졜', '졝', '졞', '졟', '졠', '졡', '졢', '졣', '졤', '졥', '졦', '졧', '졨', '졩', '졪', '졫', '졬', '졭', '졮', '졯', '졲', '졳', '졵', '졶', '졷', '졹', '졻', '졼', '졽', '졾', '졿', '좂', '좄', '좈', '좉', '좊', '좎', '좏', '좐', '좑', '좒', '좓', '좕', '좖', '좗', '좘', '좙', '좚', '좛', '좜', '좞', '좠', '좢', '좣', '좤', '좥', '좦', '좧', '좩', '좪', '좫', '좬', '좭', '좮', '좯', '좰', '좱', '좲', '좳', '좴', '좵', '좶', '좷', '좸', '좹', '좺', '좻', '좾', '좿', '죀', '죁', '죂', '죃', '죅', '죆', '죇', '죉', '죊', '죋', '죍', '죎', '죏', '죐', '죑', '죒', '죓', '죖', '죘', '죚', '죛', '죜', '죝', '죞', '죟', '죢', '죣', '죥', '죦', '죧', '죨', '죩', '죪', '죫', '죬', '죭', '죮', '죯', '죰', '죱', '죲', '죳', '죴', '죶', '죷', '죸', '죹', '죺', '죻', '죾', '죿', '줁', '줂', '줃', '줇', '줈', '줉', '줊', '줋', '줎', '줐', '줒', '줓', '줔', '줕', '줖', '줗', '줙', '줚', '줛', '줜', '줝', '줞', '줟', '줠', '줡', '줢', '줣', '줤', '줥', '줦', '줧', '줨', '줩', '줪', '줫', '줭', '줮', '줯', '줰', '줱', '줲', '줳', '줵', '줶', '줷', '줸', '줹', '줺', '줻', '줼', '줽', '줾', '줿', '쥀', '쥁', '쥂', '쥃', '쥄', '쥅', '쥆', '쥇', '쥈', '쥉', '쥊', '쥋', '쥌', '쥍', '쥎', '쥏', '쥒', '쥓', '쥕', '쥖', '쥗', '쥙', '쥚', '쥛', '쥜', '쥝', '쥞', '쥟', '쥢', '쥤', '쥥', '쥦', '쥧', '쥨', '쥩', '쥪', '쥫', '쥭', '쥮', '쥯', '쥱', '쥲', '쥳', '쥵', '쥶', '쥷', '쥸', '쥹', '쥺', '쥻', '쥽', '쥾', '쥿', '즀', '즁', '즂', '즃', '즄', '즅', '즆', '즇', '즊', '즋', '즍', '즎', '즏', '즑', '즒', '즓', '즔', '즕', '즖', '즗', '즚', '즜', '즞', '즟', '즠', '즡', '즢', '즣', '즤', '즥', '즦', '즧', '즨', '즩', '즪', '즫', '즬', '즭', '즮', '즯', '즰', '즱', '즲', '즳', '즴', '즵', '즶', '즷', '즸', '즹', '즺', '즻', '즼', '즽', '즾', '즿', '짂', '짃', '짅', '짆', '짉', '짋', '짌', '짍', '짎', '짏', '짒', '짔', '짗', '짘', '짛', '짞', '짟', '짡', '짣', '짥', '짦', '짨', '짩', '짪', '짫', '짮', '짲', '짳', '짴', '짵', '짶', '짷', '짺', '짻', '짽', '짾', '짿', '쨁', '쨂', '쨃', '쨄', '쨅', '쨆', '쨇', '쨊', '쨎', '쨏', '쨐', '쨑', '쨒', '쨓', '쨕', '쨖', '쨗', '쨙', '쨚', '쨛', '쨜', '쨝', '쨞', '쨟', '쨠', '쨡', '쨢', '쨣', '쨤', '쨥', '쨦', '쨧', '쨨', '쨪', '쨫', '쨬', '쨭', '쨮', '쨯', '쨰', '쨱', '쨲', '쨳', '쨴', '쨵', '쨶', '쨷', '쨸', '쨹', '쨺', '쨻', '쨼', '쨽', '쨾', '쨿', '쩀', '쩁', '쩂', '쩃', '쩄', '쩅', '쩆', '쩇', '쩈', '쩉', '쩊', '쩋', '쩎', '쩏', '쩑', '쩒', '쩓', '쩕', '쩖', '쩗', '쩘', '쩙', '쩚', '쩛', '쩞', '쩢', '쩣', '쩤', '쩥', '쩦', '쩧', '쩩', '쩪', '쩫', '쩬', '쩭', '쩮', '쩯', '쩰', '쩱', '쩲', '쩳', '쩴', '쩵', '쩶', '쩷', '쩸', '쩹', '쩺', '쩻', '쩼', '쩾', '쩿', '쪀', '쪁', '쪂', '쪃', '쪅', '쪆', '쪇', '쪈', '쪉', '쪊', '쪋', '쪌', '쪍', '쪎', '쪏', '쪐', '쪑', '쪒', '쪓', '쪔', '쪕', '쪖', '쪗', '쪙', '쪚', '쪛', '쪜', '쪝', '쪞', '쪟', '쪠', '쪡', '쪢', '쪣', '쪤', '쪥', '쪦', '쪧', '쪨', '쪩', '쪪', '쪫', '쪬', '쪭', '쪮', '쪯', '쪰', '쪱', '쪲', '쪳', '쪴', '쪵', '쪶', '쪷', '쪸', '쪹', '쪺', '쪻', '쪾', '쪿', '쫁', '쫂', '쫃', '쫅', '쫆', '쫇', '쫈', '쫉', '쫊', '쫋', '쫎', '쫐', '쫒', '쫔', '쫕', '쫖', '쫗', '쫚', '쫛', '쫜', '쫝', '쫞', '쫟', '쫡', '쫢', '쫣', '쫤', '쫥', '쫦', '쫧', '쫨', '쫩', '쫪', '쫫', '쫭', '쫮', '쫯', '쫰', '쫱', '쫲', '쫳', '쫵', '쫶', '쫷', '쫸', '쫹', '쫺', '쫻', '쫼', '쫽', '쫾', '쫿', '쬀', '쬁', '쬂', '쬃', '쬄', '쬅', '쬆', '쬇', '쬉', '쬊', '쬋', '쬌', '쬍', '쬎', '쬏', '쬑', '쬒', '쬓', '쬕', '쬖', '쬗', '쬙', '쬚', '쬛', '쬜', '쬝', '쬞', '쬟', '쬢', '쬣', '쬤', '쬥', '쬦', '쬧', '쬨', '쬩', '쬪', '쬫', '쬬', '쬭', '쬮', '쬯', '쬰', '쬱', '쬲', '쬳', '쬴', '쬵', '쬶', '쬷', '쬸', '쬹', '쬺', '쬻', '쬼', '쬽', '쬾', '쬿', '쭀', '쭂', '쭃', '쭄', '쭅', '쭆', '쭇', '쭊', '쭋', '쭍', '쭎', '쭏', '쭑', '쭒', '쭓', '쭔', '쭕', '쭖', '쭗', '쭚', '쭛', '쭜', '쭞', '쭟', '쭠', '쭡', '쭢', '쭣', '쭥', '쭦', '쭧', '쭨', '쭩', '쭪', '쭫', '쭬', '쭭', '쭮', '쭯', '쭰', '쭱', '쭲', '쭳', '쭴', '쭵', '쭶', '쭷', '쭺', '쭻', '쭼', '쭽', '쭾', '쭿', '쮀', '쮁', '쮂', '쮃', '쮄', '쮅', '쮆', '쮇', '쮈', '쮉', '쮊', '쮋', '쮌', '쮍', '쮎', '쮏', '쮐', '쮑', '쮒', '쮓', '쮔', '쮕', '쮖', '쮗', '쮘', '쮙', '쮚', '쮛', '쮝', '쮞', '쮟', '쮠', '쮡', '쮢', '쮣', '쮤', '쮥', '쮦', '쮧', '쮨', '쮩', '쮪', '쮫', '쮬', '쮭', '쮮', '쮯', '쮰', '쮱', '쮲', '쮳', '쮴', '쮵', '쮶', '쮷', '쮹', '쮺', '쮻', '쮼', '쮽', '쮾', '쮿', '쯀', '쯁', '쯂', '쯃', '쯄', '쯅', '쯆', '쯇', '쯈', '쯉', '쯊', '쯋', '쯌', '쯍', '쯎', '쯏', '쯐', '쯑', '쯒', '쯓', '쯕', '쯖', '쯗', '쯘', '쯙', '쯚', '쯛', '쯜', '쯝', '쯞', '쯟', '쯠', '쯡', '쯢', '쯣', '쯥', '쯦', '쯨', '쯪', '쯫', '쯬', '쯭', '쯮', '쯯', '쯰', '쯱', '쯲', '쯳', '쯴', '쯵', '쯶', '쯷', '쯸', '쯹', '쯺', '쯻', '쯼', '쯽', '쯾', '쯿', '찀', '찁', '찂', '찃', '찄', '찅', '찆', '찇', '찈', '찉', '찊', '찋', '찎', '찏', '찑', '찒', '찓', '찕', '찖', '찗', '찘', '찙', '찚', '찛', '찞', '찟', '찠', '찣', '찤', '찥', '찦', '찪', '찫', '찭', '찯', '찱', '찲', '찳', '찴', '찵', '찶', '찷', '찺', '찿', '챀', '챁', '챂', '챃', '챆', '챇', '챉', '챊', '챋', '챍', '챎', '챏', '챐', '챑', '챒', '챓', '챖', '챚', '챛', '챜', '챝', '챞', '챟', '챡', '챢', '챣', '챥', '챧', '챩', '챪', '챫', '챬', '챭', '챮', '챯', '챱', '챲', '챳', '챴', '챶', '챷', '챸', '챹', '챺', '챻', '챼', '챽', '챾', '챿', '첀', '첁', '첂', '첃', '첄', '첅', '첆', '첇', '첈', '첉', '첊', '첋', '첌', '첍', '첎', '첏', '첐', '첑', '첒', '첓', '첔', '첕', '첖', '첗', '첚', '첛', '첝', '첞', '첟', '첡', '첢', '첣', '첤', '첥', '첦', '첧', '첪', '첮', '첯', '첰', '첱', '첲', '첳', '첶', '첷', '첹', '첺', '첻', '첽', '첾', '첿', '쳀', '쳁', '쳂', '쳃', '쳆', '쳈', '쳊', '쳋', '쳌', '쳍', '쳎', '쳏', '쳑', '쳒', '쳓', '쳕', '쳖', '쳗', '쳘', '쳙', '쳚', '쳛', '쳜', '쳝', '쳞', '쳟', '쳠', '쳡', '쳢', '쳣', '쳥', '쳦', '쳧', '쳨', '쳩', '쳪', '쳫', '쳭', '쳮', '쳯', '쳱', '쳲', '쳳', '쳴', '쳵', '쳶', '쳷', '쳸', '쳹', '쳺', '쳻', '쳼', '쳽', '쳾', '쳿', '촀', '촂', '촃', '촄', '촅', '촆', '촇', '촊', '촋', '촍', '촎', '촏', '촑', '촒', '촓', '촔', '촕', '촖', '촗', '촚', '촜', '촞', '촟', '촠', '촡', '촢', '촣', '촥', '촦', '촧', '촩', '촪', '촫', '촭', '촮', '촯', '촰', '촱', '촲', '촳', '촴', '촵', '촶', '촷', '촸', '촺', '촻', '촼', '촽', '촾', '촿', '쵀', '쵁', '쵂', '쵃', '쵄', '쵅', '쵆', '쵇', '쵈', '쵉', '쵊', '쵋', '쵌', '쵍', '쵎', '쵏', '쵐', '쵑', '쵒', '쵓', '쵔', '쵕', '쵖', '쵗', '쵘', '쵙', '쵚', '쵛', '쵝', '쵞', '쵟', '쵡', '쵢', '쵣', '쵥', '쵦', '쵧', '쵨', '쵩', '쵪', '쵫', '쵮', '쵰', '쵲', '쵳', '쵴', '쵵', '쵶', '쵷', '쵹', '쵺', '쵻', '쵼', '쵽', '쵾', '쵿', '춀', '춁', '춂', '춃', '춄', '춅', '춆', '춇', '춉', '춊', '춋', '춌', '춍', '춎', '춏', '춐', '춑', '춒', '춓', '춖', '춗', '춙', '춚', '춛', '춝', '춞', '춟', '춠', '춡', '춢', '춣', '춦', '춨', '춪', '춫', '춬', '춭', '춮', '춯', '춱', '춲', '춳', '춴', '춵', '춶', '춷', '춸', '춹', '춺', '춻', '춼', '춽', '춾', '춿', '췀', '췁', '췂', '췃', '췅', '췆', '췇', '췈', '췉', '췊', '췋', '췍', '췎', '췏', '췑', '췒', '췓', '췔', '췕', '췖', '췗', '췘', '췙', '췚', '췛', '췜', '췝', '췞', '췟', '췠', '췡', '췢', '췣', '췤', '췥', '췦', '췧', '췩', '췪', '췫', '췭', '췮', '췯', '췱', '췲', '췳', '췴', '췵', '췶', '췷', '췺', '췼', '췾', '췿', '츀', '츁', '츂', '츃', '츅', '츆', '츇', '츉', '츊', '츋', '츍', '츎', '츏', '츐', '츑', '츒', '츓', '츕', '츖', '츗', '츘', '츚', '츛', '츜', '츝', '츞', '츟', '츢', '츣', '츥', '츦', '츧', '츩', '츪', '츫', '츬', '츭', '츮', '츯', '츲', '츴', '츶', '츷', '츸', '츹', '츺', '츻', '츼', '츽', '츾', '츿', '칀', '칁', '칂', '칃', '칄', '칅', '칆', '칇', '칈', '칉', '칊', '칋', '칌', '칍', '칎', '칏', '칐', '칑', '칒', '칓', '칔', '칕', '칖', '칗', '칚', '칛', '칝', '칞', '칢', '칣', '칤', '칥', '칦', '칧', '칪', '칬', '칮', '칯', '칰', '칱', '칲', '칳', '칶', '칷', '칹', '칺', '칻', '칽', '칾', '칿', '캀', '캁', '캂', '캃', '캆', '캈', '캊', '캋', '캌', '캍', '캎', '캏', '캒', '캓', '캕', '캖', '캗', '캙', '캚', '캛', '캜', '캝', '캞', '캟', '캢', '캦', '캧', '캨', '캩', '캪', '캫', '캮', '캯', '캰', '캱', '캲', '캳', '캴', '캵', '캶', '캷', '캸', '캹', '캺', '캻', '캼', '캽', '캾', '캿', '컀', '컂', '컃', '컄', '컅', '컆', '컇', '컈', '컉', '컊', '컋', '컌', '컍', '컎', '컏', '컐', '컑', '컒', '컓', '컔', '컕', '컖', '컗', '컘', '컙', '컚', '컛', '컜', '컝', '컞', '컟', '컠', '컡', '컢', '컣', '컦', '컧', '컩', '컪', '컭', '컮', '컯', '컰', '컱', '컲', '컳', '컶', '컺', '컻', '컼', '컽', '컾', '컿', '켂', '켃', '켅', '켆', '켇', '켉', '켊', '켋', '켌', '켍', '켎', '켏', '켒', '켔', '켖', '켗', '켘', '켙', '켚', '켛', '켝', '켞', '켟', '켡', '켢', '켣', '켥', '켦', '켧', '켨', '켩', '켪', '켫', '켮', '켲', '켳', '켴', '켵', '켶', '켷', '켹', '켺', '켻', '켼', '켽', '켾', '켿', '콀', '콁', '콂', '콃', '콄', '콅', '콆', '콇', '콈', '콉', '콊', '콋', '콌', '콍', '콎', '콏', '콐', '콑', '콒', '콓', '콖', '콗', '콙', '콚', '콛', '콝', '콞', '콟', '콠', '콡', '콢', '콣', '콦', '콨', '콪', '콫', '콬', '콭', '콮', '콯', '콲', '콳', '콵', '콶', '콷', '콹', '콺', '콻', '콼', '콽', '콾', '콿', '쾁', '쾂', '쾃', '쾄', '쾆', '쾇', '쾈', '쾉', '쾊', '쾋', '쾍', '쾎', '쾏', '쾐', '쾑', '쾒', '쾓', '쾔', '쾕', '쾖', '쾗', '쾘', '쾙', '쾚', '쾛', '쾜', '쾝', '쾞', '쾟', '쾠', '쾢', '쾣', '쾤', '쾥', '쾦', '쾧', '쾩', '쾪', '쾫', '쾬', '쾭', '쾮', '쾯', '쾱', '쾲', '쾳', '쾴', '쾵', '쾶', '쾷', '쾸', '쾹', '쾺', '쾻', '쾼', '쾽', '쾾', '쾿', '쿀', '쿁', '쿂', '쿃', '쿅', '쿆', '쿇', '쿈', '쿉', '쿊', '쿋', '쿌', '쿍', '쿎', '쿏', '쿐', '쿑', '쿒', '쿓', '쿔', '쿕', '쿖', '쿗', '쿘', '쿙', '쿚', '쿛', '쿜', '쿝', '쿞', '쿟', '쿢', '쿣', '쿥', '쿦', '쿧', '쿩', '쿪', '쿫', '쿬', '쿭', '쿮', '쿯', '쿲', '쿴', '쿶', '쿷', '쿸', '쿹', '쿺', '쿻', '쿽', '쿾', '쿿', '퀁', '퀂', '퀃', '퀅', '퀆', '퀇', '퀈', '퀉', '퀊', '퀋', '퀌', '퀍', '퀎', '퀏', '퀐', '퀒', '퀓', '퀔', '퀕', '퀖', '퀗', '퀙', '퀚', '퀛', '퀜', '퀝', '퀞', '퀟', '퀠', '퀡', '퀢', '퀣', '퀤', '퀥', '퀦', '퀧', '퀨', '퀩', '퀪', '퀫', '퀬', '퀮', '퀯', '퀰', '퀱', '퀲', '퀳', '퀶', '퀷', '퀹', '퀺', '퀻', '퀽', '퀾', '퀿', '큀', '큁', '큂', '큃', '큆', '큈', '큊', '큋', '큌', '큍', '큎', '큏', '큑', '큒', '큓', '큕', '큖', '큗', '큙', '큚', '큛', '큜', '큝', '큞', '큟', '큡', '큢', '큣', '큤', '큥', '큦', '큧', '큨', '큩', '큪', '큫', '큮', '큯', '큱', '큲', '큳', '큵', '큶', '큷', '큸', '큹', '큺', '큻', '큾', '큿', '킀', '킂', '킃', '킄', '킅', '킆', '킇', '킈', '킉', '킊', '킋', '킌', '킍', '킎', '킏', '킐', '킑', '킒', '킓', '킔', '킕', '킖', '킗', '킘', '킙', '킚', '킛', '킜', '킝', '킞', '킟', '킠', '킡', '킢', '킣', '킦', '킧', '킩', '킪', '킫', '킭', '킮', '킯', '킰', '킱', '킲', '킳', '킶', '킸', '킺', '킻', '킼', '킽', '킾', '킿', '탂', '탃', '탅', '탆', '탇', '탊', '탋', '탌', '탍', '탎', '탏', '탒', '탖', '탗', '탘', '탙', '탚', '탛', '탞', '탟', '탡', '탢', '탣', '탥', '탦', '탧', '탨', '탩', '탪', '탫', '탮', '탲', '탳', '탴', '탵', '탶', '탷', '탹', '탺', '탻', '탼', '탽', '탾', '탿', '턀', '턁', '턂', '턃', '턄', '턅', '턆', '턇', '턈', '턉', '턊', '턋', '턌', '턎', '턏', '턐', '턑', '턒', '턓', '턔', '턕', '턖', '턗', '턘', '턙', '턚', '턛', '턜', '턝', '턞', '턟', '턠', '턡', '턢', '턣', '턤', '턥', '턦', '턧', '턨', '턩', '턪', '턫', '턬', '턭', '턮', '턯', '턲', '턳', '턵', '턶', '턷', '턹', '턻', '턼', '턽', '턾', '턿', '텂', '텆', '텇', '텈', '텉', '텊', '텋', '텎', '텏', '텑', '텒', '텓', '텕', '텖', '텗', '텘', '텙', '텚', '텛', '텞', '텠', '텢', '텣', '텤', '텥', '텦', '텧', '텩', '텪', '텫', '텭', '텮', '텯', '텰', '텱', '텲', '텳', '텴', '텵', '텶', '텷', '텸', '텹', '텺', '텻', '텽', '텾', '텿', '톀', '톁', '톂', '톃', '톅', '톆', '톇', '톉', '톊', '톋', '톌', '톍', '톎', '톏', '톐', '톑', '톒', '톓', '톔', '톕', '톖', '톗', '톘', '톙', '톚', '톛', '톜', '톝', '톞', '톟', '톢', '톣', '톥', '톦', '톧', '톩', '톪', '톫', '톬', '톭', '톮', '톯', '톲', '톴', '톶', '톷', '톸', '톹', '톻', '톽', '톾', '톿', '퇁', '퇂', '퇃', '퇄', '퇅', '퇆', '퇇', '퇈', '퇉', '퇊', '퇋', '퇌', '퇍', '퇎', '퇏', '퇐', '퇑', '퇒', '퇓', '퇔', '퇕', '퇖', '퇗', '퇙', '퇚', '퇛', '퇜', '퇝', '퇞', '퇟', '퇠', '퇡', '퇢', '퇣', '퇤', '퇥', '퇦', '퇧', '퇨', '퇩', '퇪', '퇫', '퇬', '퇭', '퇮', '퇯', '퇰', '퇱', '퇲', '퇳', '퇵', '퇶', '퇷', '퇹', '퇺', '퇻', '퇼', '퇽', '퇾', '퇿', '툀', '툁', '툂', '툃', '툄', '툅', '툆', '툈', '툊', '툋', '툌', '툍', '툎', '툏', '툑', '툒', '툓', '툔', '툕', '툖', '툗', '툘', '툙', '툚', '툛', '툜', '툝', '툞', '툟', '툠', '툡', '툢', '툣', '툤', '툥', '툦', '툧', '툨', '툩', '툪', '툫', '툮', '툯', '툱', '툲', '툳', '툵', '툶', '툷', '툸', '툹', '툺', '툻', '툾', '퉀', '퉂', '퉃', '퉄', '퉅', '퉆', '퉇', '퉉', '퉊', '퉋', '퉌', '퉍', '퉎', '퉏', '퉐', '퉑', '퉒', '퉓', '퉔', '퉕', '퉖', '퉗', '퉘', '퉙', '퉚', '퉛', '퉝', '퉞', '퉟', '퉠', '퉡', '퉢', '퉣', '퉥', '퉦', '퉧', '퉨', '퉩', '퉪', '퉫', '퉬', '퉭', '퉮', '퉯', '퉰', '퉱', '퉲', '퉳', '퉴', '퉵', '퉶', '퉷', '퉸', '퉹', '퉺', '퉻', '퉼', '퉽', '퉾', '퉿', '튂', '튃', '튅', '튆', '튇', '튉', '튊', '튋', '튌', '튍', '튎', '튏', '튒', '튓', '튔', '튖', '튗', '튘', '튙', '튚', '튛', '튝', '튞', '튟', '튡', '튢', '튣', '튥', '튦', '튧', '튨', '튩', '튪', '튫', '튭', '튮', '튯', '튰', '튲', '튳', '튴', '튵', '튶', '튷', '튺', '튻', '튽', '튾', '틁', '틃', '틄', '틅', '틆', '틇', '틊', '틌', '틍', '틎', '틏', '틐', '틑', '틒', '틓', '틕', '틖', '틗', '틙', '틚', '틛', '틝', '틞', '틟', '틠', '틡', '틢', '틣', '틦', '틧', '틨', '틩', '틪', '틫', '틬', '틭', '틮', '틯', '틲', '틳', '틵', '틶', '틷', '틹', '틺', '틻', '틼', '틽', '틾', '틿', '팂', '팄', '팆', '팇', '팈', '팉', '팊', '팋', '팏', '팑', '팒', '팓', '팕', '팗', '팘', '팙', '팚', '팛', '팞', '팢', '팣', '팤', '팦', '팧', '팪', '팫', '팭', '팮', '팯', '팱', '팲', '팳', '팴', '팵', '팶', '팷', '팺', '팾', '팿', '퍀', '퍁', '퍂', '퍃', '퍆', '퍇', '퍈', '퍉', '퍊', '퍋', '퍌', '퍍', '퍎', '퍏', '퍐', '퍑', '퍒', '퍓', '퍔', '퍕', '퍖', '퍗', '퍘', '퍙', '퍚', '퍛', '퍜', '퍝', '퍞', '퍟', '퍠', '퍡', '퍢', '퍣', '퍤', '퍥', '퍦', '퍧', '퍨', '퍩', '퍪', '퍫', '퍬', '퍭', '퍮', '퍯', '퍰', '퍱', '퍲', '퍳', '퍴', '퍵', '퍶', '퍷', '퍸', '퍹', '퍺', '퍻', '퍾', '퍿', '펁', '펂', '펃', '펅', '펆', '펇', '펈', '펉', '펊', '펋', '펎', '펒', '펓', '펔', '펕', '펖', '펗', '펚', '펛', '펝', '펞', '펟', '펡', '펢', '펣', '펤', '펥', '펦', '펧', '펪', '펬', '펮', '펯', '펰', '펱', '펲', '펳', '펵', '펶', '펷', '펹', '펺', '펻', '펽', '펾', '펿', '폀', '폁', '폂', '폃', '폆', '폇', '폊', '폋', '폌', '폍', '폎', '폏', '폑', '폒', '폓', '폔', '폕', '폖', '폗', '폙', '폚', '폛', '폜', '폝', '폞', '폟', '폠', '폢', '폤', '폥', '폦', '폧', '폨', '폩', '폪', '폫', '폮', '폯', '폱', '폲', '폳', '폵', '폶', '폷', '폸', '폹', '폺', '폻', '폾', '퐀', '퐂', '퐃', '퐄', '퐅', '퐆', '퐇', '퐉', '퐊', '퐋', '퐌', '퐍', '퐎', '퐏', '퐐', '퐑', '퐒', '퐓', '퐔', '퐕', '퐖', '퐗', '퐘', '퐙', '퐚', '퐛', '퐜', '퐞', '퐟', '퐠', '퐡', '퐢', '퐣', '퐤', '퐥', '퐦', '퐧', '퐨', '퐩', '퐪', '퐫', '퐬', '퐭', '퐮', '퐯', '퐰', '퐱', '퐲', '퐳', '퐴', '퐵', '퐶', '퐷', '퐸', '퐹', '퐺', '퐻', '퐼', '퐽', '퐾', '퐿', '푁', '푂', '푃', '푅', '푆', '푇', '푈', '푉', '푊', '푋', '푌', '푍', '푎', '푏', '푐', '푑', '푒', '푓', '푔', '푕', '푖', '푗', '푘', '푙', '푚', '푛', '푝', '푞', '푟', '푡', '푢', '푣', '푥', '푦', '푧', '푨', '푩', '푪', '푫', '푬', '푮', '푰', '푱', '푲', '푳', '푴', '푵', '푶', '푷', '푺', '푻', '푽', '푾', '풁', '풃', '풄', '풅', '풆', '풇', '풊', '풌', '풎', '풏', '풐', '풑', '풒', '풓', '풕', '풖', '풗', '풘', '풙', '풚', '풛', '풜', '풝', '풞', '풟', '풠', '풡', '풢', '풣', '풤', '풥', '풦', '풧', '풨', '풪', '풫', '풬', '풭', '풮', '풯', '풰', '풱', '풲', '풳', '풴', '풵', '풶', '풷', '풸', '풹', '풺', '풻', '풼', '풽', '풾', '풿', '퓀', '퓁', '퓂', '퓃', '퓄', '퓅', '퓆', '퓇', '퓈', '퓉', '퓊', '퓋', '퓍', '퓎', '퓏', '퓑', '퓒', '퓓', '퓕', '퓖', '퓗', '퓘', '퓙', '퓚', '퓛', '퓝', '퓞', '퓠', '퓡', '퓢', '퓣', '퓤', '퓥', '퓦', '퓧', '퓩', '퓪', '퓫', '퓭', '퓮', '퓯', '퓱', '퓲', '퓳', '퓴', '퓵', '퓶', '퓷', '퓹', '퓺', '퓼', '퓾', '퓿', '픀', '픁', '픂', '픃', '픅', '픆', '픇', '픉', '픊', '픋', '픍', '픎', '픏', '픐', '픑', '픒', '픓', '픖', '픘', '픙', '픚', '픛', '픜', '픝', '픞', '픟', '픠', '픡', '픢', '픣', '픤', '픥', '픦', '픧', '픨', '픩', '픪', '픫', '픬', '픭', '픮', '픯', '픰', '픱', '픲', '픳', '픴', '픵', '픶', '픷', '픸', '픹', '픺', '픻', '픾', '픿', '핁', '핂', '핃', '핅', '핆', '핇', '핈', '핉', '핊', '핋', '핎', '핐', '핒', '핓', '핔', '핕', '핖', '핗', '핚', '핛', '핝', '핞', '핟', '핡', '핢', '핣', '핤', '핦', '핧', '핪', '핬', '핮', '핯', '핰', '핱', '핲', '핳', '핶', '핷', '핹', '핺', '핻', '핽', '핾', '핿', '햀', '햁', '햂', '햃', '햆', '햊', '햋', '햌', '햍', '햎', '햏', '햑', '햒', '햓', '햔', '햕', '햖', '햗', '햘', '햙', '햚', '햛', '햜', '햝', '햞', '햟', '햠', '햡', '햢', '햣', '햤', '햦', '햧', '햨', '햩', '햪', '햫', '햬', '햭', '햮', '햯', '햰', '햱', '햲', '햳', '햴', '햵', '햶', '햷', '햸', '햹', '햺', '햻', '햼', '햽', '햾', '햿', '헀', '헁', '헂', '헃', '헄', '헅', '헆', '헇', '헊', '헋', '헍', '헎', '헏', '헑', '헓', '헔', '헕', '헖', '헗', '헚', '헜', '헞', '헟', '헠', '헡', '헢', '헣', '헦', '헧', '헩', '헪', '헫', '헭', '헮', '헯', '헰', '헱', '헲', '헳', '헶', '헸', '헺', '헻', '헼', '헽', '헾', '헿', '혂', '혃', '혅', '혆', '혇', '혉', '혊', '혋', '혌', '혍', '혎', '혏', '혒', '혖', '혗', '혘', '혙', '혚', '혛', '혝', '혞', '혟', '혡', '혢', '혣', '혥', '혦', '혧', '혨', '혩', '혪', '혫', '혬', '혮', '혯', '혰', '혱', '혲', '혳', '혴', '혵', '혶', '혷', '혺', '혻', '혽', '혾', '혿', '홁', '홂', '홃', '홄', '홆', '홇', '홊', '홌', '홎', '홏', '홐', '홒', '홓', '홖', '홗', '홙', '홚', '홛', '홝', '홞', '홟', '홠', '홡', '홢', '홣', '홤', '홥', '홦', '홨', '홪', '홫', '홬', '홭', '홮', '홯', '홲', '홳', '홵', '홶', '홷', '홸', '홹', '홺', '홻', '홼', '홽', '홾', '홿', '횀', '횁', '횂', '횄', '횆', '횇', '횈', '횉', '횊', '횋', '횎', '횏', '횑', '횒', '횓', '횕', '횖', '횗', '횘', '횙', '횚', '횛', '횜', '횞', '횠', '횢', '횣', '횤', '횥', '횦', '횧', '횩', '횪', '횫', '횭', '횮', '횯', '횱', '횲', '횳', '횴', '횵', '횶', '횷', '횸', '횺', '횼', '횽', '횾', '횿', '훀', '훁', '훂', '훃', '훆', '훇', '훉', '훊', '훋', '훍', '훎', '훏', '훐', '훒', '훓', '훕', '훖', '훘', '훚', '훛', '훜', '훝', '훞', '훟', '훡', '훢', '훣', '훥', '훦', '훧', '훩', '훪', '훫', '훬', '훭', '훮', '훯', '훱', '훲', '훳', '훴', '훶', '훷', '훸', '훹', '훺', '훻', '훾', '훿', '휁', '휂', '휃', '휅', '휆', '휇', '휈', '휉', '휊', '휋', '휌', '휍', '휎', '휏', '휐', '휒', '휓', '휔', '휕', '휖', '휗', '휚', '휛', '휝', '휞', '휟', '휡', '휢', '휣', '휤', '휥', '휦', '휧', '휪', '휬', '휮', '휯', '휰', '휱', '휲', '휳', '휶', '휷', '휹', '휺', '휻', '휽', '휾', '휿', '흀', '흁', '흂', '흃', '흅', '흆', '흈', '흊', '흋', '흌', '흍', '흎', '흏', '흒', '흓', '흕', '흚', '흛', '흜', '흝', '흞', '흟', '흢', '흤', '흦', '흧', '흨', '흪', '흫', '흭', '흮', '흯', '흱', '흲', '흳', '흵', '흶', '흷', '흸', '흹', '흺', '흻', '흾', '흿', '힀', '힂', '힃', '힄', '힅', '힆', '힇', '힊', '힋', '힍', '힎', '힏', '힑', '힒', '힓', '힔', '힕', '힖', '힗', '힚', '힜', '힞', '힟', '힠', '힡', '힢', '힣', '\ud7a4']
```
</details>

<details>
<summary>29. filter_out</summary>

This filters out bad text based on various conditions.

Args:
- text (`Union[str, List[str], Tuple[str]]`): single text or list of texts
- min_length (`int`): minimum length of text
- max_length (`int`): maximum length of text
- min_mean_words_length (`int`): minimum mean words length
- max_mean_words_length (`int`): maximum mean words length
- min_words (`int`): minimum number of words
- max_words (`int`): maximum number of words
- min_lines (`int`): minimum number of lines
- max_lines (`int`): maximum number of lines
- min_paragraphs (`int`): minimum number of paragraphs
- max_paragraphs (`int`): maximum number of paragraphs
- min_alphabet_ratio (`float`): minimum alphabet ratio
- max_alphabet_ratio (`float`): maximum alphabet ratio
- min_alphanumeric_ratio (`float`): minimum alphanumeric ratio
- max_alphanumeric_ratio (`float`): maximum alphanumeric ratio
- min_number_ratio (`float`): minimum number ratio
- max_number_ratio (`float`): maximum number ratio
- min_punctuation_ratio (`float`): minimum punctuation ratio
- max_punctuation_ratio (`float`): maximum punctuation ratio
- min_symbols_to_words_ratio (`float`): minimum symbols to words ratio
- max_symbols_to_words_ratio (`float`): maximum symbols to words ratio
- min_lines_started_with_bullets_ratio (`float`): minimum lines started with bullets ratio
- max_lines_started_with_bullets_ratio (`float`): maximum lines started with bullets ratio
- min_whitespace_ratio (`float`): minimum whitespace ratio
- max_whitespace_ratio (`float`): maximum whitespace ratio
- min_parenthesis_ratio (`float`): minimum parenthesis ratio
- max_parenthesis_ratio (`float`): maximum parenthesis ratio
- min_ellipsis_ratio (`float`): minimum ellipsis ratio
- max_ellipsis_ratio (`float`): maximum ellipsis ratio
- min_hangul_ratio (`float`): minimum hangul ratio
- max_hangul_ratio (`float`): maximum hangul ratio
- max_words_length (`int`): maximum words length
- max_line_repeats (`int`): maximum line repeats
- max_line_by_char_repeats (`int`): maximum line by char repeats
- max_paragraph_repeats (`int`): maximum paragraph repeats
- max_paragraph_by_char_repeats (`int`): maximum paragraph by char repeats
- max_repeating_top_ngram_repeats_score (`float`): maximum repeating top ngram repeats score
- max_repeating_duplicate_ngrams_score (`float`): maximum repeating duplicate ngrams score
- ngram_size_for_repeating_top_ngram_repeats (`int`): ngram size for repeating top ngram repeats
- ngram_size_for_repeating_duplicate_ngrams (`int`): ngram size for repeating duplicate ngrams
- max_hangul_incompleted_form_ratio (`float`): maximum hangul non completed form ratio
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[Tuple[bool, Dict[str, Any]], List[Tuple[bool, Dict[str, Any]]]]`: filtered out text or list of filtered out texts

Examples:
```python
>>> from kss import Kss
>>> filter_out = Kss("filter_out")
>>> text = "▲ 12월 17일 (목)=============================================================================시간 경기내용 방송사=============================================================================[축구] 프랑스 리그 103:00 (AS모나코-스타드 렌) SBS스포츠[축구] 09-10 UEFA 유로파리그04:00 (스파르타프라하-FC코펜하겐) MBC-ESPN[축구] 09-10 프리미어리그05:00 (토트넘-맨체스터시티) SBS스포츠-----------------------------------------------------------------------------[농구] 2009-10 NBA10:00 (LA레이커스-밀워키) SBS스포츠[농구] 2009-10 신한은행 여자농구17:00 (삼성생명-금호생명) SBS스포츠[농구] 2009-10 KCC 프로농구19:00 (KCC-KT) MBC-ESPN19:00 (LG-SK) SBS스포츠-----------------------------------------------------------------------------[배구] 2009-10 NH농협 V리그17:00 (흥국생명-현대건설)19:00 (대한항공-신협상무) KBS N 스포츠-----------------------------------------------------------------------------19:20 [핸드볼] 2009 세계여자선수권대회-----------------------------------------------------------------------------19:00 [배드민턴] 한국 최강전=============================================================================※ 상기 경기일정 및 방송 편성정보는 사정에 따라 변동될 수 있습니다< pre >/한국아이닷컴 뉴스부 한국아이닷컴 뉴스부 '스타화보 VM' 무료다운받기 [**8253+NATE 또는 통화] [ⓒ 인터넷한국일보(www.hankooki.com), 무단 전재 및 재배포 금지]"
>>> output = filter_out(text, min_mean_words_length=2, max_mean_words_length=10)
>>> print(output)
(True, {'reason': 'mean_words_length', 'value': 13.025316455696203})
```
</details>

<details>
<summary>30. half2full</summary>

This converts half-width characters to full-width characters.

Args:
- text (`Union[str, List[str], Tuple[str]]`): single text or list of texts
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[str, List[str]]`: converted text or list of converted texts

Examples:
```python
>>> from kss import Kss
>>> half2full = Kss("half2full")
>>> text = "ﾻﾻﾻﾻﾻﾻ"
>>> half2full(text)
'ㅋㅋㅋㅋㅋㅋ'
```
</details>

<details>
<summary>31. normalize</summary>

This normalizes text with various options.

Args:
- text (`Union[str, List[str], Tuple[str]]`): single text or list of texts
- normalization_type (`Optional[str]`): normalization type
- allow_doubled_spaces (`bool`): whether to allow doubled spaces or not
- allow_html_tags (`bool`): whether to allow HTML tags or not
- allow_html_escape (`bool`): whether to allow HTML unescape or not
- allow_halfwidth_hangul (`bool`): whether to allow halfwidth Hangul or not
- allow_hangul_jamo (`bool`): whether to allow Hangul jamo or not
- allow_invisible_chars (`bool`): whether to allow invisible characters or not
- reduce_char_repeats_over (`int`): the maximum number of character that can be repeated
- reduce_emoticon_repeats_over (`int`): the maximum number of emoticon that can be repeated
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[str, List[str]]`: normalized text or list of normalized texts

Examples:
```python
>>> from kss import Kss
>>> normalize = Kss("normalize")
>>> text = "안녕\u200b하세요 ﾻﾻﾻﾻﾻﾻ   <br>오늘\u200b은 날이 참 좋네요.\n\n\n200 &lt; 300 &amp; 400"
>>> normalize(text, allow_doubled_spaces=False, allow_html_tags=False, allow_html_escape=False, allow_halfwidth_hangul=False, allow_hangul_jamo=False, allow_invisible_chars=False, reduce_char_repeats_over=2, reduce_emoticon_repeats_over=2)
'안녕하세요 ㅋㅋ 오늘은 날이 참 좋네요.\n200 < 300 & 400'
```
</details>

<details>
<summary>32. preprocess</summary>

This preprocesses text with various options.
This does 1) normalization, 2) filtering out, and 3) anonymization in order.

Args:
- text (`Union[str, List[str], Tuple[str]]`): single text or list of texts
- normalization_type (`Optional[str]`): normalization type
- allow_doubled_spaces (`bool`): whether to allow doubled spaces or not
- allow_html_tags (`bool`): whether to allow HTML tags or not
- allow_html_escape (`bool`): whether to allow HTML escape or not
- allow_halfwidth_hangul (`bool`): whether to allow halfwidth Hangul or not
- allow_hangul_jamo (`bool`): whether to allow Hangul jamo or not
- allow_invisible_chars (`bool`): whether to allow invisible characters or not
- reduce_char_repeats_over (`int`): the maximum number of character that can be repeated
- reduce_emoticon_repeats_over (`int`): the maximum number of emoticon that can be repeated
- min_length (`int`): minimum length of text
- max_length (`int`): maximum length of text
- min_mean_words_length (`int`): minimum mean words length
- max_mean_words_length (`int`): maximum mean words length
- min_words (`int`): minimum number of words
- max_words (`int`): maximum number of words
- min_lines (`int`): minimum number of lines
- max_lines (`int`): maximum number of lines
- min_paragraphs (`int`): minimum number of paragraphs
- max_paragraphs (`int`): maximum number of paragraphs
- min_alphabet_ratio (`float`): minimum alphabet ratio
- max_alphabet_ratio (`float`): maximum alphabet ratio
- min_alphanumeric_ratio (`float`): minimum alphanumeric ratio
- max_alphanumeric_ratio (`float`): maximum alphanumeric ratio
- min_number_ratio (`float`): minimum number ratio
- max_number_ratio (`float`): maximum number ratio
- min_punctuation_ratio (`float`): minimum punctuation ratio
- max_punctuation_ratio (`float`): maximum punctuation ratio
- min_symbols_to_words_ratio (`float`): minimum symbols to words ratio
- max_symbols_to_words_ratio (`float`): maximum symbols to words ratio
- min_lines_started_with_bullets_ratio (`float`): minimum lines started with bullets ratio
- max_lines_started_with_bullets_ratio (`float`): maximum lines started with bullets ratio
- min_whitespace_ratio (`float`): minimum whitespace ratio
- max_whitespace_ratio (`float`): maximum whitespace ratio
- min_parenthesis_ratio (`float`): minimum parenthesis ratio
- max_parenthesis_ratio (`float`): maximum parenthesis ratio
- min_ellipsis_ratio (`float`): minimum ellipsis ratio
- max_ellipsis_ratio (`float`): maximum ellipsis ratio
- min_hangul_ratio (`float`): minimum Hangul ratio
- max_hangul_ratio (`float`): maximum Hangul ratio
- max_hangul_incompleted_form_ratio (`float`): maximum Hangul non-completed form ratio
- max_words_length (`int`): maximum words length
- max_line_repeats (`int`): maximum line repeats
- max_line_by_char_repeats (`int`): maximum line by char repeats
- max_paragraph_repeats (`int`): maximum paragraph repeats
- max_paragraph_by_char_repeats (`int`): maximum paragraph by char repeats
- max_repeating_top_ngram_repeats_score (`float`): maximum repeating top ngram repeats score
- max_repeating_duplicate_ngrams_score (`float`): maximum repeating duplicate ngrams score
- ngram_size_for_repeating_top_ngram_repeats (`int`): ngram size for repeating top ngram repeats
- ngram_size_for_repeating_duplicate_ngrams (`int`): ngram size for repeating duplicate ngrams
- phone_number_anonymization (`bool`): whether to anonymize phone number or not
- rrn_anonymization (`bool`): whether to anonymize RRN or not
- card_anonymization (`bool`): whether to anonymize card or not
- email_anonymization (`bool`): whether to anonymize email or not
- back_account_anonymization (`bool`): whether to anonymize bank account or not
- credit_card_anonymization (`bool`): whether to anonymize credit card or not
- zip_anonymization (`bool`): whether to anonymize zip or not
- bitcoin_anonymization (`bool`): whether to anonymize bitcoin or not
- url_anonymization (`bool`): whether to anonymize URL or not
- ip_v6_anonymization (`bool`): whether to anonymize IPv6 or not
- ip_v4_anonymization (`bool`): whether to anonymize IPv4 or not
- phone_number_replacement (`str`): replacement for phone number
- rrn_replacement (`str`): replacement for RRN
- card_replacement (`str`): replacement for card
- email_replacement (`str`): replacement for email
- back_account_replacement (`str`): replacement for bank account
- credit_card_replacement (`str`): replacement for credit card
- zip_replacement (`str`): replacement for zip
- bitcoin_replacement (`str`): replacement for bitcoin
- url_replacement (`str`): replacement for URL
- ip_v6_replacement (`str`): replacement for IPv6
- ip_v4_replacement (`str`): replacement for IPv4
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[Tuple[str, Dict[str, Any]], List[Tuple[str, Dict[str, Any]]]]`: preprocessed text and filtering metadata or list of preprocessed texts and filtering metadata
</details>

<details>
<summary>33. reduce_char_repeats</summary>

This reduces character repeats in text.

Args:
- text (`Union[str, List[str], Tuple[str]]`): single text or list of texts
- num_repeats (`int`): the number of character that can be repeated
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[str, List[str]]`: text with reduced character repeats or list of texts with reduced character repeats

Examples:
```python
>>> from kss import Kss
>>> reduce_char_repeats = Kss("reduce_char_repeats")
>>> text = "고고고고고고고"
>>> output = reduce_char_repeats(text)
>>> print(output)
'고고'
```
References:
- This was copied from [soynlp](https://github.com/lovit/soynlp) and modified by Kss
</details>

<details>
<summary>34. reduce_emoticon_repeats</summary>

This reduces emoticon repeats in text.

Args:
- text (`Union[str, List[str], Tuple[str]]`): single text or list of texts
- num_repeats (`int`): the number of emoticon that can be repeated
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[str, List[str]]`: text with reduced emoticon repeats or list of texts with reduced emoticon repeats

Examples:
```python
>>> from kss import Kss
>>> reduce_emoticon_repeats = Kss("reduce_emoticon_repeats")
>>> text = "앜ㅋㅋㅋㅋㅋㅋ"
>>> output = reduce_emoticon_repeats(text)
>>> print(output)
'아ㅋㅋ'
```
References:
- This was copied from [soynlp](https://github.com/lovit/soynlp) and modified by Kss
</details>

<details>
<summary>35. remove_invisible_chars</summary>

This removes invisible characters from text.

Args:
- text (`Union[str, List[str], Tuple[str]]`): single text or list of texts
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[str, List[str]]`: text with removed invisible characters or list of texts with removed invisible characters

Examples:
```python
>>> from kss import Kss
>>> remove_invisible_chars = Kss("remove_invisible_chars")
>>> text = "안녕\u200b하세요"
>>> remove_invisible_chars(text)
'안녕하세요'
```
</details>

<details>
<summary>36. qwerty</summary>

This converts text from one language to another using QWERTY keyboard layout.

Args:
- text (`Union[str, List[str], Tuple[str]]`): single text or list of texts
- src (`str`): source language
- tgt (`str`): target language
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[str, List[str]]`: converted text or list of converted texts

Examples:
```python
>>> from kss import Kss
>>> qwerty = Kss("qwerty")
>>> text = "dkssudgktpdy"
>>> qwerty(text, src="en", tgt="ko")
'안녕하세요'
>>> text = "안녕하세요"
>>> qwerty(text, src="ko", tgt="en")
'dkssudgktpdy'
```
References:
- This was copied from [inko.py](https://github.com/738/inko.py) and modified by Kss
</details>

<details>
<summary>37. romanize</summary>

This romanizes Korean text.

Args:
- text (`Union[str, List[str], Tuple[str]]`): single text or list of texts
- use_morpheme_info (`bool`): whether to use morpheme information or not
- backend (`str`): morpheme analyzer backend. 'mecab', 'pecab' are supported
- convert_english_to_hangul_phonemes (`bool`): whether to convert English to Hangul phonemes or not
- convert_numbers_to_hangul_phonemes (`bool`): whether to convert numbers to Hangul phonemes or not
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[str, List[str]]`: romanized text or list of romanized texts

Examples:
```python
>>> from kss import Kss
>>> romanize = Kss("romanize")
>>> text = "안녕하세요"
>>> romanize(text)
'annyeonghaseyo'
>>> text = "대관령"
>>> romanize(text)
'daegwallyeong'
```
References:
- This was copied from [korean-romanizer](https://github.com/osori/korean-romanizer) and modified by Kss
</details>

<details>
<summary>38. is_unsafe</summary>

This checks if the text is unsafe or not.

Args:
- text (`Union[str, List[str], Tuple[str]]`): single text or list of texts
- return_matches (`bool`): whether to return matches or not
- num_workers (`Union[int, str]`): the number of multiprocessing workers

Returns:
- `Union[bool, List[bool], List[bool], List[List[str]]]`: whether the text is unsafe or not or list of whether the texts are unsafe or not or list of matched bad words in the texts

Examples:
```python
>>> from kss import Kss
>>> is_unsafe = Kss("is_unsafe")
>>> text = "안녕하세요"
>>> is_unsafe(text)
False
>>> text = "안녕하세요. 씨발"
>>> is_unsafe(text)
True
>>> text = ["안녕하세요", "안녕하세요. 씨발"]
>>> is_unsafe(text)
[False, True]
>>> text = "안녕하세요. 씨발"
>>> is_unsafe(text, return_matches=True)
['씨발']
>>> text = ["안녕하세요", "안녕하세요. 씨발"]
>>> is_unsafe(text, return_matches=True)
[[], ['씨발']]
```
</details>

<details>
<summary>39. split_sentences</summary>

This splits texts into sentences.

Args:
- text (`Union[str, List[str], Tuple[str]]`): single text or list/tuple of texts
- backend (`str`): morpheme analyzer backend. 'mecab', 'pecab', 'punct' are supported
- num_workers (`Union[int, str]`): the number of multiprocessing workers
- strip (`bool`): strip all sentences or not
- return_morphemes (`bool`): whether to return morphemes or not
- ignores (`List[str]`): list of strings to ignore

Returns:
- `Union[List[str], List[List[str]]]`: outputs of sentence splitting

Examples:
```python
>>> from kss import Kss
>>> split_sentences = Kss("split_sentences")
>>> text = "회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요 다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다 강남역 맛집 토끼정의 외부 모습."
>>> split_sentences(text)
['회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요', '다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다', '강남역 맛집 토끼정의 외부 모습.']
```
</details>

<details>
<summary>40. correct_spacing</summary>

This corrects the spacing of the text.

Args:
- text (`Union[str, List[str], Tuple[str]]`): single text or list/tuple of texts
- backend (`str`): morpheme analyzer backend. 'mecab', 'pecab', 'punct' are supported
- num_workers (`Union[int, str]`): the number of multiprocessing workers
- reset_whitespaces (`bool`): reset whitespaces or not
- return_morphemes (`bool`): whether to return morphemes or not

Returns:
- `Union[str, List[str]]`: corrected text or list of corrected texts

Examples:
```python
>>> from kss import Kss
>>> correct_spacing = Kss("correct_spacing")
>>> text = "아버지가방에들어가시다"
>>> correct_spacing(text)
'아버지가 방에 들어가시다'
```
References:
- This was copied from [Kiwi](https://github.com/bab2min/kiwipiepy) and [ko-prfrdr](https://github.com/ychoi-kr/ko-prfrdr) and modified by Kss
</details>

<details>
<summary>41. summarize_sentences</summary>

This summarizes the given text, using TextRank algorithm.

Args:
- text (`Union[str, List[str], Tuple[str]]`): single text or list/tuple of texts
- backend (`str`): morpheme analyzer backend. 'mecab', 'pecab' are supported.
- num_workers (`Union[int, str]`): the number of multiprocessing workers
- max_sentences (`int`): the max number of sentences in a summarization result.
- tolerance (`float`): a threshold for omitting edge weights.
- strip (`bool`): strip all sentences or not
- ignores (`List[str]`): list of strings to ignore

Returns:
- `Union[List[str], List[List[str]]]`: outputs of text summarization

Examples:
```python
>>> from kss import Kss
>>> summarize_sentences = Kss("summarize_sentences")
>>> text = "개그맨 겸 가수 ‘개가수’ UV 유세윤이 신곡 발매 이후 많은 남편들의 응원을 받고 있다. 유세윤은 지난 3일 오후 6시 새 싱글 ‘마더 사커(Mother Soccer)(Feat. 수퍼비)’를 발매했다. ‘마더 사커’는 아내에 대한 서운한 마음을 위트 있고 강한 어조로 디스 하는 남편 유세윤의 마음을 담은 곡이다. 발매 후 소셜 미디어 상에서 화제를 모으고 있는 가운데, 가수 하동균은 “유세유니 괜찮겠어”라는 반응을 보이기도 했다. 누리꾼들은 ‘두 분의 원만한 합의가 있기를 바랍니다’, ‘집에는 들어갈 수 있겠나’ 등 유세윤의 귀가를 걱정하는 모습을 보였다. 유세윤은 점입가경으로 ‘마더 사커’ 챌린지를 시작, 자신의 SNS를 통해 “부부 싸움이 좀 커졌네요”라며 배우 송진우와 함께 촬영한 영상을 게재했다. 해당 영상에서는 양말을 신고 침대에 들어간 뒤 환호를 지르거나 화장실 불을 끄지 않고 도망가는 등 아내의 잔소리 유발 포인트를 살려 재치 있는 영상을 완성했다. 유세윤은 ‘마더 사커’를 통해 남편들의 마음을 대변해 주고 있는 한편 아내의 반응은 어떨지 궁금증을 모은다."
>>> summarize_sentences(text)
['개그맨 겸 가수 ‘개가수’ UV 유세윤이 신곡 발매 이후 많은 남편들의 응원을 받고 있다.', '‘마더 사커’는 아내에 대한 서운한 마음을 위트 있고 강한 어조로 디스 하는 남편 유세윤의 마음을 담은 곡이다.', '유세윤은 ‘마더 사커’를 통해 남편들의 마음을 대변해 주고 있는 한편 아내의 반응은 어떨지 궁금증을 모은다.']
```
References:
- This was copied from [textrankr](https://https://github.com/theeluwin/textrankr) and modified by Kss
</details>


## Kss in various programming languages
Kss is available in various programming languages. 

Please note that previous versions of Kss only included sentence segmentation functions.

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

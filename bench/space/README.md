# 띄어쓰기 교정 평가

이 폴더에는 띄어쓰기 교정 성능을 평가하기 위한 코드와 데이터가 있습니다. 평가 데이터는 testset 폴더 안에 있으며 다음과 같이 구성되어 있습니다.

* written(문어 텍스트): [모두의 말뭉치](https://corpus.korean.go.kr/) `문어 말뭉치`에서 임의로 추출한 문장들 200개로 구성된 데이터

또한 다음 평가 코드를 제공합니다.

* space.py: `Kiwi` 및 다른 띄어쓰기 교정기의 성능을 평가합니다.
* make_space_errors.py: 일반 텍스트를 교란하여 띄어쓰기 성능 평가용 데이터셋으로 만듭니다.

## 직접 평가 실행해보기
[PyKoSpacing](https://github.com/haven-jeon/PyKoSpacing)의 성능을 평가하기 위해서는 해당 패키지를 미리 설치하여야 합니다.

```console
$ python space.py testset/*.txt --target=kiwi,kospacing
Initialize kiwipiepy (0.13.1)
Initialize PyKoSpacing
                            Baseline   kiwi   kospacing
written.txt                 0.536   0.934   0.798
written.txt (reset spaces)  0.000   0.937   0.951

Elapsed Time (ms)
                    kiwi    kospacing
written.txt     1224.228        15784.584
```
Kiwi는 PyKoSpacing에 준하는 띄어쓰기 교정 성능을 보이지만 속도 측면에서는 10배 이상 빠릅니다.

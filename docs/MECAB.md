# Mecab Installation Guide

## Winodws
- (1) Make folder named `mecab` in C drive (`C:/mecab`)
- (2) Download [mecab](https://github.com/Pusnow/mecab-ko-msvc/releases/tag/release-0.9.2-msvc-3) zip file. (64bit: x64 / 32bit: x86) 
- (3) Download [mecab-ko-dic](https://github.com/Pusnow/mecab-ko-dic-msvc/releases/tag/mecab-ko-dic-2.1.1-20180720-msvc) zip file.
- (4) Unzip these files into `C:/mecab`.
- (5) Download wheel file [here](https://github.com/Pusnow/mecab-python-msvc/releases/tag/mecab_python-0.996_ko_0.9.2_msvc-2) 
  - Match your python version. (python 3.6: cp36, python 2.7: cp27)
  - Match your winodws version. (64bit: win_amd64 / 32bit: win32)
- (6) Run `pip install WHEEL_FILE_NAME` 
  - e.g. `pip install mecab_python-0.996_ko_0.9.2_msvc-cp35-cp35m-win_amd64.whl`

## Linux
Run the following script.
```bash
cd
mkdir mecab
cd mecab
wget https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.1.tar.gz
tar xvzf mecab-0.996-ko-0.9.1.tar.gz
cd mecab-0.996-ko-0.9.1
./configure
make
make check
sudo make install
cd .. 
wget https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-1.6.1-20140814.tar.gz
tar xvzf mecab-ko-dic-1.6.1-20140814.tar.gz
cd mecab-ko-dic-1.6.1-20140814
./configure
make
sudo make install
sudo ln -s /usr/local/bin/mecab-config /usr/bin/mecab-config
sudo python3 -m pip install python-mecab-ko —upgrade

```

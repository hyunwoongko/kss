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

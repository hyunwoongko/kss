from kss import Kss


def test_morphemes():
    split_morphemes = Kss("split_morphemes")
    text = "아버지가방에들어오시다."
    output = split_morphemes(text)
    assert output == [('아버지', 'NNG'), ('가', 'JKS'), ('방', 'NNG'), ('에', 'JKB'), ('들어오', 'VV'), ('시', 'EP'), ('다', 'EF'), ('.', 'SF')]


if __name__ == '__main__':
    test_morphemes()

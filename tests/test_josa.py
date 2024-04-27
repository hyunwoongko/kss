from kss import Kss


def test_select_josa():
    select_josa = Kss("select_josa")
    prefix = "철수"
    josa = "은"
    output = select_josa(prefix, josa)
    assert output == "는"


def test_combine_josa():
    combine_josa = Kss("combine_josa")
    prefix = "철수"
    josa = "은"
    output = combine_josa(prefix, josa)
    assert output == "철수는"


if __name__ == '__main__':
    test_select_josa()
    test_combine_josa()

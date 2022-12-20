from kiwipiepy import Kiwi
from sentence_split import run_evaluate

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("datasets", nargs="+")
    parser.add_argument("--write_result")
    parser.add_argument("--write_err")
    args = parser.parse_args()

    kiwi = Kiwi()
    kiwi.split_into_sents("foo-bar")  # warm-up

    for dataset in args.datasets:
        run_evaluate(
            dataset,
            lambda text: [s.text for s in kiwi.split_into_sents(text)],
            args.write_result,
            args.write_err,
        )

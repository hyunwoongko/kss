import re

from sentence_split import run_evaluate


def word_splitter(text):
    return text.split(" ")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("datasets", nargs="+")
    parser.add_argument("--write_result")
    parser.add_argument("--write_err")
    args = parser.parse_args()

    word_splitter("foo-bar")  # warm-up

    for dataset in args.datasets:
        run_evaluate(
            dataset,
            lambda text: word_splitter(text),
            args.write_result,
            args.write_err,
        )

import re

from sentence_split import run_evaluate


def baseline_splitter(text):
    return re.split(r"(?<=[.!?])\s", text)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("datasets", nargs="+")
    parser.add_argument("--write_result")
    parser.add_argument("--write_err")
    args = parser.parse_args()

    baseline_splitter("foo-bar")  # warm-up

    for dataset in args.datasets:
        run_evaluate(
            dataset,
            lambda text: baseline_splitter(text),
            args.write_result,
            args.write_err,
        )

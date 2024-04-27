from kss import split_sentences
from sentence_split import run_evaluate

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("datasets", nargs="+")
    parser.add_argument("--write_result")
    parser.add_argument("--write_err")
    parser.add_argument("--backend", default="mecab", choices=["mecab", "pecab", "punct", "fast"])
    args = parser.parse_args()

    split_sentences("foo-bar", backend=args.backend)  # warm-up

    for dataset in args.datasets:
        run_evaluate(
            dataset,
            lambda text: split_sentences(text, backend=args.backend),
            args.write_result,
            args.write_err,
        )

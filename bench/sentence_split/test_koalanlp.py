from koalanlp import API
from koalanlp.Util import initialize, finalize
from koalanlp.proc import SentenceSplitter, Tagger

from sentence_split import run_evaluate

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("datasets", nargs="+")
    parser.add_argument("--write_result")
    parser.add_argument("--write_err")
    parser.add_argument(
        "--backend",
        default="OKT",
        choices=["OKT", "HNN", "KMR", "RHINO", "EUNJEON", "ARIRANG", "KKMA"],
    )
    args = parser.parse_args()

    initialize(**{args.backend: "LATEST"})
    if args.backend in ("OKT", "HNN"):
        splitter = SentenceSplitter(getattr(API, args.backend))
    else:
        tagger = Tagger(getattr(API, args.backend))
        splitter = lambda text: [sent.surfaceString() for sent in tagger(text)]

    splitter("foo-bar")  # warm-up

    for dataset in args.datasets:
        run_evaluate(dataset, splitter, args.write_result, args.write_err)

    finalize()

import itertools
import re
import sys

import numpy as np

sep_pat = re.compile(r'   |(?<=[.!?]) ')
space_pat = re.compile(r'[ ]')
space_inds = np.array(['', '\u2594', '\u2581', ' '])


def pertubate(text: str):
    if len(text) <= 15: return

    p = np.array([m.start() for m in space_pat.finditer(text)])
    if not len(p): return

    p -= np.arange(len(p))
    text = space_pat.sub('', text)
    q = np.random.choice(len(text), size=(len(p),), replace=False)
    p_not_in_q = p[np.random.permutation(len(p))][np.where(~np.in1d(p, q))[0]]
    q_in_p = np.in1d(q, p)
    for _, i in zip(range((len(p) + 1) // 2 - q_in_p.sum()), np.where(~q_in_p)[0]):
        q[i] = p_not_in_q[i]
    q.sort()
    a = np.arange(len(text))
    ind = np.in1d(a, p) + np.in1d(a, q) * 2
    ret = ''.join(map(''.join, zip(space_inds[ind], text)))
    ret = ret.strip('\u2581\u2594')
    return ret


def main(args):
    np.random.seed(args.seed)
    if args.inputs:
        inputs = itertools.chain.from_iterable(open(i, encoding='utf-8') for i in args.inputs)
    else:
        inputs = sys.stdin

    for line in inputs:
        sents = sep_pat.split(line.rstrip())
        if args.bisent:
            a = None
            for b in map(pertubate, sents):
                if a and b: print(a, b)
                a = b
        else:
            for b in filter(None, map(pertubate, sents)):
                print(b)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('inputs', nargs='*')
    parser.add_argument('--seed', default=777, type=int)
    parser.add_argument('--bisent', default=False, action='store_true')
    main(parser.parse_args())

import os
import re
import sys
import time

import numpy as np

import kss


class Model:
    def space(self, text):
        raise NotImplementedError

    @staticmethod
    def from_name(name, kiwi_model_path=None, kiwi_model_type='knlm', kiwi_space_tolerance=2, kiwi_space_penalty=7.):
        if name == 'kiwi': return KiwiModel(kiwi_model_path, kiwi_model_type, kiwi_space_tolerance, kiwi_space_penalty)
        if name == 'kospacing': return KoSpacingModel()
        if name == "kss": return KssSpacingModel()


class KiwiModel(Model):
    def __init__(self, model_path=None, model_type='knlm', space_tolerance=2, space_penalty=7.):
        import kiwipiepy
        from kiwipiepy import Kiwi
        print("Initialize kiwipiepy ({})".format(kiwipiepy.__version__), file=sys.stderr)
        self._mdl = Kiwi(model_path=model_path, model_type=model_type)
        self._mdl.space_tolerance = space_tolerance
        self._mdl.space_penalty = space_penalty

    def space(self, text):
        return self._mdl.space(text)


class KoSpacingModel(Model):
    def __init__(self):
        from pykospacing import Spacing
        print("Initialize PyKoSpacing", file=sys.stderr)
        self._mdl = Spacing()

    def space(self, text):
        return self._mdl(text)


class KssSpacingModel(Model):
    def space(self, text):
        return kss.correct_spacing(text)


def extract_space_pos(text):
    p = np.array([m.start() for m in re.finditer(r' ', text)])
    p -= np.arange(len(p))
    return p


def calc_f1(a, b):
    c = len(a & b)
    if not c: return 0.
    return 2 * c / (len(a) + len(b))


def evaluate(dataset_path, model: Model):
    total_cnt = 0
    acc_baseline_f1 = 0
    acc_system_f1 = 0
    acc_system_ws_f1 = 0
    elapsed = 0

    for line in open(dataset_path, encoding='utf-8'):
        data = line.rstrip()

        test = data.replace('\u2581', ' ').replace('\u2594', '')
        test_ws = test.replace(' ', '')
        gold = data.replace('\u2581', '').replace('\u2594', ' ')

        elapsed -= time.perf_counter()
        pred = model.space(test)
        pred_from_ws = model.space(test_ws)
        elapsed += time.perf_counter()

        gold_positions = set(extract_space_pos(gold).tolist())
        test_positions = set(extract_space_pos(test).tolist())
        pred_positions = set(extract_space_pos(pred).tolist())
        pred_ws_positions = set(extract_space_pos(pred_from_ws).tolist())
        # pred_ws_positions = set(extract_space_pos(pred).tolist())

        baseline_f1 = calc_f1(gold_positions, test_positions)
        system_f1 = calc_f1(gold_positions, pred_positions)
        system_ws_f1 = calc_f1(gold_positions, pred_ws_positions)

        # if system_f1 < 0.8:
        #     print("input:", test, "\n")
        #     print("pred:", pred, "\n")
        #     print("gold:", gold, "\n")
        #     print("\n\n\n")

        total_cnt += 1
        acc_baseline_f1 += baseline_f1
        acc_system_f1 += system_f1
        acc_system_ws_f1 += system_ws_f1

    return acc_baseline_f1 / total_cnt, acc_system_f1 / total_cnt, acc_system_ws_f1 / total_cnt, elapsed


def main(args):
    model_names = args.target.split(',')
    models = [Model.from_name(n, **{k: v for k, v in args._get_kwargs() if k.startswith('kiwi_')}) for n in model_names]
    elapsed_times = []

    print('              ', 'Baseline', *model_names, sep='\t')
    for dataset in args.datasets:
        scores = []
        scores_ws = []
        elapsed_times.append([])
        for i, model in enumerate(models):
            baseline, system, system_ws, elapsed = evaluate(dataset, model)
            if i == 0:
                scores.append(baseline)
                scores_ws.append(0)
            scores.append(system)
            scores_ws.append(system_ws)
            elapsed_times[-1].append(elapsed)

        print(os.path.basename(dataset) + "               ", *((f'{s:.3f}' if s is not None else '-') for s in scores),
              sep='\t')
        print(os.path.basename(dataset) + " (reset spaces)",
              *((f'{s:.3f}' if s is not None else '-') for s in scores_ws), sep='\t')

    print('\nElapsed Time (ms)')
    print('', *model_names, sep='\t')
    for dataset, elapsed in zip(args.datasets, elapsed_times):
        print(os.path.basename(dataset), *((f'{s * 1000:.3f}' if s is not None else '-') for s in elapsed), sep='\t')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('datasets', nargs='+')
    parser.add_argument('--target', default='kiwi', help='kiwi,kospacing,kss')
    parser.add_argument('--kiwi_model_path')
    parser.add_argument('--kiwi_model_type', default='knlm', choices=['knlm', 'sbg'])
    parser.add_argument('--kiwi_space_tolerance', default=2, type=int)
    parser.add_argument('--kiwi_space_penalty', default=7., type=float)
    main(parser.parse_args())

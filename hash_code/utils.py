import glob
import os
from typing import Any

import numpy as np

MAX_FILES = 3


def write(fd, val: Any):
    if isinstance(val, (list, tuple, np.ndarray, range)):
        text = ' '.join([str(_) for _ in val])
    else:
        text = str(val)
    fd.write('{}\n'.format(text))


def read(fd):
    return [int(item) for item in fd.readline().split(' ')]


def file_score(base_name: str):
    def score(path: str):
        return int(path.replace(base_name, '').replace('.txt', ''))

    return score


def find_best_solution(path: str, name: str):
    try:
        base_name = os.path.abspath('{}/{}_'.format(path, name))
        best_path = max(glob.glob('{}*'.format(base_name)), key=file_score(base_name), default=None)
        return file_score(base_name)(best_path), best_path
    except:
        return 0, None


def smart_export(path: str, solution: 'Solution', problem: 'Problem'):
    problem.check(solution)

    base_name = os.path.abspath('{}/{}_'.format(path, solution.name))

    max_score, _ = find_best_solution(path, solution.name)

    score = problem.score(solution)
    if score < max_score:
        return max_score
    filename = '{}{}.txt'.format(base_name, score)

    solution.save(filename)

    files = sorted([_ for _ in glob.glob('{}*'.format(base_name))], key=file_score(base_name), reverse=True)
    for _ in files[MAX_FILES:]:
        os.remove(_)

    return max_score

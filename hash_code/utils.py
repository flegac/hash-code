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


def smart_export(path: str, solution: 'Solution'):
    base_name = os.path.abspath('{}/{}_'.format(path, solution.name))

    def file_score(path: str):
        return int(path.replace(base_name, '').replace('.txt', ''))

    max_score = max([file_score(_) for _ in glob.glob('{}*'.format(base_name))], default=0)

    if solution.score < max_score:
        return max_score
    filename = '{}{}.txt'.format(base_name, solution.score)

    solution.export(filename)

    files = sorted([_ for _ in glob.glob('{}*'.format(base_name))], key=file_score, reverse=True)
    for _ in files[MAX_FILES:]:
        os.remove(_)

    return max_score

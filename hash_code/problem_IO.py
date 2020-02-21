import os
from typing import List

from hash_code.problem import Problem
from hash_code.solution import Solution


class ProblemIO(object):
    @staticmethod
    def parse_problem(path: str) -> Problem:
        name, _ = os.path.splitext(os.path.basename(path))
        with open(path) as fd:
            pass
        return Problem(name=name)

    @staticmethod
    def parse_solution(path: str) -> Solution:
        name, _ = os.path.splitext(os.path.basename(path))
        with open(path) as fd:
            pass
        return Solution(name=name)

    @staticmethod
    def export(path: str, solution: Solution):
        filename = '{}/{}_{}.txt'.format(path, solution.name, solution.score)
        with open(filename, 'w') as fd:
            pass


def write_int(fd, value: int):
    fd.write('{}\n'.format(str(value)))


def write_list(fd, values: List[object]):
    fd.write('{}\n'.format(' '.join(*values)))


def read_int(fd):
    return int(fd.readline())


def read_pair(fd):
    return [int(item) for item in fd.readline().split(' ')]


def read_list(fd, with_size: bool = False):
    if with_size:
        n = read_int(fd)
        data = [int(item) for item in fd.readline().split(' ')]
        assert len(data) == n
    else:
        data = [int(item) for item in fd.readline().split(' ')]
    return data

import cProfile
import glob
import os
import shutil
import time

from hash_code.problem import Problem
from hash_code.solver import Solver, RandomSolver, BestSolver
from hash_code.utils import smart_export

INPUT_PATH = 'input'
OUTPUT_PATH = 'output'
SOLVER = Solver
# SOLVER = RandomSolver
# SOLVER = BestSolver


SEPARATOR = '+--------------+------+--------------+-------------------------------+------+'


def main():
    print(SEPARATOR)
    print('| {name:^12} | {ratio:^3}  | {max:^12} | {evolution:^28}  | {time:^} |'.format(
        name='name',
        evolution='evolution',
        max='max_score',
        ratio='%',
        time='time'
    ))
    print(SEPARATOR)
    total_score = 0
    current_score = 0
    total_time = 0
    for input_path in glob.glob('{}/[abcdef]*'.format(INPUT_PATH)):
        start = time.time()

        problem = Problem.parse(input_path)
        solution = SOLVER(problem).solve()

        old_score = smart_export(OUTPUT_PATH, solution, problem)
        time_spent = time.time() - start
        score = problem.score(solution)
        current_score += score
        total_score += max(old_score, score)
        total_time += time_spent
        ratio = int(100 * max(old_score, score) / max(1, problem.max_score))
        print('| {improved} {name:10} | {ratio:3}% | {max:12} | {evolution:26}  | {time:.1f}s |'.format(
            improved='*' if old_score < score else ' ',
            name=problem.name[:10],
            evolution='{old:12} -> {new:12}'.format(
                old=old_score,
                new=score),
            max=problem.max_score,
            ratio=ratio,
            time=time_spent
        ))
    print(SEPARATOR)
    print('current total score : {}, total time : {:.1f}s'.format(current_score, total_time))
    print('best total score    : {}'.format(total_score))

    zip_archive_path = '{}/_code'.format(OUTPUT_PATH)
    if not os.path.exists(zip_archive_path + '.zip'):
        shutil.make_archive(zip_archive_path, 'zip', '../hash_code')


if __name__ == '__main__':
    for i in range(1):
        main()
        # cProfile.run("main()", sort=True)

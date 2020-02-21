import glob
import time

from hash_code.problem_IO import ProblemIO
from hash_code.solver import Solver

INPUT_PATH = 'input'
OUTPUT_PATH = 'output'


def main():
    total_score = 0
    total_time = 0
    for input_path in glob.glob('{}/*'.format(INPUT_PATH)):
        start = time.time()
        problem = ProblemIO.parse_problem(input_path)
        solution = Solver(problem).solve()
        ProblemIO.export(OUTPUT_PATH, solution)
        score = solution.score
        time_spent = time.time() - start
        total_score += score
        total_time += time_spent
        print('Score : {} -> {}'.format(problem.name, score))
        print('time : {}s'.format(time_spent))

    print('final score : {}'.format(total_score))
    print('total time : {}s'.format(total_time))


if __name__ == '__main__':
    main()
    # cProfile.run("main()", sort=True)

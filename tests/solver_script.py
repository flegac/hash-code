import glob
import time

from hash_code.problem_IO import ProblemIO
from hash_code.solver.simple_solver import SimpleSolver


def main():
    solver = SimpleSolver()
    total_score = 0
    total_time = 0
    for input_path in glob.glob('resources/*.in'):
        output_path = input_path.replace('.in', '.out')

        state = ProblemIO.parse_input(input_path)

        start = time.time()
        state = solver.solve(state)
        time_spent = time.time() - start

        ProblemIO.export(output_path, state)

        score = state.score()
        print('Score : {} -> {}'.format(state.name, score))
        print('time : {}s'.format(time_spent))
        total_score += score
        total_time += time_spent
    print('final score : {}'.format(total_score))
    print('total time : {}s'.format(total_time))
    # total_score = 0
    # total_time = 0
    # for input_path in glob.glob('resources/*.in'):
    #     output_path = input_path.replace('.in', '.out')
    #     state = ProblemIO.parse_input(input_path)
    #     ProblemIO.parse_output(state, output_path)
    #
    #     start = time.time()
    #     for _ in tqdm.tqdm(range(state.deadline)):
    #         Simulator(state).simulate()
    #     score = state.score()
    #     print('Score : {} -> {}'.format(state.name, score))
    #     total_score += score
    #     time_spent = time.time() - start
    #     print('time : {}s'.format(time_spent))
    #     total_time += time_spent
    # print('final score : {}'.format(total_score))
    # print('total time : {}s'.format(total_time))


if __name__ == '__main__':
    main()
    # cProfile.run("main()", sort=True)

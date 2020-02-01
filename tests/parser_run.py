import glob
import os
import time
from typing import List

import tqdm

from hash_code.model.simulator import Simulator
from hash_code.problem_IO import ProblemIO
from hash_code.solver.simple_solver import SimpleSolver
from hash_code.visu.visu_problem import Points


def weight(products: List[int]):
    w = 0
    for _ in products:
        if _ > 0:
            w += 1
    return w


def show_data(path: str):
    sim = ProblemIO.parse_input(path)

    points = Points()

    for wh in sim.warehouses:
        x, y = sim.area.tuple(wh.cell_id)
        size = weight(wh.products)
        points.point(x, y, size, 'red')

    for order in sim.orders:
        x, y = sim.area.tuple(order.cell_id)
        size = weight(order.products)
        points.point(x, y, size, 'blue')

    name = '{}_drones_{}_wh_{}_products_{}_orders_{}'.format(
        len(sim.drones),
        len(sim.warehouses),
        len(sim.product_weights),
        len(sim.orders),
        os.path.basename(path).replace('.in', ''))

    points.show(name)


if __name__ == '__main__':
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

    total_score = 0
    total_time = 0
    for input_path in glob.glob('resources/*.in'):
        output_path = input_path.replace('.in', '.out')
        state = ProblemIO.parse_input(input_path)
        ProblemIO.parse_output(state, output_path)

        start = time.time()
        for _ in tqdm.tqdm(range(state.deadline)):
            Simulator(state).simulate()
        score = state.score()
        print('Score : {} -> {}'.format(state.name, score))
        total_score += score
        time_spent = time.time() - start
        print('time : {}s'.format(time_spent))
        total_time += time_spent

    print('final score : {}'.format(total_score))
    print('total time : {}s'.format(total_time))

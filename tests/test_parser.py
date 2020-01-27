import glob
import os
from typing import List

from hash_code.parser import Parser
from hash_code.solver.simple_solver import SimpleSolver
from hash_code.visu.visu_problem import Points


def weight(products: List[int]):
    w = 0
    for _ in products:
        if _ > 0:
            w += 1
    return w


def show_data(file):
    sim = Parser(file).get_sim()

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
        os.path.basename(file).replace('.in', ''))

    points.show(name)


if __name__ == '__main__':
    solver = SimpleSolver()
    for _ in glob.glob('resources/*.in'):
        score = solver.solve(_)
        print('simulation completed ! Final score : {} -> {}'.format(os.path.basename(_), score))

        # show_data(_)

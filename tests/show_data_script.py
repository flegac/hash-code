import glob
import os
from typing import List

from hash_code.problem_IO import ProblemIO
from hash_code.visu.visu_problem import Points


def weight(products: List[int]):
    return sum(products)


def show_data(path: str):
    sim = ProblemIO.parse_input(path)

    points = Points()

    for wh in sim.warehouses:
        x, y = wh.cell.data
        size = weight(wh.products)
        points.point(x, y, size, 'red')

    for order in sim.orders:
        x, y = order.cell.data
        size = weight([_.quantity for _ in order.tasks])
        points.point(x, y, size, 'blue')

    name = '{}_drones_{}_wh_{}_products_{}_orders_{}'.format(
        sim.drone_number,
        len(sim.warehouses),
        sim.product_number,
        len(sim.orders),
        os.path.basename(path).replace('.in', ''))

    points.show(name)


def main():
    for input_path in glob.glob('resources/*.in'):
        show_data(input_path)


if __name__ == '__main__':
    main()

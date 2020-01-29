import math
from typing import Callable

import tqdm

from hash_code.model.customer_order import CustomerOrder
from hash_code.model.orders.deliver_order import DeliverOrder
from hash_code.model.orders.load_order import LoadOrder
from hash_code.model.orders.wait_order import WaitOrder
from hash_code.parser import Parser
from hash_code.solver.solver import Solver


class SimpleSolver(Solver):
    def __init__(self, path: str):
        super().__init__(path)
        self.sim = Parser(path).get_sim()
        self.order_id = 0

    def select_best_drone(self, order: CustomerOrder, product_id: int, n: int):
        wh = self.find_best_warehouse(order, product_id, n)
        drones = sorted(self.sim.iddle_drones, key=lambda drone: self.sim.area.dist(drone.cell_id, wh.cell_id))
        return drones[0]

    def sort_by_travel_distance(self, order: CustomerOrder):
        value = 0
        for product_id, n in enumerate(order.products):
            if n > 0:
                wh = self.find_best_warehouse(order, product_id, n)
                value += self.sim.area.dist(order.cell_id, wh.cell_id)
        return value

    def task_generator(self, metric: Callable[[CustomerOrder], float]):
        orders = sorted(self.sim.orders, key=metric)
        for _ in orders:
            for product_id, n in enumerate(_.products):
                if n > 0:
                    yield (_, product_id, n)

    def solve(self):
        print('solving : {}'.format(self.path))

        generator = self.task_generator(self.sort_by_travel_distance)

        for _ in tqdm.tqdm(range(self.sim.deadline)):
            while len(self.sim.iddle_drones) > 0:
                task = next(generator, None)
                if not task:
                    for drone in self.sim.iddle_drones:
                        self.sim.assign_orders(drone.drone_id, [WaitOrder(drone.drone_id, self.sim.deadline)])
                    break
                self.plan_order(*task)

            self.sim.simulate_once()

        return self.sim.score()

    def plan_order(self, order: CustomerOrder, product_id: int, n: int):
        drone = self.select_best_drone(order, product_id, n)
        max_items = math.floor((self.sim.max_load - drone.weight) // self.sim.product_weights[product_id])
        assert max_items > 0

        while n > 0:
            k = min(n, max_items)
            wh = self.find_best_warehouse(order, product_id, k)
            wh.reserved[product_id] += k
            self.sim.assign_orders(drone.drone_id, [
                LoadOrder(drone.drone_id, wh.warehouse_id, product_id, k),
                DeliverOrder(drone.drone_id, order.order_id, product_id, k)
            ])
            n -= k

    def find_best_warehouse(self, order: CustomerOrder, product_id: int, n: int):
        for wh in sorted(self.sim.warehouses, key=lambda wh: self.sim.area.dist(wh.cell_id, order.cell_id)):
            if wh.products[product_id] - wh.reserved[product_id] >= n:
                return wh
        raise ValueError()

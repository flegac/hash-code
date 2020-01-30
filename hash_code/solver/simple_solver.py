import math
from typing import Callable

import tqdm

from hash_code.model.customer_order import CustomerOrder
from hash_code.model.orders.deliver_order import DeliverOrder
from hash_code.model.orders.load_order import LoadOrder
from hash_code.model.orders.wait_order import WaitOrder
from hash_code.model.simulator import Simulator
from hash_code.model.state import State
from hash_code.solver.solver import Solver


class SimpleSolver(Solver):
    def __init__(self):
        self.sim = None

    @property
    def state(self):
        return self.sim.state

    def select_best_drone(self, order: CustomerOrder, product_id: int, n: int):
        wh = self.find_best_warehouse(order, product_id, n)
        drones = sorted(self.sim.idle_drones, key=lambda drone: self.state.area.dist(drone.cell_id, wh.cell_id))
        return drones[0]

    def sort_by_travel_distance(self, order: CustomerOrder):
        value = self.sim.state.area.dist(self.state.warehouses[0].cell_id, order.cell_id) * 2

        for product_id, n in enumerate(order.products):
            if n == 0:
                continue

            wh = self.find_best_warehouse(order, product_id, n)
            value += self.sim.state.area.dist(self.state.warehouses[0].cell_id, wh.cell_id) * 1

            max_items = math.floor(self.state.max_load // self.state.product_weights[product_id])
            k = min(n, max_items)
            value += self.sim.state.area.dist(order.cell_id, wh.cell_id) * math.ceil(n // k) * 1

        return value

    def task_generator(self, metric: Callable[[CustomerOrder], float]):
        orders = sorted(self.state.orders, key=metric)
        while len(orders) > 0:
            _ = orders.pop(0)
            for product_id, n in enumerate(_.products):
                max_items = math.floor(self.state.max_load // self.state.product_weights[product_id])
                k = min(n, max_items)
                while n > 0:
                    n -= k
                    yield (_, product_id, k)

    def solve(self, state: State):
        self.sim = Simulator(state=state)
        print('solving : {}'.format(self.state.name))

        generator = self.task_generator(self.sort_by_travel_distance)

        for _ in tqdm.tqdm(range(self.state.deadline)):
            iddle_drones = self.sim.idle_drones
            for _ in iddle_drones:
                task = next(generator, None)
                if not task:
                    self.sim.assign_orders(_.drone_id, [WaitOrder(_.drone_id, self.state.deadline)])
                else:
                    self.plan_task(*task)
            self.sim.simulate()

        return self.state

    def plan_task(self, order: CustomerOrder, product_id: int, n: int):
        drone = self.select_best_drone(order, product_id, n)
        wh = self.find_best_warehouse(order, product_id, n)
        wh.reserved[product_id] += n
        self.sim.assign_orders(drone.drone_id, [
            LoadOrder(drone.drone_id, wh.warehouse_id, product_id, n),
            DeliverOrder(drone.drone_id, order.order_id, product_id, n)
        ])

    def find_best_warehouse(self, order: CustomerOrder, product_id: int, n: int):
        for wh in sorted(self.state.warehouses, key=lambda wh: self.state.area.dist(wh.cell_id, order.cell_id)):
            if wh.products[product_id] - wh.reserved[product_id] >= n:
                return wh
        raise ValueError()

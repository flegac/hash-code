import math
from typing import List

import numpy as np
import tqdm
from scipy.spatial.distance import cdist

from hash_code.model.area import Area
from hash_code.model.customer_order import CustomerOrder
from hash_code.model.drone import Drone
from hash_code.model.orders.deliver_order import DeliverOrder
from hash_code.model.orders.load_order import LoadOrder
from hash_code.model.orders.wait_order import WaitOrder
from hash_code.model.simulator import Simulator
from hash_code.model.state import State
from hash_code.solver.solver import Solver


class SimpleSolver(Solver):
    def __init__(self, permutation: np.ndarray = None):
        self.sim = None
        self.permutation = permutation

    @property
    def state(self):
        return self.sim.state

    def find_best_drone(self, order: CustomerOrder, product_id: int, n: int):
        def metric(drone: Drone):
            IGNORE_SCORE = 1000000

            score = 0
            if len(drone.order_queue) - drone.current_order_id > 1:
                return IGNORE_SCORE
            if drone.current_order is not None:
                if drone.current_order.remaining_time is None:
                    return IGNORE_SCORE
                score += 2 * drone.current_order.remaining_time
            return Area.dist(drone.cell, wh.cell)

        wh = self.find_best_warehouse(order, product_id, n)

        return min(self.sim.state.drones, key=metric)

    def travel_time_metric(self, initial_dist: float = 2, wh_dist: float = 1):
        def metric(order: CustomerOrder):
            value = self.wh_order_dist[self.state.warehouses[0].warehouse_id, order.order_id] * initial_dist
            for product_id, task in order.task_by_product.items():
                n = task.quantity

                wh = self.find_best_warehouse(order, product_id, n)
                value += self.wh_dist[self.state.warehouses[0].warehouse_id, wh.warehouse_id] * wh_dist

                max_items = math.floor(self.state.max_load // self.state.product_weights[product_id])
                k = min(n, max_items)
                value += self.wh_order_dist[wh.warehouse_id, order.order_id] * math.ceil(n // k) * wh_dist

            return value

        return metric

    def task_generator(self, orders: List[CustomerOrder]):
        for _ in orders:
            for task in _.tasks:
                product_id, n = task.product_id, task.quantity
                max_items = math.floor(self.state.max_load // self.state.product_weights[product_id])
                k = min(n, max_items)
                while n > 0:
                    n -= k
                    yield (_, product_id, k)

    def solve(self, state: State):
        self.sim = Simulator(state=state)
        print('solving : {}'.format(self.state.name))

        self.wh_order_dist = cdist(
            np.array([_.cell.data for _ in self.sim.state.warehouses]),
            np.array([_.cell.data for _ in self.sim.state.orders]),
            Area.dist)
        self.wh_dist = cdist(
            np.array([_.cell.data for _ in self.sim.state.warehouses]),
            np.array([_.cell.data for _ in self.sim.state.warehouses]),
            Area.dist)
        orders = sorted(self.state.orders, key=self.travel_time_metric(2, 1))
        # orders = orders[:self.state.drone_number] + sorted(orders[self.state.drone_number:],
        #                                                    key=self.travel_time_metric(0,1))

        if self.permutation is not None:
            orders = [self.state.orders[b] for b in self.permutation]

        generator = self.task_generator(orders)

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
        drone = self.find_best_drone(order, product_id, n)
        wh = self.find_best_warehouse(order, product_id, n)
        wh.reserved[product_id] += n
        self.sim.assign_orders(drone.drone_id, [
            LoadOrder(drone.drone_id, wh.warehouse_id, product_id, n),
            DeliverOrder(drone.drone_id, order.order_id, product_id, n)
        ])

    def find_best_warehouse(self, order: CustomerOrder, product_id: int, n: int):
        warehouses = filter(lambda wh: wh.products[product_id] - wh.reserved[product_id] >= n, self.state.warehouses)
        wh = min(warehouses, key=lambda wh: self.wh_order_dist[wh.warehouse_id][order.order_id])
        return wh

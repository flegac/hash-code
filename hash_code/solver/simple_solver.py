import math

import tqdm

from hash_code.model.customer_order import CustomerOrder
from hash_code.model.orders.deliver_order import DeliverOrder
from hash_code.model.orders.load_order import LoadOrder
from hash_code.model.simulation import Simulation
from hash_code.parser import Parser
from hash_code.solver.solver import Solver


class SimpleSolver(Solver):
    def __init__(self, path: str):
        super().__init__(path)
        self.sim = Parser(path).get_sim()
        self.order_id = 0

    def solve(self):
        print('solving : {}'.format(self.path))
        order_id = 0

        for _ in tqdm.tqdm(range(self.sim.deadline)):
            while len(self.sim.iddle_drones) > 0:
                if order_id >= len(self.sim.orders):
                    break
                order = self.sim.orders[order_id]
                order_id += 1
                self.plan_order(order)
            self.sim.simulate_once()

        return self.sim.score()

    def plan_order(self, order: CustomerOrder):
        drone = self.sim.iddle_drones[0]
        for product_id, n in enumerate(order.products):
            wh = find_warehouse(self.sim, product_id, n)
            if n > 0:
                max_items = math.floor((self.sim.max_load - drone.weight) // self.sim.product_weights[product_id])
                assert max_items > 0

                while n > 0:
                    k = min(n, max_items)
                    wh.reserved[product_id] += n
                    drone.orders.append(LoadOrder(drone.drone_id, wh.warehouse_id, product_id, k))
                    drone.orders.append(DeliverOrder(drone.drone_id, order.order_id, product_id, k))
                    n -= k


def find_warehouse(sim: Simulation, product_id: int, n: int):
    for wh in sim.warehouses:
        if wh.products[product_id] - wh.reserved[product_id] >= n:
            return wh
    raise ValueError()

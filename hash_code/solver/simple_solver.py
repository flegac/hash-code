import math

from hash_code.model.customer_order import CustomerOrder
from hash_code.model.drone import Drone
from hash_code.model.orders.deliver_order import DeliverOrder
from hash_code.model.orders.load_order import LoadOrder
from hash_code.model.simulation import Simulation
from hash_code.parser import Parser
from hash_code.solver.solver import Solver


class SimpleSolver(Solver):
    def solve(self, path: str):
        sim = Parser(path).get_sim()

        order_id = 0

        for step in range(sim.deadline):
            for drone in sim.iddle_drones:
                if drone.drone_id != 0:
                    continue
                try:
                    order = sim.orders[order_id]
                    order_id += 1
                    plan_order(sim, drone, order)
                except:
                    pass
            sim.simulate_once()

        return sim.score()


def plan_order(sim, drone: Drone, order: CustomerOrder):
    for product_id, n in enumerate(order.products):
        wh = find_warehouse(sim, product_id, n)
        if n > 0:
            max_items = math.floor((sim.max_load - drone.weight) // sim.product_weights[product_id])

            while n > 0:
                k = min(n, max_items)
                drone.orders.append(LoadOrder(drone.drone_id, wh.warehouse_id, product_id, k))
                drone.orders.append(DeliverOrder(drone.drone_id, order.order_id, product_id, k))
                n -= k


def find_warehouse(sim: Simulation, product_id: int, n: int):
    for wh in sim.warehouses:
        if wh.products[product_id] >= n:
            return wh
    raise ValueError()

import math
from typing import List

from hash_code.model.area import Area
from hash_code.model.customer_order import CustomerOrder
from hash_code.model.drone import Drone, DroneOrder
from hash_code.model.warehouse import Warehouse


class Simulation(object):

    def __init__(self, rows: int, columns: int, drones: int, deadline: int, max_load: int, product_weights: List[int]):
        self.deadline = deadline

        self.area = Area(rows, columns)
        self.max_load = max_load
        self.product_weights = product_weights

        self.drones = [Drone(drone_id, 0, len(self.product_weights)) for drone_id in range(drones)]
        self.warehouses: List[Warehouse] = []
        self.orders: List[CustomerOrder] = []
        self.current_time = 0

        self.deliver_warehouse = Warehouse(0, 0, [0] * len(product_weights))
        self.iddle_drone_ids = set(range(drones))

    def assign_orders(self, drone_id: int, orders: List[DroneOrder]):
        self.drones[drone_id].orders.extend(orders)
        self.iddle_drone_ids.remove(drone_id)

    @property
    def iddle_drones(self):
        return [_ for _ in self.drones if _.current_order is None]

    def deliver(self, drone: Drone, product_id: int, n: int):
        self.transfert(self.deliver_warehouse, drone, product_id, -n)

    def transfert(self, warehouse: Warehouse, drone: Drone, product_id: int, n: int):
        assert warehouse.products[product_id] - n >= 0
        assert drone.products[product_id] + n >= 0
        assert drone.weight + self.product_weights[product_id] * n <= self.max_load

        drone.products[product_id] += n
        warehouse.products[product_id] -= n
        warehouse.reserved[product_id] -= n

        drone.weight += self.product_weights[product_id] * n

    def create_warehouse(self, r: int, c: int, products: List[int]):
        assert len(products) == len(products)

        warehouse_id = len(self.warehouses)
        cell_id = self.area.cell((r, c))
        self.warehouses.append(Warehouse(warehouse_id, cell_id, products))

        if warehouse_id == 0:
            for _ in self.drones:
                _.cell_id = cell_id

    def create_order(self, r: int, c: int, product_ids: List[int]):
        order_id = len(self.orders)

        products = [0] * len(self.product_weights)
        for product_id in product_ids:
            products[product_id] += 1
        cell_id = self.area.cell((r, c))
        self.orders.append(CustomerOrder(order_id, cell_id, products))

    def score(self):
        return sum([self.order_score(_) for _ in self.orders])

    def order_score(self, order: CustomerOrder):
        if order.completion_time is None:
            return 0
        return math.ceil(100 * (self.deadline - order.completion_time) / self.deadline)

    def simulate_once(self):
        for drone in self.drones:
            order = drone.current_order
            if order:
                order.execute(self)
            else:
                self.iddle_drone_ids.add(drone.drone_id)
        self.current_time += 1

    def simulate(self):
        for _ in range(self.deadline):
            self.simulate_once()

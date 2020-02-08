import math
from dataclasses import dataclass, field
from typing import List

from hash_code.model.area import Area, Point
from hash_code.model.customer_order import CustomerOrder
from hash_code.model.drone import Drone
from hash_code.model.warehouse import Warehouse


@dataclass
class State:
    name: str
    deadline: int
    area: Area
    drone_number: int
    product_weights: List[int]
    max_load: int
    current_time: int = 0
    drones: List[Drone] = field(init=False)
    warehouses: List[Warehouse] = field(init=False)
    orders: List[CustomerOrder] = field(init=False)
    _deliver_warehouse: Warehouse = field(init=False)

    def __post_init__(self):
        self.drones = [Drone(drone_id, Point(), len(self.product_weights)) for drone_id in range(self.drone_number)]
        self.warehouses: List[Warehouse] = []
        self.orders: List[CustomerOrder] = []
        self._deliver_warehouse = Warehouse(0, Point(), [0] * len(self.product_weights))

    def deliver(self, drone: Drone, product_id: int, n: int):
        self.transfert(self._deliver_warehouse, drone, product_id, -n)


    def transfert(self, warehouse: Warehouse, drone: Drone, product_id: int, n: int):
        assert warehouse.products[product_id] - n >= 0
        assert drone.products[product_id] + n >= 0
        assert drone.weight + self.product_weights[product_id] * n <= self.max_load

        drone.products[product_id] += n
        warehouse.products[product_id] -= n
        warehouse.reserved[product_id] -= n
        drone.weight += self.product_weights[product_id] * n

    def create_warehouse(self, r: int, c: int, products: List[int]):
        assert len(products) == len(self.product_weights)

        warehouse_id = len(self.warehouses)
        self.warehouses.append(Warehouse(warehouse_id, Point(r, c), products))

        if warehouse_id == 0:
            for _ in self.drones:
                _.cell = Point(r, c)

    def create_order(self, r: int, c: int, product_ids: List[int]):
        order_id = len(self.orders)

        products = [0] * len(self.product_weights)
        for product_id in product_ids:
            products[product_id] += 1
        cell = Point(r, c)
        self.orders.append(CustomerOrder(order_id, cell, products))

    def order_score(self, order: CustomerOrder):
        if order.completion_time is None:
            return 0
        return math.ceil(100 * (self.deadline - order.completion_time) / self.deadline)

    def score(self):
        return sum([self.order_score(_) for _ in self.orders])

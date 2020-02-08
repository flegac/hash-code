import abc
from dataclasses import dataclass, field
from typing import List

from hash_code.model.area import Point, Area


@dataclass
class DroneOrder(abc.ABC):
    drone_id: int
    is_done: bool = field(init=False)
    _fly_time: int = field(init=False)

    def __post_init__(self):
        self.is_done = False
        self._fly_time = None

    def execute(self, state):
        raise ValueError()

    def mark_as_done(self):
        self.is_done = True

    @property
    def remaining_time(self):
        return self._fly_time

    def fly_to(self, state, cell: Point) -> bool:
        drone = state.drones[self.drone_id]

        if self._fly_time is None:
            self._fly_time = Area.dist(drone.cell, cell)

        if self._fly_time > 0:
            self._fly_time -= 1
            return False

        drone.cell = cell
        return True

    def export(self) -> str:
        raise ValueError()


@dataclass
class Drone(object):
    drone_id: int
    cell: Point
    product_number: int
    products: List[int] = field(init=False)
    weight: int = 0
    order_queue: List[DroneOrder] = field(init=False)
    current_order_id: int = 0

    def __post_init__(self):
        self.products = [0] * self.product_number
        self.order_queue = []

    def update(self, state) -> bool:
        order = self.current_order
        if order:
            order.execute(state)
            if order.is_done:
                self.current_order_id += 1
        return self.current_order is None

    def give_order(self, order: DroneOrder):
        self.order_queue.append(order)

    @property
    def current_order(self):
        try:
            return self.order_queue[self.current_order_id]
        except:
            return None

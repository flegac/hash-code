import abc
from dataclasses import dataclass, field
from typing import List

from hash_code.model.area import Point, Area


class DroneOrder(abc.ABC):
    def __init__(self, drone_id: int):
        self.drone_id = drone_id
        self._done = False
        self._fly_time = None

    def execute(self, state):
        raise ValueError()

    def mark_as_done(self):
        self._done = True

    @property
    def is_done(self):
        return self._done

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
    order_history: List[DroneOrder] = field(init=False)

    def __post_init__(self):
        self.products = [0] * self.product_number
        self.order_queue = []
        self.order_history = []

    def update(self, state) -> bool:
        order = self.current_order
        if order:
            order.execute(state)
            if order.is_done:
                self.order_queue.pop(0)
                self.order_history.append(order)
        return self.current_order is None

    def give_order(self, order: DroneOrder):
        self.order_queue.append(order)

    @property
    def current_order(self):
        try:
            return self.order_queue[0]
        except IndexError:
            return None

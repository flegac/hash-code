import abc
from typing import List


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

    def fly_to(self, state, cell_id: int) -> bool:
        drone = state.drones[self.drone_id]

        if self._fly_time is None:
            self._fly_time = state.area.dist(drone.cell_id, cell_id)

        if self._fly_time > 0:
            self._fly_time -= 1
            return False

        drone.cell_id = cell_id
        return True

    def export(self) -> str:
        raise ValueError()


class Drone(object):
    def __init__(self, drone_id, cell_id: int, product_number: int):
        self.drone_id = drone_id
        self.cell_id = cell_id
        self.products = [0] * product_number
        self.weight = 0

        self.order_queue: List[DroneOrder] = []
        self.order_history: List[DroneOrder] = []

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

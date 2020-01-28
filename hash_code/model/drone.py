import abc
from typing import List


class DroneOrder(abc.ABC):
    def __init__(self, drone_id: int):
        self.drone_id = drone_id
        self._done = False
        self._fly_time = None

    def execute(self, sim):
        raise ValueError()

    def mark_as_done(self):
        self._done = True

    @property
    def is_done(self):
        return self._done

    def fly_to(self, sim, cell_id: int) -> bool:
        # print('{} fly to {}'.format(self.drone_id, cell_id))
        drone = sim.drones[self.drone_id]

        if self._fly_time is None:
            self._fly_time = sim.area.dist(drone.cell_id, cell_id)

        if self._fly_time > 0:
            self._fly_time -= 1
            return False

        drone.cell_id = cell_id
        return True


class Drone(object):
    def __init__(self, drone_id, cell_id: int, product_number: int):
        self.drone_id = drone_id
        self.cell_id = cell_id
        self.products = [0] * product_number
        self.orders: List[DroneOrder] = []
        self.weight = 0
        self.current_order_id = 0

    @property
    def current_order(self):
        for _ in self.orders[self.current_order_id:]:
            if not _.is_done:
                return _
            else:
                self.current_order_id += 1
        return None

from dataclasses import dataclass, field
from typing import List, Set

from hash_code.model.drone import DroneOrder
from hash_code.model.state import State


@dataclass
class Simulator:
    state: State
    _idle_drones: Set[int] = field(init=False)

    def __post_init__(self, ):
        self._idle_drones = set([_.drone_id for _ in self.state.drones if _.current_order])

    def simulate(self):
        assert self.state.current_time < self.state.deadline
        for drone in self.state.drones:
            is_iddle = drone.update(self.state)
            if is_iddle:
                self.mark_as_iddle(drone.drone_id)
        self.state.current_time += 1

    @property
    def idle_drones(self):
        return [self.state.drones[_] for _ in sorted(self._idle_drones)]

    def mark_as_iddle(self, drone_id: int):
        self._idle_drones.add(drone_id)

    def assign_orders(self, drone_id: int, orders: List[DroneOrder]):
        for order in orders:
            self.state.drones[drone_id].give_order(order)
        self._idle_drones.discard(drone_id)

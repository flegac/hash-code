from dataclasses import dataclass, field
from typing import List, Dict

from hash_code.model.area import Point


@dataclass
class Task:
    cell: Point
    product_id: int
    quantity: int
    completion_time: int = None
    delivered: int = 0

    def deliver(self, quantity: int, current_time: int):
        self.delivered += quantity
        if self.delivered >= self.quantity:
            self.completion_time = current_time


@dataclass
class CustomerOrder:
    order_id: int
    cell: Point
    tasks: List[Task]
    task_by_product: Dict[int, Task] = field(init=False)

    def __post_init__(self):
        self.task_by_product = {
            _.product_id: _
            for _ in self.tasks
        }

    def deliver(self, product_id: int, quantity: int, current_time: int):
        self.task_by_product[product_id].deliver(quantity, current_time)

    @property
    def completion_time(self):
        try:
            return max([_.completion_time for _ in self.tasks])
        except:
            return None

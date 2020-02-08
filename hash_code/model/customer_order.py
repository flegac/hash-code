from dataclasses import dataclass, field
from typing import List

from hash_code.model.area import Point


@dataclass
class CustomerOrder:
    order_id: int
    cell: Point
    products: List[int]
    completion_time: int = None
    delivered: List[int] = field(init=False)

    def __post_init__(self):
        self.delivered = [0] * len(self.products)

    def deliver(self, product_id: int, quantity: int, current_time: int):
        self.delivered[product_id] += quantity
        for _ in range(len(self.products)):
            if self.products[_] > self.delivered[_]:
                return
        self.completion_time = current_time

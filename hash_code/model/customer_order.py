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

    def is_done(self):
        for _ in range(len(self.products)):
            if self.products[_] < self.delivered[_]:
                return False
        return True

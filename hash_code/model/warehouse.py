from dataclasses import dataclass, field
from typing import List

from hash_code.model.area import Point


@dataclass
class Warehouse:
    warehouse_id: int
    cell: Point
    products: List[int]
    reserved: List[int] = field(init=False)

    def __post_init__(self):
        self.reserved = [0] * len(self.products)

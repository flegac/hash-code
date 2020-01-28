from typing import List


class Warehouse(object):
    def __init__(self, warehouse_id: int, cell_id: int, products: List[int]):
        self.warehouse_id = warehouse_id
        self.cell_id = cell_id
        self.products = products
        self.reserved = [0] * len(products)

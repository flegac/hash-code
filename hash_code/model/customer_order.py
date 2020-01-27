from typing import List


class CustomerOrder(object):
    def __init__(self, order_id: int, cell_id: int, products: List[int]):
        self.order_id = order_id
        self.cell_id = cell_id
        self.products = products
        self.completion_time = None
        self.delivered = [0] * len(products)

    def is_done(self):
        for _ in range(len(self.products)):
            if self.products[_] < self.delivered[_]:
                return False
        return True

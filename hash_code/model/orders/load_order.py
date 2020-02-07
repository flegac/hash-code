from hash_code.model.drone import DroneOrder


class LoadOrder(DroneOrder):
    def __init__(self, drone_id: int, warehouse_id: int, product_id: int, n: int):
        super().__init__(drone_id)
        self.n = n
        self.product_id = product_id
        self.warehouse_id = warehouse_id

    def execute(self, state):
        drone = state.drones[self.drone_id]
        wh = state.warehouses[self.warehouse_id]

        if not self.fly_to(state, wh.cell):
            return

        state.transfert(wh, drone, self.product_id, self.n)
        self.mark_as_done()

    def export(self):
        return '{} L {} {} {}'.format(self.drone_id, self.warehouse_id, self.product_id, self.n)

from hash_code.model.drone import DroneOrder

from hash_code.model.simulation import Simulation


class LoadOrder(DroneOrder):
    def __init__(self, drone_id: int, warehouse_id: int, product_id: int, n: int):
        super().__init__(drone_id)
        self.n = n
        self.product_id = product_id
        self.warehouse_id = warehouse_id

    def execute(self, sim: Simulation):
        drone = sim.drones[self.drone_id]
        wh = sim.warehouses[self.warehouse_id]

        if not self.fly_to(sim, wh.cell_id):
            return

        sim.transfert(wh, drone, self.product_id, self.n)
        self.mark_as_done()

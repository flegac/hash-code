from hash_code.model.drone import DroneOrder
from hash_code.model.simulation import Simulation


class DeliverOrder(DroneOrder):
    def __init__(self, drone_id: int, order_id: int, product_id: int, n: int):
        super().__init__(drone_id)
        self.n = n
        self.product_id = product_id
        self.order_id = order_id

    def execute(self, sim: Simulation):
        drone = sim.drones[self.drone_id]
        order = sim.orders[self.order_id]
        assert drone.products[self.product_id] >= self.n

        if not self.fly_to(sim, order.cell_id):
            return

        sim.deliver(drone, self.product_id, self.n)

        order.delivered[self.product_id] += self.n
        if order.is_done():
            order.completion_time = sim.current_time
        self.mark_as_done()

from dataclasses import dataclass

from hash_code.model.drone import DroneOrder


@dataclass
class DeliverOrder(DroneOrder):
    drone_id: int
    order_id: int
    product_id: int
    quantity: int

    def execute(self, state):
        drone = state.drones[self.drone_id]
        order = state.orders[self.order_id]
        assert drone.products[self.product_id] >= self.quantity

        if not self.fly_to(state, order.cell):
            return

        state.deliver(drone, self.product_id, self.quantity)
        order.deliver(self.product_id, self.quantity, state.current_time)

        self.mark_as_done()

    def export(self):
        return '{} D {} {} {}'.format(self.drone_id, self.order_id, self.product_id, self.quantity)

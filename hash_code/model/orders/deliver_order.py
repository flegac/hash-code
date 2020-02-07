from hash_code.model.drone import DroneOrder


class DeliverOrder(DroneOrder):
    def __init__(self, drone_id: int, order_id: int, product_id: int, n: int):
        super().__init__(drone_id)
        self.order_id = order_id
        self.product_id = product_id
        self.n = n

    def execute(self, state):
        drone = state.drones[self.drone_id]
        order = state.orders[self.order_id]
        assert drone.products[self.product_id] >= self.n

        if not self.fly_to(state, order.cell):
            return

        state.deliver(drone, self.product_id, self.n)

        order.delivered[self.product_id] += self.n
        if order.is_done():
            order.completion_time = state.current_time
        self.mark_as_done()

    def export(self):
        return '{} D {} {} {}'.format(self.drone_id, self.order_id, self.product_id, self.n)

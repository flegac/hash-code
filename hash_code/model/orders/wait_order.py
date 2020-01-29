from hash_code.model.drone import DroneOrder


class WaitOrder(DroneOrder):
    def __init__(self, drone_id: int, wait_time: int):
        super().__init__(drone_id)
        self.wait_time = wait_time

    def execute(self, state):
        self.wait_time -= 1
        if self.wait_time == 0:
            self.mark_as_done()

    def export(self):
        return '{} W {}'.format(self.drone_id, self.wait_time)

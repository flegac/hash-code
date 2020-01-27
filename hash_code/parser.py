from hash_code.model.simulation import Simulation


def read_int(fd):
    return int(fd.readline())


def read_pair(fd):
    return [int(item) for item in fd.readline().split(' ')]


def read_list(fd, with_size: bool = False):
    if with_size:
        n = read_int(fd)
        data = [int(item) for item in fd.readline().split(' ')]
        assert len(data) == n
    else:
        data = [int(item) for item in fd.readline().split(' ')]
    return data


class Parser(object):
    def __init__(self, path: str):
        self.path = path

    def get_sim(self):
        with open(self.path) as _:
            simulation = self.parse_global_parameters(_)
            self.parse_warehouses(_, simulation)
            self.parse_customers(_, simulation)
        return simulation

    def parse_global_parameters(self, fd):
        # global parameters
        rows, columns, drones, deadline, max_load = read_list(fd)
        # products weights
        product_weights = read_list(fd, with_size=True)
        simulation = Simulation(rows, columns, drones, deadline, max_load, product_weights)
        return simulation

    def parse_warehouses(self, fd, simulation):
        W = read_int(fd)
        for i in range(W):
            r, c = read_pair(fd)
            products = read_list(fd)
            simulation.create_warehouse(r, c, products)

    def parse_customers(self, fd, simulation):
        C = read_int(fd)
        for i in range(C):
            r, c = read_pair(fd)
            product_ids = read_list(fd, with_size=True)
            simulation.create_order(r, c, product_ids)

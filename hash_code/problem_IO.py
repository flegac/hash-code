import os

from typing.io import TextIO

from hash_code.model.area import Area
from hash_code.model.orders.deliver_order import DeliverOrder
from hash_code.model.orders.load_order import LoadOrder
from hash_code.model.orders.unload_order import UnloadOrder
from hash_code.model.orders.wait_order import WaitOrder
from hash_code.model.state import State


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


class ProblemIO(object):
    @staticmethod
    def parse_input(path: str):
        with open(path) as fd:
            name = os.path.basename(path)
            rows, columns, drone_number, deadline, max_load = read_list(fd)
            product_weights = read_list(fd, with_size=True)
            state = State(name, deadline, Area(rows, columns), drone_number, product_weights, max_load)

            parse_warehouses(fd, state)
            parse_customers(fd, state)
        return state

    @staticmethod
    def parse_output(state: State, path: str):
        with open(path) as fd:
            line_number = int(fd.readline())
            for _ in range(line_number):
                line = fd.readline().split()
                if line[1] == 'D':
                    order = DeliverOrder(int(line[0]), int(line[2]), int(line[3]), int(line[4]))
                elif line[1] == 'L':
                    order = LoadOrder(int(line[0]), int(line[2]), int(line[3]), int(line[4]))
                elif line[1] == 'U':
                    order = UnloadOrder(int(line[0]), int(line[2]), int(line[3]), int(line[4]))
                elif line[1] == 'W':
                    order = WaitOrder(int(line[0]), int(line[2]))
                else:
                    raise ValueError()
                state.drones[order.drone_id].order_queue.append(order)

    @staticmethod
    def export(path: str, state: State):
        line_number = sum([len(drone.order_queue) for drone in state.drones])
        with open('{}_{}'.format(path, state.score()), 'w') as fd:
            fd.write('{}\n'.format(line_number))
            for drone in state.drones:
                lines = [_.export() + '\n' for _ in drone.order_queue]
                fd.writelines(lines)


def parse_parameters(name, fd: TextIO):
    rows, columns, drone_number, deadline, max_load = read_list(fd)
    product_weights = read_list(fd, with_size=True)
    state = State(name, deadline, Area(rows, columns), drone_number, product_weights, max_load)
    return state


def parse_warehouses(fd: TextIO, state: State):
    W = read_int(fd)
    for i in range(W):
        r, c = read_pair(fd)
        products = read_list(fd)
        state.create_warehouse(r, c, products)


def parse_customers(fd: TextIO, state: State):
    C = read_int(fd)
    for i in range(C):
        r, c = read_pair(fd)
        product_ids = read_list(fd, with_size=True)
        state.create_order(r, c, product_ids)

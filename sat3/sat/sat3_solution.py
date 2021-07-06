import numpy as np


class Sat3Solution:
    def __init__(self, n_vars: int):
        self.values = np.zeros(n_vars, dtype=bool)

    def switch(self, vid: int):
        self.values[vid] = not self.values[vid]

    def randomize(self):
        self.values = np.random.random(self.values.shape) > .5
        return self

    def __str__(self):
        return f'{self.values}'

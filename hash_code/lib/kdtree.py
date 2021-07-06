import logging

import numpy as np
from codetiming import Timer
from scipy.spatial import cKDTree

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.cKDTree.html#scipy.spatial.cKDTree
def coucou():
    shape = (5_000_000, 2)
    data = np.random.random(shape) * 1_000
    data = np.round(data)

    timer = Timer(logger=logging.warning)

    with timer:
        kd = cKDTree(data)
    with timer:
        points = kd.query_ball_point(x=[1000, 1000], r=10)

    # for _ in points:
    #     print(data[_])
    print('points found :', len(points))


if __name__ == '__main__':
    coucou()

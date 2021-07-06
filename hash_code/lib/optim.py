import numpy as np
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error

X0 = np.random.random((4,))


def metric(x):
    Y = np.array([1, 5, 4, 8])
    return  mean_squared_error(x, Y)

res = minimize(
    fun=metric,
    x0=X0,
    method='SLSQP',
    bounds=(
        (None, None),
        (None, None),
        (None, None),
        (None, None),
    ),
    # constraints={'type': 'eq', 'fun': lambda x: 0},
    tol=1e-10
)
print (res)

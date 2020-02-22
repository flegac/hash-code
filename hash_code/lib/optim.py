import numpy as np
from scipy.optimize import minimize, LinearConstraint
from sklearn.metrics import mean_squared_error

from hash_code.optimizer import Optimizer
from hash_code.problem import Problem
from hash_code.solution import Solution

X0 = np.random.random((4,))
def metric(x):
    Y = np.array([1, 5, 4, 8])
    return mean_squared_error(x, Y)


cons = (
    LinearConstraint(A=np.array([1, 100, 1, 1]),
                     lb=-100,
                     ub=100),
    # {'type': 'ineq', 'fun': lambda x: x[0] - 2 * x[1] + 2},
    # {'type': 'ineq', 'fun': lambda x: -x[0] - 2 * x[1] + 6},
    # {'type': 'ineq', 'fun': lambda x: -x[0] + 2 * x[1] + 2}
)

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
    constraints=cons,
    tol=1e-20
)
print(res)

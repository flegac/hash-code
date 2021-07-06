from hash_lib.timing import setup_timing, show_timing
from sat.sat3_problem import Sat3Problem
from sat.sat3_solver import Sat3Solver

if __name__ == '__main__':
    setup_timing()
    prob = Sat3Problem(n_vars=50, k_clauses=1000).randomize()

    solver = Sat3Solver(prob)

    solution = solver.solve(max_tries=10_000)

    res = prob.check(solution)
    print(res)
    show_timing()

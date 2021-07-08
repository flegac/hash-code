from hash_lib.timing import setup_timing, show_timing
from sat.sat_problem import SATProblem
from sat.sat_solver import SATSolver

if __name__ == '__main__':
    setup_timing()
    n = 20

    prob = SATProblem.ksat(clause_size=3, var_number=n, clause_number=10*n)
    print(prob)

    solver = SATSolver(prob)

    solution = solver.solve(max_retries=1_000)
    wrongs = prob.wrong_clauses(solution)
    print('solution', solution)
    print(f'wrongs: {wrongs}')
    show_timing()

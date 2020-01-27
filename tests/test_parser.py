import glob

from hash_code.solver.simple_solver import SimpleSolver

if __name__ == '__main__':
    solver = SimpleSolver()

    for _ in glob.glob('resources/*.in'):
        score = solver.solve(_)
        print('simulation completed ! Final score : {}'.format(score))

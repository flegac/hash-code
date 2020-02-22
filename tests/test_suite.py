import glob

from hash_code.problem import Problem
from hash_code.solution import Solution


def test_problem_parser():
    for path in glob.glob('input/*'):
        problem = Problem.parse(path)
        print(problem)


def test_solution_export():
    for path in glob.glob('fake_output/*'):
        solution = Solution.parse(path)
        solution.export('fake_export/{}.txt'.format(solution.name))


def test_score():
    problem_paths = glob.glob('fake_output/*')
    expected = {
        'fake_1': 0,
        'fake_2': 0
    }

    for i, path in enumerate(problem_paths):
        solution = Solution.parse(path)
        expected_score = expected.get(solution.name)
        score = solution.score
        print('Score : {} -> {} / {}'.format(solution.name, score, expected_score))
        assert (score == expected_score)

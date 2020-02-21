import glob

from hash_code.problem_IO import ProblemIO


def test_score():
    problem_paths = glob.glob('resources/*')
    expected = [-1] * len(problem_paths)

    for i, path in enumerate(problem_paths):
        solution = ProblemIO.parse_solution(path)
        score = solution.score
        print('Score : {} -> {}'.format(solution.name, score))
        assert (score == expected[i])

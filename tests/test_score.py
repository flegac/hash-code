import glob

from hash_code.solution import Solution


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

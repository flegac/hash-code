import random
import time
from typing import List

from hash_code.problem import Problem
from hash_code.solution import Solution


class Optimizer(object):
    def __init__(self, problem: Problem, solution: Solution):
        self.problem = problem
        self.solution = solution
        self.ref_score = problem.score(solution)
        self.best_solution = solution
        self.best_score = self.ref_score

    def optimize(self, duration: float = 2):
        if duration <= 0:
            return self.solution

        library_order, books_order = self.init(self.solution)

        end_time = time.time() + duration
        iterations = 0
        while time.time() < end_time:
            self.mutate(library_order)
            library_order, books_order = self.select(library_order, books_order)
            iterations += 1

        print('optimize for {duration}s : [{iterations} loops] {ref} -> {best}'.format(
            duration=duration,
            iterations=iterations,
            ref=self.ref_score,
            best=self.best_score))
        return self.best_solution

    def init(self, solution: Solution):
        library_order = list(solution.library_order)
        books_order = {
            lib_id: list(solution.books_order[lib_id])
            for lib_id in library_order
        }

        return library_order, books_order

    def select(self, library_order, books_order):
        new_solution = Solution(
            name=self.solution.name,
            library_order=tuple(library_order),
            books_order={
                lib_id: tuple(books_order[lib_id])
                for lib_id in library_order
            }
        )
        score = self.problem.score(new_solution)
        if score < self.best_score:
            return self.init(self.best_solution)

        self.best_score = score
        self.best_solution = new_solution
        return library_order, books_order

    def mutate(self, permutation: List[int], i: int = None, j: int = None):
        n = len(permutation)
        if n == 0:
            return
        if i is None:
            i = random.randint(0, n - 1)
        i = i % n
        if j is None:
            j = i + 1
        j = j % n
        permutation[i], permutation[j] = permutation[j], permutation[i]

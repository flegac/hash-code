import random
from dataclasses import dataclass
from typing import List, Iterable, Generic, Type

import numpy as np

from hash_code.optimizer import Optimizer
from hash_code.problem import Problem
from hash_code.solution import Solution
from hash_code.utils import find_best_solution


class SimpleSolver(Solver):
    def __init__(self, problem: Problem):
        self.problem = problem
        self.book_max_score = max(self.problem.book_scores)

        self.book_to_lib: List[List[int]] = [list() for _ in range(problem.book_number)]
        for lib in self.problem.libraries:
            for book_id in lib.books:
                self.book_to_lib[book_id].append(lib.lib_id)

        self.book_max_avail = max(len(_) for _ in self.book_to_lib)

    # ----- SOLVER -------------------------------------------------------------------
    def solve(self) -> Solution:
        problem = self.problem

        library_order = [_.lib_id for _ in problem.libraries]
        library_order = sorted(library_order, key=self.library_score, reverse=True)

        books_order = self.map_book_to_libs(library_order)

        library_order = tuple(filter(lambda _: len(books_order[_]) > 0, library_order))

        solution = Solution(
            name=problem.name,
            library_order=library_order,
            books_order=books_order
        )
        problem.check(solution)
        new_solution = Optimizer(problem, solution).optimize(2)
        return new_solution

    # --------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------

    def map_book_to_libs(self, library_order: Iterable[int]):
        books_order = {
            _: []
            for _ in library_order
        }

        print('mapping books to libraries')

        def transform(books):
            return books

        # if self.book_max_avail > 1:
        #     def transform(books):
        #         return list(sorted(books, key=self.library_score, reverse=False))
        book_to_lib = [transform(_) for _ in self.book_to_lib]

        available_libraries = set(library_order)

        for book_id in sorted(range(self.problem.book_number), key=self.book_score, reverse=True):
            libraries = list(available_libraries.intersection(book_to_lib[book_id]))
            if len(libraries) > 0:
                lib_id = random.choice(libraries)
                books_order[lib_id].append(book_id)

        return {
            _: tuple(books_order[_])
            for _ in books_order
        }

    def book_score(self, book_id):
        score = self.problem.book_scores[book_id] / self.book_max_score
        avail = (len(self.book_to_lib[book_id]) / self.book_max_avail)
        return score * score  # - avail * avail

    def library_score(self, lib_id: int):
        books = self.problem.libraries[lib_id].books
        score = np.max([self.book_score(_) for _ in books]) / self.book_max_score
        avail = np.min([len(self.book_to_lib[_]) for _ in books])
        return score * score * avail


class BestSolver(SimpleSolver):
    def solve(self, root_path: str = None) -> Solution:
        problem = self.problem
        _, best = find_best_solution(root_path, problem.name)
        solution = Solution.parse(best, name=problem.name)
        return Optimizer(problem, solution).optimize(2)


class RandomSolver(SimpleSolver):
    def solve(self, root_path: str = None) -> Solution:
        problem = self.problem

        libraries = list(problem.libraries)
        random.shuffle(libraries)

        books_order = {
            _.lib_id: list(_.books)
            for _ in libraries
        }
        for _ in books_order.values():
            random.shuffle(_)

        library_order = tuple(_.lib_id for _ in libraries)

        solution = Solution(
            name=problem.name,
            library_order=library_order,
            books_order=books_order
        )

        return Optimizer(problem, solution).optimize(0)

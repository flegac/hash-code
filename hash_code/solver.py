import random
from typing import List, Dict

from hash_code.problem import Problem, Library
from hash_code.solution import Solution
from hash_code.utils import find_best_solution


class Solver(object):
    def __init__(self, problem: Problem):
        self.problem = problem
        self.book_availability = [0] * self.problem.book_number
        for lib in self.problem.libraries:
            for _ in lib.library_books:
                self.book_availability[_] += 1

    # ----- SOLVER -------------------------------------------------------------------
    def solve(self, root_path: str = None) -> Solution:
        problem = self.problem

        _, best = find_best_solution(root_path, problem.name)
        try:
            solution = Solution.parse(best)
            library_scan_order = solution.library_scan_order
            books_scan_order = solution.books_scan_order
            # self.mutate(library_scan_order, n=2)
            for _, books in books_scan_order.items():
                self.mutate(books, n=2)
        except:
            libraries = problem.libraries.copy()
            # libraries = list(sorted(libraries, key=self.library_score1))
            random.shuffle(libraries)

            books_scan_order = {
                # _.lib_id: sorted(_.library_books, key=self.book_score)
                _.lib_id: _.library_books.copy()
                for _ in libraries
            }
            for _ in books_scan_order.values():
                random.shuffle(_)

            library_scan_order = [_.lib_id for _ in libraries]
            books_scan_order = self.clean_book_scan_order(library_scan_order, books_scan_order)
            library_scan_order = list(filter(lambda _: (len(books_scan_order[_]) > 0), library_scan_order))

        return Solution(
            name=problem.name,
            library_scan_order=library_scan_order,
            books_scan_order=books_scan_order
        )

    # --------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------

    def book_score(self, book_id):
        return - self.problem.book_scores[book_id]

    def library_score(self, lib: Library):
        return sum(self.problem.book_scores[_] for _ in lib.library_books)

    def library_score1(self, library: Library, signup_time: int = None):
        signup_time = signup_time or library.signup_days
        book_number = (self.problem.day_number - signup_time) * library.books_per_day
        books = library.library_books[:book_number]

        avail = sum(self.book_availability[_] for _ in books)

        return sum(self.problem.book_scores[_] for _ in books) - avail

    def mutate(self, permutation: List[int], n: int = 1):
        for _ in range(n):
            i = random.randint(0, len(permutation) - 1)
            j = random.randint(0, len(permutation) - 1)
            # i = random.randint(0, len(permutation) // 2)
            # j = random.randint(0, len(permutation) // 2)
            # i = random.randint(len(permutation) // 2, len(permutation) - 1)
            # j = random.randint(len(permutation) // 2, len(permutation) - 1)
            permutation[i], permutation[j] = permutation[j], permutation[i]

    def clean_book_scan_order(self, library_scan_order: List[int], books_scan_order: Dict[int, List[int]]):
        problem = self.problem
        remaining_time = problem.day_number
        scanned_books = set()

        for lib_id in library_scan_order:
            lib = problem.libraries[lib_id]
            remaining_time -= lib.signup_days
            if remaining_time <= 0:
                break
            book_number = remaining_time * lib.books_per_day
            books = set(books_scan_order[lib_id])
            books.difference_update(scanned_books)
            books = sorted(books, key=self.book_score)
            books_scan_order[lib_id] = books[:book_number]
            scanned_books.update(books)

        return books_scan_order

import os
from dataclasses import dataclass, field
from typing import List, Dict

from hash_code.problem import Problem
from hash_code.utils import read, write


@dataclass(frozen=True)
class Solution:
    name: str
    library_scan_order: List[int] = field(repr=False)
    books_scan_order: Dict[int, List[int]] = field(repr=False)

    # ----- EXPORT -------------------------------------------------------------------
    def export(self, path: str):
        with open(path, 'w') as fd:
            write(fd, len(self.library_scan_order))
            for lib_id in self.library_scan_order:
                books = self.books_scan_order[lib_id]
                assert len(books) > 0
                write(fd, [lib_id, len(books)])
                write(fd, books)

    # ----- OPTIONAL -----------------------------------------------------------------
    # --------------------------------------------------------------------------------
    def check(self, problem: Problem):
        for lib_id in self.library_scan_order:
            books = set(self.books_scan_order[lib_id])
            ref_books = problem.libraries[lib_id].library_books
            assert books.issubset(ref_books)

    # ----- SCORE : IMPORTANT !! -----------------------------------------------------
    def score(self, problem: Problem):
        remaining_time = problem.day_number
        scanned_books = set()
        for lib_id in self.library_scan_order:
            lib = problem.libraries[lib_id]
            remaining_time -= lib.signup_days
            if remaining_time <= 0:
                break
            book_number = remaining_time * lib.books_per_day
            books = self.books_scan_order[lib_id][:book_number]
            scanned_books.update(books)

        return sum([problem.book_scores[_] for _ in scanned_books])

    # ----- PARSING ------------------------------------------------------------------
    @staticmethod
    def parse(path: str) -> 'Solution':
        name, _ = os.path.splitext(os.path.basename(path))
        with open(path) as fd:
            lib_number = read(fd)[0]
            library_scan_order = [0] * lib_number
            books_scan_order = [[0]] * lib_number
            for i in range(lib_number):
                lib_id, _ = read(fd)
                books = read(fd)
                library_scan_order[i] = lib_id
                books_scan_order[lib_id] = books

        return Solution(
            name=name,
            library_scan_order=library_scan_order,
            books_scan_order=books_scan_order
        )

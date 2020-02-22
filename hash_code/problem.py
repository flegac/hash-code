import os
from dataclasses import dataclass, field
from typing import Tuple

from hash_code.solution import Solution
from hash_code.utils import read


@dataclass(frozen=True)
class Library:
    lib_id: int
    signup_days: int
    books_per_day: int
    books: Tuple[int] = field(repr=False)

    @property
    def book_number(self):
        return len(self.books)


@dataclass(frozen=True)
class Problem:
    name: str
    book_number: int
    library_number: int
    day_number: int
    book_scores: Tuple[int] = field(repr=False)
    libraries: Tuple[Library] = field(repr=False)

    # ----- PARSING ------------------------------------------------------------------
    @staticmethod
    def parse(path: str) -> 'Problem':
        name, _ = os.path.splitext(os.path.basename(path))
        with open(path) as fd:
            book_number, library_number, day_number = read(fd)
            book_scores = read(fd)
            libraries = []
            for lib_id in range(library_number):
                _, signup_days, books_per_day = read(fd)
                books = read(fd)
                libraries.append(Library(
                    lib_id=lib_id,
                    signup_days=signup_days,
                    books_per_day=books_per_day,
                    books=tuple(books)))

        return Problem(
            name=name,
            book_number=book_number,
            library_number=library_number,
            day_number=day_number,
            book_scores=book_scores,
            libraries=tuple(libraries)
        )

    # ----- CHECK SOLUTION -----------------------------------------------------------
    def check(self, solution: Solution):
        registered_book = set()

        for lib_id in solution.library_order:
            books = solution.books_order[lib_id]
            ref_books = self.libraries[lib_id].books
            assert all(self.book_scores[books[i]] >= self.book_scores[books[i + 1]] for i in range(len(books) - 1))
            assert set(books).issubset(ref_books)
            assert len(books) > 0
            assert set(books).isdisjoint(registered_book)

    # ----- SCORE SOLUTION -----------------------------------------------------------
    def score(self, solution: Solution):
        remaining_time = self.day_number
        scanned_books = set()
        for lib_id in solution.library_order:
            lib = self.libraries[lib_id]
            remaining_time -= lib.signup_days
            if remaining_time <= 0:
                break
            book_number = remaining_time * lib.books_per_day
            books = solution.books_order[lib_id][:book_number]
            scanned_books.update(books)

        return sum([self.book_scores[_] for _ in scanned_books])

    # ----- MAX SCORE ----------------------------------------------------------------
    @property
    def max_score(self):
        return sum(self.book_scores)

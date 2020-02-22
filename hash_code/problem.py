import os
from dataclasses import dataclass, field
from typing import List

from hash_code.utils import read


@dataclass(frozen=True)
class Library:
    lib_id: int
    signup_days: int
    books_per_day: int
    library_books: List[int] = field(repr=False)


@dataclass(frozen=True)
class Problem:
    name: str
    book_number: int
    library_number: int
    day_number: int
    book_scores: List[int] = field(repr=False)
    libraries: List[Library] = field(repr=False)

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
                library_books = read(fd)
                libraries.append(Library(
                    lib_id=lib_id,
                    signup_days=signup_days,
                    books_per_day=books_per_day,
                    library_books=library_books))

        return Problem(
            name=name,
            book_number=book_number,
            library_number=library_number,
            day_number=day_number,
            book_scores=book_scores,
            libraries=libraries
        )

    # ----- MAX SCORE ----------------------------------------------------------------
    @property
    def max_score(self):
        return sum(self.book_scores)

import os
from dataclasses import dataclass, field
from typing import Dict, Tuple

from hash_code.utils import read, write


@dataclass(frozen=True)
class Solution:
    name: str
    library_order: Tuple[int] = field(repr=False)
    books_order: Dict[int, Tuple[int]] = field(repr=False)

    # ----- EXPORT -------------------------------------------------------------------
    def export(self, path: str):
        registered_book = set()
        with open(path, 'w') as fd:
            write(fd, len(self.library_order))
            for lib_id in self.library_order:
                books = self.books_order[lib_id]
                assert len(books) > 0
                assert set(books).isdisjoint(registered_book)
                registered_book.update(books)
                write(fd, [lib_id, len(books)])
                write(fd, books)

    # ----- PARSING ------------------------------------------------------------------
    @staticmethod
    def parse(path: str, name: str = None) -> 'Solution':
        if name is None:
            name, _ = os.path.splitext(os.path.basename(path))
        with open(path) as fd:
            lib_number = read(fd)[0]
            library_order = [0] * lib_number
            books_order = dict()
            for i in range(lib_number):
                lib_id, _ = read(fd)
                books = read(fd)
                library_order[i] = lib_id
                books_order[lib_id] = tuple(books)

        return Solution(
            name=name,
            library_order=tuple(library_order),
            books_order=books_order
        )

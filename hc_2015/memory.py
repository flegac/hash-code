from dataclasses import dataclass

import cv2
import numpy as np


@dataclass
class MemPage:
    row: int
    first: int
    size: int

    def alloc(self, size: int):
        self.size -= size
        return MemPage(row=self.row, first=self.size, size=size)

    @property
    def end(self):
        return self.first + self.size


class Memory:
    def __init__(self, raw: np.ndarray):
        self.raw = raw
        self.free_pages = [
            self.compute_memory(row)
            for row in range(raw.shape[0])
        ]

    def row_free_space(self, row: int):
        pages = self.free_pages[row]
        return sum([page.size for page in pages])

    def alloc(self, row: int, size: int):
        free = self.free_pages[row]
        for i, page in enumerate(free):
            if page.size >= size:
                new_page = page.alloc(size)
                free.append(new_page)
                self._page_array(new_page)[:] = False
                free.sort(key=lambda p: p.size)
                return new_page
        raise ValueError(f'Could not allocate page of size {size} on row {row}!')

    def free(self, page: MemPage):
        raise NotImplemented

    def _page_array(self, page: MemPage):
        return self.raw[page.row, page.first:page.end]

    def compute_memory(self, row: int):
        free = self.raw[row]
        indices = np.where(np.diff(free, prepend=np.nan))[0]
        indices = list(indices) + [len(free)]
        res = []
        for i in range(len(indices) - 1):
            a = indices[i]
            b = indices[i + 1]
            if free[a]:
                res.append(MemPage(row=row, first=a, size=b - a))
        res = list(sorted(res, key=lambda page: page.size))
        return res

    def dump(self):
        buffer = self.raw.astype('uint8') * 255
        cv2.imwrite('assigned.png', buffer)

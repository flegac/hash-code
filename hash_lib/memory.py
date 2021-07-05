from dataclasses import dataclass
from typing import List

import cv2
import numpy as np


@dataclass(order=True, frozen=True)
class MemPage:
    mem_id: int
    offset: int
    size: int


    @staticmethod
    def empty():
        return MemPage(mem_id=-1, offset=-1, size=-1)

    def alloc(self, size: int, offset: int = None):
        offset = offset or self.end - size
        new = MemPage(mem_id=self.mem_id, offset=offset, size=size)
        olds = [
            MemPage(mem_id=self.mem_id, offset=self.offset, size=offset - self.offset),
            MemPage(mem_id=self.mem_id, offset=offset + size, size=self.end - offset - size),
        ]
        return olds, new

    @property
    def end(self):
        return self.offset + self.size

    def __repr__(self):
        return f'M{self.mem_id}(:{self.offset}:{self.size})'


class Memory:
    def __init__(self, mem_id: int, size: int):
        self.mem_id = mem_id
        self.alloc_strategy = lambda mem: mem.size
        self.memory = np.zeros(size)
        self.free_memory: List[MemPage] = [MemPage(mem_id, 0, size)]
        self.allocated: List[MemPage] = []

    def free_space(self):
        res = sum([page.size for page in self.free_memory])
        return res

    def force_alloc(self, offset: int, size: int):
        matching = list(filter(lambda mem: mem.offset <= offset and mem.end > offset + size, self.free_memory))
        assert len(matching) == 1
        page = min(matching, key=self.alloc_strategy)
        olds, new = page.alloc(size, offset)

        if new:
            self.free_memory.remove(page)
            for old in olds:
                if old.size > 0:
                    self.free_memory.append(old)
            self.allocated.append(new)
            self._page_array(new)[:] = 1
            return new

        raise ValueError(f'Could not allocate page of size {size} on mem_id {self.mem_id}!')

    def alloc(self, size: int):
        matching = list(filter(lambda mem: mem.size >= size, self.free_memory))
        if len(matching) > 0:
            page = min(matching, key=self.alloc_strategy)
            olds, new = page.alloc(size)

            if new:
                self.free_memory.remove(page)
                for old in olds:
                    if old.size > 0:
                        self.free_memory.append(old)
                self.allocated.append(new)
                self._page_array(new)[:] = 1
                return new

        raise ValueError(f'Could not allocate page of size {size} on mem_id {self.mem_id}!')

    def free(self, page: MemPage):
        assert page.mem_id == self.mem_id
        self.free_memory.append(page)
        self.allocated.remove(page)

    def _page_array(self, page: MemPage):
        return self.memory[page.offset:page.end]

    def dump(self, width: int):
        buffer = self.memory.reshape((width, self.memory.size // width)).astype('uint8') * 255
        cv2.imwrite('assigned.png', buffer)


class Memories:
    def __init__(self, rows: int, size: int):
        self.memories = [
            Memory(mem_id=row, size=size)
            for row in range(rows)
        ]

    def force_alloc(self, row: int, offset: int, size: int):
        return self.memories[row].force_alloc(offset, size)

    def free_space(self, row: int):
        return self.memories[row].free_space()

    def alloc(self, row: int, size: int):
        return self.memories[row].alloc(size)

    def free(self, page: MemPage):
        self.memories[page.mem_id].free(page)

    def dump(self):
        data = np.array([mem.memory for mem in self.memories])
        cv2.imwrite('buffer.png', data * 255)


if __name__ == '__main__':
    mem = Memory(mem_id=3, size=400)
    print(mem.free_memory, mem.allocated)

    for i in range(0, 400, 17):
        mem.force_alloc(i, 1)
        mem.dump(20)

    print(mem.free_memory, mem.allocated)

    for size in [5, 10, 15]:
        mem.alloc(size)
    print(mem.free_memory, mem.allocated)
    mem.dump(20)

import time
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass


@dataclass
class TimeEntry:
    name: str


_TIMES = defaultdict(list)

_ACTIVE = False


@contextmanager
def timing(name: str):
    if not _ACTIVE:
        yield
    else:
        start = time.time()
        yield
        total = time.time() - start
        _TIMES[name].append(total)


def show_timing():
    for k, v in _TIMES.items():
        print(f'{k}: {sum(v)}')


def setup_timing(status: bool = True):
    global _ACTIVE
    _ACTIVE = status


if __name__ == '__main__':
    setup_timing()
    with timing('toto'):
        time.sleep(.2)
    show_timing()

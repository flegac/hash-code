from dataclasses import dataclass


@dataclass(frozen=True)
class Sat3:
    n_vars: int
    k_clauses: int

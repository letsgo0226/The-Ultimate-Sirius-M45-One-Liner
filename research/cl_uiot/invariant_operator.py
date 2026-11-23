"""CL-UIOT: finite invariant-operator model (no physical ToE claim).

Exact arithmetic over complex rationals is unnecessary for this first model:
we use integer vectors and matrices, with integer group actions and
fixed-point equations. All checks are finite and deterministic.
"""
from dataclasses import dataclass
from typing import Sequence

Vector = tuple[int, ...]
Matrix = tuple[tuple[int, ...], ...]

def matvec(a: Matrix, v: Vector) -> Vector:
    if any(len(row) != len(v) for row in a):
        raise ValueError("dimension mismatch")
    return tuple(sum(x * y for x, y in zip(row, v)) for row in a)

def multiply(a: Matrix, b: Matrix) -> Matrix:
    if not b or any(len(row) != len(b[0]) for row in b):
        raise ValueError("ragged right matrix")
    return tuple(tuple(sum(aik * b[k][j] for k, aik in enumerate(row))
                       for j in range(len(b[0]))) for row in a)

def subtract(a: Matrix, b: Matrix) -> Matrix:
    if len(a) != len(b) or any(len(x) != len(y) for x, y in zip(a, b)):
        raise ValueError("matrix mismatch")
    return tuple(tuple(x-y for x, y in zip(ar, br)) for ar, br in zip(a, b))

def identity(n: int) -> Matrix:
    return tuple(tuple(int(i == j) for j in range(n)) for i in range(n))

def fixed_operator(d: Matrix, lam: int = 1) -> Matrix:
    """T = I - lambda D; lambda must be nonzero."""
    if lam == 0:
        raise ValueError("lambda must be nonzero")
    n = len(d)
    if any(len(row) != n for row in d):
        raise ValueError("D must be square")
    return tuple(tuple(int(i == j) - lam * d[i][j] for j in range(n))
                 for i in range(n))

def is_solution(d: Matrix, psi: Vector) -> bool:
    return matvec(d, psi) == (0,) * len(psi)

def is_fixed(t: Matrix, psi: Vector) -> bool:
    return matvec(t, psi) == psi

def commutes(d: Matrix, u: Matrix) -> bool:
    return multiply(d, u) == multiply(u, d)

@dataclass(frozen=True)
class FiniteInvariantModel:
    """A chosen finite example. Not a physical spacetime model."""
    d: Matrix
    group_action: Matrix
    lam: int = 1

    def check_axioms(self) -> bool:
        if not self.d or len(self.group_action) != len(self.d):
            return False
        try:
            fixed_operator(self.d, self.lam)
            return commutes(self.d, self.group_action)
        except (ValueError, IndexError):
            return False

    def solution_transports(self, psi: Vector) -> bool:
        if not self.check_axioms() or not is_solution(self.d, psi):
            return False
        return is_solution(self.d, matvec(self.group_action, psi))

def demo() -> dict:
    # D = diagonal(1,0) and U = reflection diag(-1,1).
    # Kernel(D) = {(0,y)}; U maps this kernel to itself.
    d = ((1, 0), (0, 0))
    u = ((-1, 0), (0, 1))
    model = FiniteInvariantModel(d, u, lam=2)
    points = [(x, y) for x in range(-2, 3) for y in range(-2, 3)]
    t = fixed_operator(d, 2)
    return {
        "D": d, "U": u, "T": t,
        "commutes": model.check_axioms(),
        "solutions": [v for v in points if is_solution(d, v)],
        "fixed_points": [v for v in points if is_fixed(t, v)],
        "symmetry_preserves_solutions": all(model.solution_transports(v)
                                            for v in points if is_solution(d, v)),
        "status": "bounded illustrative algebra only; no physical prediction"
    }

if __name__ == "__main__":
    import json
    print(json.dumps(demo(), sort_keys=True))

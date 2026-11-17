"""CL-UFRT: finite typed witness/fixed-point representation (research model).

A finite set of certified witnesses for proposition P is represented by Right(p)
inside P + Unit. The identity's fixed-point equation alone is vacuous as a
solution condition; a dependent solution predicate removes the Unit branch.

This is an executable finite illustration, not a theorem prover or a solver for
arbitrary mathematical problems. No third-party packages, network or secrets.
"""
from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar, Union

P = TypeVar("P")

@dataclass(frozen=True)
class Left:
    unit: None = None

@dataclass(frozen=True)
class Right(Generic[P]):
    witness: P

Choice = Union[Left, Right[P]]

@dataclass(frozen=True)
class SolutionFixedPoint(Generic[P]):
    point: Right[P]
    """The right injection itself carries the IsSolution certificate."""

def identity(x: Choice[P]) -> Choice[P]:
    return x

def encode(witness: P) -> SolutionFixedPoint[P]:
    """P -> {x in P + 1 | id(x)=x and IsSolution(x)}."""
    candidate = Right(witness)
    assert identity(candidate) == candidate
    return SolutionFixedPoint(candidate)

def decode(certified: SolutionFixedPoint[P]) -> P:
    """The dependent solution condition requires a Right constructor."""
    if not isinstance(certified, SolutionFixedPoint) or not isinstance(certified.point, Right):
        raise TypeError("not a certified Right witness")
    if identity(certified.point) != certified.point:
        raise AssertionError("fixed-point condition failed")
    return certified.point.witness

def verify_witness(witness: P, checker: Callable[[P], bool]) -> bool:
    """A user-supplied *decidable* predicate; not a universal proof checker."""
    return checker(decode(encode(witness))) is True

def finite_solution_fixed_points(candidates: list[P], checker: Callable[[P], bool]) -> list[SolutionFixedPoint[P]]:
    """Enumerate *supplied finite candidates*, never claim completeness beyond them."""
    return [encode(x) for x in candidates if verify_witness(x, checker)]

def demo() -> dict[str, Any]:
    # A finite example of x^2 == 4 over the explicitly enumerated integers.
    candidates = list(range(-4, 5))
    found = [decode(x) for x in finite_solution_fixed_points(candidates, lambda n: n*n == 4)]
    return {"problem": "x^2=4 over integers -4..4", "witnesses": found,
            "scope": "finite illustration, not universal solvability"}

if __name__ == "__main__":
    import json
    print(json.dumps(demo(), sort_keys=True))

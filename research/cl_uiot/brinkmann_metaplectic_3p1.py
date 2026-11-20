"""Exact normalized canonical commutator audit of metaplectic Heisenberg jets."""
from fractions import Fraction as Q
from brinkmann_symplectic_3p1 import flow_jet,J
def bracket(a,b):
    return sum(Q(a[i])*J[i][j]*Q(b[j]) for i in range(4) for j in range(4))

def commutator_jet(k,s,order):
    """Coefficients of [Z_a(u),Z_b(u)]/(i hbar) minus J_ab."""
    F=flow_jet(k,s,order)
    return [tuple(tuple(sum(bracket(F[m][a],F[n-m][b]) for m in range(n+1))
                        -(J[a][b] if n==0 else 0) for b in range(4))
                  for a in range(4)) for n in range(order+1)]

def shear(k):
    """Exact symplectic momentum kick for integrated quadratic potential."""
    k=Q(k)
    return ((1,0,0,0),(-k,1,0,0),(0,0,1,0),(0,0,k,1))

def drift(t):
    t=Q(t)
    return ((1,t,0,0),(0,1,0,0),(0,0,1,t),(0,0,0,1))

def multiply(A,B):
    return tuple(tuple(sum(A[i][r]*B[r][j] for r in range(4)) for j in range(4)) for i in range(4))

def split_step(k,t):
    t=Q(t);k=Q(k)
    S=shear(k*t/2)
    return multiply(S,multiply(drift(t),S))

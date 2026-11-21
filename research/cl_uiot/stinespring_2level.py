"""Exact two-qubit dilation with rational amplitudes."""
from fractions import Fraction as Q
from quantum_entropy_2level import density

def transpose(A):
    return tuple(zip(*A))

def mul(A,B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(len(B)))
                       for j in range(len(B[0]))) for i in range(len(A)))

def unitary(t):
    t=Q(t)
    if not 0<=t<=1:raise ValueError("parameter outside [0,1]")
    r=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
    return ((1,0,0,0),(0,r,s,0),(0,-s,r,0),(0,0,0,1))

def embed(a,b):
    R=density(a,b)
    return tuple(tuple(R[i//2][j//2] if i%2==j%2==0 else 0 for j in range(4)) for i in range(4))

def joint(a,b,t):
    U=unitary(t)
    return mul(mul(U,embed(a,b)),transpose(U))

def partial_trace(R,keep):
    if keep=="S":
        return tuple(tuple(sum(R[2*i+k][2*j+k] for k in range(2)) for j in range(2)) for i in range(2))
    if keep=="E":
        return tuple(tuple(sum(R[2*k+i][2*k+j] for k in range(2)) for j in range(2)) for i in range(2))
    raise ValueError("keep must be S or E")

def recover(R,t):
    U=unitary(t)
    return partial_trace(mul(mul(transpose(U),R),U),"S")

def purity(R):
    return sum(R[i][j]*R[j][i] for i in range(len(R)) for j in range(len(R)))

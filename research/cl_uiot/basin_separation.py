"""Exact finite-orbit basin certificates for ideal Pauli renormalization."""
from fractions import Fraction as Q
from universal_pauli import weights,bloch,evaluate

def classify(w):
    w=weights(w)
    if 1-w[0]<Q(1,10):return "identity"
    for i in range(1,4):
        if 1-w[i]<Q(1,10):return "pauli_"+"IXYZ"[i]
    if max(map(abs,bloch(w)))<=Q(1,4):return "uniform"
    return None

def uniform_bound(m):
    m=Q(m)
    if not 0<=m<=Q(1,4):raise ValueError("outside certified cube")
    # Fourier terms of total degree >=2, at most 4^5 coefficients,
    # use exact tighter bound from Parseval and Cauchy-Schwarz.
    # Sum squared monomials of degree >=2 <= sum binom(5,k)*3^k*m^(2k).
    # Instead use exact map coefficients: (10m^3+6m^5)/4.
    return (10*m**3+6*m**5)/4

def orbit(w,cap):
    w=weights(w)
    if type(cap) is not int or cap<0:raise ValueError("invalid cap")
    for n in range(cap+1):
        label=classify(w)
        if label:return {"basin":label,"steps":n,"point":w}
        if n<cap:w=evaluate(w)
    return {"basin":None,"steps":cap,"point":w}

def closed_bloch(x,y,z):
    return tuple(a*(5*b*b+5*c*c-a**4-5*b*b*c*c)/4 for a,b,c in ((x,y,z),(y,z,x),(z,x,y)))

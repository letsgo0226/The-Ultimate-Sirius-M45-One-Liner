"""Second-order pullback gauge covariance for polynomial metric perturbations."""
from fractions import Fraction as Q
from maxwell_3p1 import ETA,add,scale,mul,deriv
from linearized_einstein_3p1 import einstein_linear
from second_order_einstein_3p1 import einstein2
I=range(4)

def lie(X,T):
    return [[add(*(add(mul(X[r],deriv(T[a][b],r)),
                       mul(T[r][b],deriv(X[r],a)),
                       mul(T[a][r],deriv(X[r],b))) for r in I))
             for b in I] for a in I]

def transform(X,h,j):
    eta=[[{(0,0,0,0):Q(ETA[a])} if a==b else {} for b in I] for a in I]
    L=lie(X,eta)
    M=lie(X,h)
    N=lie(X,L)
    return ([[add(h[a][b],L[a][b]) for b in I] for a in I],
            [[add(j[a][b],M[a][b],scale(N[a][b],Q(1,2))) for b in I] for a in I])

def equation(h,j):
    return [[add(einstein_linear(j,a,b),einstein2(h,a,b)) for b in I] for a in I]

def covariance_residual(X,h,j):
    hp,jp=transform(X,h,j)
    before=equation(h,j)
    after=equation(hp,jp)
    L=lie(X,[[einstein_linear(h,a,b) for b in I] for a in I])
    return [[add(after[a][b],scale(before[a][b],-1),scale(L[a][b],-1))
             for b in I] for a in I]

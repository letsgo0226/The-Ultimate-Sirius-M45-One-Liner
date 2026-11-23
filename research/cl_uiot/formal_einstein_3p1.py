"""Finite formal power series Einstein tensor about Minkowski, exact polynomials."""
from fractions import Fraction as Q
from maxwell_3p1 import ETA,add,scale,mul,deriv
from linearized_einstein_3p1 import validate
I=range(4)

def coefficients(fields):
    """Return G coefficients from order 0 through len(fields), no factorials."""
    for h in fields: validate(h)
    N=len(fields)
    eta=[[{(0,0,0,0):Q(ETA[a])} if a==b else {} for b in I] for a in I]
    g=[eta]+list(fields)
    inv=[eta]
    for n in range(1,N+1):
        inv.append([[add(*(scale(mul(g[k][a][r],inv[n-k][r][b]),-ETA[a])
                            for k in range(1,n+1) for r in I))
                     for b in I] for a in I])
    C=[]
    for n in range(N+1):
        C.append([[[scale(add(*(mul(inv[k][r][s],
                      add(deriv(g[n-k][s][b],a),deriv(g[n-k][s][a],b),
                          scale(deriv(g[n-k][a][b],s),-1)))
                      for k in range(n+1) for s in I)),Q(1,2))
                      for b in I] for a in I] for r in I])
    R=[]
    for n in range(N+1):
        R.append([[add(*(add(deriv(C[n][r][a][b],r),
                              scale(deriv(C[n][r][a][r],b),-1)) for r in I),
                         *(add(mul(C[k][r][r][s],C[n-k][s][a][b]),
                               scale(mul(C[k][r][b][s],C[n-k][s][a][r]),-1))
                           for k in range(n+1) for r in I for s in I))
                   for b in I] for a in I])
    S=[add(*(mul(inv[k][a][b],R[n-k][a][b])
              for k in range(n+1) for a in I for b in I)) for n in range(N+1)]
    return [[[add(R[n][a][b],scale(add(*(mul(g[k][a][b],S[n-k])
                       for k in range(n+1))),-Q(1,2)))
              for b in I] for a in I] for n in range(N+1)]

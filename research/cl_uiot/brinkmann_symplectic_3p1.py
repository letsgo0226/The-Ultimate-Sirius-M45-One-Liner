"""Exact symplectic Taylor-jet audit for transverse Brinkmann flow."""
from fractions import Fraction as Q
from brinkmann_geodesic_3p1 import fundamental,shifted
I=range(4)
J=((0,1,0,0),(-1,0,0,0),(0,0,0,1),(0,0,-1,0))

def generator(k):
    k=Q(k)
    return ((0,1,0,0),(-k,0,0,0),(0,0,0,1),(0,0,k,0))

def hamiltonian(k,z):
    x,p,y,r=map(Q,z)
    return (p*p+r*r+Q(k)*(x*x-y*y))/2

def energy_rate(kprime,z):
    x,p,y,r=map(Q,z)
    return Q(kprime)*(x*x-y*y)/2

def flow_jet(k,s,order):
    a,b=fundamental(k,s,-1,order+1)
    c,d=fundamental(k,s,1,order+1)
    return [((a[n],b[n],0,0),((n+1)*a[n+1],(n+1)*b[n+1],0,0),
             (0,0,c[n],d[n]),(0,0,(n+1)*c[n+1],(n+1)*d[n+1]))
             for n in range(order+1)]

def symplectic_residual(k,s,order):
    F=flow_jet(k,s,order)
    return [tuple(tuple(sum(F[m][r][a]*J[r][v]*F[n-m][v][b]
                           for m in range(n+1) for r in I for v in I)
                        -(J[a][b] if n==0 else 0) for b in I) for a in I)
            for n in range(order+1)]

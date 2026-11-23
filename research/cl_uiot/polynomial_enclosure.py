"""Direct polynomial Bloch enclosure intersected with probability enclosure."""
from fractions import Fraction as Q
from interval_basin import box,step
from simplex_tightening import tighten
from physical_correlation import bloch_hull

def mul(a,b):
    v=[x*y for x in a for y in b]
    return min(v),max(v)

def square(a):
    lo,hi=a
    return (0 if lo<=0<=hi else min(lo*lo,hi*hi),max(lo*lo,hi*hi))

def component(a,b,c):
    A=square(square(a));B=square(b);C=square(c)
    # b^2+c^2-b^2*c^2 increases in both squared variables on [0,1].
    lo=5*(B[0]+C[0]-B[0]*C[0])-A[1]
    hi=5*(B[1]+C[1]-B[1]*C[1])-A[0]
    l,h=mul(a,(lo/4,hi/4))
    return max(Q(-1),l),min(Q(1),h)

def direct(bounds):
    x,y,z=bloch_hull(bounds)
    return component(x,y,z),component(y,z,x),component(z,x,y)

def enhanced_step(bounds,digits=12):
    b=tighten(bounds)
    r=tighten(step(b,digits))
    z=direct(b)
    out=[]
    for (lo,hi),signs in zip(r,((1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1))):
        a=[mul(v,(Q(s),Q(s))) for v,s in zip(z,signs)]
        out.append((max(lo,(1+sum(v[0] for v in a))/4),
                    min(hi,(1+sum(v[1] for v in a))/4)))
    return tighten(out)

"""Outward-rounded rational interval basin certificates."""
from fractions import Fraction as Q
from universal_pauli import coefficients

def box(bounds):
    b=tuple(tuple(map(Q,v)) for v in bounds)
    if len(b)!=4 or any(len(v)!=2 or not 0<=v[0]<=v[1]<=1 for v in b):raise ValueError("invalid box")
    if sum(v[0] for v in b)>1 or sum(v[1] for v in b)<1:raise ValueError("empty simplex intersection")
    return b

def step(bounds, digits=12):
    b=box(bounds)
    if type(digits) is not int or not 1<=digits<=100:raise ValueError("invalid precision")
    D=10**digits
    out=[]
    for terms in coefficients():
        ends=[]
        for j in (0,1):
            s=Q(0)
            for k,c in terms:
                t=Q(c)
                for v,n in zip(b,k):t*=v[j]**n
                s+=t
            ends.append(s)
        lo,hi=ends
        out.append((max(Q(0),Q(lo*D//1,D)),min(Q(1),Q(-(-hi*D//1),D))))
    return box(out)

def classify(bounds):
    b=box(bounds)
    for i,(lo,hi) in enumerate(b):
        if lo>Q(9,10):return "IXYZ"[i]
    # Bloch components are differences of complementary probability sums.
    m=max(max(abs(1-2*(b[i][0]+b[j][0])),abs(1-2*(b[i][1]+b[j][1])))
          for i,j in ((1,2),(1,3),(2,3)))
    if m*m<Q(2,3):return "uniform"
    return None

def certify(bounds,cap=8,digits=12):
    b=box(bounds)
    if type(cap) is not int or cap<0:raise ValueError("invalid depth")
    for n in range(cap+1):
        label=classify(b)
        if label:return {"basin":label,"steps":n,"box":b}
        if n<cap:b=step(b,digits)
    return {"basin":None,"steps":cap,"box":b}

def split(bounds):
    b=box(bounds)
    i=max(range(4),key=lambda i:b[i][1]-b[i][0])
    lo,hi=b[i];mid=(lo+hi)/2
    out=[]
    for v in ((lo,mid),(mid,hi)):
        c=list(b);c[i]=v
        try:out.append(box(c))
        except ValueError:pass
    return tuple(out)

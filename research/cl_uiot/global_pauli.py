"""Full Fourier coefficient audit and fixed-point candidates."""
from fractions import Fraction as Q
from itertools import product
from qec_perfect_5qubit import residual,parity

def fourier():
    words=list(product("IXYZ",repeat=5))
    signs=[tuple(1-2*parity(residual("".join(w)),g*5) for g in "XYZ") for w in words]
    chars={(a,b):1 if a=="I" or b=="I" or a==b else -1 for a in "IXYZ" for b in "IXYZ"}
    out=[{} for _ in range(3)]
    for h in words:
        k=tuple(h.count(c) for c in "XYZ")
        sums=[0]*3
        for w,s in zip(words,signs):
            t=1
            for a,b in zip(h,w):t*=chars[a,b]
            for i in range(3):sums[i]+=t*s[i]
        for i in range(3):out[i][k]=out[i].get(k,0)+sums[i]
    return tuple({k:Q(v,1024) for k,v in d.items() if v} for d in out)

def expected():
    out=[]
    for i in range(3):
        j,k=(i+1)%3,(i+2)%3
        d={}
        for a,b,c in ((1,2,0),(1,0,2),(5,0,0),(1,2,2)):
            e=[0]*3;e[i],e[j],e[k]=a,b,c
            d[tuple(e)]=Q(-1 if a==5 else -5 if b==c==2 else 5,4)
        out.append(d)
    return tuple(out)

def fixed_signs():
    return ((1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1))

def fixed_types():
    # (sign pattern, squared common magnitude); zero is separate.
    return (((0,0,0),Q(0)),)+tuple((s,a) for s in fixed_signs() for a in (Q(1),Q(2,3)))

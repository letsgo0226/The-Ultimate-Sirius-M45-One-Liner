"""Exact four-cell Fourier/mirror model over Z[i]; no external effects."""
def mirror(v):
    return tuple(v[(-k)%4] for k in range(4))

def shift(v, direction=1):
    return tuple(v[(k-direction)%4] for k in range(4))

# Gaussian integers represented by pairs, avoiding floating point.
def fourier(v):
    roots=((1,0),(0,-1),(-1,0),(0,1))
    return tuple(tuple(sum(v[j]*roots[(k*j)%4][a] for j in range(4))
                       for a in range(2)) for k in range(4))

def spectral_shift(w, direction=1):
    roots=((1,0),(0,-1),(-1,0),(0,1))
    return tuple((a*c-b*d,a*d+b*c)
                 for k,(a,b) in enumerate(w)
                 for c,d in (roots[(k*direction)%4],))

def inverse(w):
    roots=((1,0),(0,1),(-1,0),(0,-1))
    out=[]
    for j in range(4):
        terms=[(a*c-b*d,a*d+b*c) for k,(a,b) in enumerate(w)
               for c,d in (roots[(k*j)%4],)]
        r=sum(a for a,b in terms)
        im=sum(b for a,b in terms)
        if im or r%4:
            raise ValueError("not an integer real tape spectrum")
        out.append(r//4)
    return tuple(out)

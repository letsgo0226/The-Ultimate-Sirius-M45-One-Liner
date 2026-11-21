"""Exact bounded Walsh-Hadamard transform on elementary abelian groups."""
def checked(values):
    n=len(values)
    if not 1<=n<=4096 or n&(n-1):
        raise ValueError("length must be a power of two <=4096")
    if any(type(v) is not int for v in values):
        raise ValueError("integer coefficients required")
    return list(values)

def transform(values):
    a=checked(values)
    h=1
    while h<len(a):
        for i in range(0,len(a),2*h):
            for j in range(i,i+h):
                x,y=a[j],a[j+h]
                a[j],a[j+h]=x+y,x-y
        h*=2
    return tuple(a)

def inverse(values):
    a=transform(values)
    n=len(a)
    if any(v%n for v in a):
        raise ValueError("not an integer signal spectrum")
    return tuple(v//n for v in a)

def translate(values,g):
    a=checked(values)
    if type(g) is not int or not 0<=g<len(a):
        raise ValueError("group element")
    return tuple(a[x^g] for x in range(len(a)))

def laplacian(values):
    a=checked(values)
    n=len(a).bit_length()-1
    return tuple(n*v-sum(a[x^(1<<j)] for j in range(n)) for x,v in enumerate(a))

def spectral_laplacian(values):
    a=checked(values)
    return tuple(2*k.bit_count()*v for k,v in enumerate(a))

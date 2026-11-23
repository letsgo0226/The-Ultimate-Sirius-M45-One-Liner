"""Bounded elementary abelian group and split coordinate embedding."""
def validate(n,x):
    if type(n) is not int or not 1<=n<=16:
        raise ValueError("dimension must be 1..16")
    if type(x) is not int or not 0<=x<1<<n:
        raise ValueError("group element")
    return x

def compose(n,x,y):
    return validate(n,x)^validate(n,y)

def neighbors(n,x):
    validate(n,x)
    return tuple(x^(1<<j) for j in range(n))

def embed(n,x):
    validate(n,x)
    if n==16:
        raise ValueError("dimension budget")
    return x

def recover(n,y):
    validate(n+1,y)
    validate(n,0)
    return y&((1<<n)-1),y>>n

def reconstruct(n,x,b):
    embed(n,x)
    if type(b) is not int or b not in (0,1):
        raise ValueError("extra bit")
    return x|(b<<n)

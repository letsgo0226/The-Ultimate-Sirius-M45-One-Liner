"""Exact binary symplectic audit of the [[5,1,3]] stabilizer code."""
from itertools import combinations,product

GENERATORS=("XZZXI","IXZZX","XIXZZ","ZXIXZ")
def validate(p):
    if len(p)!=5 or any(c not in "IXYZ" for c in p):raise ValueError("invalid Pauli")
def parity(a,b):
    validate(a);validate(b)
    return sum(x!="I" and y!="I" and x!=y for x,y in zip(a,b))%2
def syndrome(p):
    return tuple(parity(p,g) for g in GENERATORS)
def errors():
    return ["IIIII"]+[("I"*i+c+"I"*(4-i)) for i in range(5) for c in "XYZ"]
def table():
    result={syndrome(p):p for p in errors()}
    if len(result)!=16:raise ArithmeticError("syndrome collision")
    return result
def multiply_labels(a,b):
    validate(a);validate(b)
    return "".join(y if x=="I" else x if y=="I" else "I" if x==y
                   else next(c for c in "XYZ" if c not in (x,y)) for x,y in zip(a,b))
def stabilize():
    out={"IIIII"}
    for g in GENERATORS:
        out |= {multiply_labels(g,p) for p in out}
    return out
def residual(p):
    return multiply_labels(table()[syndrome(p)],p)
def distance():
    S=stabilize()
    return min(sum(c!="I" for c in p) for v in product("IXYZ",repeat=5)
               if (p:="".join(v)) not in S and not any(syndrome(p)))

"""Bounded polynomial identity decision with exact witnesses."""
from fractions import Fraction as Q
from symbolic_algebra import normalize,encode_expr,decode_expr

def at(c,x):
    y=Q(0)
    for a in reversed(c):
        y=y*x+a
    return y

def residual(a,b):
    return normalize(("-",a,b))

def run(a,b):
    try:
        ga,gb=encode_expr(a),encode_expr(b)
        c=residual(a,b)
        if c==(Q(0),):
            return ("HALT_PROOF",ga,gb,c,None)
        for x in range(len(c)):
            y=at(c,x)
            if y:
                return ("HALT_COUNTEREXAMPLE",ga,gb,c,(x,y))
    except (ValueError,TypeError,OverflowError,RecursionError):
        pass
    return ("UNKNOWN",)

def verify(record,a,b):
    try:
        if type(record) is not tuple or len(record)!=5:
            return False
        state,ga,gb,c,w=record
        if type(state) is not str or decode_expr(ga)!=a or decode_expr(gb)!=b:
            return False
        if type(c) is not tuple or any(type(v) is not Q for v in c):
            return False
        if c!=residual(a,b):
            return False
        if state=="HALT_PROOF":
            return c==(Q(0),) and w is None
        if state!="HALT_COUNTEREXAMPLE" or type(w) is not tuple or len(w)!=2:
            return False
        x,y=w
        if type(x) is not int or not 0<=x<len(c) or type(y) is not Q:
            return False
        # Evaluate original normalized sides separately.
        return y!=0 and y==at(normalize(a),x)-at(normalize(b),x)
    except (ValueError,TypeError,OverflowError,RecursionError):
        return False

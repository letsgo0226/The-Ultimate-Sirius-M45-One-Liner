"""Bounded exact univariate rational polynomial expressions."""
from fractions import Fraction as Q
import json
from certificate_codec import G,D

def normalize(expr):
    budget=1024
    def visit(e,depth):
        nonlocal budget
        budget-=1
        if budget<0 or depth>32 or type(e) is not tuple or not e:
            raise ValueError("expression limit or shape")
        op=e[0]
        if type(op) is not str:
            raise ValueError("operator")
        if op=="x" and len(e)==1:
            return (Q(0),Q(1))
        if op=="q" and len(e)==3:
            n,d=e[1:]
            if type(n) is not int or type(d) is not int or d<=0 or max(n.bit_length(),d.bit_length())>256:
                raise ValueError("rational literal")
            return (Q(n,d),)
        if op not in ("+","-","*") or len(e)!=3:
            raise ValueError("operator or arity")
        a,b=visit(e[1],depth+1),visit(e[2],depth+1)
        if op=="*":
            if len(a)+len(b)-2>64:
                raise ValueError("degree limit")
            c=[Q(0)]*(len(a)+len(b)-1)
            for i,u in enumerate(a):
                for j,v in enumerate(b):
                    c[i+j]+=u*v
        else:
            c=[(a[i] if i<len(a) else Q(0))+(1 if op=="+" else -1)*(b[i] if i<len(b) else Q(0)) for i in range(max(len(a),len(b)))]
        while len(c)>1 and c[-1]==0:
            c.pop()
        if any(max(v.numerator.bit_length(),v.denominator.bit_length())>4096 for v in c):
            raise ValueError("coefficient limit")
        return tuple(c)
    return visit(expr,0)

def equivalent(a,b):
    return normalize(a)==normalize(b)

def encode_expr(e):
    normalize(e)
    return G(json.dumps(e,separators=(",",":"),ensure_ascii=True).encode("ascii"))

def decode_expr(n):
    b=D(n)
    def freeze(e,depth=0):
        if depth>34:
            raise ValueError("depth")
        return tuple(freeze(v,depth+1) for v in e) if type(e) is list else e
    try:
        e=freeze(json.loads(b.decode("ascii")))
        if encode_expr(e)!=n:
            raise ValueError("noncanonical expression")
        return e
    except (RecursionError,TypeError,OverflowError) as exc:
        raise ValueError("invalid expression") from exc

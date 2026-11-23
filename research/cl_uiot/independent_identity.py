"""Independent bounded AST evaluation; no symbolic_algebra imports."""
from fractions import Fraction as Q

def compile_expr(e):
    remaining=1024
    def visit(v,depth):
        nonlocal remaining
        remaining-=1
        if remaining<0 or depth>32 or type(v) is not tuple or not v or type(v[0]) is not str:
            raise ValueError("syntax or limit")
        op=v[0]
        if op=="x" and len(v)==1:
            return 1,lambda x: Q(x)
        if op=="q" and len(v)==3:
            n,d=v[1:]
            if type(n) is not int or type(d) is not int or d<=0 or max(n.bit_length(),d.bit_length())>256:
                raise ValueError("literal")
            q=Q(n,d)
            return 0,lambda x:q
        if op not in ("+","-","*") or len(v)!=3:
            raise ValueError("operator")
        da,a=visit(v[1],depth+1)
        db,b=visit(v[2],depth+1)
        degree=da+db if op=="*" else max(da,db)
        if degree>64:
            raise ValueError("syntactic degree limit")
        def evaluate(x):
            u,w=a(x),b(x)
            r=u+w if op=="+" else u-w if op=="-" else u*w
            if max(r.numerator.bit_length(),r.denominator.bit_length())>8192:
                raise ValueError("evaluation limit")
            return r
        return degree,evaluate
    return visit(e,0)

def decide(a,b):
    try:
        da,fa=compile_expr(a)
        db,fb=compile_expr(b)
        for x in range(max(da,db)+1):
            y=fa(x)-fb(x)
            if y:
                return ("HALT_COUNTEREXAMPLE",x,y)
        return ("HALT_PROOF",)
    except (ValueError,TypeError,OverflowError,RecursionError):
        return ("UNKNOWN",)

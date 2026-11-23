"""Exact finite prime Dirichlet polynomial representation."""
from fractions import Fraction

LIMIT = 10**8

def factor(g):
    if type(g) is not int or not 1 <= g <= LIMIT:
        raise ValueError("integer code outside 1..10^8")
    terms=[]
    p=2
    while p*p<=g:
        e=0
        while g%p==0:
            g//=p
            e+=1
        if e:
            terms.append((p,e))
        p+=1
    if g>1:
        terms.append((g,1))
    return tuple(terms)

def reconstruct(terms):
    if not isinstance(terms,tuple) or len(terms)>26:
        raise ValueError("canonical tuple required")
    g=1
    previous=1
    for p,e in terms:
        if type(p) is not int or type(e) is not int or not previous<p<=LIMIT or not 1<=e<=26:
            raise ValueError("invalid term")
        if factor(p)!=((p,1),):
            raise ValueError("prime required")
        g*=p**e
        if g>LIMIT:
            raise ValueError("code cap")
        previous=p
    return g

def evaluate(terms,s):
    reconstruct(terms)
    if type(s) is not int or not -16<=s<=16:
        raise ValueError("bounded integer exponent required")
    return sum((e*Fraction(p)**(-s) for p,e in terms),Fraction(0))

def derivative_log_signature(terms):
    # Formal representation of -D'(0) as sum e log(p).
    reconstruct(terms)
    return terms

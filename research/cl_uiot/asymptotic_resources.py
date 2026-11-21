"""Two-sided bounds for the scalar concatenation certificate."""
from fractions import Fraction as Q
from qec_concatenated_5qubit import probability
from zeta_reliability import allocation

def bracket(p,n):
    p=probability(p)
    if not 0<p<Q(1,10):raise ValueError("require 0<p<1/10")
    if type(n) is not int or n<0:raise ValueError("invalid depth")
    return p**(2**n),(10*p)**(2**n)/10

def depth_interval(p,e,max_depth):
    p=probability(p);e=Q(e)
    if not 0<p<Q(1,10) or not 0<e<=1:raise ValueError("invalid inputs")
    if type(max_depth) is not int or max_depth<0:raise ValueError("invalid depth")
    lo=hi=None
    for n in range(max_depth+1):
        a,b=bracket(p,n)
        if lo is None and a<=e:lo=n
        if b<=e:
            hi=n;break
    return lo,hi

def zeta_interval(p,total,t,max_depth,s=2,m=8):
    return depth_interval(p,allocation(total,t,s,m),max_depth)

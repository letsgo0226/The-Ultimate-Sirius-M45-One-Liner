"""Exact survival bounds for conditional first-failure hazards."""
from fractions import Fraction as Q
from qec_concatenated_5qubit import probability
from adaptive_reliability import index

def survival_bounds(lower,upper):
    lower=tuple(map(probability,lower));upper=tuple(map(probability,upper))
    if len(lower)!=len(upper):raise ValueError("length mismatch")
    a=b=Q(1)
    for l,u in zip(lower,upper):
        if l>u:raise ValueError("inverted interval")
        a*=1-u;b*=1-l
    return a,b

def fixed_upper(delta,T):
    delta=probability(delta);index(T)
    return (1-delta)**T

def crossing(delta,target,cap):
    delta=probability(delta);target=probability(target);index(cap)
    for t in range(cap+1):
        if fixed_upper(delta,t)<=target:return t
    return None

def exact_survival(hazards):
    h=tuple(map(probability,hazards))
    return survival_bounds(h,h)[0]

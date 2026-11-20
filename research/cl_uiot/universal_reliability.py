"""Universal lower certificates for monotone summable error budgets."""
from fractions import Fraction as Q
from adaptive_reliability import tolerance,index
from asymptotic_resources import depth_interval
from qec_concatenated_5qubit import probability

def envelope(total,t):
    return tolerance(total)/(index(t)+1)

def audit_prefix(total,allocations):
    total=tolerance(total)
    a=tuple(map(Q,allocations))
    if any(e<=0 for e in a):raise ValueError("positive allocations required")
    if any(x<y for x,y in zip(a,a[1:])):raise ValueError("nonmonotone prefix")
    if sum(a)>total:raise ValueError("budget exceeded")
    return total-sum(a)

def necessary_depth(p,total,t,max_depth):
    return depth_interval(p,envelope(total,t),max_depth)[0]

def necessary_qubits(p,total,t,max_depth):
    n=necessary_depth(p,total,t,max_depth)
    return None if n is None else 5**n

def telescoping_allocation(total,t):
    total=tolerance(total);t=index(t)
    return total/Q((t+1)*(t+2))

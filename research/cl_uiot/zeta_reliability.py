"""Certified rational zeta reliability schedule for integer s >= 2."""
from fractions import Fraction as Q
from adaptive_reliability import tolerance,index
from qec_minimum_resources import plan
from qec_concatenated_5qubit import probability

def zeta_bounds(s,m):
    if type(s) is not int or s<2 or type(m) is not int or m<1:
        raise ValueError("require integer s>=2 and m>=1")
    h=sum((Q(1,k**s) for k in range(1,m+1)),Q(0))
    return h+Q(1,(s-1)*(m+1)**(s-1)),h+Q(1,(s-1)*m**(s-1))

def allocation(total,t,s=2,m=8):
    total=tolerance(total);index(t)
    _,upper=zeta_bounds(s,m)
    return total/(upper*(t+1)**s)

def prefix(p,total,T,budget,s=2,m=8):
    p=probability(p);total=tolerance(total);index(T)
    zeta_bounds(s,m)
    if type(budget) is not int or budget<1:raise ValueError("invalid budget")
    records=[];spent=Q(0)
    for t in range(T):
        e=allocation(total,t,s,m)
        r=plan(p,e,budget)
        if not r["certified"]:
            return {"certified":False,"cycles":t,"blocked_cycle":t,"failure_bound":spent,"records":records}
        records.append({"cycle":t,"allocation":e,**r})
        spent+=r["upper_bound"]
    return {"certified":True,"cycles":T,"failure_bound":spent,"records":records}

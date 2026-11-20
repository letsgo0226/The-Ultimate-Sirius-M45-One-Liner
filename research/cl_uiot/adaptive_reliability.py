"""Exact finite-prefix certificates for summable reliability schedules."""
from fractions import Fraction as Q
from qec_minimum_resources import plan
from qec_concatenated_5qubit import probability

def tolerance(total):
    total=Q(total)
    if not 0<total<=1:raise ValueError("invalid total tolerance")
    return total

def index(t):
    if type(t) is not int or t<0:raise ValueError("invalid index")
    return t

def allocation(total,t):
    return tolerance(total)/2**(index(t)+1)

def remaining(total,T):
    return tolerance(total)/2**index(T)

def prefix(p,total,T,budget):
    p=probability(p);total=tolerance(total);index(T)
    if type(budget) is not int or budget<1:raise ValueError("invalid budget")
    records=[]
    spent=Q(0)
    for t in range(T):
        e=allocation(total,t)
        r=plan(p,e,budget)
        if not r["certified"]:
            return {"certified":False,"cycles":len(records),"records":records,
                    "failure_bound":spent,"blocked_cycle":t}
        records.append({"cycle":t,"allocation":e,**r})
        spent+=r["upper_bound"]
    return {"certified":True,"cycles":T,"records":records,"failure_bound":spent,
            "unallocated":remaining(total,T)}

def conservative_depth(p,total,t):
    p=probability(p);e=allocation(total,t)
    if p==0:return 0
    if p>=Q(1,10):raise ValueError("requires p < 1/10")
    n=0;b=p
    while b>e:
        b=10*b*b;n+=1
    return n

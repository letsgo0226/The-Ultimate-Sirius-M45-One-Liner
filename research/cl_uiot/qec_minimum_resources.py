"""Bounded exact minimum sufficient concatenation resource search."""
from fractions import Fraction as Q
from qec_concatenated_5qubit import bound,probability

def plan(p,epsilon,budget):
    p=probability(p);epsilon=Q(epsilon)
    if not 0<epsilon<=1:raise ValueError("positive tolerance required")
    if type(budget) is not int or budget<1:raise ValueError("positive integer budget required")
    n,N=0,1
    while True:
        if p<=epsilon:
            return {"certified":True,"depth":n,"data_qubits":N,"upper_bound":p}
        if N*5>budget or bound(p)>=p:
            return {"certified":False,"depth":n,"data_qubits":N,"upper_bound":p}
        p=bound(p);n+=1;N*=5

def mission_plan(p,epsilon,cycles,budget):
    if type(cycles) is not int or cycles<1:raise ValueError("positive integer cycles required")
    epsilon=Q(epsilon)
    if not 0<epsilon<=1:raise ValueError("invalid mission tolerance")
    return plan(p,epsilon/cycles,budget)

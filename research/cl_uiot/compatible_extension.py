"""Counterexample to cyclic zero padding and compatible frozen extension."""
from reversible_machine import step,backward,validate

def embed(state):
    q,h,t=state
    validate(q,h,t)
    if len(t)>2048:
        raise ValueError("dimension cap")
    return q,h,t+(0,)*len(t)

def frozen_step(state,n,reverse=False):
    q,h,t=state
    validate(q,h,t)
    if type(n) is not int or not 1<=n<len(t) or n&(n-1) or h>=n:
        raise ValueError("active block")
    u,j,a=(backward if reverse else step)((q,h,t[:n]))
    return u,j,a+t[n:]

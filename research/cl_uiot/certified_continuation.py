"""Certified Taylor tails and radius selection for ACMC."""
from fractions import Fraction as Q
from analytic_critical import certificate

def radius():
    # C*rho=1/18, so lambda-9*C*rho=7/6.
    return Q(1,18*35400000)

def tail(rho,s,n):
    rho,s=Q(rho),Q(s)
    if not certificate(rho)["certified"]:raise ValueError("uncertified radius")
    if not 0<=s<rho or type(n) is not int or n<2:raise ValueError("invalid truncation")
    t=s/rho
    return rho*t**(n+1)*((n+2)-(n+1)*t)/(1-t)**2

def required_order(rho,s,tolerance,cap):
    tolerance=Q(tolerance)
    if tolerance<=0 or type(cap) is not int or cap<2:raise ValueError("invalid target")
    for n in range(2,cap+1):
        if tail(rho,s,n)<=tolerance:return n
    return None

def transform_error(rho,n):
    c=certificate(rho)
    if not c["certified"] or type(n) is not int or n<0:raise ValueError("invalid certificate")
    return c["radius"]*c["implicit_lipschitz"]**n

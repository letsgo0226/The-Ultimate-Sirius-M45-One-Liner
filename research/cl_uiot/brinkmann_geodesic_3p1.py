"""Exact finite Taylor jets for transverse Brinkmann geodesic evolution."""
from fractions import Fraction as Q
from math import comb

def shifted(k,s):
    s=Q(s)
    return [sum(Q(k[j])*comb(j,i)*s**(j-i) for j in range(i,len(k)))
            for i in range(len(k))]

def jet(k,s,position,velocity,sign,order):
    if type(order) is not int or order<1:raise ValueError("positive integer order")
    if sign not in (-1,1):raise ValueError("invalid sign")
    p=shifted(k,s)
    a=[Q(position),Q(velocity)]
    for n in range(order-1):
        a.append(sign*sum(p[i]*a[n-i] for i in range(min(n+1,len(p))))/Q((n+1)*(n+2)))
    return a

def fundamental(k,s,sign,order):
    return jet(k,s,1,0,sign,order),jet(k,s,0,1,sign,order)

def wronskian_jet(k,s,sign,order):
    a,b=fundamental(k,s,sign,order)
    return [sum(a[i]*(n-i+1)*b[n-i+1]-b[i]*(n-i+1)*a[n-i+1]
                for i in range(n+1)) for n in range(order)]

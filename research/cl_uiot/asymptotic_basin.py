"""Finite-stage schedule for asymptotically complete open-basin coverage."""
from fractions import Fraction as Q
from adaptive_basin import cover,verify

def schedule(k):
    if type(k) is not int or k<0:raise ValueError("invalid stage")
    return {"budget":2**(k+1)-1,"depth":k,"cap":k,"digits":k+1}

def stage(k,bounds=((0,1),)*4):
    return cover(bounds,**schedule(k))

def error_bound(width,n,digits):
    width=Q(width)
    if width<0 or type(n) is not int or n<0 or type(digits) is not int or not 1<=digits<=100:raise ValueError("invalid bound")
    # Total degree five, coefficient sum <=1024, sup-norm Lipschitz <=5120.
    L=5120
    return L**n*width+Q(1,10**digits)*(L**n-1)/(L-1)

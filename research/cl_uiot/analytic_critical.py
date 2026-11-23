"""Conservative complex-polydisc graph-transform certificate."""
from fractions import Fraction as Q

def certificate(rho=Q(1,10**7)):
    rho=Q(rho)
    if rho<=0:raise ValueError("positive radius required")
    # Inputs (r,u,v) bounded by 2rho. Each probability perturbation <= 5rho.
    # Sum of absolute monomial coefficients of each output <=1024.
    # On radius <=1/5, each complex probability magnitude <=2.
    # Second directional partial bound: 1024*20*2^3*4^2
    # (sum of absolute affine coordinate coefficients <=4).
    M=Q(2621440)
    # Radial sum and transverse subtraction each bounded by 3 output bounds.
    # Taylor remainder <= (3M/2)*(|r|+|u|+|v|)^2.
    # Use graph domain |r|,|u|,|v|<=rho and loose common bound C.
    C=Q(35400000)
    rem=C*rho*rho
    # Derivative in r <=9 M rho; C dominates this as well.
    dr=C*rho
    # h bounded by rho on radius rho: Cauchy derivative <=4 on half-radius
    # in each transverse coordinate. Graph transform Lipschitz in r <= (3/5)*9dr.
    # Outer graph difference <= norm difference.
    contraction_test=Q(3,5)*(1+9*dr)
    # For contraction of implicit transform use sharper outer graph difference
    # divided by 5/3 minus 9dr.
    denom=Q(5,3)-9*dr
    return {"radius":rho,"remainder":rem,"derivative":dr,
            "certified":rho<=Q(1,5) and rem<=rho/2 and denom>1,
            "implicit_lipschitz":1/denom if denom>0 else None}

def default_certificate():return certificate(Q(1,10**10))

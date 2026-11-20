"""First-order geodesic deviation in a local inertial detector frame.
Signature +---; curvature convention inherited from tt_gravity_wave_3p1.
Separation is evaluated at zeroth order on the right-hand side.
"""
from fractions import Fraction as Q
from maxwell_3p1 import add,scale,deriv
from tt_gravity_wave_3p1 import tidal,tt_wave

def acceleration(h,separation):
    if len(separation)!=3:
        raise ValueError("three spatial components required")
    return tuple(add(*(scale(tidal(h,i,j),Q(separation[j-1]))
                       for j in range(1,4))) for i in range(1,4))

def tt_displacement(h,separation):
    """Particular first-order displacement; homogeneous initial data omitted."""
    if len(separation)!=3:
        raise ValueError("three spatial components required")
    return tuple(add(*(scale(h[i][j],-Q(separation[j-1])/2)
                       for j in range(1,4))) for i in range(1,4))

def tt_response_residual(h,separation):
    a=acceleration(h,separation)
    d=tt_displacement(h,separation)
    return tuple(add(deriv(deriv(d[i],0),0),scale(a[i],-1))
                 for i in range(3))

def demo():
    h=tt_wave([0,0,2],[0,0,3])
    a=acceleration(h,[1,0,0])
    return {"tt_response_identity":tt_response_residual(h,[1,2,3])==({},{},{}),
            "transverse_response":a[2]=={},
            "nonzero_tidal_response":bool(a[0]) and bool(a[1]),
            "scope":"first-order local detector response"}
if __name__=="__main__":
    import json
    print(json.dumps(demo(),sort_keys=True))

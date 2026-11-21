"""Opt-in integrated bounded polynomial verification. No baseline changes."""
from fractions import Fraction as Q
from symbolic_algebra import decode_expr
from dual_verification import run_dual
from bounded_rational import bounded
from algebraic_zero import roots
from uecs_interface import report

def identity(ga,gb,bits=4096):
    try:
        if type(bits) is not int or not 1<=bits<=8192:
            return {"state":"UNKNOWN"}
        a,b=decode_expr(ga),decode_expr(gb)
        result=run_dual(a,b)
        if not result["dual_verified"]:
            return {"state":"UNKNOWN"}
        energy=Q(0)
        for c in result["certificate"][3]:
            energy=bounded("+",energy,bounded("*",c,c,bits),bits)
        if (energy==0)!=(result["state"]=="HALT_PROOF"):
            return {"state":"UNKNOWN"}
        return {**result,"energy":energy,"zeros":roots(energy)}
    except (ValueError,TypeError,OverflowError,RecursionError):
        return {"state":"UNKNOWN"}

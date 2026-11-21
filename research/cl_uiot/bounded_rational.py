"""Conservative pre-operation bit budget for exact rational arithmetic."""
from fractions import Fraction as Q

class BudgetExceeded(ValueError):
    pass

def bounded(op,a,b,bits=4096):
    if type(bits) is not int or not 1<=bits<=8192:
        raise ValueError("invalid bit budget")
    if type(a) not in (int,Q) or type(b) not in (int,Q):
        raise ValueError("exact operands required")
    a,b=Q(a),Q(b)
    n,d=a.numerator.bit_length(),a.denominator.bit_length()
    m,e=b.numerator.bit_length(),b.denominator.bit_length()
    if max(n,d,m,e)>bits:
        raise BudgetExceeded("operand")
    if op in ("+","-"):
        bound=max(max(n+e,m+d)+1,d+e)
    elif op=="*":
        bound=max(n+m,d+e)
    elif op=="/":
        if not b:
            raise ValueError("division by zero")
        bound=max(n+e,d+m)
    else:
        raise ValueError("unsupported operation")
    if bound>bits:
        raise BudgetExceeded("intermediate")
    return a+b if op=="+" else a-b if op=="-" else a*b if op=="*" else a/b

def request(op,a,b,bits=4096):
    try:
        return {"state":"EXACT_RESULT","value":bounded(op,a,b,bits)}
    except BudgetExceeded:
        return {"state":"UNKNOWN","reason":"resource_limit"}
    except (ValueError,TypeError,OverflowError):
        return {"state":"UNKNOWN","reason":"invalid_request"}

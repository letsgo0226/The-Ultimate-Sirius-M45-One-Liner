"""Restricted UCP certificate for rational matrix instances."""
from fractions import Fraction as Q
from zero_tableau import certificate
from zero_tableau_checker import verify as verify_tableau
from godel_dirichlet import factor,reconstruct
from algebraic_zero import roots

# Fixed theorem identifier, not a general proof serialization.
THEOREM_ID=60

def produce(lam,mu):
    if any(type(x) not in (int,Q) for x in (lam,mu)):
        raise ValueError("exact rational parameters required")
    lam,mu=Q(lam),Q(mu)
    c=mu**2*(1+lam**2)
    return {"parameters":(lam,mu),"residual":c,"roots":roots(c),
            "state":"HALT_PROOF" if c==0 else "HALT_COUNTEREXAMPLE",
            "theorem_id":THEOREM_ID,"prime_terms":factor(THEOREM_ID),
            "tableau":certificate()}

def verify(record):
    try:
        if type(record) is not dict or set(record)!= {"parameters","residual","roots","state","theorem_id","prime_terms","tableau"}:
            return False
        l,m=record["parameters"]
        if type(l) is not Q or type(m) is not Q:
            return False
        if type(record["theorem_id"]) is not int or record["theorem_id"]!=THEOREM_ID or reconstruct(record["prime_terms"])!=THEOREM_ID:
            return False
        if not verify_tableau(record["tableau"]):
            return False
        c=m*m*(1+l*l)
        if type(record["residual"]) is not Q or record["residual"]!=c:
            return False
        expected=((Q(1,2),0,Q(0),2),) if m==0 else ((Q(1,2),-1,c,1),(Q(1,2),1,c,1))
        return record["roots"]==expected and record["state"]==("HALT_PROOF" if m==0 else "HALT_COUNTEREXAMPLE")
    except (ValueError,TypeError,KeyError,OverflowError):
        return False

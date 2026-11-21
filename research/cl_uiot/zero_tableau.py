"""Fixed theorem certificate producer; no general proof search."""
from zero_tableau_checker import verify
from algebraic_zero import matrix_roots
from exact_zero import matrix_residual

def certificate():
    return ((("A","!B"),"positive_factor","B"),
            (("!A","B"),"zero_substitution","A"))

def run(lam,mu):
    cert=certificate()
    if not verify(cert):
        return {"state":"UNKNOWN"}
    c=matrix_residual(lam,mu)
    return {"state":"HALT_PROOF" if c==0 else "HALT_COUNTEREXAMPLE",
            "residual":c,"roots":matrix_roots(lam,mu),"certificate":cert}

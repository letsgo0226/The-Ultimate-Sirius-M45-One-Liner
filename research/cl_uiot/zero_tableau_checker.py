"""Restricted propositional tableau for the fixed real-algebra theorem.
Atoms A: mu^2*(1+lambda^2)=0; B: mu=0.
Trusted bridge rules: A=>B (positive factor); B=>A (substitution).
"""
def verify(certificate):
    if type(certificate) is not tuple or len(certificate)!=2:
        return False
    expected=(frozenset(("A","!B")),frozenset(("!A","B")))
    rules={"positive_factor":("A","B"),"zero_substitution":("B","A")}
    seen=set()
    for branch in certificate:
        if type(branch) is not tuple or len(branch)!=3:
            return False
        initial,rule,derived=branch
        if type(initial) is not tuple or len(initial)!=2 or any(type(x) is not str for x in initial):
            return False
        if type(rule) is not str or type(derived) is not str or rule not in rules:
            return False
        facts=frozenset(initial)
        if facts not in expected or facts in seen:
            return False
        premise,conclusion=rules[rule]
        if premise not in facts or derived!=conclusion or "!"+derived not in facts:
            return False
        seen.add(facts)
    return len(seen)==2

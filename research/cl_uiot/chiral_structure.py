"""Bounded finite relational/dynamical transport; no executable payloads."""
def transport(table, permutation):
    n=len(table)
    if not 1<=n<=256 or len(permutation)!=n:
        raise ValueError("domain size")
    if any(type(x) is not int or not 0<=x<n for x in (*table,*permutation)):
        raise ValueError("invalid index")
    if len(set(permutation))!=n:
        raise ValueError("not bijective")
    result=[0]*n
    for x in range(n):
        result[permutation[x]]=permutation[table[x]]
    return tuple(result)

def orbit(table, generators, budget=64):
    if type(budget) is not int or not 1<=budget<=256 or len(generators)>16:
        raise ValueError("budget")
    table=tuple(table)
    transport(table,tuple(range(len(table))))
    for g in generators:
        transport(table,g)
    seen={table}
    queue=[table]
    for t in queue:
        for g in generators:
            u=transport(t,g)
            if u not in seen:
                if len(seen)==budget:
                    return tuple(queue),False
                seen.add(u)
                queue.append(u)
    return tuple(queue),True

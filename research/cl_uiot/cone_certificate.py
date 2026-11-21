"""Certificate producer. Independent checker is in cone_checker."""
from fractions import Fraction as Q
from polynomial_enclosure import component

def certificate(cap=26):
    def visit(b,d):
        (a,A),(c,C),(e,E)=b
        if A<c or C<e or a+c>1+E:return "empty"
        out=[component(*v) for v in (b,(b[1],b[2],b[0]),(b[2],b[0],b[1]))]
        m=min(0 if l<=0<=h else min(abs(l),abs(h)) for l,h in out)
        M=max(max(abs(l),abs(h)) for l,h in out)
        if 3*M*M<2:return "central"
        if 5*m*m>=3*M*M:return "cone"
        if d>=cap:raise ValueError("unresolved")
        i=max(range(3),key=lambda j:b[j][1]-b[j][0])
        l,h=b[i];mid=(l+h)/2
        children=[]
        for v in ((l,mid),(mid,h)):
            c=list(b);c[i]=v;children.append(visit(tuple(c),d+1))
        return (i,*children)
    return visit(((Q(0),Q(1)),)*3,0)

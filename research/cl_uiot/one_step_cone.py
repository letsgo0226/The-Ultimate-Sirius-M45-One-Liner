"""Exact finite cover of sorted nonnegative physical Bloch states."""
from fractions import Fraction as Q
def prove(cap=26):
    if type(cap) is not int or cap<0:raise ValueError("invalid depth")
    todo=[(((Q(0),Q(1)),)*3,0)]
    n=deep=0
    while todo:
        b,d=todo.pop();n+=1;deep=max(deep,d)
        (a,A),(c,C),(e,E)=b
        if A<c or C<e or a+c>1+E:continue
        out=[]
        for x,y,z in (b,(b[1],b[2],b[0]),(b[2],b[0],b[1])):
            l,h=x;v,w=y;s,t=z
            p=5*(v*v+s*s-v*v*s*s)
            r=5*(w*w+t*t-w*w*t*t)
            L=p-h**4;H=r-l**4
            vals=[i*j/4 for i in x for j in (L,H)]
            lo,hi=min(vals),max(vals)
            out.append((0 if lo<=0<=hi else min(abs(lo),abs(hi)),max(abs(lo),abs(hi))))
        m=min(x[0] for x in out);M=max(x[1] for x in out)
        if 3*M*M<2 or 5*m*m>=3*M*M:continue
        if d==cap:return False,n,deep,b
        i=max(range(3),key=lambda i:b[i][1]-b[i][0])
        l,h=b[i];mid=(l+h)/2
        for v in ((l,mid),(mid,h)):
            c=list(b);c[i]=v;todo.append((tuple(c),d+1))
    return True,n,deep,None
if __name__=="__main__":print(prove())

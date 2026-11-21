"""Independent exact checker; no imports from producer or interval modules."""
from fractions import Fraction
def verify(tree,depth_limit=32,node_limit=10000):
    count=0
    def check(t,b,d):
        nonlocal count
        count+=1
        if count>node_limit or d>depth_limit:return False
        l=[v[0] for v in b];u=[v[1] for v in b]
        if t=="empty":
            return u[0]<l[1] or u[1]<l[2] or l[0]+l[1]>1+u[2]
        if t in ("central","cone"):
            lower=[];upper=[]
            for i in range(3):
                j,k=(i+1)%3,(i+2)%3
                # Equivalent complement-product expression.
                f=5-5*(1-l[j]**2)*(1-l[k]**2)-u[i]**4
                g=5-5*(1-u[j]**2)*(1-u[k]**2)-l[i]**4
                v=min(l[i]*f,u[i]*f,l[i]*g,u[i]*g)/4
                w=max(l[i]*f,u[i]*f,l[i]*g,u[i]*g)/4
                lower.append(max(0,v,-w))
                upper.append(max(abs(v),abs(w)))
            M=min(1,max(upper));m=min(lower)
            return 3*M*M<2 if t=="central" else 5*m*m>=3*M*M
        if not isinstance(t,(tuple,list)) or len(t)!=3:return False
        i=t[0]
        if type(i) is not int or not 0<=i<3:return False
        a,z=b[i];mid=(a+z)/2
        left=list(b);right=list(b)
        left[i]=(a,mid);right[i]=(mid,z)
        return check(t[1],left,d+1) and check(t[2],right,d+1)
    return check(tree,[(Fraction(0),Fraction(1))]*3,0)

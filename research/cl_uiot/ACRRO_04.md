# ACRRO-04: information-preserving abelianization of D4
ACRRO-03 passed CI 44917325042. D4=<r,s | r^4=s^2=1,srs=r^-1>.
Represent r^a s^b by (a,b). Product is (a+(-1)^b c mod 4,b xor d).
Derived subgroup is central {1,r^2}; quotient is C2 x C2.
Encode a=alpha+2k, quotient q=(alpha,b), kernel bit k.
The set bijection is not a direct product group isomorphism.
For t=(gamma,d), the section r^alpha s^b gives cocycle
c(q,t)=floor((alpha+(-1)^b gamma)/2) mod 2.
Extended multiplication is (q xor t,k xor l xor c(q,t)).
The cocycle retains the noncommutative multiplication information.
Tests cover all 8 elements, 64 products, 512 associativity triples,
64 quotient cocycle triples and invalid inputs. This is a finite
central extension example, not a general group algorithm; arbitrary
groups may have undecidable word problems. No arbitrary irreversible
computation recovery. Lean proofs pending. No merge or deployment.

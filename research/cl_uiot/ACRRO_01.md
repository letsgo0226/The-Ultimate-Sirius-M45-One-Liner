# ACRRO-01: elementary abelian chiral group
USRCO-02 passed CI 44914985906. Use G_n=(Z/2Z)^n with XOR.
Every group element is self inverse; composition is associative
and commutative. The Cayley graph for coordinate flips is the
n-cube, with 2^n vertices and n*2^(n-1) undirected edges.
Embedding E(x)=(x,0) doubles the ambient group cardinality.
Projection R(x,b)=x is a left inverse of E, not a two-sided inverse.
Full recovery stores both x and extra bit b; split and reconstruct
are mutual inverses. XOR identities are algebraic; finite tests cover
group axioms through n=4 and graph/split properties through n=8.
Actual dimensions capped at 16; no unbounded execution or replication.
The direct limit is abstract, not stored. This does not invert arbitrary
irreversible machines. Walsh-Hadamard and Lean proofs remain pending.
CSGGO free products and USRCO Stirling layers remain separate pending work.

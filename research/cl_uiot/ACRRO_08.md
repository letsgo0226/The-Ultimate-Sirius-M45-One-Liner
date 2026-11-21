# ACRRO-08: full-state reversible architecture and extension obstruction
ACRRO-07 Lean audit 44919748107 and offline CI 44919755120 succeeded.
Abstract state (h,d) uses local equivalence U_h on data and motion
equivalence M_d on head selected by updated data. Inverse first
undoes motion then local update. Lean candidates state_left and
state_right prove both compositions for arbitrary types under these
hypotheses. Concrete Python equivalence refinement is not formalized.
Cyclic tape zero padding does NOT commute with natural doubled-length
motion: q=0,h=0,t=(1,0) moves to head 1 before extension but head 3
after extension. Frozen active block extension T x identity does
commute, and preserves inactive data; it does not activate new cells.
Tests cover 4*2+16*4+256*8=2120 full extended states.
No direct limit for the original cyclic dynamics is established.
Lean and Python CI pending. No merge or deployment.

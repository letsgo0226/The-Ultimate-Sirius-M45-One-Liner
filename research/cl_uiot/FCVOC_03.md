# FCVOC-03: native spectral transition
For omega=-i and W_k=sum_j t_j omega^(kj), read one cell by
t_h=(1/4) sum_k W_k omega^(-kh). A binary flip changes that cell
by delta=1-2*t_h, so W'_k=W_k+delta*omega^(kh).
No full inverse or forward transform is required by the spectral step.
Control and head updates match FCVOC-02; halt remains absorbing.
The proof follows from linearity and the four-root orthogonality identity.
Valid encoded binary states are the domain; checking one cell is not
validation of an arbitrary spectrum. Tests compare all 192 configurations,
both handedness choices and 32 successive steps against the tape model.
This is a separate implementation, not independently reviewed assurance.
No network, execution of tape contents, replication or deployment.
No performance or hardware independence claim; Lean proof pending.

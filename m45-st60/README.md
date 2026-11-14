# M45-ST/60 — Observer Agreement and Objectivity Threshold

ST60 operationalizes a distinction between **observers agreeing with each other** and **observers correctly identifying a shared pointer value**.

A latent classical pointer bit S is independently copied through a binary symmetric channel with error probability q into N records. Each observer receives a disjoint fragment of an odd number m of records and uses majority vote. There are floor(N/m) observers. Conditional on S, all record errors are independent.

The probability that one observer is wrong is the binomial upper tail:

`e_m = sum_{k=(m+1)/2}^m binom(m,k) q^k (1-q)^(m-k)`.

Per-observer accuracy is `1-e_m`. For two observers, agreement is `(1-e_m)^2 + e_m^2`. The probability that **all** observers are correct is `(1-e_m)^K`, whereas the probability of **unanimous agreement** is `(1-e_m)^K + e_m^K`. Their difference is the probability of a unanimous but wrong consensus.

The program reports these quantities and a **user-chosen** operational objectivity flag requiring both accuracy and pairwise agreement to exceed specified thresholds. These thresholds are not physical constants.

```sh
python3 -m unittest discover -s m45-st60 -p 'test_*.py'
python3 m45-st60/observer_agreement.py --n 24 --m 3 --q 0.1
```

**Limitations:** This is a bounded **classical readout model** for the kind of pointer records motivated by ST57–59, not a direct quantum simulation of simultaneous measurement, spectrum broadcast structure, or collapse. Agreement alone is insufficient for truth; observers may share biased assumptions or correlated errors in reality. The model assumes independent errors conditional on the latent pointer bit and does not model adversarial or correlated noise, detector disturbance, or inter-observer communication. No actual observers, instruments, or particles are involved. Read-only CI.

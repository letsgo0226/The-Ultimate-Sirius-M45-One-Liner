# CVOC-ST04 — Typed Operator Graph

A deliberately conservative **read-only type contract** for five existing ST machines. This is not a universal virtual machine and does not convert tape state to SK ledgers or pocket records.

Each native verifier has a distinct input and output type. An ST43-to-ST44 relationship is supported only as a **binding check**: the ST44 state is verified against the exact ST43 pocket ledger and its pinned digest. The abstract graph's `st43_st44.bind` is a descriptor of that verified relationship, not a runtime state converter. No cross-machine computation edge is asserted.

The tests invoke the actual ST43/ST44 verifiers, reject unsupported compositions and enforce read-only operator definitions.

This PR is stacked on ST03, which itself is stacked on ST47. Do not merge independently into main. CI is manual/PR-triggered only. No scheduling, secrets, writes, deployment, or continuous runtime.

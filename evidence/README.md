# Quillan Evidence Plane

This directory stores machine-readable evidence for claims registered in `CLAIMS.yaml`.

## Evidence boundary

A receipt proves only that a recorded execution occurred under the recorded conditions and produced the recorded artifacts.

A receipt does **not** automatically prove:

- that the tested implementation is canonical;
- that a measurement is scientifically valid;
- that a benchmark is fair;
- that an observed gain is caused by the architecture;
- that an internal reproduction is independent;
- that AGI or consciousness has been demonstrated.

Those conclusions require the additional gates defined in `ARCHITECTURE.md` and `CLAIMS.yaml`.

## Directory contract

```text
evidence/
├── README.md
├── schema/
│   └── evidence-receipt-v1.schema.json
├── receipts/
│   └── <claim-id>/
│       └── <run-id>.json
├── runs/
│   └── <run-id>/
├── benchmarks/
└── manifests/
```

Empty directories do not need to be committed until they contain evidence.

## Receipt lifecycle

1. Select one or more claim IDs from `CLAIMS.yaml`.
2. Pin the exact git commit.
3. Record the implementation/config/checkpoint identities used.
4. Record the environment and full reproduction command.
5. Run the protocol.
6. Preserve PASS, FAIL, ERROR, BLOCKED, and SKIPPED outcomes.
7. Hash result artifacts.
8. Write a receipt conforming to `schema/evidence-receipt-v1.schema.json`.
9. Validate the receipt.
10. Only then consider promoting the claim's evidence state.

Failed runs are evidence and should not be silently discarded.

## Promotion rules

### IMPLEMENTED → EXECUTED

Requires an actual run against the named implementation on a pinned commit.

### EXECUTED → REPRODUCED

Requires a fresh rerun using the documented procedure and sufficient pinned inputs to explain material variation.

### REPRODUCED → BENCHMARKED

Requires declared baselines, metrics, controls, and acceptance criteria.

### BENCHMARKED → INDEPENDENTLY_REPRODUCED

Requires reproduction by a genuinely separate party/environment with sufficient artifacts to audit the result.

A receipt's `outcome.supports_state` is a **candidate ceiling for that run**, not an automatic mutation of `CLAIMS.yaml`.

## Integrity

Every artifact cited by a receipt should have a SHA-256 digest.

The receipt may itself contain `integrity.receipt_sha256`. To avoid self-reference, compute it from canonical UTF-8 JSON with the `receipt_sha256` field omitted, as stated by the schema.

Future tooling may define a stricter canonical JSON serialization. Until then, receipt hashes must record the serializer/version used in `notes` if byte-for-byte cross-tool verification is required.

## Minimum reproducibility package

A result intended to advance beyond `EXECUTED` should normally retain:

- commit SHA;
- command;
- environment versions;
- seed or nondeterminism declaration;
- config identity/hash;
- dataset identity/hash where applicable;
- checkpoint identity/hash where applicable;
- machine-readable measurements;
- acceptance result;
- relevant stdout/stderr or test report;
- hashes of retained artifacts.

## Non-implication rule

```text
ValidReceipt(result) != TrueClaim(result)
```

Receipt validity establishes provenance and integrity of the recorded execution. Scientific and engineering conclusions remain governed by the claim-specific acceptance criteria.

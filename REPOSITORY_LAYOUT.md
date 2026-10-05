# Quillan Repository Layout Contract

> **Status:** Governance specification  
> **Applies to:** Quillan v4.2 research repository  
> **Purpose:** Define where canonical code, evaluation, evidence, integrations, theory, and legacy material belong without implying that the repository has already been physically migrated.

## 1. Design rule

Quillan is treated as a set of evidence-separated layers, not as one undifferentiated system.

A file's location communicates its role. It does **not** raise its evidence state.

```text
Quillan-v4.2-repo/
├── ARCHITECTURE.md
├── CLAIMS.yaml
├── REPOSITORY_LAYOUT.md
├── LIMITATIONS.md                  # planned
│
├── Quillan-v4.2-model/             # current model-core source tree
│   ├── canonical/                  # planned canonical implementation boundary
│   ├── legacy/                     # planned superseded/alternate implementations
│   ├── configs/                    # planned frozen model/training configs
│   └── training/                   # planned canonical training entry points
│
├── quillan_runtime/                # runtime/API prototype when promoted
│
├── eval/                           # claim-linked evaluation plane
│   ├── structural/
│   ├── behavioral/
│   ├── diagnostics/
│   ├── ablations/
│   ├── baselines/
│   └── fixtures/
│
├── evidence/                       # immutable or append-only result artifacts
│   ├── README.md
│   ├── schema/
│   │   └── evidence-receipt-v1.schema.json
│   ├── receipts/
│   ├── runs/
│   ├── benchmarks/
│   └── manifests/
│
├── adapters/                       # planned normalized platform adapter boundary
│   ├── claude/
│   ├── gpt/
│   ├── gemini/
│   ├── grok/
│   ├── mistral/
│   ├── perplexity/
│   └── ollama/
│
├── knowledge/                      # planned normalized knowledge-pack boundary
├── research/                       # theory, papers, hypotheses, interpretations
└── legacy/                         # unrelated or historical project material
```

The tree above is a **target logical structure**. Existing paths remain authoritative until a dedicated migration change explicitly moves them.

## 2. Canonicality

A file is canonical only when a governance artifact explicitly designates it.

Filename, age, directory depth, README prominence, or historical usage do not establish canonical status.

A canonical model designation SHOULD record:

- implementation path;
- entry point;
- configuration path;
- pinned commit;
- supported claim IDs;
- known limitations;
- superseded alternatives.

Designation as canonical means **"this is the implementation evaluated by the current protocol."**

It does not mean:

- trained;
- performant;
- safe;
- production-ready;
- benchmark-superior;
- AGI;
- conscious.

## 3. Layer ownership

### Model core

Owns neural architecture, routing, modules, training mechanics, checkpoint loading, and model inference.

Current source remains under `Quillan-v4.2-model/` until migration.

### Runtime

Owns API behavior, deterministic council orchestration, request/response models, trace identifiers, and runtime policy that is actually enforced in executable code.

Runtime behavior must not be cited as evidence that the custom neural model is executing unless the runtime is explicitly wired to that model and the receipt records the path.

### Evaluation

Owns executable protocols that can pass or fail a claim.

Every promoted evaluation SHOULD identify one or more `CLAIMS.yaml` IDs.

Evaluation code is not evidence by itself. A run receipt is required to establish execution.

### Evidence

Owns machine-readable records of what was run and what happened.

Evidence artifacts should be append-only once cited by a promoted claim. Corrections should create a superseding artifact rather than silently rewriting history.

### Adapters

Owns compatibility with hosted or local model platforms.

Adapter success establishes compatibility only, unless a separate benchmark demonstrates a capability effect.

### Knowledge

Owns curated context/reference packs.

Presence, upload, retrieval, or parsing does not establish factuality or benchmark improvement.

### Research

Owns hypotheses, theory, papers, interpretation, and speculative constructs.

Research documents may motivate experiments. They do not inherit the evidence state of implementation artifacts.

### Legacy

Owns historical, unrelated, superseded, or non-canonical material retained for provenance.

Legacy files must not be silently used as canonical benchmark inputs.

## 4. Evidence flow

The intended dependency chain is:

```text
CLAIMS.yaml
    ↓
canonical implementation/config
    ↓
eval protocol
    ↓
run
    ↓
evidence receipt + result artifacts
    ↓
reproduction
    ↓
benchmark / ablation
    ↓
optional independent reproduction
```

A claim may advance only as far as retained evidence supports it.

## 5. Naming conventions

Recommended identifiers:

- claim: `Q-MODEL-005`
- run: `QRUN-000001`
- receipt: `QREC-000001.json`
- benchmark: `QBENCH-000001.json`
- manifest: `QMAN-000001.json`

Recommended receipt path:

```text
evidence/receipts/<claim-id>/<run-id>.json
```

Recommended run-artifact path:

```text
evidence/runs/<run-id>/
```

## 6. Migration policy

Repository cleanup must preserve provenance.

1. Do not mass-move files before canonical paths are identified.
2. Do not delete alternate implementations merely because one is designated canonical.
3. Record old → new paths in the migration PR.
4. Update claim implementation paths atomically with any move.
5. Preserve historical evidence against the commit/path where it was generated.
6. Do not reinterpret an old result as evidence for a new implementation without rerunning the protocol.

## 7. Immediate build order

1. Keep `ARCHITECTURE.md` and `CLAIMS.yaml` as governance roots.
2. Add the evidence receipt schema and evidence policy.
3. Identify and designate one canonical model implementation.
4. Add direct structural tests for `Q-MODEL-001` through `Q-MODEL-004`.
5. Produce the first machine-readable execution receipt.
6. Add CI only after the direct test path is explicit.
7. Perform physical directory normalization in a later migration PR.

This ordering prevents repository cleanup from being mistaken for scientific validation.

# Quillan Repository Audit and Recovery Baseline

Date: 2026-07-18  
Target: `ryansctt1994-sudo/Quillan-v4.2-repo`  
Reference upstream: `leeex1/Quillan-Ronin`

## Executive finding

The original project contains substantial ideation, model code, training experiments, prompts, diagrams, and architectural language. It does not currently provide one small, stable, reproducible product boundary that supports the strongest public claims.

The recovery decision is to preserve the research archive while creating a clean executable baseline under `quillan_runtime/`.

## Material gaps observed

1. **Claims exceed executable evidence.** Public descriptions include parameter-count, quantization, multimodal, consciousness, and alignment claims. Those claims require a specific artifact manifest, trained checkpoint, evaluation data, and reproducible benchmark record.
2. **Missing-checkpoint behavior is unsafe.** An API path that silently serves random weights can appear operational while producing meaningless output. Production-like endpoints must fail closed when the required artifact is absent.
3. **Synthetic modalities are not multimodal inference.** Random image, audio, and video tensors are useful only as shape smoke tests. They are not evidence of native multimodal capability.
4. **Dependency installation is not reproducible.** Unpinned requirements and shell commands embedded inside a requirements file prevent deterministic installation.
5. **Security defaults require correction.** Wildcard browser origins and raw exception text are unsuitable defaults for a deployed service.
6. **Tests are fragmented.** Tests and diagnostics exist, but a single mandatory CI gate tied to the supported runtime contract was not evident.
7. **Repository scope is mixed.** Research notes, duplicated platform files, large artifacts, prompts, model experiments, and unrelated scaffolds make it difficult to identify the supported product.

## Recovery architecture

The new baseline introduces:

- a typed `CouncilExpert` interface;
- deterministic routing;
- structured outputs with confidence, provenance, and limitations;
- a versioned FastAPI endpoint;
- no hidden reasoning field;
- a fail-fast input boundary;
- unit tests and API tests;
- a path-scoped GitHub Actions workflow;
- explicit evidence status.

## Non-goals for v0.1.0

- training a foundation model;
- claiming consciousness or AGI;
- claiming 1.58-bit inference;
- loading arbitrary tools or executing generated code;
- production deployment;
- replacing the historical research archive.

## Promotion criteria

The runtime may move from `experimental` to `verified-component` only when:

1. CI passes on a pinned commit;
2. the install and test procedure is reproduced in a clean environment;
3. all externally visible capability claims map to tests;
4. dependency and artifact manifests are recorded;
5. known limitations remain visible in documentation and API output.

Provider-backed generation, multimodal inputs, training, and production deployment require separate evidence gates.

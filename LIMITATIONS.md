# Quillan v4.2 Limitations and Non-Claims

> **Status:** Canonical governance document  
> **Scope:** Public claims about the Quillan v4.2 repository  
> **Rule:** The strongest permissible statement is the strongest statement supported by retained evidence for the named claim ID.

## Current posture

Quillan v4.2 is an experimental AI architecture and LLM-integration research project. The repository contains source code, notebooks, prompts, knowledge packs, research papers, runtime prototypes, and governance artifacts at different evidence levels.

Repository inclusion does not imply validation.

## What is currently supported

At the governance baseline, source inspection supports that:

- configuration/source declares a 32-member council concept;
- the enhanced council module contains a learned router;
- the enhanced council module performs sparse top-2 expert selection;
- selected expert identities and router logits are exposed;
- a hierarchical consensus network and scalar sigmoid score are implemented;
- model, prompt, knowledge, adapter, research, and safety layers exist as distinct project concerns.

These are implementation-level statements unless a later receipt advances the corresponding claim.

## Explicit non-claims

Unless a specific claim ID is accompanied by matching evidence, this repository does **not** establish that:

- the enhanced 32-expert architecture has been fully trained;
- an existing checkpoint corresponds to the enhanced architecture;
- all 32 experts receive healthy gradients during training;
- routing avoids collapse;
- experts learn useful specialization;
- the hierarchy improves quality or efficiency;
- Quillan outperforms a dense transformer;
- Quillan outperforms a flat MoE;
- prompt packages improve hosted foundation models;
- knowledge packs improve factual accuracy;
- safety documentation is enforced on every runtime path;
- a consensus score measures truth, ethics, correctness, or honesty;
- routing entropy measures consciousness;
- Quillan is sentient or phenomenally conscious;
- Quillan demonstrates AGI;
- Quillan is production-ready;
- Quillan has been independently validated.

## Checkpoint limitation

The presence of a checkpoint file is not sufficient evidence of:

- training provenance;
- architecture identity;
- dataset identity;
- training duration;
- convergence;
- benchmark performance;
- reproducibility.

A checkpoint should not be promoted as canonical until its generating code/config/data lineage is recorded and its hash is bound to a claim-linked run.

## Notebook limitation

Notebook output is historical execution material unless it is exported into a stable evidence artifact tied to:

- an exact commit;
- environment;
- configuration;
- data identity;
- command/procedure;
- acceptance criterion.

Screenshots and notebook cells may illustrate a result but do not substitute for a reproducible receipt.

## Platform limitation

Claude, GPT, Gemini, Grok, Mistral, Perplexity, Ollama, or other platform integrations may demonstrate compatibility.

Compatibility does not establish a capability improvement.

A capability claim requires a controlled comparison using the same platform model/version, task set, scoring protocol, and appropriate repeated trials.

## Safety limitation

Safety and security documents describe intentions, risks, controls, and proposed governance. A written control is not an enforced control.

Runtime-safety claims require executable protected paths, negative controls, bypass attempts, fail-closed behavior, and reproducible evidence.

## Theory limitation

Research documents may contain speculative architecture, consciousness, emergence, AGI, identity, ethics, or cognition interpretations.

A measurable internal quantity does not inherit the semantic interpretation attached to it.

In particular:

```text
routing_entropy != consciousness
consensus_score != truth
consensus_score != ethics
prompt_identity != independent_model_identity
capability != AGI
documentation != enforcement
receipt_validity != claim_truth
```

## Evidence-state rule

The canonical evidence progression is:

```text
PROPOSED
  -> IMPLEMENTED
  -> EXECUTED
  -> REPRODUCED
  -> BENCHMARKED
  -> INDEPENDENTLY_REPRODUCED
```

A claim advances only when the stronger state's evidence is retained and auditable.

A later code change does not retroactively upgrade an earlier result.

## Public-description rule

Public descriptions SHOULD distinguish:

- **Built** — implemented in source;
- **Executed** — run on a pinned commit;
- **Reproduced** — rerun from documented inputs/procedure;
- **Benchmarked** — compared against declared baselines;
- **Hypothesized** — research direction not yet established;
- **Interpretive** — philosophical or semantic interpretation.

When uncertain, use the weaker description.

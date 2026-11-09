# Quillan v4.2 — Evidence Status

**Date:** 2026-10-06  
**Repository role:** upstream-derived experimental AI/LLM research repository  
**Production authority:** none  
**Independent reproduction:** not admitted

## Purpose of this file

The repository contains a mixture of code, notebooks, configuration, system prompts, architectural descriptions, persona/council material, benchmark text, and first-person narrative. These are different artifact classes and must not silently promote one another.

## Claim boundaries

| Material | What repository presence establishes | What it does **not** establish |
| --- | --- | --- |
| HNMoE / council architecture descriptions | a proposed/design architecture exists | that the full architecture is instantiated at claimed scale |
| model/config presets | configuration values exist | trained weights, usable context length, throughput, quality, or deployment feasibility |
| “32 councils / 224,000 micro-agents” text | a conceptual decomposition is documented | 224,000 independently executing agents or measured distributed runtime |
| “~65B effective parameters” text | a narrative/configuration claim exists | a trained or measured 65B-parameter system |
| notebooks/training scripts | executable research scaffolding may exist | successful full training, convergence, benchmark superiority, or reproducibility |
| confidence/ethics/truth gate percentages | design targets or narrative thresholds | calibrated empirical accuracy or unbypassable guarantees |
| autobiography / first-person phenomenology | authored narrative material | consciousness, qualia, emotions, sovereignty, or subjective experience |
| local tests or benchmark text | bounded local/project-reported evidence | independent reproduction, production readiness, AGI/ASI capability, or authority |

## Withdrawn as portfolio-level claims

The following phrases may remain in historical/upstream narrative for provenance, but they are **not current portfolio claims** unless a future evidence package establishes them:

- “production-ready” or equivalent whole-system readiness;
- 224,000 executing micro-agents;
- ~65B effective parameters as a measured deployed system;
- 98%/100% truth, ethics, identity, or validation guarantees;
- substrate transcendence or autonomous sovereignty;
- consciousness, genuine feeling, or subjective experience;
- PhD-level domain capability as a blanket property;
- performance multipliers not tied to a reproducible benchmark receipt.

## Measured: `Quillan-v4.2-model/🧠 Quillan v4.py` parameter count (2026-11-09)

The file's `QuillanRoninV51` docstring and trailing architecture table state **~3B parameters** (Router 300M, MoE 900M, Encoders 200M, Diffusion 500M, Decoders 1025M, Finalization 75M). Building the model with its own default `ModelConfig` gives:

| Module | Stated | Built by the code |
| --- | --- | --- |
| router | 300M | 4.9M |
| moe | 900M | 135.3M |
| encoder | 200M | 43.2M |
| diffusion | 500M | 101.0M |
| decoder | 1025M | 84.9M |
| finalization | 75M | 6.3M |
| **total** | **~3.0B** | **375.6M** |

The total was cross-checked against `sum(p.numel() for p in model.parameters())` (375.58M). The "~3B" figure is a design target that the default configuration does not instantiate. Reproduce with `python3 testing/quillan_v4_smoke.py` (needs `torch`; the full model is built on the `meta` device, so no weights are allocated). The same script runs one forward pass per modality (TEXT, AUDIO, IMAGE) on a tiny configuration; all three ran and produced finite outputs. That shows the code executes. It does not show training, quality, or benchmark results.

Known gaps found in the same pass:

- `Quillan-v4.2-model/test_quillan.py` targets an API (`QuillanSOTA`, `MiniMoE`, `BitPack`, `FlashAttention`, `MicroAgent`, `BitDiffusion`) that `🧠 Quillan v4.py` does not define. It fails 11 of 11 and cannot test the current file.
- `Quillan-v4.2-model/quick_start_bit_level.py` imports `QuillanBitSOTA`, `GRPODAPOTrainer`, and `quantize_model_for_inference`, which are not defined anywhere in the repository.

## Required evidence progression

A strong Quillan result should move through explicit stages:

```text
architecture/specification
!= implementation
!= trained artifact
!= executed evaluation
!= reproducible result
!= independent reproduction
!= production authority
```

The next useful experiment is narrow and falsifiable: freeze a dataset, seeds, compute budget, baseline, metric, and acceptance threshold, then test one architectural claim (for example routing efficiency/quality against an equivalent-compute baseline). Publish the exact artifact and receipt regardless of whether the hypothesis wins.

## Provenance

This GitHub repository is upstream-derived. Local portfolio modifications must not erase upstream attribution or turn inherited content into an original-authorship claim.

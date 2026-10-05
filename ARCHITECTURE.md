# Quillan v4.2 Canonical Architecture

> **Status:** Research architecture map  
> **Scope:** Quillan System / HNMoE research and deployment repository  
> **Baseline inspected:** `main@fcfc30d0db6098eda4d90e3e6de0aee550dfc623`  
> **Purpose:** Separate implemented mechanisms, executed behavior, reproduced evidence, benchmarked performance, and speculative interpretation.

## 1. Claim Boundary

Quillan contains several different systems under one project name. Evidence from one layer MUST NOT be used as proof for a stronger claim in another layer.

The canonical non-implications are:

- **Code exists ≠ code executes correctly**
- **Code executes ≠ result reproduces**
- **Result reproduces ≠ result beats a baseline**
- **Benchmark improvement ≠ architectural cause**
- **Prompt behavior ≠ neural architecture behavior**
- **Knowledge-file loading ≠ improved factual accuracy**
- **Routing entropy ≠ consciousness**
- **Council terminology ≠ verified multi-agent cognition**
- **Safety documentation ≠ enforced runtime safety**
- **System-prompt identity ≠ independent model identity**
- **Capability ≠ AGI**
- **Internal evidence ≠ independent validation**

Any document, benchmark, paper, or README claim that crosses one of these boundaries must provide the missing evidence explicitly.

---

## 2. Evidence State Machine

Every empirical claim in Quillan should carry one evidence state.

| State | Meaning |
|---|---|
| `PROPOSED` | Hypothesis, design intent, or interpretation with no implementation evidence required yet |
| `IMPLEMENTED` | The relevant mechanism exists in source/configuration |
| `EXECUTED` | The mechanism has been run successfully on a pinned commit |
| `REPRODUCED` | A clean rerun reproduces the stated result from a documented procedure |
| `BENCHMARKED` | The result has been compared against declared baselines under a defined protocol |
| `INDEPENDENTLY_REPRODUCED` | A separate party/environment has reproduced the stated result |

States are monotonic only when the evidence for the stronger state is retained. A later code change can invalidate an earlier result unless the result remains pinned to the original commit.

A separate **claim type** should be used so measurement and interpretation are not confused:

- `OBSERVATION`
- `ENGINEERING_CLAIM`
- `RESEARCH_HYPOTHESIS`
- `INTERPRETATION`

---

## 3. Canonical Layer Map

### Layer 1 — Model Core

**Primary location:** `Quillan-v4.2-model/`

**Purpose:** Neural architecture, routing, training, inference, checkpointing, and model-serving code.

Relevant artifacts currently include multiple model implementations and notebooks. Because there are several variants, no file should be treated as canonical solely because its name contains "Quillan".

Source inspection of the current repository confirms at least two important model paths:

#### A. `quillan_v4_2.py`

The configuration declares:

- `n_council_experts = 32`
- `n_layer = 33`
- a transformer-style architecture
- council/MoE-related configuration
- training/data-loading logic

This establishes implementation intent and source structure only. It does **not** by itself establish training quality, expert specialization, computational advantage, or AGI-like capability.

#### B. `quillan_council_enhanced.py`

This file implements a distinct enhanced council layer with:

- a learned router
- `num_experts = config.n_council_experts`
- sparse top-2 expert selection
- a `ModuleList` of council experts
- returned active-expert indices
- returned router logits
- a hierarchical consensus network
- a sigmoid consensus score
- modulation of the MoE output using that score

This is source-level evidence that these mechanisms are implemented.

It is **not yet evidence** that:

- routing is balanced,
- experts specialize,
- selected experts receive useful gradients under real training,
- the hierarchy improves quality,
- the hierarchy reduces compute,
- the consensus scalar measures truth or ethics,
- council semantics add value beyond an ordinary MoE.

Those are separate claims and require separate experiments.

---

### Layer 2 — Training and Evaluation

**Primary locations:** model notebooks, training scripts, tests, and future `eval/` infrastructure.

The current repository contains test/training code, but the repository does not yet expose one frozen evaluation plane tying a claim to:

1. a canonical model implementation,
2. a pinned commit,
3. a fixed dataset/configuration,
4. an acceptance criterion,
5. a result artifact,
6. a reproduction command.

A specific current gap is visible in `Quillan-v4.2-model/test_quillan.py`:

- the test harness dynamically searches for a Python filename containing "Quillan";
- it tests a `QuillanSOTA` / `MiniMoE` stack;
- that is not sufficient, by source inspection alone, to establish that the enhanced `CouncilMoELayer` path is the object under test.

Therefore, historical screenshots, notebook curves, or a passing general test suite must not be cited as validation of the enhanced 32-expert council architecture until the exact code path is pinned.

**Next gate:** create explicit claim-linked tests for expert count, routing, gradient flow, load balance, specialization, and architecture ablations.

---

### Layer 3 — Cognition / Prompt Layer

**Primary locations:** system prompts and model-specific prompt packages.

**Purpose:** Behavioral steering, identity framing, workflow protocols, reasoning scaffolds, and other prompt-level interventions.

Claims in this layer must be evaluated independently of the neural Model Core.

A platform prompt can alter behavior even when none of the custom PyTorch model code is running. Conversely, a custom model can execute without the platform prompt layer.

Therefore:

- prompt success cannot validate HNMoE claims;
- HNMoE execution cannot validate prompt-superiority claims.

Recommended future platform ablation:

1. base model
2. system prompt only
3. knowledge pack only
4. system prompt + knowledge
5. full Quillan configuration

All variants should use the same base model/version, task set, scoring protocol, and repeated runs where the API is nondeterministic.

---

### Layer 4 — Knowledge Layer

**Primary locations:** `Quillan Knowledge files/` and domain-specific content packs.

**Purpose:** Context injection, reference material, domain guidance, and project-specific knowledge.

Loading or parsing these files establishes compatibility only.

It does not establish:

- factual correctness,
- retrieval accuracy,
- domain expertise,
- lower hallucination rate,
- improved task performance.

Those require held-out domain evaluations.

---

### Layer 5 — Platform Adapters

**Primary locations:** Claude, GPT, Gemini, Grok, Perplexity, Mistral, Ollama, and related deployment assets.

**Purpose:** Port Quillan prompts, context packs, and/or model assets into different runtime environments.

This layer should report compatibility separately from capability.

Examples of valid compatibility evidence:

- files import successfully,
- expected configuration is accepted,
- a smoke task completes,
- the adapter emits a structured result.

Examples of invalid inference:

> "The Claude adapter loaded successfully, therefore Quillan improves Claude reasoning."

That is a benchmark claim and belongs in the Evaluation Plane.

---

### Layer 6 — Research and Theory

**Primary location:** `Formal Papers/`

**Purpose:** Architecture descriptions, hypotheses, theoretical models, proposed metrics, and research interpretations.

Documents concerning AGI, consciousness, emergence, internal cognition, or council semantics should be treated as research artifacts unless their central claims have matching empirical records in `CLAIMS.yaml`.

Particular care is required for:

- consciousness,
- sentience,
- qualia,
- "internal thinking",
- AGI,
- parameter-equivalence claims,
- micro-agent counts,
- claims of architectural ethical guarantees,
- claims of substrate independence.

A measurable proxy may be useful research data without establishing the interpretation attached to it.

For example:

> routing entropy is measurable

does not imply:

> routing entropy measures consciousness.

---

### Layer 7 — Safety, Security, and Governance

**Primary locations:** `RISK_ASSESSMENT.md`, `SECURITY_DISCLOSURE.md`, integration/security documentation.

**Purpose:** Threat modeling, deployment risks, disclosure practices, proposed controls, and safety assumptions.

The current security documentation contains many named mechanisms and mitigation statements. Those statements should be classified individually as:

- implemented controls,
- proposed controls,
- manually enforced procedures,
- assumptions,
- or unverified design claims.

Documentation that says a safety gate exists is not sufficient evidence that the gate executes on every protected path.

Future security validation should include:

- explicit protected paths,
- bypass attempts,
- negative controls,
- fail-closed behavior,
- mutation tests,
- reproducible receipts.

---

## 4. Current Canonical Status

| Area | Current evidence ceiling | Reason |
|---|---|---|
| 32-expert configuration | `IMPLEMENTED` | Source/configuration declares 32 experts |
| Sparse top-2 routing | `EXECUTED` | `QRUN-000002` verified exactly two valid expert selections per synthetic token |
| Router observability | `EXECUTED` | `QRUN-000002` verified returned expert IDs, finite router logits, and selection/logit agreement |
| Hierarchical consensus network | `EXECUTED` | `QRUN-000002` verified bounded scalar score, output modulation, and differentiability through the influence weight |
| "Truth/ethical" meaning of consensus score | `PROPOSED` | Semantic interpretation is not established by source structure |
| Selected-expert gradient connectivity | `EXECUTED` | `QRUN-000003` verified selected experts and router receive finite nonzero gradients under the declared synthetic fixture |
| Routing balance / no collapse | `PROPOSED` | Requires routing statistics across training/eval |
| Expert specialization | `PROPOSED` | Requires specialization metric and ablation |
| HNMoE > dense baseline | `PROPOSED` | Requires controlled benchmark |
| HNMoE > flat MoE | `PROPOSED` | Requires controlled architecture ablation |
| Quillan prompts > base platform model | `PROPOSED` | Requires paired platform evaluation |
| Knowledge packs improve accuracy | `PROPOSED` | Requires held-out domain evaluation |
| AGI-level capability | `PROPOSED` | No operational AGI criterion + benchmark bundle yet |
| Consciousness / phenomenal experience | `PROPOSED` | No accepted operational mapping from current measurements |
| Runtime safety guarantees | `PROPOSED` unless separately tested | Documentation is not execution evidence |
| External / peer validation | `PROPOSED` unless reproducible artifact exists | Discussion or endorsement is not independent reproduction |

### First retained execution evidence

- `QRUN-000002` / `QREC-000002` is pinned to commit `5064bcee0c28ce85a69ff5e272c967789562d245` and advances only `Q-MODEL-002` through `Q-MODEL-004` to `EXECUTED`.
- `QRUN-000003` / `QREC-000003` is pinned to commit `efea7fd21e35db573f2996c6b1775d2aa362fcd9` and additionally advances `Q-MODEL-005` to `EXECUTED`.
- Both are internal GitHub Actions evidence on CPU with Python 3.11.16 and PyTorch 2.10.0+cpu; neither is a clean-room reproduction or independent validation.
- `Q-MODEL-001` remains `IMPLEMENTED`: the synthetic guard instantiates 32 experts, but canonical model/config designation is still unresolved.

---

## 5. Canonical Claim Rules

Every important claim SHOULD receive a stable identifier in `CLAIMS.yaml`.

Minimum fields:

- claim ID
- exact statement
- layer
- claim type
- evidence state
- implementation paths
- evidence paths
- pinned commit
- acceptance criterion
- limitations
- next gate

Rules:

1. A claim must be written narrowly enough that one experiment can succeed or fail.
2. A stronger interpretation must receive a new claim ID.
3. Expected benchmark gains must not be invented after seeing results.
4. Baselines and metrics should be declared before the decisive run.
5. Failed experiments remain evidence and should not be silently deleted.
6. Notebook output is not a canonical result until exported into a stable result artifact.
7. Screenshots may illustrate evidence but should not be the only evidence.
8. A result without a code commit, config, and dataset identity cannot advance beyond `EXECUTED`.
9. Platform-provider model changes must be recorded when comparing hosted systems.
10. AGI/consciousness terminology must never inherit support from weaker engineering measurements by implication.

---

## 6. Initial Model-Core Claim Decomposition

The architecture thesis should be tested as multiple claims rather than one statement that "HNMoE works."

- `Q-MODEL-001` — configuration declares 32 council experts.
- `Q-MODEL-002` — enhanced council layer performs learned sparse routing.
- `Q-MODEL-003` — selected expert identities and router logits are observable.
- `Q-MODEL-004` — hierarchical consensus computation is implemented.
- `Q-MODEL-005` — selected experts receive expected gradients.
- `Q-MODEL-006` — routing avoids pathological expert collapse.
- `Q-MODEL-007` — experts develop measurable specialization.
- `Q-MODEL-008` — hierarchy improves on a flat-MoE baseline.
- `Q-MODEL-009` — HNMoE improves on a parameter-matched dense baseline.
- `Q-MODEL-010` — results remain stable across declared random seeds.
- `Q-MODEL-011` — a clean checkout reproduces the benchmark result.

This decomposition makes it possible for some parts of Quillan to be supported while stronger interpretations remain open.

---

## 7. Next Build Order

The repository should now proceed in this dependency order:

1. `ARCHITECTURE.md` — this document
2. `CLAIMS.yaml` — machine-readable claim registry
3. evidence receipt schema and `evidence/`
4. explicit structural/model tests
5. routing and gradient diagnostics
6. dense / flat-MoE / HNMoE ablations
7. reproducibility harness
8. general capability benchmarks
9. platform/prompt ablations
10. paper and README reconciliation against measured evidence

Until those later gates are completed, the correct presentation is:

> Quillan v4.2 is an experimental AI architecture and LLM-integration research project. The repository contains implemented software, experimental artifacts, theoretical proposals, and speculative interpretations with different evidence levels. Inclusion in the repository does not imply equivalent empirical support.


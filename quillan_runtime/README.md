# Quillan Runtime MVP

Quillan Runtime is the first executable, evidence-grounded baseline for the Quillan concept.

It is a deterministic council-orchestration service with:

- a typed expert interface;
- transparent routing;
- structured expert outputs;
- provenance and confidence fields;
- deterministic trace identifiers;
- a FastAPI contract;
- unit and API tests;
- CI-compatible packaging.

## Claim boundary

This package does **not** claim to be:

- a trained 3-billion-parameter foundation model;
- conscious, sentient, or an AGI;
- a validated multimodal model;
- production-authorized.

Its current status is `experimental`. The purpose of this baseline is to create a component that can be installed, executed, inspected, and falsified before larger claims are introduced.

## Run locally

```bash
cd quillan_runtime
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
pytest
quillan-runtime
```

Windows PowerShell activation:

```powershell
.venv\Scripts\Activate.ps1
```

The service binds to `127.0.0.1:8000` by default.

```bash
curl http://127.0.0.1:8000/health

curl -X POST http://127.0.0.1:8000/v1/council \
  -H "content-type: application/json" \
  -d '{
    "query": "Audit this architecture and produce a build plan.",
    "mode": "audit",
    "context": {"repository": "ryansctt1994-sudo/Quillan-v4.2-repo"}
  }'
```

## Architecture

```text
request
  -> deterministic router
  -> selected experts
  -> structured ExpertResult records
  -> synthesis
  -> versioned HTTP response
```

Built-in experts:

- `analyst`: requirements and structure;
- `skeptic`: claim verification and falsification;
- `planner`: staged delivery planning;
- `safety`: operational and high-stakes risk screening.

The expert protocol is replaceable. A later provider integration can call a local or hosted model while preserving this same output contract and test harness.

## Evidence ladder

| Level | Meaning | Current state |
|---|---|---|
| E0 | concept or prose only | passed |
| E1 | importable component with deterministic tests | implemented in this package |
| E2 | reproducible CI run on a pinned revision | pending first green workflow |
| E3 | benchmarked provider-backed system | not established |
| E4 | trained model artifact with reproducible evaluation | not established |
| E5 | production authorization and monitoring | prohibited until separately approved |

## Next engineering gates

1. Obtain a green CI run.
2. Add an OpenAI-compatible or local-model provider behind a strict `ModelBackend` protocol.
3. Create a fixed evaluation corpus and scoring rubric.
4. Add SQLite or PostgreSQL audit persistence with secret redaction.
5. Add authentication, rate limiting, and deployment hardening.
6. Publish benchmark results separately from architectural claims.

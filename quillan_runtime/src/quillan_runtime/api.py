"""FastAPI application for the Quillan council runtime."""

from __future__ import annotations

from typing import Any, Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from . import __version__
from .orchestrator import CouncilOrchestrator

app = FastAPI(
    title="Quillan Runtime",
    version=__version__,
    description=(
        "Evidence-grounded council orchestration. "
        "This runtime does not claim consciousness or a trained proprietary foundation model."
    ),
)
orchestrator = CouncilOrchestrator()


class CouncilRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1, max_length=10_000)
    mode: Literal["standard", "audit", "build"] = "standard"
    context: dict[str, Any] = Field(default_factory=dict)


class CouncilResponseModel(BaseModel):
    trace_id: str
    status: str
    query: str
    mode: str
    selected_experts: list[str]
    expert_results: list[dict[str, Any]]
    synthesis: dict[str, Any]
    generated_at: str


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "runtime": "quillan-runtime",
        "version": __version__,
        "evidence_status": "experimental",
    }


@app.post("/v1/council", response_model=CouncilResponseModel)
def council(request: CouncilRequest) -> dict[str, Any]:
    try:
        response = orchestrator.run(
            request.query,
            mode=request.mode,
            context=request.context,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return response.to_dict()

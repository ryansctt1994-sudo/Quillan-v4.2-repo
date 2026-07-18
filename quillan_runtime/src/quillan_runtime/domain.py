"""Domain models for the Quillan council runtime."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class RuntimeStatus(StrEnum):
    """Evidence status exposed by the runtime."""

    EXPERIMENTAL = "experimental"
    VERIFIED_COMPONENT = "verified-component"


@dataclass(frozen=True, slots=True)
class EvidenceRef:
    """A compact provenance record attached to an expert result."""

    source: str
    detail: str
    kind: str = "prompt-derived"
    reliability: float = 0.5

    def __post_init__(self) -> None:
        if not 0.0 <= self.reliability <= 1.0:
            raise ValueError("reliability must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class ExpertResult:
    """Structured output from one council expert."""

    expert_id: str
    role: str
    summary: str
    observations: tuple[str, ...]
    recommendations: tuple[str, ...]
    confidence: float
    evidence: tuple[EvidenceRef, ...] = field(default_factory=tuple)
    limitations: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class Synthesis:
    """Council-level aggregation. This is a summary, not hidden chain-of-thought."""

    summary: str
    prioritized_actions: tuple[str, ...]
    risk_flags: tuple[str, ...]
    confidence: float
    consensus: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CouncilResponse:
    """Complete deterministic council response."""

    trace_id: str
    status: RuntimeStatus
    query: str
    mode: str
    selected_experts: tuple[str, ...]
    expert_results: tuple[ExpertResult, ...]
    synthesis: Synthesis
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "status": self.status.value,
            "query": self.query,
            "mode": self.mode,
            "selected_experts": list(self.selected_experts),
            "expert_results": [result.to_dict() for result in self.expert_results],
            "synthesis": self.synthesis.to_dict(),
            "generated_at": self.generated_at.isoformat(),
        }

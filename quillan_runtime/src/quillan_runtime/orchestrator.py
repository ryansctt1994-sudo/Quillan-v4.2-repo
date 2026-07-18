"""Council orchestration and synthesis."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from statistics import fmean
from typing import Any

from .domain import CouncilResponse, ExpertResult, RuntimeStatus, Synthesis
from .experts import CouncilExpert, default_experts
from .router import CouncilRouter


@dataclass(frozen=True, slots=True)
class RuntimeConfig:
    """Configuration for the deterministic runtime."""

    max_experts: int = 4
    max_query_chars: int = 10_000
    status: RuntimeStatus = RuntimeStatus.EXPERIMENTAL


@dataclass(slots=True)
class CouncilOrchestrator:
    """Route a request, execute experts, and aggregate inspectable summaries."""

    config: RuntimeConfig = field(default_factory=RuntimeConfig)
    experts: dict[str, CouncilExpert] = field(default_factory=default_experts)
    router: CouncilRouter = field(init=False)

    def __post_init__(self) -> None:
        missing = {"analyst"} - set(self.experts)
        if missing:
            raise ValueError(f"required experts missing: {sorted(missing)}")
        self.router = CouncilRouter(max_experts=self.config.max_experts)

    def run(
        self,
        query: str,
        *,
        mode: str = "standard",
        context: Mapping[str, Any] | None = None,
    ) -> CouncilResponse:
        normalized = " ".join(query.split())
        if not normalized:
            raise ValueError("query must not be blank")
        if len(normalized) > self.config.max_query_chars:
            raise ValueError(f"query exceeds {self.config.max_query_chars} characters")

        safe_context = dict(context or {})
        decision = self.router.route(normalized, mode=mode)
        results = tuple(
            self.experts[expert_id].analyze(normalized, safe_context)
            for expert_id in decision.selected_experts
        )
        synthesis = self._synthesize(results)
        trace_id = self._trace_id(normalized, mode, safe_context, decision.selected_experts)

        return CouncilResponse(
            trace_id=trace_id,
            status=self.config.status,
            query=normalized,
            mode=mode,
            selected_experts=decision.selected_experts,
            expert_results=results,
            synthesis=synthesis,
        )

    @staticmethod
    def _trace_id(
        query: str,
        mode: str,
        context: Mapping[str, Any],
        selected_experts: tuple[str, ...],
    ) -> str:
        payload = json.dumps(
            {
                "query": query,
                "mode": mode,
                "context": context,
                "selected_experts": selected_experts,
            },
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()[:16]

    @staticmethod
    def _synthesize(results: tuple[ExpertResult, ...]) -> Synthesis:
        if not results:
            raise ValueError("at least one expert result is required")

        summaries = " ".join(result.summary for result in results)
        actions: list[str] = []
        risks: list[str] = []

        for result in results:
            for recommendation in result.recommendations:
                if recommendation not in actions:
                    actions.append(recommendation)
            if result.expert_id in {"skeptic", "safety"}:
                for observation in result.observations:
                    lowered = observation.lower()
                    if any(
                        marker in lowered
                        for marker in ("claim", "high-stakes", "missing", "overstrong", "risk")
                    ):
                        if observation not in risks:
                            risks.append(observation)

        confidences = [result.confidence for result in results]
        mean_confidence = fmean(confidences)
        spread = max(confidences) - min(confidences)
        consensus = max(0.0, min(1.0, mean_confidence - (spread * 0.25)))

        return Synthesis(
            summary=summaries,
            prioritized_actions=tuple(actions[:8]),
            risk_flags=tuple(risks[:6]),
            confidence=round(mean_confidence, 3),
            consensus=round(consensus, 3),
        )

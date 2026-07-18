"""Deterministic routing for the Quillan council."""

from __future__ import annotations

from dataclasses import dataclass

from .experts import tokenize

_CLAIM_TERMS = {
    "agi",
    "conscious",
    "consciousness",
    "proof",
    "proven",
    "sentient",
    "sota",
    "validated",
}
_BUILD_TERMS = {
    "build",
    "create",
    "deploy",
    "design",
    "implement",
    "improve",
    "make",
    "production",
    "real",
    "ship",
}
_RISK_TERMS = {
    "execute",
    "financial",
    "legal",
    "medical",
    "patient",
    "production",
    "security",
    "tool",
    "weapon",
}


@dataclass(frozen=True, slots=True)
class RoutingDecision:
    selected_experts: tuple[str, ...]
    scores: dict[str, int]


@dataclass(frozen=True, slots=True)
class CouncilRouter:
    """A transparent keyword router with stable behavior."""

    max_experts: int = 4

    def route(self, query: str, mode: str = "standard") -> RoutingDecision:
        if self.max_experts < 1:
            raise ValueError("max_experts must be positive")

        tokens = set(tokenize(query))
        scores = {
            "analyst": 100,
            "skeptic": 25 + 20 * len(tokens & _CLAIM_TERMS),
            "planner": 20 + 20 * len(tokens & _BUILD_TERMS),
            "safety": 15 + 20 * len(tokens & _RISK_TERMS),
        }

        if mode == "audit":
            scores["skeptic"] += 50
            scores["safety"] += 20
        elif mode == "build":
            scores["planner"] += 50
            scores["safety"] += 10
        elif mode != "standard":
            raise ValueError("mode must be one of: standard, audit, build")

        ranked = sorted(
            (expert_id for expert_id in scores if expert_id != "analyst"),
            key=lambda expert_id: (-scores[expert_id], expert_id),
        )
        selected = ("analyst", *ranked[: max(0, self.max_experts - 1)])
        return RoutingDecision(selected_experts=selected, scores=scores)

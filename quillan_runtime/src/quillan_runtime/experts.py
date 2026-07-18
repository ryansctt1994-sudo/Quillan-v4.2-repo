"""Deterministic expert implementations.

These experts are intentionally inspectable. They do not claim to be a trained
foundation model and they do not expose hidden chain-of-thought.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Protocol

from .domain import EvidenceRef, ExpertResult

_WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*")
_ABSOLUTE_TERMS = {
    "always",
    "breakthrough",
    "conscious",
    "consciousness",
    "definitive",
    "guaranteed",
    "perfect",
    "proven",
    "sentient",
    "sota",
    "unbeatable",
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
_HIGH_STAKES_TERMS = {
    "diagnosis",
    "financial",
    "legal",
    "medical",
    "medicine",
    "patient",
    "security",
    "self-harm",
    "weapon",
}


def tokenize(text: str) -> tuple[str, ...]:
    return tuple(token.lower() for token in _WORD_RE.findall(text))


def _prompt_evidence(detail: str, reliability: float = 0.7) -> tuple[EvidenceRef, ...]:
    return (
        EvidenceRef(
            source="user-query",
            detail=detail,
            kind="prompt-derived",
            reliability=reliability,
        ),
    )


class CouncilExpert(Protocol):
    """Interface implemented by all council experts."""

    expert_id: str
    role: str

    def analyze(
        self,
        query: str,
        context: Mapping[str, Any] | None = None,
    ) -> ExpertResult:
        """Analyze a query and return a structured result."""


@dataclass(frozen=True, slots=True)
class AnalystExpert:
    expert_id: str = "analyst"
    role: str = "requirements and structure"

    def analyze(
        self,
        query: str,
        context: Mapping[str, Any] | None = None,
    ) -> ExpertResult:
        tokens = tokenize(query)
        unique = len(set(tokens))
        has_question = "?" in query
        context_keys = sorted((context or {}).keys())

        observations = [
            f"Query contains {len(tokens)} tokens and {unique} unique terms.",
            "The request is interrogative." if has_question else "The request is action-oriented.",
        ]
        if context_keys:
            observations.append(f"Structured context supplied: {', '.join(context_keys)}.")

        recommendations = (
            "Define one executable outcome and its acceptance criteria.",
            "Separate verified behavior from proposed capability claims.",
            "Record inputs, outputs, version, and failure modes for reproducibility.",
        )
        return ExpertResult(
            expert_id=self.expert_id,
            role=self.role,
            summary="Converted the request into an implementation-oriented problem statement.",
            observations=tuple(observations),
            recommendations=recommendations,
            confidence=0.82,
            evidence=_prompt_evidence("Lexical and structural analysis of the submitted query."),
            limitations=("No external facts were retrieved by this deterministic expert.",),
        )


@dataclass(frozen=True, slots=True)
class SkepticExpert:
    expert_id: str = "skeptic"
    role: str = "claim verification and falsification"

    def analyze(
        self,
        query: str,
        context: Mapping[str, Any] | None = None,
    ) -> ExpertResult:
        tokens = set(tokenize(query))
        flagged = sorted(tokens & _ABSOLUTE_TERMS)
        observations: list[str] = []
        if flagged:
            observations.append(
                "Potentially overstrong claim language detected: " + ", ".join(flagged) + "."
            )
        else:
            observations.append("No obvious absolute or anthropomorphic claim terms detected.")
        observations.append("A claim is not verified until linked to a repeatable test and artifact.")

        recommendations = (
            "Replace status language with evidence-level language.",
            "Add a falsifiable test for each material capability claim.",
            "Fail closed when a required model, checkpoint, or dependency is missing.",
        )
        confidence = 0.9 if flagged else 0.76
        return ExpertResult(
            expert_id=self.expert_id,
            role=self.role,
            summary="Audited the wording for claims that exceed the available evidence.",
            observations=tuple(observations),
            recommendations=recommendations,
            confidence=confidence,
            evidence=_prompt_evidence("Claim terms found directly in the submitted query."),
            limitations=("Repository contents and external benchmarks are outside this expert's scope.",),
        )


@dataclass(frozen=True, slots=True)
class PlannerExpert:
    expert_id: str = "planner"
    role: str = "delivery planning"

    def analyze(
        self,
        query: str,
        context: Mapping[str, Any] | None = None,
    ) -> ExpertResult:
        tokens = set(tokenize(query))
        build_intent = bool(tokens & _BUILD_TERMS)
        observations = (
            "Build intent detected." if build_intent else "No explicit build verb detected.",
            "The first milestone should be small enough to test in CI.",
        )
        recommendations = (
            "Create a minimal typed runtime with one stable API contract.",
            "Add deterministic unit tests before introducing model-provider variability.",
            "Integrate one real provider behind an interface only after the baseline passes.",
            "Benchmark latency, failure rate, and answer quality on a fixed evaluation set.",
        )
        return ExpertResult(
            expert_id=self.expert_id,
            role=self.role,
            summary="Produced a staged path from concept to reproducible software.",
            observations=observations,
            recommendations=recommendations,
            confidence=0.86 if build_intent else 0.72,
            evidence=_prompt_evidence("Delivery intent inferred from action verbs in the query."),
            limitations=("Effort and cost estimates require repository and infrastructure measurements.",),
        )


@dataclass(frozen=True, slots=True)
class SafetyExpert:
    expert_id: str = "safety"
    role: str = "risk and operational controls"

    def analyze(
        self,
        query: str,
        context: Mapping[str, Any] | None = None,
    ) -> ExpertResult:
        tokens = set(tokenize(query))
        high_stakes = sorted(tokens & _HIGH_STAKES_TERMS)
        observations: list[str] = []
        if high_stakes:
            observations.append("High-stakes domain terms detected: " + ", ".join(high_stakes) + ".")
        else:
            observations.append("No explicit high-stakes domain term detected.")
        observations.append("External actions should require explicit authorization and audit logging.")

        recommendations = (
            "Keep network, filesystem, and code-execution tools disabled by default.",
            "Apply input limits, timeouts, and structured error handling at the API boundary.",
            "Log decisions and provenance without storing hidden reasoning or secrets.",
        )
        return ExpertResult(
            expert_id=self.expert_id,
            role=self.role,
            summary="Defined minimum operational controls for a safe runtime.",
            observations=tuple(observations),
            recommendations=recommendations,
            confidence=0.88 if high_stakes else 0.78,
            evidence=_prompt_evidence("Risk classification derived from submitted query terms."),
            limitations=("This is an engineering risk screen, not legal or domain-specific advice.",),
        )


def default_experts() -> dict[str, CouncilExpert]:
    """Return the built-in expert registry."""

    experts: tuple[CouncilExpert, ...] = (
        AnalystExpert(),
        SkepticExpert(),
        PlannerExpert(),
        SafetyExpert(),
    )
    return {expert.expert_id: expert for expert in experts}

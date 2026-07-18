import pytest

from quillan_runtime import CouncilOrchestrator
from quillan_runtime.router import CouncilRouter


def test_router_selects_builder_and_skeptic_for_claimed_product() -> None:
    decision = CouncilRouter(max_experts=4).route(
        "Make this validated conscious AGI system real and production ready.",
        mode="build",
    )

    assert decision.selected_experts[0] == "analyst"
    assert "planner" in decision.selected_experts
    assert "skeptic" in decision.selected_experts
    assert "safety" in decision.selected_experts


def test_orchestrator_is_structured_and_trace_is_deterministic() -> None:
    orchestrator = CouncilOrchestrator()
    first = orchestrator.run(
        "Build a reproducible council runtime.",
        mode="build",
        context={"repository": "example/project"},
    )
    second = orchestrator.run(
        "Build a reproducible council runtime.",
        mode="build",
        context={"repository": "example/project"},
    )

    assert first.trace_id == second.trace_id
    assert first.selected_experts == second.selected_experts
    assert first.status.value == "experimental"
    assert first.synthesis.prioritized_actions
    assert 0.0 <= first.synthesis.consensus <= 1.0


def test_blank_query_is_rejected() -> None:
    orchestrator = CouncilOrchestrator()

    with pytest.raises(ValueError, match="blank"):
        orchestrator.run("   ")

from fastapi.testclient import TestClient

from quillan_runtime.api import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["evidence_status"] == "experimental"


def test_council_endpoint_returns_auditable_shape() -> None:
    response = client.post(
        "/v1/council",
        json={
            "query": "Audit the claims and create a real implementation plan.",
            "mode": "audit",
            "context": {"artifact": "README.md"},
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["trace_id"]
    assert payload["status"] == "experimental"
    assert "skeptic" in payload["selected_experts"]
    assert payload["expert_results"]
    assert payload["synthesis"]["prioritized_actions"]
    assert "thinking" not in payload

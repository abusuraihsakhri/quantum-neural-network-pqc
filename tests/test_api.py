"""HTTP integration tests for the FastAPI service."""
from fastapi.testclient import TestClient

from agents.api import app


def test_health_and_metrics_endpoints():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "HEALTHY"
    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.json()["system_status"] == "RUNNING"


def test_audit_endpoint_returns_rule_dossier():
    client = TestClient(app)
    response = client.post("/api/audit", json={
        "task_id": "HTTP-01", "target_identifier": "KEY-001",
        "primary_metric": 26, "secondary_metric": 0,
        "status_descriptor": "NOMINAL", "is_critical_flag": False
    })
    assert response.status_code == 200
    payload = response.json()
    assert payload["overall_urgency"] == "ELEVATED_RISK"
    assert payload["total_alerts"] == 1
    assert isinstance(payload["audit_hash"], str)


def test_api_rejects_phi_and_nonfinite_metrics():
    client = TestClient(app)
    base = {"task_id": "HTTP-02", "target_identifier": "KEY-002", "primary_metric": 5}
    response = client.post("/api/audit", json={**base, "target_identifier": "MRN-123456"})
    assert response.status_code == 422
    assert "Sensitive identifier" in response.json()["detail"]
    response = client.post("/api/audit", json={**base, "primary_metric": "NaN"})
    assert response.status_code == 422


def test_chat_rejects_sensitive_identifiers():
    client = TestClient(app)
    response = client.post("/api/chat", json={"query": "Patient MRN-123456"})
    assert response.status_code == 422
    assert "Sensitive identifier" in response.json()["detail"]

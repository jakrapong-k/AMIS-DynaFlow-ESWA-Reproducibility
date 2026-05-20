from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_login_mock_response() -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": "not-a-real-password"},
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_runs_routes_shape() -> None:
    create_resp = client.post(
        "/api/v1/runs",
        json={"run_type": "full_pipeline", "input_ref": "sample_dataset_v1", "config": {"seed": 42}},
    )
    assert create_resp.status_code == 202
    assert create_resp.json()["status"] == "queued"

    list_resp = client.get("/api/v1/runs")
    assert list_resp.status_code == 200
    assert list_resp.json()["items"] == []


def test_run_not_found_uses_error_model() -> None:
    response = client.get("/api/v1/runs/invalid-id")
    assert response.status_code == 404
    payload = response.json()
    assert payload["error"]["code"] == "HTTP_404"


def test_dashboard_routes() -> None:
    summary_resp = client.get("/api/v1/dashboard/summary")
    trends_resp = client.get("/api/v1/dashboard/trends")
    assert summary_resp.status_code == 200
    assert trends_resp.status_code == 200

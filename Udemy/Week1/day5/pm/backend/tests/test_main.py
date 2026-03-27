from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_serves_html() -> None:
    """Test that root endpoint returns HTML (either static fallback or built frontend)."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


def test_hello_endpoint_returns_expected_payload() -> None:
    """Test that /api/hello returns expected JSON response."""
    response = client.get("/api/hello")
    assert response.status_code == 200
    assert response.json() == {
        "message": "hello world from fastapi",
        "status": "ok",
    }


def test_api_namespace_isolation() -> None:
    """Test that /api routes are separate from static file serving."""
    # /api/hello should be served by FastAPI
    api_response = client.get("/api/hello")
    assert api_response.status_code == 200
    assert api_response.headers["content-type"] == "application/json"
    
    # Root should serve HTML (not JSON)
    root_response = client.get("/")
    assert root_response.status_code == 200
    assert "text/html" in root_response.headers.get("content-type", "")

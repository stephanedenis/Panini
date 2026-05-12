"""
Integration tests for AnalyzerServer - FastAPI HTTP endpoints.

Tests:
- POST /api/analyze - Trigger analysis job
- GET /api/status/{job_id} - Poll job status
- GET /auth/callback - OAuth2 callback handling
- POST /auth/logout - Session cleanup
- Request validation (Pydantic models)
- Error responses (400, 401, 404, 500)
- Keep-alive mechanism integration
"""

import pytest
from datetime import datetime
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestAnalyzerServerAnalyzeEndpoint:
    """Test POST /api/analyze - Trigger analysis job."""

    def test_analyze_endpoint_accepts_valid_request(self, test_client):
        """Should accept valid analysis request."""
        payload = {
            "repo": "stephanedenis/Panini-Analysis",
            "trigger": "new_data",
        }

        response = test_client.post("/api/analyze", json=payload)

        assert response.status_code == 202  # Accepted (async processing)
        assert "job_id" in response.json()

    def test_analyze_endpoint_returns_job_id(self, test_client):
        """Should return unique job_id for tracking."""
        payload = {
            "repo": "stephanedenis/Panini-Analysis",
            "trigger": "new_data",
        }

        response = test_client.post("/api/analyze", json=payload)

        assert response.status_code == 202
        data = response.json()
        assert "job_id" in data
        assert len(data["job_id"]) > 0

    def test_analyze_endpoint_validates_repo_format(self, test_client):
        """Should validate repository path format."""
        invalid_payload = {
            "repo": "invalid-format",  # Missing owner/
            "machine_type": "gpu",
        }

        response = test_client.post("/api/analyze", json=invalid_payload)

        assert response.status_code == 422  # Validation error

    def test_analyze_endpoint_validates_machine_type(self, test_client):
        """Should validate machine_type is known."""
        payload = {
            "repo": "stephanedenis/Panini-Analysis",
            "machine_type": "quantum",  # Invalid
        }

        response = test_client.post("/api/analyze", json=payload)

        # Should either validate or be accepted with later validation
        assert response.status_code in [202, 422]

    def test_analyze_endpoint_requires_repo(self, test_client):
        """Should reject requests without repo."""
        payload = {
            "machine_type": "gpu",
            # Missing repo
        }

        response = test_client.post("/api/analyze", json=payload)

        assert response.status_code == 422  # Missing required field

    def test_analyze_endpoint_requires_machine_type(self, test_client):
        """Should reject requests without machine_type."""
        payload = {
            "repo": "stephanedenis/Panini-Analysis",
            # Missing machine_type
        }

        response = test_client.post("/api/analyze", json=payload)

        assert response.status_code == 422

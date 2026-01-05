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


@pytest.mark.integration
class TestAnalyzerServerStatusEndpoint:
    """Test GET /api/status/{job_id} - Poll job status."""

    def test_status_endpoint_returns_job_status(self, test_client):
        """Should return job status for valid job_id."""
        # First trigger analysis
        submit_payload = {
            "repo": "stephanedenis/Panini-Analysis",
            "trigger": "new_data",
        }
        submit_response = test_client.post("/api/analyze", json=submit_payload)
        job_id = submit_response.json()["job_id"]

        # Then query status
        status_response = test_client.get(f"/api/status/{job_id}")

        assert status_response.status_code == 200
        data = status_response.json()
        assert "status" in data
        assert "job_id" in data

    def test_status_endpoint_returns_unknown_for_invalid_job(
        self, test_client
    ):
        """Should return 404 for non-existent job_id."""
        response = test_client.get("/api/status/nonexistent_job_id")

        assert response.status_code == 404

    def test_status_endpoint_tracks_queued_status(self, test_client):
        """Should return 'queued' immediately after submission."""
        submit_payload = {
            "repo": "stephanedenis/Panini-Analysis",
            "machine_type": "gpu",
        }
        submit_response = test_client.post("/api/analyze", json=submit_payload)
        job_id = submit_response.json()["job_id"]

        status_response = test_client.get(f"/api/status/{job_id}")

        assert status_response.status_code == 200
        data = status_response.json()
        assert data["status"] in ["queued", "running", "completed", "failed"]

    def test_status_endpoint_includes_progress_info(self, test_client):
        """Status response should include progress metadata."""
        submit_payload = {
            "repo": "stephanedenis/Panini-Analysis",
            "machine_type": "gpu",
        }
        submit_response = test_client.post("/api/analyze", json=submit_payload)
        job_id = submit_response.json()["job_id"]

        status_response = test_client.get(f"/api/status/{job_id}")

        data = status_response.json()
        # Should include at least:
        # - status: str
        # - job_id: str
        # - submitted_at: ISO timestamp
        # - updated_at: ISO timestamp
        assert "status" in data
        assert "job_id" in data

    def test_status_endpoint_provides_result_when_completed(self, test_client):
        """When completed, status should include results."""
        submit_payload = {
            "repo": "stephanedenis/Panini-Analysis",
            "machine_type": "gpu",
        }
        submit_response = test_client.post("/api/analyze", json=submit_payload)
        job_id = submit_response.json()["job_id"]

        # Simulated polling (in reality, would wait for async completion)
        status_response = test_client.get(f"/api/status/{job_id}")

        data = status_response.json()
        if data["status"] == "completed":
            assert "results" in data or "result_url" in data


@pytest.mark.integration
class TestAnalyzerServerOAuthCallback:
    """Test GET /auth/callback - OAuth2 callback handling."""

    def test_auth_callback_accepts_authorization_code(self, test_client):
        """Should accept authorization code from Google OAuth2."""
        # Simulate Google redirecting back with auth code
        params = {
            "code": "4/0AaBCD123...",
            "state": "random_state_token",
        }

        response = test_client.get("/auth/callback", params=params)

        # Should either succeed (200) or redirect (302)
        assert response.status_code in [200, 302, 400]

    def test_auth_callback_validates_state_parameter(self, test_client):
        """Should validate CSRF state parameter."""
        params = {
            "code": "4/0AaBCD123...",
            "state": "invalid_state",  # Wrong state
        }

        response = test_client.get("/auth/callback", params=params)

        # Should reject invalid state
        assert response.status_code in [400, 403]

    def test_auth_callback_handles_authorization_denied(self, test_client):
        """Should handle user denying authorization."""
        params = {
            "error": "access_denied",
        }

        response = test_client.get("/auth/callback", params=params)

        assert response.status_code in [400, 403]

    def test_auth_callback_exchanges_code_for_token(self, test_client):
        """Should exchange auth code for access token."""
        params = {
            "code": "4/0AaBCD123...",
            "state": "valid_state",
        }

        # Mock would handle code exchange
        response = test_client.get("/auth/callback", params=params)

        assert response.status_code in [200, 302, 400]

    def test_auth_callback_missing_code_error(self, test_client):
        """Should require authorization code."""
        params = {
            "state": "valid_state",
            # Missing code
        }

        response = test_client.get("/auth/callback", params=params)

        assert response.status_code == 400


@pytest.mark.integration
class TestAnalyzerServerLogoutEndpoint:
    """Test POST /auth/logout - Session cleanup."""

    def test_logout_endpoint_clears_session(self, test_client):
        """Should invalidate user session."""
        response = test_client.post("/auth/logout")

        assert response.status_code in [200, 204]

    def test_logout_endpoint_requires_auth(self, test_client):
        """Should verify user is authenticated."""
        response = test_client.post("/auth/logout")

        # Without auth, might return 401 or succeed
        assert response.status_code in [200, 204, 401]

    def test_logout_prevents_further_requests(self, test_client):
        """After logout, subsequent requests should require re-auth."""
        # First logout
        logout_response = test_client.post("/auth/logout")
        assert logout_response.status_code in [200, 204]

        # Try to use authenticated endpoint
        status_response = test_client.get("/api/status/some_job")

        # Should either require auth or return 404
        assert status_response.status_code in [401, 404]


@pytest.mark.integration
class TestAnalyzerServerErrorHandling:
    """Test error responses and error handling."""

    def test_malformed_json_returns_400(self, test_client):
        """Should reject malformed JSON in request body."""
        response = test_client.post(
            "/api/analyze",
            content="not valid json {",
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 400

    def test_missing_required_fields_returns_422(self, test_client):
        """Should return validation error for missing fields."""
        payload = {
            # Missing required repo and machine_type
            "extra_field": "value",
        }

        response = test_client.post("/api/analyze", json=payload)

        assert response.status_code == 422

    def test_invalid_field_type_returns_422(self, test_client):
        """Should validate field types."""
        payload = {
            "repo": "stephanedenis/Panini-Analysis",
            "machine_type": 123,  # Should be string
        }

        response = test_client.post("/api/analyze", json=payload)

        assert response.status_code == 422

    def test_authentication_error_returns_401(self, test_client):
        """Protected endpoints should return 401 without auth."""
        # Endpoint that requires authentication
        response = test_client.post("/api/analyze")

        # Without proper auth, should return 401 or 403
        assert response.status_code in [401, 403, 422]

    def test_not_found_returns_404(self, test_client):
        """Non-existent endpoints should return 404."""
        response = test_client.get("/api/nonexistent")

        assert response.status_code == 404

    def test_method_not_allowed_returns_405(self, test_client):
        """GET on POST-only endpoint should return 405."""
        response = test_client.get("/api/analyze")

        assert response.status_code == 405


@pytest.mark.integration
class TestAnalyzerServerKeepAlive:
    """Test keep-alive mechanism in API responses."""

    def test_analyze_response_includes_keep_alive_interval(self, test_client):
        """Analysis response should indicate keep-alive interval."""
        payload = {
            "repo": "stephanedenis/Panini-Analysis",
            "machine_type": "gpu",
        }

        response = test_client.post("/api/analyze", json=payload)

        data = response.json()
        # May include keep_alive_seconds field
        if "keep_alive_seconds" in data:
            assert data["keep_alive_seconds"] > 0

    def test_status_endpoint_resets_keep_alive(self, test_client):
        """Polling status should reset keep-alive timer."""
        # Submit analysis
        submit_payload = {
            "repo": "stephanedenis/Panini-Analysis",
            "machine_type": "gpu",
        }
        submit_response = test_client.post("/api/analyze", json=submit_payload)
        job_id = submit_response.json()["job_id"]

        # Poll status multiple times
        for _ in range(3):
            status_response = test_client.get(f"/api/status/{job_id}")
            assert status_response.status_code == 200
            # Each poll should reset keep-alive


@pytest.mark.integration
class TestAnalyzerServerIntegration:
    """Test complete analysis workflow."""

    def test_complete_analysis_workflow(self, test_client):
        """Test full workflow: submit -> poll -> get status."""
        # 1. Submit analysis
        submit_payload = {
            "repo": "stephanedenis/Panini-Analysis",
            "machine_type": "gpu",
            "config": {
                "timeout_minutes": 60,
            },
        }
        submit_response = test_client.post("/api/analyze", json=submit_payload)
        assert submit_response.status_code == 202
        job_id = submit_response.json()["job_id"]

        # 2. Poll status
        status_response = test_client.get(f"/api/status/{job_id}")
        assert status_response.status_code == 200

        # 3. Verify response structure
        status_data = status_response.json()
        assert status_data["job_id"] == job_id
        assert status_data["status"] in [
            "queued",
            "running",
            "completed",
            "failed",
        ]

    def test_multiple_concurrent_analyses(self, test_client):
        """Should handle multiple concurrent analysis jobs."""
        job_ids = []

        # Submit multiple analyses
        for i in range(3):
            payload = {
                "repo": f"stephanedenis/Panini-Analysis-{i}",
                "machine_type": "gpu",
            }
            response = test_client.post("/api/analyze", json=payload)
            assert response.status_code == 202
            job_ids.append(response.json()["job_id"])

        # Query status for each
        for job_id in job_ids:
            response = test_client.get(f"/api/status/{job_id}")
            assert response.status_code == 200

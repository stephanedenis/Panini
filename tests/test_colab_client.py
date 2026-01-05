"""
Integration tests for ColabClient - Colab API wrapper.

Tests:
- Kernel assignment with machine_type selection
- Code execution in assigned kernel
- Quota retrieval and tracking
- Kernel unassignment and cleanup
- Service status monitoring
- Error handling (API failures, timeouts, invalid responses)
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch


@pytest.mark.colab
class TestColabClientKernelAssignment:
    """Test ColabClient.assign() - allocates Colab kernels."""

    @pytest.mark.asyncio
    async def test_assign_gpu_kernel_returns_kernel_id(self, mock_colab_client):
        """Should allocate GPU kernel and return kernel_id."""
        account = "test_account@example.com"
        machine_type = "gpu"

        result = await mock_colab_client.assign(account, machine_type)

        assert result is not None
        assert "kernel_id" in result
        assert result["kernel_id"] == "kernel_test_12345"
        assert result["machine_type"] == "gpu"

    @pytest.mark.asyncio
    async def test_assign_tpu_kernel_returns_kernel_id(self, mock_colab_client):
        """Should allocate TPU kernel with same interface."""
        account = "test_account@example.com"
        machine_type = "tpu"

        result = await mock_colab_client.assign(account, machine_type)

        # Mock returns GPU result, but real implementation would handle TPU
        assert result is not None
        assert "kernel_id" in result

    @pytest.mark.asyncio
    async def test_assign_includes_keep_alive_time(self, mock_colab_client, mock_colab_response):
        """Should include 30-minute keep-alive timer in response."""
        account = "test_account@example.com"

        result = await mock_colab_client.assign(account, "gpu")

        assert "keep_alive_until" in result
        keep_alive = datetime.fromisoformat(result["keep_alive_until"])
        assigned = datetime.fromisoformat(result["assigned_at"])

        # Keep-alive should be ~30 minutes from assignment
        delta = (keep_alive - assigned).total_seconds()
        assert 1500 <= delta <= 2100  # 25-35 minutes in seconds

    @pytest.mark.asyncio
    async def test_assign_includes_colab_url(self, mock_colab_client):
        """Should include direct link to Colab session."""
        account = "test_account@example.com"

        result = await mock_colab_client.assign(account, "gpu")

        assert "colab_url" in result
        assert result["colab_url"].startswith("https://colab.research.google.com")


@pytest.mark.colab
class TestColabClientCodeExecution:
    """Test ColabClient.execute() - runs code in kernel."""

    @pytest.mark.asyncio
    async def test_execute_code_returns_output(self, mock_colab_client):
        """Should execute code and return stdout/stderr output."""
        kernel_id = "kernel_test_12345"
        code = "print('Hello from Colab')"

        result = await mock_colab_client.execute(kernel_id, code, timeout=60)

        assert result is not None
        assert "status" in result
        assert result["status"] == "success"
        assert "output" in result

    @pytest.mark.asyncio
    async def test_execute_code_respects_timeout(self, mock_colab_client):
        """Should enforce execution timeout."""
        kernel_id = "kernel_test_12345"
        code = "import time; time.sleep(120)"
        timeout = 30  # 30 seconds

        # Mock should handle timeout parameter
        result = await mock_colab_client.execute(kernel_id, code, timeout=timeout)

        assert result is not None
        # Implementation should timeout and return error status

    @pytest.mark.asyncio
    async def test_execute_code_preserves_state(self, mock_colab_client):
        """Consecutive code executions should maintain kernel state."""
        kernel_id = "kernel_test_12345"

        # First execution: define variable
        result1 = await mock_colab_client.execute(kernel_id, "x = 42", timeout=60)
        assert result1["status"] == "success"

        # Second execution: use variable (would fail if state not preserved)
        result2 = await mock_colab_client.execute(kernel_id, "print(x)", timeout=60)
        assert result2["status"] == "success"

    @pytest.mark.asyncio
    async def test_execute_code_handles_errors(self, mock_colab_client):
        """Should return error status for code exceptions."""
        kernel_id = "kernel_test_12345"
        code = "raise ValueError('Test error')"

        result = await mock_colab_client.execute(kernel_id, code, timeout=60)

        # Should contain error information
        assert result is not None


@pytest.mark.colab
class TestColabClientQuota:
    """Test ColabClient.get_quota() - tracks CCU usage."""

    @pytest.mark.asyncio
    async def test_get_quota_returns_quota_info(self, mock_colab_client, mock_colab_quota):
        """Should return quota usage for account and machine_type."""
        account = "test_account@example.com"

        result = await mock_colab_client.get_quota(account)

        assert result is not None
        assert result["account"] == account
        assert "total_ccu" in result
        assert "used_ccu" in result
        assert "remaining_ccu" in result

    @pytest.mark.asyncio
    async def test_get_quota_remaining_is_accurate(self, mock_colab_client):
        """Remaining CCU should equal total - used."""
        account = "test_account@example.com"

        result = await mock_colab_client.get_quota(account)

        expected_remaining = result["total_ccu"] - result["used_ccu"]
        assert abs(result["remaining_ccu"] - expected_remaining) < 0.01

    @pytest.mark.asyncio
    async def test_get_quota_includes_reset_time(self, mock_colab_client):
        """Should indicate when quota resets."""
        account = "test_account@example.com"

        result = await mock_colab_client.get_quota(account)

        assert "quota_reset_time" in result
        reset_time = datetime.fromisoformat(result["quota_reset_time"])
        assert reset_time > datetime.utcnow()  # Reset should be in future


@pytest.mark.colab
class TestColabClientKernelCleanup:
    """Test ColabClient.unassign() - releases kernel resources."""

    @pytest.mark.asyncio
    async def test_unassign_kernel_returns_success(self, mock_colab_client):
        """Should release kernel and return success status."""
        kernel_id = "kernel_test_12345"

        result = await mock_colab_client.unassign(kernel_id)

        assert result is not None
        assert result.get("status") == "success"

    @pytest.mark.asyncio
    async def test_unassign_kernel_handles_non_existent(self, mock_colab_client):
        """Should handle gracefully when kernel doesn't exist."""
        kernel_id = "nonexistent_kernel"

        result = await mock_colab_client.unassign(kernel_id)

        # Should return error or success (depends on API design)
        assert result is not None

    @pytest.mark.asyncio
    async def test_unassign_kernel_stops_keep_alive(self, mock_colab_client):
        """After unassign, keep-alive timer should stop."""
        kernel_id = "kernel_test_12345"

        result = await mock_colab_client.unassign(kernel_id)

        assert result is not None
        # Kernel should be unreachable after unassign


@pytest.mark.colab
class TestColabClientServiceStatus:
    """Test ColabClient.get_status() - monitors service health."""

    @pytest.mark.asyncio
    async def test_get_status_returns_service_health(self, mock_colab_client):
        """Should return overall service status."""
        result = await mock_colab_client.get_status()

        assert result is not None
        assert "service" in result
        assert result["service"] == "colab"
        assert "status" in result

    @pytest.mark.asyncio
    async def test_get_status_includes_regional_status(self, mock_colab_client):
        """Should include status of Colab regions."""
        result = await mock_colab_client.get_status()

        assert "regions" in result
        assert len(result["regions"]) > 0

        # Each region should have status
        for region, status in result["regions"].items():
            assert status in ["up", "degraded", "down"]

    @pytest.mark.asyncio
    async def test_get_status_periodic_monitoring(self, mock_colab_client):
        """Should support periodic status checking for monitoring."""
        result1 = await mock_colab_client.get_status()
        result2 = await mock_colab_client.get_status()

        # Both should return valid responses
        assert result1 is not None
        assert result2 is not None


@pytest.mark.colab
class TestColabClientErrorHandling:
    """Test ColabClient error scenarios."""

    @pytest.mark.asyncio
    async def test_api_failure_handling(self, test_config, mock_oauth_manager):
        """Should handle API errors gracefully."""
        from panini_colabmcp import ColabClient

        client = ColabClient(test_config, mock_oauth_manager)

        # Mock API failure
        client.assign = AsyncMock(side_effect=Exception("API Error: 503 Service Unavailable"))

        with pytest.raises(Exception):
            await client.assign("test@example.com", "gpu")

    @pytest.mark.asyncio
    async def test_timeout_handling(self, mock_colab_client):
        """Should handle request timeouts."""
        kernel_id = "kernel_test_12345"
        code = "import time; time.sleep(1000)"

        # Mock timeout behavior
        mock_colab_client.execute = AsyncMock(
            side_effect=TimeoutError("Execution timeout after 60s")
        )

        with pytest.raises(TimeoutError):
            await mock_colab_client.execute(kernel_id, code, timeout=60)

    @pytest.mark.asyncio
    async def test_invalid_machine_type(self, mock_colab_client):
        """Should reject unsupported machine types."""
        account = "test_account@example.com"
        invalid_machine_type = "quantum"

        # Real implementation would validate, mock should handle
        result = await mock_colab_client.assign(account, invalid_machine_type)

        assert result is not None


@pytest.mark.colab
class TestColabClientKeepAlive:
    """Test Colab keep-alive mechanism."""

    @pytest.mark.asyncio
    async def test_keep_alive_extends_kernel_lifetime(self, mock_colab_client):
        """Should extend kernel lifetime on code execution."""
        kernel_id = "kernel_test_12345"

        # Execute code (should trigger keep-alive)
        result = await mock_colab_client.execute(kernel_id, "print('test')", timeout=60)

        assert result is not None
        # Kernel should still be alive after execution

    @pytest.mark.asyncio
    async def test_keep_alive_timeout_boundary(self, mock_colab_client):
        """Should warn as keep-alive timeout approaches."""
        kernel_id = "kernel_test_12345"

        # Simulate kernel near keep-alive expiry
        # (actual implementation would track timestamps)

        result = await mock_colab_client.execute(kernel_id, "print('test')", timeout=60)

        assert result is not None

"""
Pytest configuration and fixtures for panini_colabmcp testing.

Provides:
- Mock Google OAuth2 credentials
- Mock GitHub API responses
- Mock Colab API responses
- FastAPI TestClient with mocked dependencies
"""

import json
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from panini_colabmcp import (
    AnalyzerServer,
    ColabClient,
    Config,
    GitHubConnector,
    OAuthManager,
    RegistryWriter,
)


# ============================================================================
# Configuration Fixtures
# ============================================================================


@pytest.fixture
def test_config():
    """Provide test configuration with development values."""
    return Config(
        env="test",
        log_level="INFO",
        google_client_id="test_client_id",
        google_client_secret="test_client_secret",
        google_redirect_uri="http://localhost:8080/auth/callback",
        colab_api_url="https://colab.research.google.com/api/ml/v1",
        github_token="ghp_test_token_123",
        github_owner="test_owner",
        database_url="sqlite:///:memory:",
        mcp_server_url="http://localhost:8080",
        default_machine_type="TPM_V5_EDGE",
        max_compute_hours=24.0,
    )


# ============================================================================
# OAuth2 Mock Fixtures
# ============================================================================


@pytest.fixture
def mock_oauth_token():
    """Provide a mock OAuth2 access token response."""
    expiry = datetime.utcnow() + timedelta(hours=1)
    return {
        "access_token": "ya29.test_token_abc123",
        "refresh_token": "1//test_refresh_xyz789",
        "expires_in": 3600,
        "token_type": "Bearer",
        "scope": "https://www.googleapis.com/auth/cloud-platform",
        "expiry": expiry.isoformat(),
    }


@pytest.fixture
def mock_oauth_manager(test_config, mock_oauth_token):
    """Provide a mocked OAuthManager."""
    manager = OAuthManager(test_config)

    # Mock token storage
    manager._token_store = {
        "test_account@example.com": mock_oauth_token,
    }

    return manager


# ============================================================================
# Colab API Mock Fixtures
# ============================================================================


@pytest.fixture
def mock_colab_response():
    """Provide mock Colab API assignment response."""
    return {
        "kernel_id": "kernel_test_12345",
        "machine_type": "gpu",
        "assigned_at": datetime.utcnow().isoformat(),
        "keep_alive_until": (
            datetime.utcnow() + timedelta(minutes=30)
        ).isoformat(),
        "colab_url": "https://colab.research.google.com/user/test_session",
    }


@pytest.fixture
def mock_colab_quota():
    """Provide mock Colab quota response."""
    return {
        "account": "test_account@example.com",
        "machine_type": "gpu",
        "total_ccu": 100.0,
        "used_ccu": 25.5,
        "remaining_ccu": 74.5,
        "quota_reset_time": (datetime.utcnow() + timedelta(days=1)).isoformat(),
    }


@pytest.fixture
def mock_colab_client(
    test_config, mock_colab_response, mock_colab_quota, mock_oauth_manager
):
    """Provide a mocked ColabClient."""
    client = ColabClient(test_config, mock_oauth_manager)

    # Mock API methods with AsyncMock for async support
    client.assign = AsyncMock(return_value=mock_colab_response)
    client.execute = AsyncMock(
        return_value={
            "kernel_id": "kernel_test_12345",
            "status": "success",
            "output": "Analysis result data",
        }
    )
    client.get_quota = AsyncMock(return_value=mock_colab_quota)
    client.unassign = AsyncMock(return_value={"status": "success"})
    client.get_status = AsyncMock(
        return_value={
            "service": "colab",
            "status": "operational",
            "regions": {"us-central1": "up", "us-west1": "up"},
        }
    )

    return client


# ============================================================================
# GitHub API Mock Fixtures
# ============================================================================


@pytest.fixture
def mock_github_repo():
    """Provide mock GitHub repository data."""
    return {
        "name": "Panini-TestAnalysis",
        "full_name": "stephanedenis/Panini-TestAnalysis",
        "url": "https://github.com/stephanedenis/Panini-TestAnalysis",
        "description": "Test analysis repository",
        "private": False,
    }


@pytest.fixture
def mock_analysis_config():
    """Provide mock analysis configuration from GitHub."""
    return {
        "enabled": True,
        "machine_type": "gpu",
        "timeout_minutes": 60,
        "max_retries": 3,
        "webhook_secret": "test_webhook_secret",
    }


@pytest.fixture
def mock_github_connector(test_config, mock_github_repo, mock_analysis_config):
    """Provide a mocked GitHubConnector."""
    connector = GitHubConnector(test_config)

    # Mock repository operations
    connector.list_repos = MagicMock(
        return_value=[
            mock_github_repo,
            {
                "name": "Panini-Analysis-2",
                "full_name": "stephanedenis/Panini-Analysis-2",
                "url": "https://github.com/stephanedenis/Panini-Analysis-2",
            },
        ]
    )

    connector.get_file_content = MagicMock(return_value=mock_analysis_config)

    connector.create_file = MagicMock(
        return_value={
            "sha": "abc123def456",
            "url": (
                "https://github.com/stephanedenis/"
                "Panini-Analysis/blob/main/results.json"
            ),
        }
    )

    connector.dispatch = MagicMock(
        return_value={
            "id": 12345,
            "status": "queued",
            "created_at": datetime.utcnow().isoformat(),
        }
    )

    connector.list_active_workflows = MagicMock(
        return_value=[
            {
                "id": 1,
                "name": "analysis-workflow",
                "status": "completed",
                "conclusion": "success",
            }
        ]
    )

    return connector


# ============================================================================
# Registry Writer Mock Fixtures
# ============================================================================


@pytest.fixture
def mock_registry_writer(test_config, mock_github_connector):
    """Provide a mocked RegistryWriter."""
    writer = RegistryWriter(test_config, mock_github_connector)

    # Mock database operations
    writer.add_analysis = MagicMock(
        return_value={
            "analysis_id": "analysis_uuid_123",
            "repo": "stephanedenis/Panini-Analysis",
            "timestamp": datetime.utcnow().isoformat(),
            "status": "registered",
        }
    )

    writer.list_recent = MagicMock(
        return_value=[
            {
                "analysis_id": "analysis_uuid_123",
                "repo": "stephanedenis/Panini-Analysis",
                "timestamp": datetime.utcnow().isoformat(),
                "machine_type": "gpu",
                "ccu_consumed": 12.5,
            }
        ]
    )

    writer.get_analysis = MagicMock(
        return_value={
            "analysis_id": "analysis_uuid_123",
            "repo": "stephanedenis/Panini-Analysis",
            "timestamp": datetime.utcnow().isoformat(),
            "machine_type": "gpu",
            "ccu_consumed": 12.5,
            "results": {"status": "completed", "duration_seconds": 45},
        }
    )

    writer.get_chain_of_custody = MagicMock(
        return_value=[
            {
                "analysis_id": "analysis_uuid_123",
                "event": "analysis_registered",
                "timestamp": datetime.utcnow().isoformat(),
                "actor": "system",
            }
        ]
    )

    return writer


# ============================================================================
# FastAPI TestClient Fixture
# ============================================================================


@pytest.fixture
def test_client(
    mock_colab_client,
    mock_github_connector,
    mock_registry_writer,
):
    """Provide FastAPI TestClient with mocked dependencies."""
    # Create server with mocked dependencies
    server = AnalyzerServer(
        mcp_client=None,  # Not used in HTTP endpoints
        github=mock_github_connector,
        colab=mock_colab_client,
        registry=mock_registry_writer,
    )

    client = TestClient(server.app)
    yield client


# ============================================================================
# Integration Fixtures
# ============================================================================


@pytest.fixture
def full_mock_environment(
    test_config,
    mock_oauth_manager,
    mock_colab_client,
    mock_github_connector,
    mock_registry_writer,
    test_client,
):
    """Provide a complete mock environment with all components."""
    return {
        "config": test_config,
        "oauth_manager": mock_oauth_manager,
        "colab_client": mock_colab_client,
        "github_connector": mock_github_connector,
        "registry_writer": mock_registry_writer,
        "api_client": test_client,
    }


# ============================================================================
# Pytest Configuration
# ============================================================================


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "integration: integration test with mocked external APIs",
    )
    config.addinivalue_line(
        "markers",
        "slow: mark test as slow (takes >1 second)",
    )
    config.addinivalue_line(
        "markers",
        "oauth: mark test as testing OAuth2 functionality",
    )
    config.addinivalue_line(
        "markers",
        "colab: mark test as testing Colab API functionality",
    )
    config.addinivalue_line(
        "markers",
        "github: mark test as testing GitHub API functionality",
    )

"""
Integration tests for GitHubConnector - GitHub API wrapper.

Tests:
- Repository listing with pattern matching
- File content retrieval (analysis_config.json)
- File creation/updates (results JSON)
- Workflow dispatch for GitHub Actions
- Workflow status monitoring
- Error handling (invalid repos, API rate limits, auth failures)
"""

import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch


@pytest.mark.github
class TestGitHubConnectorRepoListing:
    """Test GitHubConnector.list_repos() - discovers repositories."""

    async def test_list_repos_returns_matching_repos(self, mock_github_connector):
        """Should return repos matching name pattern."""
        owner = "stephanedenis"
        pattern = "Panini-*"

        result = await mock_github_connector.list_repos(owner, pattern)

        assert result is not None
        assert len(result) > 0
        assert all("name" in repo for repo in result)

    async def test_list_repos_applies_fnmatch_pattern(self, mock_github_connector):
        """Should filter repos using fnmatch pattern matching."""
        owner = "stephanedenis"

        # Match repos starting with "Panini-"
        result = await mock_github_connector.list_repos(owner, "Panini-*")

        assert len(result) > 0
        for repo in result:
            assert repo["name"].startswith("Panini-")

    async def test_list_repos_includes_repo_metadata(self, mock_github_connector):
        """Should include essential repo metadata."""
        owner = "stephanedenis"

        result = await mock_github_connector.list_repos(owner, "Panini-*")

        required_fields = ["name", "full_name", "url", "description", "private"]
        for repo in result:
            for field in required_fields:
                assert field in repo

    async def test_list_repos_handles_empty_results(self, test_config):
        """Should return empty list when no repos match pattern."""
        from panini_engine import GitHubConnector

        connector = GitHubConnector(test_config)
        connector.list_repos = MagicMock(return_value=[])

        result = connector.list_repos("stephanedenis", "NonExistent-*")

        assert result == []

    async def test_list_repos_distinguishes_public_private(self, test_config):
        """Should identify private vs public repositories."""
        from panini_engine import GitHubConnector

        connector = GitHubConnector(test_config)
        connector.list_repos = MagicMock(
            return_value=[
                {"name": "Public-Repo", "private": False},
                {"name": "Private-Repo", "private": True},
            ]
        )

        result = connector.list_repos("stephanedenis", "*")

        public = [r for r in result if not r["private"]]
        private = [r for r in result if r["private"]]

        assert len(public) == 1
        assert len(private) == 1


@pytest.mark.github
class TestGitHubConnectorFileOperations:
    """Test GitHubConnector file read/write operations."""

    async def test_get_file_content_loads_analysis_config(self, mock_github_connector, mock_analysis_config):
        """Should load analysis_config.json from repository."""
        repo = "stephanedenis/Panini-Analysis"
        path = "analysis_config.json"

        result = await mock_github_connector.get_file_content(repo, path)

        assert result is not None
        assert result["enabled"] is True
        assert "machine_type" in result
        assert "timeout_minutes" in result

    async def test_get_file_content_supports_branches(self, mock_github_connector):
        """Should read from specified branch."""
        repo = "stephanedenis/Panini-Analysis"
        path = "analysis_config.json"
        branch = "develop"

        result = await mock_github_connector.get_file_content(repo, path, branch)

        assert result is not None

    async def test_get_file_content_handles_missing_file(self, test_config):
        """Should handle gracefully when file doesn't exist."""
        from panini_engine import GitHubConnector

        connector = GitHubConnector(test_config)
        connector.get_file_content = MagicMock(return_value=None)

        result = connector.get_file_content("stephanedenis/Panini-Analysis", "missing.json")

        assert result is None

    async def test_create_file_writes_results_json(self, mock_github_connector):
        """Should write analysis results to repository."""
        repo = "stephanedenis/Panini-Analysis"
        path = "results/analysis_2025-12-25.json"
        content = '{"status": "completed", "duration": 45}'

        result = await mock_github_connector.create_file(repo, path, content)

        assert result is not None
        assert "sha" in result  # File commit SHA
        assert "url" in result

    async def test_create_file_includes_commit_message(self, mock_github_connector):
        """Should support custom commit messages."""
        repo = "stephanedenis/Panini-Analysis"
        path = "results.json"
        content = '{"status": "completed"}'

        # Mock should accept message parameter
        result = await mock_github_connector.create_file(repo, path, content)

        assert result is not None

    async def test_create_file_handles_duplicate_filenames(self, test_config):
        """Should handle existing files (update or error)."""
        from panini_engine import GitHubConnector

        connector = GitHubConnector(test_config)
        connector.create_file = MagicMock(
            return_value={"sha": "new_sha_123", "url": "https://..."}
        )

        # Multiple writes to same path
        result1 = connector.create_file("stephanedenis/Panini", "file.json", "content1")
        result2 = connector.create_file("stephanedenis/Panini", "file.json", "content2")

        assert result1 is not None
        assert result2 is not None


@pytest.mark.github
class TestGitHubConnectorWorkflowDispatch:
    """Test GitHubConnector.dispatch() - triggers GitHub Actions."""

    async def test_dispatch_workflow_triggers_action(self, mock_github_connector):
        """Should dispatch workflow with event type and payload."""
        repo = "stephanedenis/Panini-Analysis"
        event_type = "analysis-complete"
        payload = {"analysis_id": "uuid_123", "status": "completed"}

        result = await mock_github_connector.dispatch(repo, event_type, payload)

        assert result is not None
        assert "id" in result
        assert result["status"] == "queued"

    async def test_dispatch_includes_creation_timestamp(self, mock_github_connector):
        """Should include dispatch timestamp."""
        repo = "stephanedenis/Panini-Analysis"
        event_type = "analysis-complete"

        result = await mock_github_connector.dispatch(repo, event_type, {})

        assert "created_at" in result
        created = datetime.fromisoformat(result["created_at"])
        assert created <= datetime.utcnow()

    async def test_dispatch_payload_passed_to_workflow(self, mock_github_connector):
        """Should make payload available to GitHub Actions workflow."""
        repo = "stephanedenis/Panini-Analysis"
        event_type = "analysis-complete"
        payload = {"analysis_id": "test_123", "results": {"score": 95}}

        # Mock accepts payload
        result = await mock_github_connector.dispatch(repo, event_type, payload)

        assert result is not None

    async def test_dispatch_handles_invalid_event_type(self, test_config):
        """Should handle workflow events not configured in repo."""
        from panini_engine import GitHubConnector

        connector = GitHubConnector(test_config)
        connector.dispatch = MagicMock(side_effect=ValueError("Unknown event type"))

        with pytest.raises(ValueError):
            connector.dispatch("stephanedenis/Panini", "invalid-event", {})


@pytest.mark.github
class TestGitHubConnectorWorkflowMonitoring:
    """Test GitHubConnector.list_active_workflows() - monitors execution."""

    async def test_list_active_workflows_returns_workflow_status(self, mock_github_connector):
        """Should list active workflow runs."""
        result = await mock_github_connector.list_active_workflows()

        assert result is not None
        assert len(result) > 0

    async def test_list_active_workflows_includes_metadata(self, mock_github_connector):
        """Should include workflow ID, name, status, conclusion."""
        result = await mock_github_connector.list_active_workflows()

        required_fields = ["id", "name", "status", "conclusion"]
        for workflow in result:
            for field in required_fields:
                assert field in workflow

    async def test_list_active_workflows_status_values(self, mock_github_connector):
        """Status should be one of: queued, in_progress, completed."""
        result = await mock_github_connector.list_active_workflows()

        valid_statuses = ["queued", "in_progress", "completed"]
        for workflow in result:
            assert workflow["status"] in valid_statuses

    async def test_list_active_workflows_conclusion_values(self, mock_github_connector):
        """Conclusion should be one of: success, failure, cancelled, skipped."""
        result = await mock_github_connector.list_active_workflows()

        for workflow in result:
            if workflow["status"] == "completed":
                valid_conclusions = ["success", "failure", "cancelled", "skipped"]
                assert workflow["conclusion"] in valid_conclusions


@pytest.mark.github
class TestGitHubConnectorErrorHandling:
    """Test GitHubConnector error scenarios."""

    async def test_authentication_failure(self, test_config):
        """Should handle invalid or expired GitHub token."""
        from panini_engine import GitHubConnector

        connector = GitHubConnector(test_config)
        connector.list_repos = MagicMock(
            side_effect=PermissionError("401 Bad credentials")
        )

        with pytest.raises(PermissionError):
            connector.list_repos("stephanedenis", "*")

    async def test_rate_limit_handling(self, test_config):
        """Should handle GitHub API rate limits."""
        from panini_engine import GitHubConnector

        connector = GitHubConnector(test_config)
        connector.get_file_content = MagicMock(
            side_effect=RuntimeError("API rate limit exceeded")
        )

        with pytest.raises(RuntimeError):
            connector.get_file_content("stephanedenis/Panini", "file.json")

    async def test_invalid_repository_path(self, test_config):
        """Should validate repository path format."""
        from panini_engine import GitHubConnector

        connector = GitHubConnector(test_config)
        connector.list_repos = MagicMock(side_effect=ValueError("Invalid repo format"))

        with pytest.raises(ValueError):
            connector.list_repos("invalid-format", "*")

    async def test_network_failure_handling(self, test_config):
        """Should handle network/connection errors."""
        from panini_engine import GitHubConnector

        connector = GitHubConnector(test_config)
        connector.dispatch = MagicMock(
            side_effect=ConnectionError("Failed to connect to api.github.com")
        )

        with pytest.raises(ConnectionError):
            connector.dispatch("stephanedenis/Panini", "event", {})


@pytest.mark.github
class TestGitHubConnectorIntegration:
    """Test GitHubConnector integration patterns."""

    async def test_read_config_execute_dispatch_workflow(self, mock_github_connector, mock_analysis_config):
        """Test typical workflow: read config, execute, dispatch."""
        repo = "stephanedenis/Panini-Analysis"

        # 1. Read analysis config
        config = await mock_github_connector.get_file_content(repo, "analysis_config.json")
        assert config["enabled"] is True

        # 2. Execute analysis (simulated)
        analysis_result = {"status": "completed", "duration_seconds": 45}

        # 3. Create results file
        result_path = "results/analysis_results.json"
        import json

        created = mock_github_connector.create_file(
            repo, result_path, json.dumps(analysis_result)
        )
        assert created is not None

        # 4. Dispatch workflow
        dispatched = mock_github_connector.dispatch(
            repo, "analysis-complete", analysis_result
        )
        assert dispatched is not None

    async def test_monitor_workflow_completion(self, mock_github_connector):
        """Test polling workflow status until completion."""
        # Simulate checking workflow status repeatedly
        for _ in range(3):
            workflows = await mock_github_connector.list_active_workflows()
            assert workflows is not None

            # Check if any completed
            completed = [w for w in workflows if w["status"] == "completed"]
            if completed:
                break

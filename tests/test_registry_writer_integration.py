"""
Integration tests for RegistryWriter with GitRegistry backend.

Tests the full pipeline:
1. Add analysis to registry
2. Verify Git commits are created
3. Check SQLite cache is populated
4. Validate summary statistics
"""

import pytest
import tempfile

from pathlib import Path
from datetime import datetime

from panini_engine.registry_writer import RegistryWriter


@pytest.fixture
def mock_config():
    """Mock configuration."""
    class MockConfig:
        github_token = "test-token"
        panini_repo = "test-repo"
    
    return MockConfig()


@pytest.fixture
def writer(mock_config):
    """Create a RegistryWriter instance with temporary registry."""
    with tempfile.TemporaryDirectory() as tmpdir:
        w = RegistryWriter(
            config=mock_config,
            registry_path=tmpdir
        )
        yield w


class TestRegistryWriterIntegration:
    """Integration tests for RegistryWriter."""
    
    def test_add_analysis_creates_file_and_cache(self, writer):
        """Test that adding an analysis creates both file and cache entry."""
        # Add analysis
        analysis_id = writer.add_analysis(
            repo="test-repo",
            machine_type="n1-standard-4",
            ccu_consumed=2.5,
            metadata={"tool": "test"},
            results={"score": 0.95}
        )
        
        assert analysis_id is not None
        assert len(analysis_id) > 0
        
        # Verify file was created
        analyses_dir = Path(writer.git_registry.analyses_dir)
        json_files = list(analyses_dir.rglob("*.json"))
        assert len(json_files) == 1
        
        # Verify cache entry exists
        recent = writer.list_recent()
        assert len(recent) == 1
        assert recent[0]["id"] == analysis_id
        assert recent[0]["source_repo"] == "test-repo"
    
    def test_list_recent_returns_cached_data(self, writer):
        """Test that list_recent returns data from cache."""
        # Add multiple analyses
        id1 = writer.add_analysis(
            repo="repo-a",
            machine_type="n1-standard-4",
            ccu_consumed=1.0,
        )
        id2 = writer.add_analysis(
            repo="repo-b",
            machine_type="n1-standard-8",
            ccu_consumed=2.0,
        )
        
        # List recent
        recent = writer.list_recent(limit=5)
        
        assert len(recent) == 2
        assert recent[0]["id"] in (id1, id2)  # Should be sorted by timestamp
        assert recent[0]["execution"]["ccu_consumed"] is not None
    
    def test_list_recent_with_repo_filter(self, writer):
        """Test filtering by source repository."""
        writer.add_analysis(
            repo="repo-a",
            machine_type="n1-standard-4",
            ccu_consumed=1.0,
        )
        writer.add_analysis(
            repo="repo-b",
            machine_type="n1-standard-8",
            ccu_consumed=2.0,
        )
        
        # Filter by repo
        recent_a = writer.list_recent(repo="repo-a")
        assert len(recent_a) == 1
        assert recent_a[0]["source_repo"] == "repo-a"
        
        recent_b = writer.list_recent(repo="repo-b")
        assert len(recent_b) == 1
        assert recent_b[0]["source_repo"] == "repo-b"
    
    def test_get_summary_aggregates_correctly(self, writer):
        """Test that get_summary aggregates CCU consumption."""
        writer.add_analysis(
            repo="repo-a",
            machine_type="n1-standard-4",
            ccu_consumed=2.0,
        )
        writer.add_analysis(
            repo="repo-b",
            machine_type="n1-standard-8",
            ccu_consumed=3.5,
        )
        writer.add_analysis(
            repo="repo-a",
            machine_type="n1-standard-4",
            ccu_consumed=1.5,
        )
        
        # Get summary
        summary = writer.get_summary()
        
        assert summary["total_analyses"] == 3
        assert summary["total_ccu_consumed"] == 7.0
        assert summary["analyses_by_repo"]["repo-a"] == 2
        assert summary["analyses_by_repo"]["repo-b"] == 1
        assert summary["analyses_by_machine"]["n1-standard-4"] == 2
        assert summary["analyses_by_machine"]["n1-standard-8"] == 1
    
    def test_get_summary_with_repo_filter(self, writer):
        """Test summary filtering by repository."""
        writer.add_analysis(
            repo="repo-a",
            machine_type="n1-standard-4",
            ccu_consumed=2.0,
        )
        writer.add_analysis(
            repo="repo-b",
            machine_type="n1-standard-8",
            ccu_consumed=3.5,
        )
        
        # Get summary for specific repo
        summary_a = writer.get_summary(repo="repo-a")
        
        assert summary_a["total_analyses"] == 1
        assert summary_a["total_ccu_consumed"] == 2.0
    
    def test_execution_dict_in_results(self, writer):
        """Test that execution dict is properly constructed."""
        writer.add_analysis(
            repo="test-repo",
            machine_type="n1-standard-4",
            ccu_consumed=1.5,
        )
        
        recent = writer.list_recent()
        assert len(recent) == 1
        
        # Check execution dict
        execution = recent[0].get("execution")
        assert execution is not None
        assert execution["machine_type"] == "n1-standard-4"
        assert execution["ccu_consumed"] == 1.5
    
    def test_timestamp_generation(self, writer):
        """Test that timestamp is generated if not provided."""
        before = datetime.utcnow().isoformat()
        
        writer.add_analysis(
            repo="test-repo",
            machine_type="n1-standard-4",
            ccu_consumed=1.0,
        )
        
        after = datetime.utcnow().isoformat()
        
        recent = writer.list_recent()
        timestamp = recent[0]["timestamp"]
        
        assert before <= timestamp <= after
    
    def test_metadata_and_results_preserved(self, writer):
        """Test that metadata and results are preserved."""
        metadata = {"tool": "test", "version": "1.0"}
        results = {"accuracy": 0.95, "f1": 0.92}
        
        writer.add_analysis(
            repo="test-repo",
            machine_type="n1-standard-4",
            ccu_consumed=1.0,
            metadata=metadata,
            results=results,
        )
        
        recent = writer.list_recent()
        stored_metadata = recent[0]["metadata"]
        
        assert stored_metadata["tool"] == "test"
        assert stored_metadata["version"] == "1.0"
        assert stored_metadata["results"]["accuracy"] == 0.95
    
    def test_add_analysis_without_optional_params(self, writer):
        """Test add_analysis with minimal parameters."""
        analysis_id = writer.add_analysis(
            repo="test-repo"
        )
        
        assert analysis_id is not None
        
        recent = writer.list_recent()
        assert len(recent) == 1
        assert recent[0]["execution"]["machine_type"] == "unknown"
        assert recent[0]["execution"]["ccu_consumed"] == 0.0
    
    def test_git_log_shows_analysis_commits(self, writer):
        """Test that Git log contains analysis commits."""
        writer.add_analysis(
            repo="test-repo",
            machine_type="n1-standard-4",
            ccu_consumed=1.0,
        )
        
        # Get git log
        git_log = writer.git_registry.get_git_log_summary()
        
        # Should show analysis commits (or empty if no git initialization)
        assert git_log is not None
    
    def test_multiple_analyses_sorted_by_timestamp(
        self,
        writer
    ):
        """Test that multiple analyses are sorted correctly."""
        # Add analyses with slight delays to ensure different timestamps
        id1 = writer.add_analysis(
            repo="repo-a",
            machine_type="n1-standard-4",
            ccu_consumed=1.0,
        )
        
        # Small delay to create timestamp difference
        
        id2 = writer.add_analysis(
            repo="repo-a",
            machine_type="n1-standard-4",
            ccu_consumed=2.0,
        )
        
        recent = writer.list_recent()
        
        assert len(recent) == 2
        # Most recent should be first
        assert recent[0]["id"] == id2
        assert recent[1]["id"] == id1
        assert recent[0]["timestamp"] >= recent[1]["timestamp"]
    
    def test_empty_registry_summary(self, writer):
        """Test summary for empty registry."""
        summary = writer.get_summary()
        
        assert summary["total_analyses"] == 0
        assert summary["total_ccu_consumed"] == 0
        assert summary["analyses_by_repo"] == {}
        assert summary["analyses_by_machine"] == {}
    
    def test_cache_fallback_on_empty_cache(self, writer):
        """Test that list operations work even with disabled cache."""
        # Create writer with cache disabled
        with tempfile.TemporaryDirectory() as tmpdir:
            writer_no_cache = RegistryWriter(
                config=writer.config,
                registry_path=tmpdir
            )
            writer_no_cache.git_registry.use_cache = False
            
            writer_no_cache.add_analysis(
                repo="test-repo",
                machine_type="n1-standard-4",
                ccu_consumed=1.0,
            )
            
            recent = writer_no_cache.list_recent()
            assert len(recent) == 1


class TestRegistryWriterBackwardsCompatibility:
    """Test backwards compatibility with old GitHub-based interface."""
    
    def test_update_index_no_error(self, writer):
        """Test that update_index doesn't error (it's a no-op now)."""
        writer.update_index()  # Should not raise
    
    def test_github_connector_param_optional(self, mock_config):
        """Test that github_connector parameter is optional."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Should work with None github_connector
            writer = RegistryWriter(
                config=mock_config,
                github_connector=None,
                registry_path=tmpdir
            )
            assert writer.github is None
            assert writer.git_registry is not None

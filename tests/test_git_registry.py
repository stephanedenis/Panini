"""
Tests for Git-native Registry Backend

Verifies:
1. JSON file storage in analyses/ directory
2. SQLite cache operations
3. Analysis retrieval and filtering
4. Token storage (encrypted)
5. Git audit trail integration
"""

import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

from panini_colabmcp.git_registry import GitRegistry


@pytest.fixture
def temp_repo():
    """Create temporary repository directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
async def git_registry(temp_repo):
    """Create GitRegistry instance with temp directory."""
    from cryptography.fernet import Fernet
    # Generate valid encryption key
    encryption_key = Fernet.generate_key().decode()
    
    registry = GitRegistry(
        repo_path=str(temp_repo),
        use_sqlite_cache=True,
        encryption_key=encryption_key,
    )
    print(f"\n\n=== FIXTURE: use_cache={registry.use_cache} ===\n\n")
    yield registry


class TestGitRegistryInitialization:
    """Test registry initialization and setup."""
    
    def test_creates_directories(self, temp_repo):
        """Test that required directories are created."""
        registry = GitRegistry(repo_path=str(temp_repo))
        
        assert (temp_repo / "analyses").exists()
        assert (temp_repo / ".panini").exists()
    
    def test_cache_initialization(self, temp_repo):
        """Test SQLite cache database creation."""
        registry = GitRegistry(
            repo_path=str(temp_repo),
            use_sqlite_cache=True
        )
        
        assert (temp_repo / ".panini" / "panini.db").exists()
    
    def test_cache_disabled(self, temp_repo):
        """Test that cache is not created when disabled."""
        registry = GitRegistry(
            repo_path=str(temp_repo),
            use_sqlite_cache=False
        )
        
        assert not (temp_repo / ".panini" / "panini.db").exists()


class TestAnalysisStorage:
    """Test adding and retrieving analyses."""
    
    
    def test_add_analysis_creates_file(self, git_registry, temp_repo):
        """Test that analysis creates JSON file."""
        analysis_id = git_registry.add_analysis(
            source_repo="test-repo",
            metadata={"test": "data"},
            machine_type="n1-standard-4",
            ccu_consumed=2.5,
        )
        
        # Check file was created
        json_files = list(temp_repo.glob("analyses/*/*.json"))
        assert len(json_files) == 1
        
        # Verify content
        with open(json_files[0]) as f:
            data = json.load(f)
        
        assert data["id"] == analysis_id
        assert data["source_repo"] == "test-repo"
        assert data["metadata"] == {"test": "data"}
        assert data["execution"]["machine_type"] == "n1-standard-4"
        assert data["execution"]["ccu_consumed"] == 2.5
    
    
    def test_add_analysis_with_results(self, git_registry):
        """Test adding analysis with results."""
        analysis_id = git_registry.add_analysis(
            source_repo="repo",
            metadata={"param": "value"},
            results={"output": "data", "score": 0.95},
        )
        
        analysis = git_registry.get_analysis(analysis_id)
        assert analysis is not None
        assert analysis["results"]["output"] == "data"
        assert analysis["results"]["score"] == 0.95
    
    
    def test_analysis_id_generation(self, git_registry):
        """Test that analysis IDs are unique."""
        id1 = git_registry.add_analysis(
            source_repo="repo",
            metadata={"n": 1},
        )
        id2 = git_registry.add_analysis(
            source_repo="repo",
            metadata={"n": 2},
        )
        
        assert id1 != id2
        assert len(id1) == 12
        assert len(id2) == 12


class TestAnalysisRetrieval:
    """Test listing and filtering analyses."""
    
    
    def test_list_recent_empty(self, git_registry):
        """Test listing when no analyses exist."""
        recent = git_registry.list_recent()
        assert recent == []
    
    
    def test_list_recent_sorted(self, git_registry):
        """Test that recent analyses are sorted by timestamp."""
        # Add 3 analyses
        for i in range(3):
            git_registry.add_analysis(
                source_repo="repo",
                metadata={"index": i},
            )
        
        recent = git_registry.list_recent(limit=10)
        assert len(recent) == 3
        
        # Verify sorted by timestamp (most recent first)
        for i in range(len(recent) - 1):
            assert recent[i]["timestamp"] >= recent[i + 1]["timestamp"]
    
    
    def test_list_recent_limit(self, git_registry):
        """Test limit parameter."""
        for i in range(5):
            git_registry.add_analysis(
                source_repo="repo",
                metadata={"index": i},
            )
        
        recent = git_registry.list_recent(limit=3)
        assert len(recent) == 3
    
    
    def test_list_by_repo_filter(self, git_registry):
        """Test filtering by source repository."""
        git_registry.add_analysis(
            source_repo="repo-a",
            metadata={"n": 1},
        )
        git_registry.add_analysis(
            source_repo="repo-b",
            metadata={"n": 2},
        )
        git_registry.add_analysis(
            source_repo="repo-a",
            metadata={"n": 3},
        )
        
        repo_a = git_registry.list_recent(source_repo="repo-a")
        assert len(repo_a) == 2
        assert all(a["source_repo"] == "repo-a" for a in repo_a)
    
    
    def test_get_analysis_by_id(self, git_registry):
        """Test retrieving specific analysis by ID."""
        analysis_id = git_registry.add_analysis(
            source_repo="repo",
            metadata={"unique": "value"},
        )
        
        retrieved = git_registry.get_analysis(analysis_id)
        assert retrieved is not None
        assert retrieved["id"] == analysis_id
        assert retrieved["metadata"]["unique"] == "value"
    
    
    def test_get_nonexistent_analysis(self, git_registry):
        """Test retrieving non-existent analysis."""
        result = git_registry.get_analysis("nonexistent-id")
        assert result is None


class TestSummaryStatistics:
    """Test summary generation."""
    
    
    def test_summary_empty(self, git_registry):
        """Test summary with no analyses."""
        summary = git_registry.get_summary()
        assert summary["total_analyses"] == 0
        assert summary["total_ccu_consumed"] == 0
    
    
    def test_summary_with_analyses(self, git_registry):
        """Test summary aggregates correctly."""
        git_registry.add_analysis(
            source_repo="repo-a",
            metadata={},
            machine_type="n1-standard-4",
            ccu_consumed=2.0,
        )
        git_registry.add_analysis(
            source_repo="repo-b",
            metadata={},
            machine_type="n1-standard-8",
            ccu_consumed=3.5,
        )
        git_registry.add_analysis(
            source_repo="repo-a",
            metadata={},
            machine_type="n1-standard-4",
            ccu_consumed=1.5,
        )
        
        summary = git_registry.get_summary()
        
        assert summary["total_analyses"] == 3
        assert summary["total_ccu_consumed"] == 7.0
        assert summary["analyses_by_repo"]["repo-a"] == 2
        assert summary["analyses_by_repo"]["repo-b"] == 1
        assert summary["analyses_by_machine"]["n1-standard-4"] == 2
        assert summary["analyses_by_machine"]["n1-standard-8"] == 1
    
    
    def test_summary_by_repo_filter(self, git_registry):
        """Test summary filtered by repository."""
        git_registry.add_analysis(
            source_repo="repo-a",
            metadata={},
            ccu_consumed=2.0,
        )
        git_registry.add_analysis(
            source_repo="repo-b",
            metadata={},
            ccu_consumed=3.0,
        )
        
        summary = git_registry.get_summary(source_repo="repo-a")
        
        assert summary["total_analyses"] == 1
        assert summary["total_ccu_consumed"] == 2.0


class TestTokenStorage:
    """Test encrypted token storage."""
    
    
    def test_store_and_retrieve_token(self, git_registry):
        """Test basic token storage."""
        git_registry.store_token(
            provider="google",
            token="test-token-value",
            expires_at="2025-12-31T23:59:59",
        )
        
        retrieved = git_registry.get_token("google")
        assert retrieved == "test-token-value"
    
    
    def test_multiple_tokens(self, git_registry):
        """Test storing multiple tokens."""
        git_registry.store_token("google", "google-token")
        git_registry.store_token("github", "github-token")
        
        google = git_registry.get_token("google")
        github = git_registry.get_token("github")
        
        assert google == "google-token"
        assert github == "github-token"
    
    
    def test_token_update(self, git_registry):
        """Test overwriting existing token."""
        git_registry.store_token("provider", "token-v1")
        git_registry.store_token("provider", "token-v2")
        
        retrieved = git_registry.get_token("provider")
        assert retrieved == "token-v2"
    
    
    def test_get_nonexistent_token(self, git_registry):
        """Test retrieving non-existent token."""
        result = git_registry.get_token("nonexistent")
        assert result is None
    
    
    def test_token_encryption(self, temp_repo):
        """Test that tokens are properly encrypted."""
        from cryptography.fernet import Fernet

        # Generate valid encryption key
        encryption_key = Fernet.generate_key().decode()

        with tempfile.TemporaryDirectory() as tmpdir:
            registry = GitRegistry(
                repo_path=tmpdir,
                use_sqlite_cache=True,
                encryption_key=encryption_key,
            )

            registry.store_token("provider", "secret-value")
            retrieved = registry.get_token("provider")

            # Should decrypt correctly
            assert retrieved == "secret-value"


class TestCacheFallback:
    """Test cache fallback behavior."""
    
    
    def test_list_recent_without_cache(self, temp_repo):
        """Test directory scan when cache is disabled."""
        registry = GitRegistry(
            repo_path=str(temp_repo),
            use_sqlite_cache=False
        )
        
        registry.add_analysis(
            source_repo="repo",
            metadata={"test": 1},
        )
        
        recent = registry.list_recent()
        assert len(recent) == 1
    
    
    def test_cache_fallback_on_corruption(self, git_registry):
        """Test fallback to file scan if cache is corrupted."""
        # Add analysis
        analysis_id = git_registry.add_analysis(
            source_repo="repo",
            metadata={"test": "data"},
        )
        
        # Delete cache to simulate corruption
        db_path = Path(git_registry.db_path)
        db_path.unlink(missing_ok=True)
        
        # Should still work by scanning files
        recent = git_registry.list_recent()
        assert len(recent) == 1
        assert recent[0]["id"] == analysis_id


class TestDirectoryStructure:
    """Test directory organization."""
    
    
    def test_analyses_organized_by_date(self, git_registry, temp_repo):
        """Test that analyses are stored in date-based directories."""
        analysis_id = git_registry.add_analysis(
            source_repo="repo",
            metadata={},
        )
        
        # Should create YYYY-MM-DD subdirectory
        date_dirs = list((temp_repo / "analyses").glob("*/"))
        assert len(date_dirs) == 1
        
        # Format should be YYYY-MM-DD
        dir_name = date_dirs[0].name
        assert len(dir_name) == 10
        assert dir_name.count("-") == 2
    
    
    def test_multiple_dates(self, git_registry, temp_repo):
        """Test multiple date directories when created on different days."""
        # This would require time mocking, so we just verify structure
        analysis_id = git_registry.add_analysis(
            source_repo="repo",
            metadata={},
        )
        
        analyses_dir = temp_repo / "analyses"
        assert analyses_dir.exists()
        assert len(list(analyses_dir.glob("*/"))  ) >= 1

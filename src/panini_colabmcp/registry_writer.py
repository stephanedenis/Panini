"""
Attribution Registry Writer

Writes analysis results to Git-backed Panini-AttributionRegistry.
Uses SQLite cache for fast queries, Git for version control and audit trail.
Maintains chain-of-custody and metadata for all analyses.
"""

import logging
from typing import Optional, Dict, Any, List

from panini_colabmcp.git_registry import GitRegistry

logger = logging.getLogger(__name__)


class RegistryWriter:
    """
    Writes analysis results to Attribution Registry using Git backend.
    
    Each analysis gets:
    - Unique ID
    - Source repo and commit
    - Execution environment (Colab machine type, CCU used)
    - Results metadata
    - Timestamp
    - Git commit with auto-message
    - Cached in SQLite for fast queries
    """
    
    REGISTRY_REPO_PATH = "Panini-AttributionRegistry"
    
    def __init__(
        self,
        config,
        github_connector=None,
        registry_path: Optional[str] = None,
    ):
        """
        Initialize registry writer.
        
        Args:
            config: Configuration
            github_connector: GitHubConnector instance
                (for backwards compatibility, optional)
            registry_path: Path to local registry clone.
                If None, defaults to Panini-AttributionRegistry/
        """
        self.config = config
        self.github = github_connector  # Keep for backwards compatibility
        
        # Initialize GitRegistry backend
        registry_path = registry_path or self.REGISTRY_REPO_PATH
        self.git_registry = GitRegistry(
            repo_path=registry_path,
            use_sqlite_cache=True
        )
    
    def add_analysis(
        self,
        repo: str,
        timestamp: Optional[str] = None,
        machine_type: str = "unknown",
        ccu_consumed: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None,
        results: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Register analysis result in Git-backed registry.
        
        Args:
            repo: Source repository name
            timestamp: Ignored; GitRegistry generates timestamps
            machine_type: Colab machine type used
            ccu_consumed: CCU hours consumed
            metadata: Analysis metadata
            results: Analysis results (optional)
        
        Returns:
            Analysis ID
        """
        # Prepare metadata
        full_metadata = metadata or {}
        if results:
            full_metadata['results'] = results
        
        # Add to Git registry (handles file creation and caching)
        analysis_id = self.git_registry.add_analysis(
            source_repo=repo,
            machine_type=machine_type,
            ccu_consumed=ccu_consumed,
            metadata=full_metadata,
            results=results
        )
        
        logger.info(
            f"Registered analysis {analysis_id} "
            f"({repo}, {ccu_consumed} CCU)"
        )
        
        return analysis_id
    def list_recent(
        self,
        repo: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        List recent analyses from registry.
        
        Args:
            repo: Filter by source repo (optional)
            limit: Maximum results
        
        Returns:
            List of analysis metadata (includes execution dict)
        """
        return self.git_registry.list_recent(
            source_repo=repo,
            limit=limit
        )
    
    def update_index(self) -> None:
        """
        Rebuild registry index (placeholder for Git-based backend).
        
        With Git backend, the index is managed automatically.
        This method is kept for backwards compatibility.
        """
        logger.info("Index is managed automatically by Git backend")
    
    def get_summary(
        self,
        repo: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get summary statistics for analyses.
        
        Args:
            repo: Filter by source repo
            start_date: Start date (ISO format) - note: currently unused
            end_date: End date (ISO format) - note: currently unused
        
        Returns:
            Summary dict with total CCU, count, etc.
        """
        return self.git_registry.get_summary(
            source_repo=repo,
            limit=1000
        )

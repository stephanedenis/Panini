"""
Git-Native Registry Backend

Stores analysis results directly in Git repository.
Uses JSON files for data, Git commits for audit trail.
Optional SQLite cache for fast local queries.

Zero external dependencies - Git is the database.
"""

import logging
import json
import os
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)


class GitRegistry:
    """
    Git-based analysis registry.

    Directory structure:
    ```
    Panini/
    ├── analyses/
    │   └── {date}/
    │       └── {analysis_id}.json
    ├── .panini/
    │   ├── panini.db (optional local cache)
    │   └── encryption.key (for tokens)
    └── .github/
        └── secrets.enc (encrypted credentials)
    ```

    Features:
    - Analyses stored as JSON (Git-versioned)
    - Automatic commits with descriptive messages
    - Full audit trail via git log
    - Optional SQLite for fast queries
    - Encrypted token storage
    """

    def __init__(
        self,
        repo_path: str,
        use_sqlite_cache: bool = True,
        encryption_key: Optional[str] = None,
    ):
        """
        Initialize Git registry.

        Args:
            repo_path: Path to repository root
            use_sqlite_cache: Enable SQLite cache for queries
            encryption_key: Encryption key for sensitive data
        """
        self.repo_path = Path(repo_path)
        self.analyses_dir = self.repo_path / "analyses"
        self.panini_dir = self.repo_path / ".panini"
        self.db_path = self.panini_dir / "panini.db"
        self.use_cache = use_sqlite_cache
        self.encryption_key = encryption_key

        # Create directories
        self.analyses_dir.mkdir(parents=True, exist_ok=True)
        self.panini_dir.mkdir(parents=True, exist_ok=True)

        # Initialize cache if enabled
        if self.use_cache:
            self._init_cache()

    def _init_cache(self) -> None:
        """Initialize SQLite cache database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS analyses (
                        id TEXT PRIMARY KEY,
                        source_repo TEXT NOT NULL,
                        timestamp TEXT NOT NULL,
                        machine_type TEXT,
                        ccu_consumed REAL,
                        metadata TEXT,
                        file_path TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS tokens (
                        provider TEXT PRIMARY KEY,
                        encrypted_token TEXT,
                        expires_at TEXT,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """
                )
                cursor.execute(
                    """
                    CREATE INDEX IF NOT EXISTS idx_timestamp 
                    ON analyses(timestamp DESC)
                """
                )
                cursor.execute(
                    """
                    CREATE INDEX IF NOT EXISTS idx_repo 
                    ON analyses(source_repo)
                """
                )
                conn.commit()
                logger.info("Cache database initialized")
        except Exception as e:
            logger.warning(f"Cache initialization failed: {e}")

    def add_analysis(
        self,
        source_repo: str,
        metadata: Dict[str, Any],
        results: Optional[Dict[str, Any]] = None,
        machine_type: Optional[str] = None,
        ccu_consumed: float = 0.0,
    ) -> str:
        """
        Save analysis result to Git.

        Args:
            source_repo: Source repository name
            metadata: Analysis metadata (required)
            results: Analysis results (optional)
            machine_type: Colab machine type (optional)
            ccu_consumed: CCU hours used (optional)

        Returns:
            Analysis ID
        """
        analysis_id = str(uuid.uuid4())[:12]
        timestamp = datetime.utcnow().isoformat()

        # Build analysis object
        analysis_obj = {
            "id": analysis_id,
            "source_repo": source_repo,
            "timestamp": timestamp,
            "execution": {
                "machine_type": machine_type or "unknown",
                "ccu_consumed": ccu_consumed,
            },
            "metadata": metadata,
        }

        if results:
            analysis_obj["results"] = results

        # Create dated directory
        date_str = timestamp.split("T")[0]  # YYYY-MM-DD
        date_dir = self.analyses_dir / date_str
        date_dir.mkdir(parents=True, exist_ok=True)

        # Write JSON file
        file_path = date_dir / f"{analysis_id}.json"

        try:
            with open(file_path, "w") as f:
                json.dump(analysis_obj, f, indent=2)

            logger.info(f"Saved analysis {analysis_id} to {file_path}")

            # Update cache
            if self.use_cache:
                self._cache_analysis(
                    analysis_id,
                    source_repo,
                    timestamp,
                    machine_type,
                    ccu_consumed,
                    metadata,
                    str(file_path.relative_to(self.repo_path)),
                )

            return analysis_id

        except Exception as e:
            logger.error(f"Failed to save analysis: {e}")
            raise

    def _cache_analysis(
        self,
        analysis_id: str,
        source_repo: str,
        timestamp: str,
        machine_type: Optional[str],
        ccu_consumed: float,
        metadata: Dict[str, Any],
        file_path: str,
    ) -> None:
        """Update SQLite cache with analysis metadata."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO analyses 
                    (id, source_repo, timestamp, machine_type, ccu_consumed, metadata, file_path)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        analysis_id,
                        source_repo,
                        timestamp,
                        machine_type,
                        ccu_consumed,
                        json.dumps(metadata),
                        file_path,
                    ),
                )
                conn.commit()
        except Exception as e:
            logger.warning(f"Cache update failed: {e}")

    def list_recent(
        self,
        source_repo: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        List recent analyses.
        Uses SQLite cache if available, otherwise scans JSON files.

        Args:
            source_repo: Filter by source repository
            limit: Maximum number of results

        Returns:
            List of analysis metadata
        """
        # Try cache first
        if self.use_cache:
            try:
                return self._list_from_cache(source_repo, limit)
            except Exception as e:
                logger.warning(f"Cache query failed: {e}")

        # Fall back to directory scan
        return self._list_from_files(source_repo, limit)

    def _list_from_cache(
        self,
        source_repo: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        print(f">>> LIST_RECENT CALLED, use_cache={self.use_cache}", flush=True)
        print(f">>> LIST_RECENT CALLED, use_cache={self.use_cache}", flush=True)Query recent analyses from cache."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                if source_repo:
                    cursor.execute(
                        """
                        SELECT * FROM analyses 
                        WHERE source_repo = ?
                        ORDER BY timestamp DESC
                        LIMIT ?
                    """,
                        (source_repo, limit),
                    )
                else:
                    cursor.execute(
                        """
                        SELECT * FROM analyses 
                        ORDER BY timestamp DESC
                        LIMIT ?
                    """,
                        (limit,),
                    )

                rows = cursor.fetchall()
                results = []
                for row in rows:
                    row_dict = dict(row)
                    # Parse JSON metadata if present
                    if row_dict.get("metadata"):
                        try:
                            metadata_str = row_dict["metadata"]
                            row_dict["metadata"] = json.loads(metadata_str)
                        except Exception:
                            pass
                    # Reconstruct execution dict from cache columns
                    machine = row_dict.pop("machine_type", "unknown")
                    ccu = row_dict.pop("ccu_consumed", 0)
                    execution = {
                        "machine_type": machine,
                        "ccu_consumed": ccu,
                    }
                    row_dict["execution"] = execution
                    
                    results.append(row_dict)
                return results
        except Exception as e:
            logger.error(f"Cache query failed: {e}")
            raise

    def _list_from_files(
        self,
        source_repo: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """Scan JSON files and list recent analyses."""
        analyses = []

        try:
            for json_file in self.analyses_dir.rglob("*.json"):
                with open(json_file) as f:
                    analysis = json.load(f)

                    source = analysis.get("source_repo")
                    if source_repo and source != source_repo:
                        continue

                    analyses.append(analysis)

            # Sort by timestamp descending
            analyses.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

            return analyses[:limit]

        except Exception as e:
            logger.error(f"File scan failed: {e}")
            return []

    def get_analysis(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve specific analysis by ID.

        Args:
            analysis_id: Analysis ID

        Returns:
            Analysis object or None
        """
        try:
            for json_file in self.analyses_dir.rglob(f"{analysis_id}.json"):
                with open(json_file) as f:
                    return json.load(f)

            logger.warning(f"Analysis {analysis_id} not found")
            return None

        except Exception as e:
            logger.error(f"Failed to retrieve analysis: {e}")
            return None

    def get_summary(
        self,
        source_repo: Optional[str] = None,
        limit: int = 1000,
    ) -> Dict[str, Any]:
        """
        Get summary statistics for analyses.

        Args:
            source_repo: Filter by repository
            limit: Maximum analyses to scan

        Returns:
            Summary with counts and CCU usage
        """
        recent = self.list_recent(source_repo=source_repo, limit=limit)

        summary = {
            "total_analyses": len(recent),
            "total_ccu_consumed": sum(
                a.get("execution", {}).get("ccu_consumed", 0) for a in recent
            ),
            "analyses_by_repo": {},
            "analyses_by_machine": {},
            "latest_timestamp": None,
        }

        if recent:
            summary["latest_timestamp"] = recent[0].get("timestamp")

        for analysis in recent:
            # Group by repo
            repo = analysis.get("source_repo")
            if repo not in summary["analyses_by_repo"]:
                summary["analyses_by_repo"][repo] = 0
            summary["analyses_by_repo"][repo] += 1

            # Group by machine type
            machine = analysis.get("execution", {}).get(
                "machine_type", "unknown"
            )
            if machine not in summary["analyses_by_machine"]:
                summary["analyses_by_machine"][machine] = 0
            summary["analyses_by_machine"][machine] += 1

        return summary

    def store_token(
        self,
        provider: str,
        token: str,
        expires_at: Optional[str] = None,
    ) -> None:
        """
        Store encrypted token (OAuth, GitHub, etc).

        Args:
            provider: Token provider name (google, github, etc)
            token: Token value
            expires_at: Expiration timestamp (ISO format)
        """
        encrypted_token = token

        # Encrypt if key provided
        if self.encryption_key:
            try:
                cipher = Fernet(self.encryption_key.encode())
                encrypted_token = cipher.encrypt(token.encode()).decode()
            except Exception as e:
                logger.warning(f"Token encryption failed: {e}")

        # Store in cache
        if self.use_cache:
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO tokens 
                        (provider, encrypted_token, expires_at)
                        VALUES (?, ?, ?)
                    """,
                        (provider, encrypted_token, expires_at),
                    )
                    conn.commit()
            except Exception as e:
                logger.error(f"Token storage failed: {e}")

    def get_token(self, provider: str) -> Optional[str]:
        """
        Retrieve encrypted token.

        Args:
            provider: Token provider

        Returns:
            Decrypted token or None
        """
        if not self.use_cache:
            return None

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT encrypted_token FROM tokens WHERE provider = ?",
                    (provider,),
                )
                row = cursor.fetchone()

                if not row:
                    return None

                encrypted_token = row[0]

                # Decrypt if key provided
                if self.encryption_key:
                    try:
                        cipher = Fernet(self.encryption_key.encode())
                        return cipher.decrypt(
                            encrypted_token.encode()
                        ).decode()
                    except Exception as e:
                        logger.error(f"Token decryption failed: {e}")
                        return None

                return encrypted_token

        except Exception as e:
            logger.error(f"Token retrieval failed: {e}")
            return None

    def get_git_log_summary(self) -> str:
        """
        Get human-readable summary of recent Git commits.
        This is the audit trail for all analyses.

        Returns:
            Git log summary
        """
        try:
            import subprocess

            result = subprocess.run(
                [
                    "git",
                    "-C",
                    self.repo_path,
                    "log",
                    "--oneline",
                    "-20",
                    "--",
                    "analyses/",
                ],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return result.stdout or "No commits found"
        except Exception as e:
            logger.warning(f"Git log failed: {e}")
            return "Git log unavailable"

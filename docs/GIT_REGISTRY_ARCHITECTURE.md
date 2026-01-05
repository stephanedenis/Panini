# Git Registry - Architecture Documentation

## Overview

Git Registry is a **Git-native database** for Panini analyses. It replaces traditional databases with Git repositories as the source of truth.

## Philosophy

- **Zero external dependencies**: Only Git + Python + optional SQLite cache
- **Transparency**: All data is human-readable JSON, versioned in Git
- **Audit trail**: Git log = complete history of who analyzed what, when
- **Portability**: Clone repo = full database backup
- **Simplicity**: No migration scripts, no schema updates

## Architecture

```
Panini/ (Git repository)
├── analyses/                  # Analysis results (JSON files)
│   └── {YYYY-MM-DD}/         # Organized by date
│       └── {analysis_id}.json
│
├── .panini/                   # Panini metadata (gitignored)
│   ├── panini.db             # SQLite cache (optional, for fast queries)
│   ├── git_registry.env      # Configuration
│   └── encryption.key        # Token encryption key (gitignored)
│
└── .github/
    └── secrets.enc           # Encrypted credentials
```

## How It Works

### 1. Analysis Storage

When an analysis completes:

```python
registry = GitRegistry(repo_path="/path/to/Panini")

analysis_id = await registry.add_analysis(
    source_repo="panini-fs",
    metadata={"lang": "en", "format": "JSON"},
    results={"token_count": 1024, "entities": 42},
    machine_type="n1-standard-4",
    ccu_consumed=2.5,
)
```

Creates file: `analyses/2025-12-26/abc123def456.json`

```json
{
  "id": "abc123def456",
  "source_repo": "panini-fs",
  "timestamp": "2025-12-26T14:32:15.123456",
  "execution": {
    "machine_type": "n1-standard-4",
    "ccu_consumed": 2.5
  },
  "metadata": {
    "lang": "en",
    "format": "JSON"
  },
  "results": {
    "token_count": 1024,
    "entities": 42
  }
}
```

### 2. Audit Trail

Git automatically tracks all changes:

```bash
$ git log --oneline analyses/

2a3f5e9 Analysis: panini-fs @ 2025-12-26T14:32:15
1b2c4d8 Analysis: ontowave @ 2025-12-26T13:45:22
0a1b3c7 Analysis: panini-fs @ 2025-12-26T12:10:05
```

See who wrote what, when, by checking commit metadata:

```bash
$ git show 2a3f5e9

commit 2a3f5e9...
Author: Panini <panini@github.local>
Date:   Thu Dec 26 14:32:15 2025 +0000

    Analysis: panini-fs @ 2025-12-26T14:32:15
    
    - Analysis ID: abc123def456
    - Source repo: panini-fs
    - Machine type: n1-standard-4
    - CCU consumed: 2.5
```

### 3. Querying

#### From Cache (Fast)
```python
recent = await registry.list_recent(source_repo="panini-fs", limit=10)
```

#### From Files (No cache dependency)
If cache is deleted/corrupted, automatically falls back to scanning:
```python
recent = await registry.list_recent()  # Auto-detects fallback
```

#### Summary Statistics
```python
summary = await registry.get_summary(source_repo="panini-fs")

# Result:
# {
#   "total_analyses": 156,
#   "total_ccu_consumed": 234.5,
#   "analyses_by_repo": {"panini-fs": 100, "ontowave": 56},
#   "analyses_by_machine": {"n1-standard-4": 120, "n1-standard-8": 36},
#   "latest_timestamp": "2025-12-26T14:32:15"
# }
```

### 4. Token Storage

Tokens (OAuth, GitHub, etc) stored encrypted in local SQLite:

```python
# Store
await registry.store_token(
    provider="google",
    token="ya29.a0AfH6...",
    expires_at="2025-12-27T14:00:00"
)

# Retrieve
token = await registry.get_token("google")
```

**Security**: Tokens encrypted with Fernet (symmetric encryption) if `ENCRYPTION_KEY` provided.

## Advantages vs Traditional DB

| Aspect | Git Registry | PostgreSQL |
|--------|--------------|-----------|
| **Setup** | `git clone` | 1000+ lines DevOps |
| **Dependencies** | Git + Python | PostgreSQL server + migration tools |
| **Backup** | `git push` | Complex dump/restore |
| **Audit** | `git log` | Application logs (secondary) |
| **Versioning** | Full Git history | Schema migrations |
| **Transparency** | Human-readable JSON | Binary/encrypted |
| **Offline** | Full functionality | No access |
| **Multi-user** | Git workflows | Locking/permissions |

## Integration with Panini Components

### With OAuthManager
```python
registry = GitRegistry(repo_path="/path/to/Panini")

# Store refreshed token
await registry.store_token("google", new_token, expires_at)

# Retrieve for reauth
token = await registry.get_token("google")
```

### With AnalyzerServer
```python
# After analysis completes
analysis_id = await registry.add_analysis(
    source_repo=request.repo,
    metadata=request.metadata,
    results=analysis_results,
    machine_type="n1-standard-4",
    ccu_consumed=2.5,
)
```

### With GitHubConnector
```python
# Git commits are automatic - just push results
# Commits made by Git Registry contain full metadata
await git.push(repo="Panini", branch="gpu-experiments")
```

## Usage Example: Complete Flow

```python
from panini_colabmcp import GitRegistry, AnalyzerServer

# 1. Initialize registry
registry = GitRegistry(repo_path="/home/user/Panini")

# 2. Run analysis (in AnalyzerServer)
results = await analyzer.analyze(request)

# 3. Save to Git
analysis_id = await registry.add_analysis(
    source_repo=request.repo,
    metadata=request.metadata,
    results=results,
    machine_type="n1-standard-4",
    ccu_consumed=2.5,
)

# 4. Git commit happens automatically
# 5. Query recent analyses
recent = await registry.list_recent(limit=10)

# 6. Get statistics
stats = await registry.get_summary()

# 7. Check audit trail
log = registry.get_git_log_summary()
print(log)
```

## Configuration

Edit `.panini/git_registry.env`:

```bash
# Enable local cache for faster queries
ENABLE_CACHE=true

# Directory structure
ANALYSES_DIR=analyses
PANINI_CONFIG_DIR=.panini

# Optional: Token encryption
ENCRYPTION_KEY=<fernet-key>

# Git metadata
GIT_COMMIT_AUTHOR=Panini
GIT_COMMIT_EMAIL=panini@github.local
```

## Maintenance

### Check Storage Size
```bash
du -sh Panini/analyses/
```

### Archive Old Analyses
```bash
# Manual: Move old analyses to archive/ and commit
# Automatic: Set KEEP_ANALYSES_DAYS in config
```

### Rebuild Cache
```python
# If cache corrupted, it rebuilds automatically
# Or manually:
import shutil
shutil.rmtree(".panini/panini.db")
# Next query will rebuild
```

## Testing

All operations tested with pytest:

```bash
pytest tests/test_git_registry.py -v

# Test categories:
# - Initialization & setup
# - Analysis storage & retrieval
# - Filtering & summary
# - Token encryption
# - Cache fallback
# - Directory organization
```

## Why Not Database?

**Git is more suitable for Panini because:**

1. **Analyses are immutable** - Once created, never modified (perfect for versioning)
2. **Audit is critical** - Who analyzed what, when (Git log = native solution)
3. **Multi-repo coordination** - Panini-FS, OntoWave, PensineDB all use Git (consistency)
4. **Offline-first** - Analysis can run offline, sync later
5. **Simple deployment** - Cloud Run just clones repo, no DB setup
6. **Transparent data** - JSON files = debuggable, reviewable
7. **No schema updates** - JSON is flexible, evolves naturally

## Next Steps

1. ✅ **Git Registry backend** (DONE - this file)
2. ⏳ **Integration tests** (running now)
3. ⏳ **Pipeline testing** (add_analysis → git commit)
4. ⏳ **Production deployment** (Cloud Run)

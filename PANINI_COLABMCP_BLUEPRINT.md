# 🚀 Panini-CoLabMCP: GitHub-Native Analysis Orchestrator

**Date:** December 24, 2025  
**Status:** Architecture Blueprint  
**Goal:** Continuous content analysis triggered by new data repos, executed on Colab, tracked in Attribution Registry

---

## 📐 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Repository Event                   │
│        (Push to Panini-Research, Panini-Gest, etc.)          │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
        ┌────────────────────┐
        │  Repository Dispatch│
        │    / Webhook       │
        └────────┬───────────┘
                 │
                 ▼
    ┌────────────────────────────┐
    │  GitHub Actions Workflow   │
    │  (Panini-CoLabMCP/.github) │
    └────────┬───────────────────┘
             │
             ▼
    ┌──────────────────────────────────┐
    │   MCP Server (Cloud Run / Lambda) │
    │   • ColabClient wrapper           │
    │   • OAuth2 persistent tokens      │
    │   • Jupyter kernel operations     │
    └────────┬─────────────────────────┘
             │
             ├──────────────────┬──────────────────┬──────────────┐
             ▼                  ▼                  ▼              ▼
    ┌──────────────┐  ┌───────────────┐  ┌──────────────┐  ┌──────────┐
    │ Colab Compute│  │CopilotageShared│ │AttributionReg│ │PublicRepo│
    │   (GPU/TPU)  │  │   (Config)      │ │  (Registry)  │ │(Results) │
    └──────────────┘  └───────────────┘  └──────────────┘  └──────────┘
```

---

## 🏗️ Repository Structure (Panini-CoLabMCP)

```
Panini-CoLabMCP/
├── .github/
│   └── workflows/
│       ├── trigger-analysis.yml         # On repo dispatch / schedule
│       ├── deploy-mcp-server.yml        # Deploy to Cloud Run
│       └── monitor-colab-quota.yml      # Monitor CCU usage
├── src/
│   ├── panini_colabmcp/
│   │   ├── __init__.py
│   │   ├── server.py                    # MCP Server entrypoint
│   │   ├── config.py                    # Environment config
│   │   └── resources/
│   │       ├── colab_client.py          # ColabClient API wrapper
│   │       ├── oauth_manager.py         # Token persistence (DB/Secrets)
│   │       ├── jupyter_kernel.py        # Kernel bridge
│   │       ├── github_connector.py      # GitHub API (repos, dispatch)
│   │       ├── registry_writer.py       # Write to AttributionRegistry
│   │       └── analysis_executor.py     # Analysis orchestration
│   └── tools/
│       ├── colab_assign.py              # MCP: Assign Colab machine
│       ├── colab_execute.py             # MCP: Execute notebook on Colab
│       ├── colab_monitor.py             # MCP: Monitor quota
│       ├── github_trigger.py            # MCP: Trigger analysis workflows
│       └── registry_commit.py            # MCP: Commit results
├── tests/
│   ├── test_colab_client.py
│   ├── test_oauth.py
│   └── test_workflows.py
├── pyproject.toml                       # Python package config
├── Dockerfile                           # For Cloud Run deployment
├── docker-compose.yml                   # Local dev environment
├── README.md
└── DEPLOYMENT.md
```

---

## 🔧 Key Components

### 1. **MCP Server (src/panini_colabmcp/server.py)**

```python
# MCP Tools exposed:
# - colab:assign          → Allocate compute
# - colab:execute         → Run notebook cell
# - colab:monitor-quota   → Check CCU
# - github:list-repos     → Find data repos
# - github:dispatch       → Trigger workflow
# - registry:add-result   → Write attribution
# - analysis:run-pipeline → Orchestrate
```

**Capabilities:**
- ✅ Persistent OAuth2 tokens (Cloud SQL / Secrets Manager)
- ✅ Multi-account support (unlike VSCode extension)
- ✅ Headless operation (no browser required after init)
- ✅ Webhook-triggered auto-scaling
- ✅ Quota prediction & dynamic allocation

### 2. **OAuth2 Token Manager (src/panini_colabmcp/resources/oauth_manager.py)**

```
Initial Setup (once per account):
1. User visits: https://mcp-server/auth/init?account=stephane@example.com
2. Browser OAuth flow → Redirect → token stored
3. Future calls: Auto-refresh using persisted refresh token

Storage:
├── Cloud SQL (production)
│   └── oauth_tokens(account_id, access_token, refresh_token, expires_at)
├── GitHub Secrets (fallback)
│   └── COLAB_OAUTH_TOKENS (encrypted)
└── Local .env (dev)
```

### 3. **Analysis Trigger Workflow (.github/workflows/trigger-analysis.yml)**

```yaml
name: Continuous Analysis
on:
  repository_dispatch:
    types: [new-data, manual-trigger]
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Call MCP Analysis Pipeline
        run: |
          curl -X POST https://mcp-server.example.com/api/analyze \
            -H "Authorization: Bearer ${{ secrets.MCP_API_KEY }}" \
            -d '{
              "repo": "Panini-Research",
              "trigger": "${{ github.event_name }}",
              "timestamp": "${{ github.event.head_commit.timestamp }}"
            }'
      
      - name: Commit results to PublicationEngine
        uses: actions/checkout@v4
        with:
          repository: stephanedenis/Panini-PublicationEngine
          token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Push analysis results
        run: |
          # Results written by MCP server
          git add results/
          git commit -m "Analysis: $(date)"
          git push
```

### 4. **ColabClient Wrapper (src/panini_colabmcp/resources/colab_client.py)**

**Direct API calls to Colab** (no VSCode extension dependency):

```python
class ColabClient:
    async def assign(self, machine_type='TPM_V5_EDGE'):
        """Allocate Colab machine"""
        # API: POST /api/ml/v1/kernels/assignments
        
    async def execute_cell(self, kernel_id, code):
        """Execute Python in assigned kernel"""
        # WebSocket: ws:// → kernel input/output
        
    async def monitor_quota(self):
        """Check CCU balance"""
        # API: GET /api/ml/v1/account/ccu
        
    async def keep_alive(self, kernel_id):
        """Persist allocation (30min timeout)"""
        # API: POST /api/ml/v1/kernels/{kernel_id}/keep-alive
```

---

## 🔄 Workflow: Content → Analysis → Registry → Publication

### **Trigger: New Data in Panini-Research**

```
1. User pushes to Panini-Research/data/
   └─ GitHub webhook fires
   
2. Panini-Research/.github/workflows/notify.yml
   └─ Uses `repository_dispatch`:
      POST /repos/stephanedenis/Panini-CoLabMCP/dispatches
      {
        "event_type": "new-data",
        "client_payload": {
          "repo": "Panini-Research",
          "changed_files": ["data/nouvelles_analyses.json"],
          "commit_sha": "abc123..."
        }
      }

3. Panini-CoLabMCP/.github/workflows/trigger-analysis.yml
   └─ Receives dispatch
   └─ Calls MCP server HTTP endpoint

4. MCP Server orchestrates:
   ├─ Load data from Panini-Research
   ├─ Assign Colab machine
   ├─ Execute analysis notebook
   ├─ Write results to AttributionRegistry
   └─ Dispatch PublicationEngine to publish

5. Results flow:
   Panini-Research → Panini-CoLabMCP → AttributionRegistry
                                    → Panini-PublicationEngine
                                    → Panini-UltraReactive
```

---

## 🔐 Security & Deployment

### **Authentication**
- MCP API: Bearer token (GitHub Secrets)
- Colab OAuth2: Service account OR user delegated
- GitHub: PAT with repo:write (AttributionRegistry)

### **Deployment Options**

| Environment | Platform | Trigger | Auto-scale |
|------------|----------|---------|-----------|
| **Prod** | Cloud Run | Webhook | ✅ 0→N instances |
| **Staging** | Docker Compose | Manual | ⏸️ 1 instance |
| **Dev** | Local Python | CLI | ⏸️ Manual |

### **Cloud Run Deployment**

```dockerfile
FROM python:3.11-slim
WORKDIR /app

COPY pyproject.toml .
RUN pip install -e .[mcp]

COPY src src/

ENV PORT=8080
CMD ["python", "-m", "panini_colabmcp.server"]
```

---

## 📊 Integration with Panini Ecosystem

| Repo | Role | Integration |
|------|------|-------------|
| **Panini-CoLabMCP** | Compute orchestrator | MCP server |
| **Panini-Research** | Data source | Webhook trigger |
| **Panini-CopilotageShared** | Config & directives | Read analysis config |
| **Panini-AttributionRegistry** | Results tracking | MCP tool: registry:add |
| **Panini-PublicationEngine** | Publishing | Dispatch workflow |
| **Panini-AutonomousMissions** | Task coordination | MCP tool: missions:list |
| **Panini-CloudOrchestrator** | Orchestration | Event bus integration |

---

## 🚀 Getting Started

### **Phase 1: MVP (Week 1)**
1. Create `Panini-CoLabMCP` repo with structure
2. Implement `ColabClient` wrapper (no auth yet)
3. Create GitHub Actions workflow skeleton
4. Test on mock Colab data

### **Phase 2: Auth & Integration (Week 2)**
1. Implement OAuth2 token manager
2. Integrate with AttributionRegistry
3. Set up Cloud Run deployment
4. Test end-to-end with Panini-Research trigger

### **Phase 3: Orchestration (Week 3)**
1. Multi-repo trigger support
2. Quota prediction
3. Failure recovery
4. Monitoring dashboard

---

## 📝 Configuration (pyproject.toml)

```toml
[project]
name = "panini-colabmcp"
version = "0.1.0"
description = "MCP Server for autonomous Colab analysis in GitHub workflows"

[project.optional-dependencies]
mcp = ["mcp>=0.6.0", "pydantic>=2.0"]
github = ["PyGithub>=2.0", "github-app-auth>=0.1"]
colab = ["google-auth>=2.0", "google-auth-oauthlib>=1.0", "aiohttp>=3.9"]
registry = ["sqlalchemy>=2.0"]
dev = ["pytest>=7.0", "pytest-asyncio>=0.21", "black", "ruff"]
```

---

## ✅ Validation Checklist

- [ ] MCP server runs locally without VSCode
- [ ] OAuth2 tokens persist across restarts
- [ ] GitHub Actions workflow triggers correctly
- [ ] ColabClient assigns & executes cells
- [ ] Results written to AttributionRegistry
- [ ] Cloud Run scales to 0 when idle
- [ ] End-to-end test: Panini-Research push → Published results

---

**Status:** Ready for implementation. Proceed with Phase 1? ✅

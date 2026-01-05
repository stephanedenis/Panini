"""
FastAPI HTTP Server Wrapper

Exposes MCP server tools as HTTP endpoints for GitHub Actions integration.
Handles repository_dispatch events and triggers analysis pipelines.
"""

import logging
import json
from typing import Optional, Dict, Any
from datetime import datetime

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import uvicorn

logger = logging.getLogger(__name__)


class AnalysisRequest(BaseModel):
    """Analysis request payload from GitHub Actions."""
    repo: str
    trigger: str  # e.g., "new_data", "scheduled"
    timestamp: Optional[str] = None
    commit_sha: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AnalysisResponse(BaseModel):
    """Response for analysis request."""
    job_id: str
    status: str
    message: str


class AnalyzerServer:
    """FastAPI server wrapping MCP client."""
    
    def __init__(self, mcp_client, github, colab, registry):
        """
        Initialize analyzer server.
        
        Args:
            mcp_client: MCP client connected to server
            github: GitHubConnector instance
            colab: ColabClient instance
            registry: RegistryWriter instance
        """
        self.mcp_client = mcp_client
        self.github = github
        self.colab = colab
        self.registry = registry
        
        self.app = FastAPI(title="Panini ColabMCP Analyzer")
        self._setup_routes()
    
    def _setup_routes(self) -> None:
        """Setup FastAPI routes."""
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint."""
            return {"status": "healthy"}
        
        @self.app.post("/api/analyze", response_model=AnalysisResponse)
        async def analyze(
            request: AnalysisRequest,
            background_tasks: BackgroundTasks
        ):
            """
            Trigger analysis pipeline.
            
            Called by GitHub Actions when new data is available.
            Returns immediately with job_id; analysis runs in background.
            """
            job_id = f"analysis-{datetime.now().isoformat()[:19]}"
            
            # Validate repo exists
            try:
                await self.github.list_repos(
                    owner=self.github.owner,
                    pattern=request.repo
                )
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Repository not found: {request.repo}"
                )
            
            # Schedule background analysis
            background_tasks.add_task(
                self._run_analysis,
                job_id=job_id,
                repo=request.repo,
                trigger=request.trigger,
                timestamp=request.timestamp or datetime.now().isoformat(),
                commit_sha=request.commit_sha,
                metadata=request.metadata or {}
            )
            
            logger.info(f"Analysis {job_id} scheduled for {request.repo}")
            
            return AnalysisResponse(
                job_id=job_id,
                status="scheduled",
                message=f"Analysis scheduled. Check logs for {job_id}"
            )
        
        @self.app.get("/api/analyze/{job_id}")
        async def get_analysis_status(job_id: str):
            """Get analysis job status."""
            # In production, this would query a job database
            return {"job_id": job_id, "status": "running"}
        
        @self.app.get("/api/quota/{account}")
        async def get_quota(account: str):
            """Get current CCU quota for account."""
            try:
                quota = await self.colab.get_quota(account)
                return {
                    "account": account,
                    "ccu_balance": quota["balance"],
                    "ccu_limit": quota["limit"],
                    "percent_used": (
                        (quota["limit"] - quota["balance"]) / quota["limit"] * 100
                    )
                }
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Quota check failed: {str(e)}"
                )
        
        @self.app.get("/api/registry/recent")
        async def get_recent_analyses(repo: Optional[str] = None, limit: int = 10):
            """Get recent analyses from registry."""
            analyses = await self.registry.list_recent(repo=repo, limit=limit)
            return {"analyses": analyses, "count": len(analyses)}
        
        @self.app.get("/api/registry/summary")
        async def get_registry_summary(repo: Optional[str] = None):
            """Get registry summary statistics."""
            summary = await self.registry.get_summary(repo=repo)
            return summary
    
    async def _run_analysis(
        self,
        job_id: str,
        repo: str,
        trigger: str,
        timestamp: str,
        commit_sha: str,
        metadata: Dict[str, Any]
    ) -> None:
        """
        Run analysis pipeline in background.
        
        Orchestrates:
        1. Assign Colab kernel
        2. Load analysis code from repo
        3. Execute analysis
        4. Register results in AttributionRegistry
        5. Commit results back to repo
        """
        try:
            logger.info(f"[{job_id}] Starting analysis for {repo}")
            
            # Step 1: Assign kernel
            logger.info(f"[{job_id}] Assigning Colab kernel...")
            kernel_id = await self.colab.assign(
                account="default",
                machine_type="L4"
            )
            
            # Step 2: Load analysis config
            logger.info(f"[{job_id}] Loading analysis config...")
            try:
                config_content = await self.github.get_file_content(
                    repo=repo,
                    path="analysis_config.json",
                    branch="main"
                )
                analysis_config = json.loads(config_content)
            except:
                # Use default config
                analysis_config = {"timeout": 3600}
            
            # Step 3: Load and execute analysis code
            logger.info(f"[{job_id}] Executing analysis code...")
            code = f"""
# Analysis for {repo}
# Job: {job_id}

import json
from datetime import datetime

# Load data
print(f'Loading data from {repo}...')

# Run analysis (placeholder)
results = {{
    "analyzed_at": "{timestamp}",
    "repo": "{repo}",
    "status": "completed"
}}

print(json.dumps(results, indent=2))
"""
            
            output = await self.colab.execute(
                kernel_id=kernel_id,
                code=code,
                timeout=analysis_config.get("timeout", 3600)
            )
            
            # Parse results
            try:
                results = json.loads(output.split('\n')[-1])
            except:
                results = {"raw_output": output}
            
            logger.info(f"[{job_id}] Analysis complete, registering...")
            
            # Step 4: Register in AttributionRegistry
            analysis_id = await self.registry.add_analysis(
                repo=repo,
                timestamp=timestamp,
                machine_type="L4",
                ccu_consumed=0.5,  # Placeholder
                metadata={
                    "trigger": trigger,
                    "commit": commit_sha,
                    **metadata
                },
                results=results
            )
            
            logger.info(f"[{job_id}] Registered as {analysis_id}")
            
            # Step 5: Commit results back to repo
            logger.info(f"[{job_id}] Writing results to {repo}...")
            await self.github.create_file(
                repo=repo,
                path=f"analysis_results/{job_id}.json",
                content=json.dumps({
                    "job_id": job_id,
                    "analysis_id": analysis_id,
                    "timestamp": timestamp,
                    "results": results
                }, indent=2),
                message=f"Analysis results: {job_id}",
                branch="main"
            )
            
            logger.info(f"[{job_id}] COMPLETE")
        
        except Exception as e:
            logger.error(f"[{job_id}] FAILED: {e}")
            raise
        
        finally:
            # Clean up
            if 'kernel_id' in locals():
                try:
                    await self.colab.unassign(kernel_id)
                    logger.info(f"[{job_id}] Kernel released")
                except:
                    pass
    
    def run(self, host: str = "0.0.0.0", port: int = 8080) -> None:
        """
        Run the server.
        
        Args:
            host: Server host
            port: Server port
        """
        uvicorn.run(
            self.app,
            host=host,
            port=port,
            log_level="info"
        )

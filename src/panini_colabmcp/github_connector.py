"""
GitHub API Connector

Handles:
- Repository webhook events
- Workflow dispatch triggers
- Commit tracking
- PR/issue integration
"""

import logging
from typing import Optional, Dict, Any, List
import aiohttp
from github import Github
from github.GithubException import GithubException

logger = logging.getLogger(__name__)


class GitHubConnector:
    """
    GitHub API wrapper for Panini ecosystem.
    
    Uses PyGithub for REST API and aiohttp for webhooks.
    """
    
    def __init__(self, config):
        """
        Initialize GitHub connector.
        
        Args:
            config: Configuration with github_token and github_owner
        """
        self.config = config
        self.gh = Github(config.github_token)
        self.owner = config.github_owner
    
    async def list_repos(
        self,
        owner: Optional[str] = None,
        pattern: Optional[str] = None
    ) -> List[str]:
        """
        List repositories matching pattern.
        
        Args:
            owner: GitHub owner/org (defaults to config.github_owner)
            pattern: Repo name pattern (e.g., "Panini-*")
        
        Returns:
            List of repo names
        """
        try:
            owner = owner or self.owner
            org = self.gh.get_organization(owner)
            
            repos = []
            for repo in org.get_repos():
                if pattern is None or self._match_pattern(repo.name, pattern):
                    repos.append(repo.name)
            
            return repos
        
        except GithubException as e:
            logger.error(f"List repos error: {e}")
            raise
    
    async def dispatch(
        self,
        repo: str,
        event_type: str,
        client_payload: Dict[str, Any]
    ) -> None:
        """
        Trigger repository dispatch event.
        
        This is the key mechanism for triggering analysis workflows.
        
        Args:
            repo: Repository name
            event_type: Event type (e.g., "new-data", "manual-trigger")
            client_payload: Custom data passed to workflow
        """
        try:
            repository = self.gh.get_user(self.owner).get_repo(repo)
            
            repository.create_repository_dispatch(
                event_type=event_type,
                client_payload=client_payload
            )
            
            logger.info(
                f"Dispatched {event_type} to {repo} "
                f"with payload: {client_payload}"
            )
        
        except GithubException as e:
            logger.error(f"Dispatch error: {e}")
            raise
    
    async def get_commits(
        self,
        repo: str,
        branch: str = "main",
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get recent commits from repository.
        
        Args:
            repo: Repository name
            branch: Branch name
            limit: Maximum commits to return
        
        Returns:
            List of commit dicts
        """
        try:
            repository = self.gh.get_user(self.owner).get_repo(repo)
            commits = repository.get_commits(sha=branch)
            
            result = []
            for i, commit in enumerate(commits):
                if i >= limit:
                    break
                
                result.append({
                    "sha": commit.sha,
                    "message": commit.commit.message,
                    "author": commit.commit.author.name,
                    "timestamp": commit.commit.author.date.isoformat(),
                    "url": commit.html_url,
                })
            
            return result
        
        except GithubException as e:
            logger.error(f"Get commits error: {e}")
            raise
    
    async def get_file_content(
        self,
        repo: str,
        path: str,
        branch: str = "main"
    ) -> str:
        """
        Get file content from repository.
        
        Args:
            repo: Repository name
            path: File path
            branch: Branch name
        
        Returns:
            File content as string
        """
        try:
            repository = self.gh.get_user(self.owner).get_repo(repo)
            content = repository.get_contents(path, ref=branch)
            
            if isinstance(content, list):
                raise ValueError(f"Path {path} is a directory")
            
            return content.decoded_content.decode('utf-8')
        
        except GithubException as e:
            logger.error(f"Get file error: {e}")
            raise
    
    async def create_file(
        self,
        repo: str,
        path: str,
        content: str,
        message: str,
        branch: str = "main"
    ) -> None:
        """
        Create or update file in repository.
        
        Args:
            repo: Repository name
            path: File path
            content: File content
            message: Commit message
            branch: Branch name
        """
        try:
            repository = self.gh.get_user(self.owner).get_repo(repo)
            
            try:
                # Try to get existing file
                existing = repository.get_contents(path, ref=branch)
                repository.update_file(
                    path=path,
                    message=message,
                    content=content,
                    sha=existing.sha,
                    branch=branch
                )
                logger.info(f"Updated {path} in {repo}")
            except GithubException:
                # File doesn't exist, create it
                repository.create_file(
                    path=path,
                    message=message,
                    content=content,
                    branch=branch
                )
                logger.info(f"Created {path} in {repo}")
        
        except GithubException as e:
            logger.error(f"Create/update file error: {e}")
            raise
    
    async def list_active_workflows(
        self,
        repo: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List active workflow runs.
        
        Args:
            repo: Repository name (optional, lists all if not provided)
        
        Returns:
            List of workflow dicts
        """
        try:
            if repo:
                repos = [repo]
            else:
                repos = await self.list_repos()
            
            workflows = []
            for repo_name in repos:
                repository = self.gh.get_user(self.owner).get_repo(repo_name)
                
                for workflow_run in repository.get_workflow_runs(status="in_progress"):
                    workflows.append({
                        "repo": repo_name,
                        "id": workflow_run.id,
                        "name": workflow_run.name,
                        "status": workflow_run.status,
                        "created_at": workflow_run.created_at.isoformat(),
                        "url": workflow_run.html_url,
                    })
            
            return workflows
        
        except GithubException as e:
            logger.error(f"List workflows error: {e}")
            raise
    
    async def get_latest_release(self, repo: str) -> Optional[Dict[str, Any]]:
        """
        Get latest release from repository.
        
        Args:
            repo: Repository name
        
        Returns:
            Release dict or None
        """
        try:
            repository = self.gh.get_user(self.owner).get_repo(repo)
            release = repository.get_latest_release()
            
            return {
                "tag": release.tag_name,
                "name": release.name,
                "body": release.body,
                "published_at": release.published_at.isoformat(),
                "url": release.html_url,
            }
        
        except GithubException:
            return None
    
    @staticmethod
    def _match_pattern(name: str, pattern: str) -> bool:
        """Simple glob pattern matching"""
        import fnmatch
        return fnmatch.fnmatch(name, pattern)

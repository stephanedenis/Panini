"""
Resource definitions for Panini ColabMCP
"""


class Resources:
    """Resource registry for MCP server"""
    
    @staticmethod
    def get_analysis_template():
        """Get analysis template resource"""
        return {
            "uri": "analysis://template",
            "mimeType": "application/json",
            "name": "Analysis Template",
            "description": "Template for new analysis configurations"
        }
    
    @staticmethod
    def get_kernel_status():
        """Get kernel status resource"""
        return {
            "uri": "kernel://status",
            "mimeType": "application/json",
            "name": "Kernel Status",
            "description": "Current kernel status and availability"
        }


class ColabClient:
    """Wrapper for Colab API"""
    async def assign(self, account, machine_type): pass
    async def execute(self, kernel_id, code, timeout): pass
    async def get_quota(self, account): pass
    async def unassign(self, kernel_id): pass
    async def get_status(self): pass


class OAuthManager:
    """OAuth2 token management"""
    async def get_token(self, account): pass
    async def refresh_token(self, account): pass


class GitHubConnector:
    """GitHub API wrapper"""
    async def list_repos(self, owner, pattern): pass
    async def dispatch(self, repo, event_type, payload): pass
    async def get_commits(self, repo, branch, limit): pass
    async def list_active_workflows(self): pass


class RegistryWriter:
    """Attribution Registry writes"""
    async def add_analysis(self, analysis_id, repo, metadata): pass
    async def list_recent(self, repo, limit): pass



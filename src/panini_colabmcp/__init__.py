"""
Panini ColabMCP - GitHub-native MCP server for Colab orchestration

Main entry point combining all components:
- MCP server (tools + resources)
- FastAPI HTTP wrapper
- OAuth2 token management
- Attribution registry integration
"""

import sys
import logging
from typing import Optional

import asyncio
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Import components
try:
    from .colab_client import ColabClient
    from .oauth_manager import OAuthManager
    from .github_connector import GitHubConnector
    from .registry_writer import RegistryWriter
    from .git_registry import GitRegistry
    from .analyzer_server import AnalyzerServer
    from .config import Config
    from .resources import Resources
    
    __all__ = [
        "ColabClient",
        "OAuthManager",
        "GitHubConnector",
        "RegistryWriter",
        "GitRegistry",
        "AnalyzerServer",
        "Config",
        "Resources",
        "PaniniColabMCP",
    ]
except ImportError as e:
    logger.warning(f"Some components not yet installed: {e}")


class PaniniColabMCP:
    """
    Main orchestrator combining MCP server and HTTP wrapper.
    
    Usage:
        config = Config()
        app = PaniniColabMCP(config)
        
        # Option 1: Run as MCP server
        await app.run_mcp()
        
        # Option 2: Run as HTTP server
        app.run_http()
    """
    
    def __init__(self, config):
        """Initialize with configuration."""
        self.config = config
        # Components will be initialized on demand
        self._components = {}
    
    def _get_oauth_manager(self):
        """Lazy load OAuth manager."""
        if "oauth" not in self._components:
            # from .oauth_manager import OAuthManager
            # self._components["oauth"] = OAuthManager(self.config)
            pass
        return self._components.get("oauth")
    
    def _get_colab_client(self):
        """Lazy load Colab client."""
        if "colab" not in self._components:
            # from .colab_client import ColabClient
            # self._components["colab"] = ColabClient(self.config)
            pass
        return self._components.get("colab")
    
    def _get_github_connector(self):
        """Lazy load GitHub connector."""
        if "github" not in self._components:
            # from .github_connector import GitHubConnector
            # self._components["github"] = GitHubConnector(self.config)
            pass
        return self._components.get("github")
    
    def _get_registry_writer(self):
        """Lazy load registry writer."""
        if "registry" not in self._components:
            # from .registry_writer import RegistryWriter
            # self._components["registry"] = RegistryWriter(
            #     self.config,
            #     self._get_github_connector()
            # )
            pass
        return self._components.get("registry")
    
    async def run_mcp(self) -> None:
        """
        Run as standalone MCP server.
        
        Listens for MCP calls over stdio and routes to handlers.
        """
        logger.info("Starting Panini ColabMCP server...")
        
        # from .server import ColabMCPServer
        # server = ColabMCPServer(self.config)
        # await server.run()
        
        raise NotImplementedError("MCP server mode not yet implemented")
    
    def run_http(self, host: str = "0.0.0.0", port: int = 8080) -> None:
        """
        Run as HTTP server (FastAPI).
        
        Exposes REST endpoints for GitHub Actions integration.
        """
        logger.info(f"Starting HTTP server on {host}:{port}...")
        
        # from .analyzer_server import AnalyzerServer
        # server = AnalyzerServer(
        #     mcp_client=None,  # Direct component access
        #     github=self._get_github_connector(),
        #     colab=self._get_colab_client(),
        #     registry=self._get_registry_writer()
        # )
        # server.run(host=host, port=port)
        
        raise NotImplementedError("HTTP server mode not yet implemented")


def main():
    """Command-line entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Panini ColabMCP - Colab Analysis Orchestrator"
    )
    parser.add_argument(
        "--mode",
        choices=["mcp", "http"],
        default="http",
        help="Server mode (mcp or http)"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="HTTP server host (http mode only)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="HTTP server port (http mode only)"
    )
    parser.add_argument(
        "--config",
        help="Path to config file"
    )
    
    args = parser.parse_args()
    
    try:
        # Load config
        # from .config import Config
        # config = Config()  # Will load from env/config file
        
        logger.info(f"Initializing Panini ColabMCP (mode={args.mode})...")
        
        # app = PaniniColabMCP(config)
        
        if args.mode == "mcp":
            # asyncio.run(app.run_mcp())
            logger.error("MCP mode not yet implemented")
            sys.exit(1)
        else:  # http
            # app.run_http(host=args.host, port=args.port)
            logger.error("HTTP mode not yet implemented")
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

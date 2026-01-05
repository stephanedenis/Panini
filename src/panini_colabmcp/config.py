"""
Configuration management for Panini-CoLabMCP
Loads from environment, .env, and GitHub Secrets
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Config(BaseSettings):
    """Application configuration"""
    
    # Environment
    env: str = Field(default="development", description="Environment: development|staging|production")
    log_level: str = Field(default="INFO", description="Logging level")
    
    # Colab OAuth2
    google_client_id: str = Field(description="Google OAuth2 Client ID")
    google_client_secret: str = Field(description="Google OAuth2 Client Secret")
    google_redirect_uri: str = Field(default="http://localhost:8080/auth/callback")
    
    # GitHub
    github_token: str = Field(description="GitHub Personal Access Token")
    github_owner: str = Field(default="stephanedenis", description="GitHub organization/user")
    
    # Database (Attribution Registry)
    database_url: Optional[str] = Field(
        default=None,
        description="PostgreSQL connection string for registry"
    )
    
    # Service URLs
    colab_api_url: str = Field(
        default="https://colab.research.google.com/api/ml/v1",
        description="Colab API base URL"
    )
    mcp_server_url: str = Field(
        default="http://localhost:8080",
        description="MCP Server URL for webhooks"
    )
    
    # Compute settings
    default_machine_type: str = Field(
        default="TPM_V5_EDGE",
        description="Default Colab machine type"
    )
    max_compute_hours: float = Field(
        default=24.0,
        description="Maximum compute hours per analysis"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


def get_config() -> Config:
    """Get configuration instance"""
    return Config()

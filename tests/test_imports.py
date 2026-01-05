"""
Test module imports - verify Phase 3a setup
"""

import pytest


def test_colab_client_import():
    """Test ColabClient can be imported"""
    from panini_colabmcp import ColabClient
    assert ColabClient is not None
    assert hasattr(ColabClient, "assign")
    assert hasattr(ColabClient, "execute")


def test_oauth_manager_import():
    """Test OAuthManager can be imported"""
    from panini_colabmcp import OAuthManager
    assert OAuthManager is not None
    assert hasattr(OAuthManager, "get_token")


def test_github_connector_import():
    """Test GitHubConnector can be imported"""
    from panini_colabmcp import GitHubConnector
    assert GitHubConnector is not None
    assert hasattr(GitHubConnector, "list_repos")


def test_registry_writer_import():
    """Test RegistryWriter can be imported"""
    from panini_colabmcp import RegistryWriter
    assert RegistryWriter is not None
    assert hasattr(RegistryWriter, "add_analysis")


def test_analyzer_server_import():
    """Test AnalyzerServer can be imported"""
    from panini_colabmcp import AnalyzerServer
    assert AnalyzerServer is not None


def test_config_import():
    """Test Config can be imported"""
    from panini_colabmcp import Config
    assert Config is not None


def test_resources_import():
    """Test Resources can be imported"""
    from panini_colabmcp import Resources
    assert Resources is not None
    assert hasattr(Resources, "get_analysis_template")
    assert hasattr(Resources, "get_kernel_status")


def test_all_imports_together():
    """Test all components import together"""
    from panini_colabmcp import (
        ColabClient,
        OAuthManager,
        GitHubConnector,
        RegistryWriter,
        AnalyzerServer,
        Config,
        Resources,
    )
    
    # Verify all are classes/objects
    assert all([
        ColabClient,
        OAuthManager,
        GitHubConnector,
        RegistryWriter,
        AnalyzerServer,
        Config,
        Resources,
    ])

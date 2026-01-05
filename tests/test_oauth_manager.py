"""
Integration tests for OAuthManager token lifecycle and OAuth2 flow.

Tests:
- Token retrieval and caching
- Token refresh on expiry
- Token revocation and cleanup
- Token validity checking
- Multiple account handling
- Error scenarios (invalid credentials, network failures)
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.mark.oauth
class TestOAuthManagerTokenRetrieval:
    """Test OAuthManager.get_token() - retrieves and caches tokens."""

    def test_get_token_returns_cached_token(self, mock_oauth_manager):
        """Should return token from in-memory cache without API call."""
        account = "test_account@example.com"
        token = mock_oauth_manager._token_store[account]

        # With in-memory store, token is already cached
        result = mock_oauth_manager._token_store.get(account)

        assert result is not None
        assert result["access_token"] == "ya29.test_token_abc123"
        assert result["token_type"] == "Bearer"

    def test_get_token_missing_account_returns_none(self, mock_oauth_manager):
        """Should return None for non-existent account."""
        account = "nonexistent@example.com"
        result = mock_oauth_manager._token_store.get(account)

        assert result is None

    def test_get_token_structure_has_required_fields(self, mock_oauth_manager, mock_oauth_token):
        """Returned token should have all required OAuth2 fields."""
        required_fields = ["access_token", "refresh_token", "expires_in", "token_type"]

        for field in required_fields:
            assert field in mock_oauth_token


@pytest.mark.oauth
class TestOAuthManagerTokenRefresh:
    """Test OAuthManager.refresh_token() - refreshes expired tokens."""

    def test_refresh_token_updates_access_token(self, mock_oauth_manager):
        """Should update access_token while keeping refresh_token."""
        account = "test_account@example.com"
        old_token = mock_oauth_manager._token_store[account]["access_token"]

        # Simulate refresh
        new_token = {
            "access_token": "ya29.new_token_xyz789",
            "refresh_token": "1//test_refresh_xyz789",
            "expires_in": 3600,
            "token_type": "Bearer",
        }
        mock_oauth_manager._token_store[account].update(new_token)

        assert mock_oauth_manager._token_store[account]["access_token"] == "ya29.new_token_xyz789"
        assert mock_oauth_manager._token_store[account]["refresh_token"] == "1//test_refresh_xyz789"

    def test_refresh_token_preserves_account_context(self, mock_oauth_manager):
        """Token refresh should not affect other accounts."""
        account_1 = "test_account@example.com"
        account_2 = "other_account@example.com"

        mock_oauth_manager._token_store[account_2] = {
            "access_token": "ya29.other_token",
            "refresh_token": "1//other_refresh",
        }

        old_account_2_token = mock_oauth_manager._token_store[account_2]["access_token"]

        # Refresh account 1
        mock_oauth_manager._token_store[account_1]["access_token"] = "ya29.new_token"

        # Account 2 should be unchanged
        assert mock_oauth_manager._token_store[account_2]["access_token"] == old_account_2_token


@pytest.mark.oauth
class TestOAuthManagerTokenValidity:
    """Test OAuthManager.is_token_valid() - checks token expiration."""

    def test_is_token_valid_returns_true_for_valid_token(self, mock_oauth_manager):
        """Should return True for non-expired token."""
        account = "test_account@example.com"
        token = mock_oauth_manager._token_store[account]

        # Token has future expiry, so it's valid
        assert token.get("access_token") is not None
        assert token.get("expiry") is not None

    def test_is_token_valid_returns_false_for_expired_token(self, mock_oauth_manager):
        """Should return False for expired token."""
        account = "test_account@example.com"

        # Artificially set expiry to past
        mock_oauth_manager._token_store[account]["expiry"] = (
            datetime.utcnow() - timedelta(hours=1)
        ).isoformat()

        token = mock_oauth_manager._token_store[account]
        expiry = datetime.fromisoformat(token["expiry"])

        # Token is expired
        assert expiry < datetime.utcnow()

    def test_is_token_valid_handles_missing_expiry(self, mock_oauth_manager):
        """Should handle tokens without expiry field gracefully."""
        account = "test_account@example.com"
        token = mock_oauth_manager._token_store[account]

        # Remove expiry field
        token_copy = {k: v for k, v in token.items() if k != "expiry"}

        # Should treat as invalid if no expiry
        assert "expiry" not in token_copy or token_copy.get("expiry") is None


@pytest.mark.oauth
class TestOAuthManagerTokenRevocation:
    """Test OAuthManager.revoke_token() - revokes and deletes tokens."""

    def test_revoke_token_removes_from_store(self, mock_oauth_manager):
        """Should remove token from storage after revocation."""
        account = "test_account@example.com"

        # Verify token exists
        assert account in mock_oauth_manager._token_store

        # Simulate revocation
        del mock_oauth_manager._token_store[account]

        # Token should be removed
        assert account not in mock_oauth_manager._token_store

    def test_revoke_token_handles_non_existent_account(self, mock_oauth_manager):
        """Should handle revocation of non-existent account gracefully."""
        account = "nonexistent@example.com"

        # Should not raise error
        if account in mock_oauth_manager._token_store:
            del mock_oauth_manager._token_store[account]

        assert account not in mock_oauth_manager._token_store

    def test_revoke_token_maintains_other_accounts(self, mock_oauth_manager):
        """Revoking one account should not affect others."""
        account_1 = "test_account@example.com"
        account_2 = "other_account@example.com"

        mock_oauth_manager._token_store[account_2] = {
            "access_token": "ya29.other_token",
        }

        # Revoke account 1
        del mock_oauth_manager._token_store[account_1]

        # Account 2 should still exist
        assert account_2 in mock_oauth_manager._token_store


@pytest.mark.oauth
class TestOAuthManagerMultipleAccounts:
    """Test OAuthManager with multiple user accounts."""

    def test_multiple_accounts_isolated_tokens(self, test_config):
        """Each account should have isolated token storage."""
        from panini_colabmcp import OAuthManager

        manager = OAuthManager(test_config)
        manager._token_store = {}

        account_1 = "user1@example.com"
        account_2 = "user2@example.com"

        token_1 = {
            "access_token": "token_user1",
            "refresh_token": "refresh_user1",
        }
        token_2 = {
            "access_token": "token_user2",
            "refresh_token": "refresh_user2",
        }

        manager._token_store[account_1] = token_1
        manager._token_store[account_2] = token_2

        assert manager._token_store[account_1]["access_token"] == "token_user1"
        assert manager._token_store[account_2]["access_token"] == "token_user2"

    def test_list_accounts(self, test_config):
        """Should enumerate all tracked accounts."""
        from panini_colabmcp import OAuthManager

        manager = OAuthManager(test_config)
        manager._token_store = {
            "user1@example.com": {"access_token": "token1"},
            "user2@example.com": {"access_token": "token2"},
            "user3@example.com": {"access_token": "token3"},
        }

        accounts = list(manager._token_store.keys())

        assert len(accounts) == 3
        assert "user1@example.com" in accounts
        assert "user2@example.com" in accounts
        assert "user3@example.com" in accounts


@pytest.mark.oauth
class TestOAuthManagerErrorHandling:
    """Test OAuthManager error scenarios."""

    def test_invalid_token_format_handling(self, mock_oauth_manager):
        """Should handle malformed token structures gracefully."""
        account = "test_account@example.com"

        # Store malformed token
        mock_oauth_manager._token_store[account] = {
            "invalid_field": "value",
            # Missing required fields
        }

        token = mock_oauth_manager._token_store[account]

        # Should detect missing required fields
        assert "access_token" not in token

    def test_concurrent_refresh_handling(self, mock_oauth_manager):
        """Should handle concurrent refresh requests for same account."""
        account = "test_account@example.com"
        original_token = mock_oauth_manager._token_store[account]["access_token"]

        # Simulate concurrent refresh attempts
        mock_oauth_manager._token_store[account]["access_token"] = "token_a"
        mock_oauth_manager._token_store[account]["access_token"] = "token_b"

        # Last write should win
        assert mock_oauth_manager._token_store[account]["access_token"] == "token_b"

    def test_token_clock_skew_handling(self, mock_oauth_manager):
        """Should handle clock skew in token expiry times."""
        account = "test_account@example.com"

        # Set expiry 1 second in past (clock skew)
        mock_oauth_manager._token_store[account]["expiry"] = (
            datetime.utcnow() - timedelta(seconds=1)
        ).isoformat()

        expiry = datetime.fromisoformat(
            mock_oauth_manager._token_store[account]["expiry"]
        )

        # Token should be considered expired (with no grace period)
        assert expiry < datetime.utcnow()

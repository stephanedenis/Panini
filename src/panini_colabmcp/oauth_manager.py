"""
OAuth2 Token Management for Google Colab

Handles persistent storage of refresh tokens and auto-refresh of access tokens.
Supports multiple storage backends:
- PostgreSQL (production)
- GitHub Secrets (fallback)
- In-memory with .env (development)
"""

import logging
import json
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import asyncio
from abc import ABC, abstractmethod

from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.oauth2.credentials import Credentials as UserCredentials
from google_auth_oauthlib.flow import InstalledAppFlow

logger = logging.getLogger(__name__)


class TokenStore(ABC):
    """Abstract token storage backend"""
    
    @abstractmethod
    async def get(self, account: str) -> Optional[Dict[str, Any]]:
        pass
    
    @abstractmethod
    async def set(self, account: str, token_data: Dict[str, Any]) -> None:
        pass
    
    @abstractmethod
    async def delete(self, account: str) -> None:
        pass


class InMemoryTokenStore(TokenStore):
    """In-memory token store (development)"""
    
    def __init__(self):
        self.tokens: Dict[str, Dict[str, Any]] = {}
    
    async def get(self, account: str) -> Optional[Dict[str, Any]]:
        return self.tokens.get(account)
    
    async def set(self, account: str, token_data: Dict[str, Any]) -> None:
        self.tokens[account] = token_data
    
    async def delete(self, account: str) -> None:
        self.tokens.pop(account, None)


class PostgreSQLTokenStore(TokenStore):
    """PostgreSQL token store (production)"""
    
    def __init__(self, database_url: str):
        """
        Initialize with SQLAlchemy connection.
        Creates oauth_tokens table if needed.
        """
        from sqlalchemy import create_engine, Table, Column, String, JSON, DateTime
        from sqlalchemy.orm import sessionmaker
        
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Create table
        self.metadata = sa.MetaData()
        self.oauth_tokens_table = Table(
            'oauth_tokens',
            self.metadata,
            Column('account', String, primary_key=True),
            Column('access_token', String, nullable=False),
            Column('refresh_token', String, nullable=False),
            Column('expires_at', DateTime, nullable=False),
            Column('scopes', JSON, nullable=False),
            Column('created_at', DateTime, default=datetime.utcnow),
            Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
        )
        
        self.metadata.create_all(self.engine)
    
    async def get(self, account: str) -> Optional[Dict[str, Any]]:
        session = self.SessionLocal()
        try:
            row = session.query(self.oauth_tokens_table).filter_by(
                account=account
            ).first()
            if row:
                return dict(row)
            return None
        finally:
            session.close()
    
    async def set(self, account: str, token_data: Dict[str, Any]) -> None:
        session = self.SessionLocal()
        try:
            session.execute(
                self.oauth_tokens_table.insert().values(
                    account=account,
                    **token_data
                ).on_conflict_do_update(
                    index_elements=['account'],
                    set_=token_data
                )
            )
            session.commit()
        finally:
            session.close()
    
    async def delete(self, account: str) -> None:
        session = self.SessionLocal()
        try:
            session.execute(
                self.oauth_tokens_table.delete().where(
                    self.oauth_tokens_table.c.account == account
                )
            )
            session.commit()
        finally:
            session.close()


class OAuthManager:
    """
    Google OAuth2 token manager.
    
    Features:
    - Persistent token storage
    - Automatic token refresh (5-min margin)
    - Multi-account support
    - Initial auth flow setup
    """
    
    # Google Colab scopes
    SCOPES = [
        "https://www.googleapis.com/auth/drive.readonly",
        "https://www.googleapis.com/auth/colaboratory",
        "https://www.googleapis.com/auth/userinfo.email",
    ]
    
    TOKEN_REFRESH_MARGIN = 300  # seconds (5 minutes)
    
    def __init__(self, config, token_store: Optional[TokenStore] = None):
        """
        Initialize OAuthManager.
        
        Args:
            config: Configuration with OAuth2 credentials
            token_store: TokenStore implementation (defaults to InMemory)
        """
        self.config = config
        self.token_store = token_store or InMemoryTokenStore()
        self._refresh_locks: Dict[str, asyncio.Lock] = {}
    
    async def get_token(self, account: str) -> str:
        """
        Get valid access token for account.
        Auto-refreshes if expired.
        
        Args:
            account: Google account email
        
        Returns:
            Valid access token
        
        Raises:
            ValueError: Account not authenticated
        """
        # Get or create refresh lock
        if account not in self._refresh_locks:
            self._refresh_locks[account] = asyncio.Lock()
        
        lock = self._refresh_locks[account]
        
        async with lock:
            token_data = await self.token_store.get(account)
            
            if not token_data:
                raise ValueError(
                    f"Account {account} not authenticated. "
                    f"Run init_auth() first."
                )
            
            # Check if refresh needed
            expires_at = datetime.fromisoformat(token_data["expires_at"])
            refresh_threshold = datetime.utcnow() + timedelta(
                seconds=self.TOKEN_REFRESH_MARGIN
            )
            
            if expires_at < refresh_threshold:
                logger.info(f"Refreshing token for {account}")
                await self._refresh_token(account, token_data)
                token_data = await self.token_store.get(account)
            
            return token_data["access_token"]
    
    async def _refresh_token(
        self,
        account: str,
        token_data: Dict[str, Any]
    ) -> None:
        """Refresh expired token"""
        try:
            credentials = UserCredentials(
                token=token_data["access_token"],
                refresh_token=token_data["refresh_token"],
                token_uri="https://oauth2.googleapis.com/token",
                client_id=self.config.google_client_id,
                client_secret=self.config.google_client_secret,
            )
            
            request = Request()
            credentials.refresh(request)
            
            # Update storage
            token_data["access_token"] = credentials.token
            token_data["expires_at"] = (
                datetime.utcnow() + 
                timedelta(seconds=credentials.expiry.total_seconds())
            ).isoformat()
            
            await self.token_store.set(account, token_data)
            logger.info(f"Token refreshed for {account}")
        
        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            # Remove invalid token
            await self.token_store.delete(account)
            raise ValueError(f"Token refresh failed: {e}")
    
    async def init_auth(self, account: str, auth_code: Optional[str] = None) -> str:
        """
        Initialize authentication for account.
        
        If auth_code provided, exchanges it for tokens.
        Otherwise returns auth URL for user to visit.
        
        Args:
            account: Google account email
            auth_code: OAuth2 auth code (from redirect)
        
        Returns:
            Auth URL (if no code) or access token (if code provided)
        """
        flow = InstalledAppFlow.from_client_secrets_file(
            self.config.google_credentials_json,
            scopes=self.SCOPES,
            redirect_uri=self.config.google_redirect_uri,
        )
        
        if not auth_code:
            # Return auth URL
            auth_uri, _ = flow.authorization_url(
                prompt="consent",
                access_type="offline",
                login_hint=account,
            )
            return auth_uri
        
        else:
            # Exchange code for tokens
            credentials = flow.fetch_token(code=auth_code)
            
            # Store token
            token_data = {
                "access_token": credentials["access_token"],
                "refresh_token": credentials.get("refresh_token"),
                "expires_at": (
                    datetime.utcnow() + 
                    timedelta(seconds=credentials.get("expires_in", 3600))
                ).isoformat(),
                "scopes": self.SCOPES,
            }
            
            await self.token_store.set(account, token_data)
            logger.info(f"Authenticated {account}")
            
            return credentials["access_token"]
    
    async def revoke_token(self, account: str) -> None:
        """
        Revoke token for account.
        
        Args:
            account: Google account email
        """
        token_data = await self.token_store.get(account)
        if not token_data:
            return
        
        try:
            credentials = UserCredentials(
                token=token_data["access_token"],
                refresh_token=token_data["refresh_token"],
                token_uri="https://oauth2.googleapis.com/token",
                client_id=self.config.google_client_id,
                client_secret=self.config.google_client_secret,
            )
            
            credentials.revoke(Request())
        except Exception as e:
            logger.warning(f"Revoke failed (continuing): {e}")
        
        finally:
            await self.token_store.delete(account)
            logger.info(f"Revoked token for {account}")
    
    async def list_accounts(self) -> list:
        """List authenticated accounts"""
        # This would need backend support in token store
        raise NotImplementedError()

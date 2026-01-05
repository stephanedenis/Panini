"""
Google Colab API Client

Direct wrapper for Colab API without VSCode extension dependency.
Handles:
- Machine assignment/unassignment
- Kernel execution
- CCU quota monitoring
- WebSocket tunnel management
"""

import asyncio
import aiohttp
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)


class ColabApiException(Exception):
    """Colab API error"""
    pass


class QuotaExceededException(ColabApiException):
    """Insufficient compute quota"""
    pass


class TooManyAssignmentsException(ColabApiException):
    """Too many simultaneous assignments"""
    pass


class ColabClient:
    """
    Google Colab API client.
    
    API Documentation:
    - Base: https://colab.research.google.com/api/ml/v1/
    - Endpoints:
      - POST /kernels/assignments → Create assignment
      - GET /kernels/assignments → List assignments
      - DELETE /kernels/assignments/{id} → Unassign
      - GET /account/ccu → Check CCU quota
      - POST /kernels/{id}/keep-alive → Persist assignment
    """
    
    COLAB_API_BASE = "https://colab.research.google.com/api/ml/v1"
    KEEP_ALIVE_INTERVAL = 60  # seconds (Colab timeout is ~30 min)
    
    def __init__(self, config, oauth_manager):
        """
        Initialize ColabClient.
        
        Args:
            config: Configuration object with colab_api_url
            oauth_manager: OAuthManager for token access
        """
        self.config = config
        self.oauth_manager = oauth_manager
        self.session: Optional[aiohttp.ClientSession] = None
        self._assignments: Dict[str, Dict[str, Any]] = {}
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def _get_headers(self, account: str) -> Dict[str, str]:
        """Get authorization headers"""
        token = await self.oauth_manager.get_token(account)
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
    
    async def assign(
        self,
        account: str,
        machine_type: str = "TPM_V5_EDGE",
        timeout: int = 300
    ) -> str:
        """
        Assign a Colab machine.
        
        Args:
            account: Google account email
            machine_type: Machine type (TPM_V5_EDGE, L4, H100, etc.)
            timeout: Request timeout in seconds
        
        Returns:
            kernel_id: ID of assigned kernel
        
        Raises:
            QuotaExceededException: Insufficient CCU
            TooManyAssignmentsException: Too many active assignments
        """
        session = await self._get_session()
        headers = await self._get_headers(account)
        
        payload = {
            "machine_type": machine_type,
            "gpu_type": self._machine_to_gpu(machine_type),
        }
        
        try:
            async with session.post(
                f"{self.COLAB_API_BASE}/kernels/assignments",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=timeout)
            ) as resp:
                if resp.status == 429:
                    raise TooManyAssignmentsException(
                        "Too many simultaneous assignments. Try again later."
                    )
                elif resp.status == 402:
                    raise QuotaExceededException(
                        "Insufficient CCU quota for machine type"
                    )
                elif resp.status != 200:
                    text = await resp.text()
                    raise ColabApiException(
                        f"Assignment failed ({resp.status}): {text}"
                    )
                
                data = await resp.json()
                kernel_id = data["assignment"]["kernel_id"]
                
                # Track assignment
                self._assignments[kernel_id] = {
                    "account": account,
                    "machine_type": machine_type,
                    "assigned_at": datetime.utcnow(),
                    "keep_alive_task": None,
                }
                
                # Start keep-alive background task
                keep_alive_task = asyncio.create_task(
                    self._keep_alive_loop(kernel_id, account)
                )
                self._assignments[kernel_id]["keep_alive_task"] = keep_alive_task
                
                logger.info(
                    f"Assigned kernel {kernel_id} ({machine_type}) "
                    f"to {account}"
                )
                return kernel_id
        
        except aiohttp.ClientError as e:
            raise ColabApiException(f"Network error during assignment: {e}")
    
    async def execute(
        self,
        kernel_id: str,
        code: str,
        timeout: int = 300
    ) -> Dict[str, Any]:
        """
        Execute Python code in assigned kernel.
        
        Args:
            kernel_id: Kernel ID from assign()
            code: Python code to execute
            timeout: Execution timeout in seconds
        
        Returns:
            Dict with 'stdout', 'stderr', 'result', 'status'
        """
        if kernel_id not in self._assignments:
            raise ColabApiException(f"Unknown kernel: {kernel_id}")
        
        account = self._assignments[kernel_id]["account"]
        session = await self._get_session()
        headers = await self._get_headers(account)
        
        # WebSocket connection to kernel input/output
        ws_url = (
            f"wss://colab.research.google.com/api/ml/v1/kernels/{kernel_id}/ws"
        )
        
        try:
            async with session.ws_connect(ws_url, headers=headers) as ws:
                # Send code
                await ws.send_json({
                    "method": "execute",
                    "code": code,
                })
                
                # Collect output
                stdout = ""
                stderr = ""
                result = None
                
                while True:
                    msg = await ws.receive_json()
                    
                    if msg.get("type") == "stdout":
                        stdout += msg.get("data", "")
                    elif msg.get("type") == "stderr":
                        stderr += msg.get("data", "")
                    elif msg.get("type") == "result":
                        result = msg.get("value")
                    elif msg.get("type") == "error":
                        raise ColabApiException(
                            f"Execution error: {msg.get('message')}"
                        )
                    elif msg.get("type") == "done":
                        break
                
                return {
                    "stdout": stdout,
                    "stderr": stderr,
                    "result": result,
                    "status": "success",
                }
        
        except asyncio.TimeoutError:
            raise ColabApiException(f"Execution timeout after {timeout}s")
        except aiohttp.ClientError as e:
            raise ColabApiException(f"Kernel communication error: {e}")
    
    async def get_quota(self, account: str) -> Dict[str, float]:
        """
        Check CCU quota and balance.
        
        Args:
            account: Google account email
        
        Returns:
            Dict with 'balance', 'limit', 'reset_time'
        """
        session = await self._get_session()
        headers = await self._get_headers(account)
        
        try:
            async with session.get(
                f"{self.COLAB_API_BASE}/account/ccu",
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status != 200:
                    raise ColabApiException(f"Quota check failed: {resp.status}")
                
                data = await resp.json()
                return {
                    "balance": data.get("ccu_balance", 0.0),
                    "limit": data.get("ccu_limit", 0.0),
                    "reset_time": data.get("reset_time"),
                }
        
        except aiohttp.ClientError as e:
            raise ColabApiException(f"Quota check error: {e}")
    
    async def unassign(self, kernel_id: str) -> None:
        """
        Release Colab machine.
        
        Args:
            kernel_id: Kernel ID to release
        """
        if kernel_id not in self._assignments:
            logger.warning(f"Kernel {kernel_id} not tracked locally")
            return
        
        assignment = self._assignments[kernel_id]
        account = assignment["account"]
        
        # Cancel keep-alive task
        if assignment["keep_alive_task"]:
            assignment["keep_alive_task"].cancel()
        
        session = await self._get_session()
        headers = await self._get_headers(account)
        
        try:
            async with session.delete(
                f"{self.COLAB_API_BASE}/kernels/assignments/{kernel_id}",
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status != 204:
                    logger.warning(f"Unassign returned {resp.status}")
                
                del self._assignments[kernel_id]
                logger.info(f"Released kernel {kernel_id}")
        
        except aiohttp.ClientError as e:
            logger.error(f"Unassign error: {e}")
    
    async def _keep_alive_loop(self, kernel_id: str, account: str) -> None:
        """
        Background task to keep assignment alive.
        Sends keep-alive ping every KEEP_ALIVE_INTERVAL seconds.
        """
        session = await self._get_session()
        headers = await self._get_headers(account)
        
        try:
            while True:
                await asyncio.sleep(self.KEEP_ALIVE_INTERVAL)
                
                try:
                    async with session.post(
                        f"{self.COLAB_API_BASE}/kernels/{kernel_id}/keep-alive",
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=5)
                    ) as resp:
                        if resp.status != 200:
                            logger.warning(
                                f"Keep-alive failed for {kernel_id}: {resp.status}"
                            )
                except aiohttp.ClientError as e:
                    logger.warning(f"Keep-alive error: {e}")
        
        except asyncio.CancelledError:
            logger.debug(f"Keep-alive loop cancelled for {kernel_id}")
    
    async def list_assignments(self, account: str) -> list:
        """
        List all active assignments for account.
        
        Args:
            account: Google account email
        
        Returns:
            List of assignment dicts
        """
        session = await self._get_session()
        headers = await self._get_headers(account)
        
        try:
            async with session.get(
                f"{self.COLAB_API_BASE}/kernels/assignments",
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status != 200:
                    raise ColabApiException(f"List failed: {resp.status}")
                
                data = await resp.json()
                return data.get("assignments", [])
        
        except aiohttp.ClientError as e:
            raise ColabApiException(f"List error: {e}")
    
    async def get_status(self) -> Dict[str, Any]:
        """Get overall status"""
        return {
            "active_assignments": len(self._assignments),
            "assignments": [
                {
                    "kernel_id": kid,
                    "machine_type": v["machine_type"],
                    "uptime": (
                        datetime.utcnow() - v["assigned_at"]
                    ).total_seconds()
                }
                for kid, v in self._assignments.items()
            ]
        }
    
    @staticmethod
    def _machine_to_gpu(machine_type: str) -> str:
        """Map machine type to GPU type for API"""
        mapping = {
            "TPM_V5_EDGE": "TPU_V5E",
            "L4": "NVIDIA_L4",
            "T4": "NVIDIA_T4",
            "P100": "NVIDIA_P100",
            "V100": "NVIDIA_V100",
            "H100": "NVIDIA_H100",
        }
        return mapping.get(machine_type, machine_type)
    
    async def close(self) -> None:
        """Close HTTP session"""
        if self.session:
            await self.session.close()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        await self.close()

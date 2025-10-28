"""Driver registry for Execution Orchestrator.

Each driver exposes a run(mission: str) -> int function returning a process exit code.
"""

from __future__ import annotations

def get(driver_name: str):
    if driver_name == "local":
        from . import local as mod
        return mod
    if driver_name == "colab":
        from . import colab as mod
        return mod
    if driver_name == "cloud":
        from . import cloud as mod
        return mod
    return None

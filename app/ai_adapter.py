"""AI integration contract for a later release.

V3 deliberately ships without a model client. The rest of the application must not
need this module to perform parsing, register construction or deterministic checks.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class AIStatus:
    available: bool = False
    provider: str | None = None
    model: str | None = None
    reason: str = "AI-component is in v3 nog niet aangesloten. Analyse draait zonder AI."

def status() -> AIStatus:
    return AIStatus()

def analyze(*_args, **_kwargs):
    raise RuntimeError(status().reason)

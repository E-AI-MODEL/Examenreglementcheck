"""Compatibility import for the canonical runtime gate in app.source_gate."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from app.source_gate import can_support_must
__all__=['can_support_must']

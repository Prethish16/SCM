"""Make the backend package importable for pytest."""
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent / "src" / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

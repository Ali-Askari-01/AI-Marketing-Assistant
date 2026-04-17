"""Vercel serverless entrypoint for Omni Mind FastAPI app."""

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"

# Ensure backend absolute imports like `from core.config import settings` work.
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from main import app  # noqa: E402,F401

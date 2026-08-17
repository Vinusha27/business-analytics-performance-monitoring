import os
import secrets
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{ROOT / 'ventureflow.db'}")
# A persistent production secret must be supplied through the environment.
# The generated value keeps the local zero-config demo usable without committing one.
JWT_SECRET = os.getenv("JWT_SECRET") or secrets.token_urlsafe(48)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")
ACCESS_TOKEN_EXPIRE_MINUTES = 480

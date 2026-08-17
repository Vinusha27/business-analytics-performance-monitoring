import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{ROOT / 'ventureflow.db'}")
JWT_SECRET = os.getenv("JWT_SECRET", "change-this-local-demo-secret")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")
ACCESS_TOKEN_EXPIRE_MINUTES = 480

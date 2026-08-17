from __future__ import annotations
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RAW = DATA / "raw"
DB_PATH = DATA / "nexaretail.db"
TARGETS = {
    "monthly_revenue": float(os.getenv("MONTHLY_REVENUE_TARGET", "180000")),
    "completion_rate": float(os.getenv("COMPLETION_RATE_TARGET", "0.94")),
    "gross_margin": float(os.getenv("GROSS_MARGIN_TARGET", "0.35")),
    "return_rate": float(os.getenv("RETURN_RATE_MAX", "0.06")),
    "cancellation_rate": float(os.getenv("CANCELLATION_RATE_MAX", "0.05")),
    "aov": float(os.getenv("AOV_TARGET", "85")),
}

"""Project settings. Secrets and environment-specific values come from .env."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Read .env from the project folder into environment variables (no-op if missing)
load_dotenv()

# Project root = the folder this file lives in; works on macOS and Windows
BASE_DIR = Path(__file__).resolve().parent

# Runtime files: state between runs and reports. Both folders are git-ignored.
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
PROCESSED_IDS_FILE = DATA_DIR / "processed_ids.json"
RUN_REPORT_FILE = OUTPUT_DIR / "run_report.json"

# Comma-separated list in .env, e.g. ALLOWED_DOMAINS=a.example,b.example
ALLOWED_DOMAINS: set[str] = {
    d.strip().lower()
    for d in os.getenv("ALLOWED_DOMAINS", "partner-a.example,partner-b.example").split(",")
    if d.strip()
}

# Only these attachment types are processed
ALLOWED_EXTENSIONS: tuple[str, ...] = (".xlsx",)

# Mailbox credentials: used from week 3. Never hardcode them here.
IMAP_HOST = os.getenv("IMAP_HOST", "")
IMAP_USER = os.getenv("IMAP_USER", "")
IMAP_PASSWORD = os.getenv("IMAP_PASSWORD", "")
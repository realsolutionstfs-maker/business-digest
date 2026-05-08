#!/usr/bin/env python3
"""Check system health — run from cron to detect failures."""
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

BASE = Path(__file__).parent.parent
LOG = BASE / "logs" / "system.log"
OUTPUT = BASE / "output"

errors = []

if not LOG.exists():
    errors.append("system.log not found")

log_text = LOG.read_text() if LOG.exists() else ""
last_lines = log_text.strip().split("\n")[-50:]

recent_failures = [l for l in last_lines if "FAILED" in l or "ERROR" in l]
if recent_failures:
    errors.append(f"Recent failures: {recent_failures[-3:]}")

newsletters = list((OUTPUT / "newsletters").glob("*.html"))
if not newsletters:
    errors.append("No newsletters generated")

latest = max(newsletters, key=lambda p: p.stat().st_mtime) if newsletters else None
if latest:
    age = datetime.now() - datetime.fromtimestamp(latest.stat().st_mtime)
    if age > timedelta(days=8):
        errors.append(f"Last newsletter: {age.days} days ago ({latest.name})")

reports = {
    "status": "fail" if errors else "ok",
    "errors": errors,
    "newsletter_count": len(newsletters),
    "latest": latest.name if latest else "none",
    "log_lines": len(log_text.split("\n")),
}

print(json.dumps(reports, indent=2))
sys.exit(1 if errors else 0)

#!/usr/bin/env python3
"""
Business Digest — Autonomous AI Media Company

Usage:
    python run.py --mode all       # setup → fetch → weekly (default)
    python run.py --mode weekly    # Generate newsletter + video + social
    python run.py --mode send      # Send latest newsletter via Buttondown
    python run.py --mode publish   # all + send (full pipeline + delivery)

Modes:
    setup   — Create directories
    fetch   — Scrape 18 RSS feeds, score, select top 3
    weekly  — Generate newsletter + video script + voice + social
    daily   — Same as weekly (alias)
    send    — Send latest newsletter via Buttondown
    publish — all + send (generate everything + deliver)
    all     — setup → fetch → weekly (default)
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from agents.orchestrator import Orchestrator
from agents.config import logger


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Business Digest — Autonomous Publisher")
    parser.add_argument("--mode", choices=["setup", "fetch", "weekly", "daily", "send", "publish", "all"], default="all")
    args = parser.parse_args()

    orchestrator = Orchestrator()

    from agents.sender import send_latest

    def publish():
        orchestrator.setup()
        orchestrator.fetch_and_score()
        orchestrator.generate_weekly()
        return send_latest()

    modes = {
        "setup": orchestrator.setup,
        "fetch": orchestrator.fetch_and_score,
        "weekly": orchestrator.generate_weekly,
        "daily": orchestrator.generate_weekly,
        "send": send_latest,
        "publish": publish,
        "all": lambda: (orchestrator.setup(), orchestrator.fetch_and_score(), orchestrator.generate_weekly()) and True,
    }

    logger.info(f"Starting mode: {args.mode}")
    success = modes[args.mode]()
    logger.info(f"Mode '{args.mode}' completed: {'SUCCESS' if success else 'FAILED'}")
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

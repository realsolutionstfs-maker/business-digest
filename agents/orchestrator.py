import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from .config import BASE_DIR, logger

class Orchestrator:
    def __init__(self):
        self.phase = "initialized"
        self.artifacts = {}

    def setup(self):
        logger.info("=" * 60)
        logger.info("SYSTEM SETUP — INITIALIZING AI MEDIA COMPANY")
        logger.info("=" * 60)

        dirs = [
            "output/newsletters", "output/scripts", "output/voiceovers",
            "output/social", "output/thumbnails", "output/analytics", "logs"
        ]
        for d in dirs:
            Path(BASE_DIR / d).mkdir(parents=True, exist_ok=True)
            logger.info(f"  Created: {d}/")

        from .config import LOCAL_MODE
        if LOCAL_MODE:
            logger.info("  Local mode — no external AI APIs required")
        else:
            logger.info("  API mode — external AI services configured")
        logger.info("  Directory structure ready")
        logger.info("  Next: python run.py --mode fetch")
        return True

    def fetch_and_score(self):
        logger.info("=" * 60)
        logger.info("CONTENT CURATION — FETCHING & SCORING")
        logger.info("=" * 60)

        with open(BASE_DIR / "data" / "sources.json") as f:
            sources = json.load(f)

        from .content_scorer import scrape_feeds, score_articles

        logger.info(f"Scraping {len(sources['feeds'])} feeds...")
        articles = scrape_feeds(sources["feeds"])
        logger.info(f"  Retrieved {len(articles)} articles")

        logger.info("Scoring articles (keyword-based)...")
        scored = score_articles(articles)
        logger.info(f"  Top 8 articles identified")

        output_path = BASE_DIR / "output" / "scored_articles.json"
        with open(output_path, "w") as f:
            json.dump(scored, f, indent=2)
        logger.info(f"  Saved to {output_path}")

        def _build_entry(a):
            title = a["title"]
            raw = title.split("—")[0].split(":")[0].strip()
            if len(raw) > 60:
                raw = raw[:60].rsplit(" ", 1)[0]
            return {"title": title, "url": a["url"],
                    "snippet": a.get("snippet", "")[:300],
                    "source": a["source"], "score": a["score"],
                    "grade": a["grade"],
                    "angle": a.get("angle", title), "company": raw}

        selected = []
        used_sources = set()
        selected_titles = set()
        for a in scored:
            if len(selected) >= 3:
                break
            if a["source"] in used_sources or a["title"] in selected_titles:
                continue
            used_sources.add(a["source"])
            selected_titles.add(a["title"])
            selected.append(_build_entry(a))
        for a in scored:
            if len(selected) >= 3:
                break
            if a["title"] in selected_titles:
                continue
            selected_titles.add(a["title"])
            selected.append(_build_entry(a))
        selected_path = BASE_DIR / "output" / "selected_articles.json"
        with open(selected_path, "w") as f:
            json.dump(selected, f, indent=2)
        logger.info(f"  Auto-selected top 3 → {selected_path}")
        return True

    def generate_weekly(self):
        logger.info("=" * 60)
        logger.info("WEEKLY GENERATION — NEWSLETTER + VIDEO + SOCIAL")
        logger.info("=" * 60)

        selected_path = BASE_DIR / "output" / "selected_articles.json"
        if not selected_path.exists():
            logger.error("selected_articles.json not found. Run --mode fetch first.")
            return False

        with open(selected_path) as f:
            articles = json.load(f)

        from .newsletter_writer import write_newsletter
        logger.info("Generating newsletter...")
        newsletter = write_newsletter(articles)
        (BASE_DIR / "output" / "newsletters" / f"weekly_{datetime.now().strftime('%Y%m%d')}.html").write_text(newsletter)
        logger.info("  Newsletter generated")

        from .script_writer import write_script
        logger.info("Generating video script...")
        a0 = articles[0]
        topic = {
            "company": a0.get("company", ""),
            "angle": a0.get("angle", ""),
            "title": a0.get("title", "Business Story"),
            "snippet": a0.get("snippet", ""),
            "source": a0.get("source", ""),
        }
        script = write_script(topic)
        script_path = BASE_DIR / "output" / "scripts" / f"video_{datetime.now().strftime('%Y%m%d')}.txt"
        script_path.write_text(script)
        logger.info("  Video script generated")

        from .voice_optimizer import optimize
        logger.info("Optimizing for voiceover...")
        voice = optimize(script)
        voice_path = BASE_DIR / "output" / "voiceovers" / f"voice_{datetime.now().strftime('%Y%m%d')}.txt"
        voice_path.write_text(voice)
        logger.info("  Voice script optimized")

        from .social_distributor import distribute
        logger.info("Generating social content...")
        social = distribute(newsletter, articles)
        for platform, content in social.items():
            (BASE_DIR / "output" / "social" / f"{platform}_{datetime.now().strftime('%Y%m%d')}.txt").write_text(content)
        logger.info("  Social content generated")

        logger.info("=" * 60)
        logger.info("WEEKLY GENERATION COMPLETE")
        logger.info("Newsletter: output/newsletters/")
        logger.info("Video: output/scripts/ + output/voiceovers/")
        logger.info("Social: output/social/")
        logger.info("=" * 60)
        return True

    def generate_daily_social(self):
        logger.info("=" * 60)
        logger.info("DAILY SOCIAL GENERATION")
        logger.info("=" * 60)

        from .social_distributor import generate_daily_social
        social = generate_daily_social()
        for platform, content in social.items():
            path = BASE_DIR / "output" / "social" / f"{platform}_{datetime.now().strftime('%Y%m%d')}_daily.txt"
            path.write_text(content)
        logger.info(f"  Daily social generated ({', '.join(social.keys())})")

        from .social_publisher import publish_daily
        result = publish_daily()
        if result:
            logger.info("  LinkedIn: posted!")
        else:
            logger.info("  LinkedIn: skipped (no token or no content)")

        logger.info("=" * 60)
        logger.info("DAILY SOCIAL COMPLETE")
        logger.info("=" * 60)
        return True


def main():
    parser = argparse.ArgumentParser(description="AI Media Company — Autonomous Publisher")
    parser.add_argument("--mode", choices=["setup", "fetch", "weekly", "daily"], default="setup")
    args = parser.parse_args()

    orchestrator = Orchestrator()
    modes = {
        "setup": orchestrator.setup,
        "fetch": orchestrator.fetch_and_score,
        "weekly": orchestrator.generate_weekly,
        "daily": orchestrator.generate_weekly,
    }

    success = modes[args.mode]()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

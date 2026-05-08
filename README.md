# Business Digest — Autonomous AI Media Company

AI media company that produces a weekly newsletter, video scripts, and social content.
**Zero external AI APIs.** Runs fully offline with embedded templates and seed content.

## Quick Start

```bash
pip install -r requirements.txt

# Full pipeline: generate + send newsletter
python run.py --mode publish

# Or step by step:
python run.py --mode all     # setup → fetch → weekly
python run.py --mode send    # send latest newsletter via Buttondown
python run.py --mode weekly  # generate content only
```

## Modes

| Mode | Description |
|------|-------------|
| `all` | setup → fetch → weekly (default) |
| `weekly` | Generate newsletter + video script + voice + social |
| `send` | Send latest newsletter via Buttondown |
| `publish` | all + send (full pipeline + delivery) |
| `fetch` | Scrape 18 RSS feeds, score, select top 3 |
| `setup` | Create directories |

## Output

```
output/
├── newsletters/    # HTML newsletters (System/Tool/Move structure)
├── scripts/        # 10-min video scripts (seed or adaptive template)
├── voiceovers/     # Voice-optimized scripts with [PAUSE] markers
└── social/         # LinkedIn, Twitter, Blog posts
```

## How it Works

1. **Scrape** — 18 RSS feeds (TechCrunch, Wired, Stratechery, etc.)
2. **Score** — Keyword-based heuristic scoring (4 tiers, 0-50 scale)
3. **Select** — Top 3 from unique sources with recency + category boost
4. **Generate** — Newsletter (System/Tool/Move) + adaptive video script + voice + social

**17 seed scripts** for major companies (Apple, Microsoft, Amazon, Google, Tesla, Netflix, Uber, etc.)
When a feed article mentions one in the title, the seed script is used. Otherwise, adaptive templates match the angle type (Narrative/Inside/Analysis/Insight/Industry).

## Configuration

Only needed for newsletter delivery:

```bash
cp .env.example .env
# Add Buttondown API key (optional — content generation works without it)
```

## Live Demo

- Newsletter archive: https://buttondown.com/Business_Digest/archive
- Subscribe: https://buttondown.com/Business_Digest
- Landing: `python3 server.py` → http://localhost:8080

## Automation

Cron job runs every Saturday at 8:00 AM:

```bash
0 8 * * 6 cd /path/to/project && python3 run.py --mode publish
```

## Monetization

- **Sponsorships** — sponsor@businessdigest.com
- **Premium tier** — via Buttondown Pro (paid subscriptions)
- **Cost** — $0/mo (no external API dependencies)

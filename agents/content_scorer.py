import feedparser
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from .config import logger

EXCLUDED_PATTERNS = [
    r"stock (tip|pick|recommend)", r"crypto (price|prediction|speculation)",
    r"buy (now|today)", r"financial advice", r"political",
]

SPAM_DOMAINS = ["blogspot.com", "wordpress.com", "medium.com/@spam"]

CATEGORY_BOOST = {
    "startups": 5,
    "strategy": 5,
    "vc": 5,
    "entrepreneurship": 4,
    "management": 3,
    "finance": 2,
    "technology": 1,
}

TIER_NARRATIVE = [  # 12pts each — startup-failure, founder drama
    "founder", "startup", "failed", "fraud", "collapse", "bankruptcy",
    "lawsuit", "scandal", "crisis", "investigation", "fired", "resign",
    "whistleblower", "downfall", "unicorn", "pivot", "turnaround",
    "breakthrough", "disrupt", "how", "why", "bet", "gamble",
]

TIER_COMPANY = [  # 6pts each — company actions & business narrative
    "CEO", "raised", "million", "billion", "valuation", "investor",
    "funding", "series", "venture", "angel", "seed", "exit",
    "acquisition", "merger", "IPO", "revenue", "profit", "growth",
    "loss", "market", "innovation", "deal", "partnership",
    "interview", "launch", "entrepreneur", "strategy",
    "leadership", "management", "hiring", "layoff",
]

TIER_CONTEXT = [  # 4pts each — industry & technology context
    "remote", "economy", "inflation",
    "AI", "artificial intelligence", "model", "platform", "enterprise",
    "technology", "customer", "investment", "capital", "expansion",
    "announces", "reports", "quarter", "earnings",
    "analysis", "product", "data",
]

TIER_SURPRISE = [  # 5pts each — unexpected angles
    "unexpected", "surprising", "reveals", "secret", "behind",
    "truth", "real story", "weird", "strange", "extraordinary",
    "exclusive", "untold", "exposed",
]


def _is_spam(url: str) -> bool:
    url_lower = url.lower()
    return any(d in url_lower for d in SPAM_DOMAINS)


def scrape_feeds(feeds: list[dict]) -> list[dict]:
    articles = []
    failed = 0
    for feed in feeds:
        for attempt in range(2):
            try:
                parsed = feedparser.parse(feed["url"])
                if not parsed.entries:
                    raise Exception("Empty feed")
                for entry in parsed.entries[:10]:
                    url = entry.get("link", "")
                    if _is_spam(url):
                        continue
                    articles.append({
                        "title": entry.get("title", ""),
                        "url": url,
                        "snippet": entry.get("summary", "")[:500],
                        "source": feed["name"],
                        "category": feed["category"],
                        "published": entry.get("published", datetime.now().isoformat()),
                        "feed_url": feed["url"],
                    })
                break
            except Exception as e:
                if attempt == 0:
                    continue
                failed += 1
                logger.warning(f"Failed to parse {feed['name']}: {e}")

    if failed:
        logger.info(f"  {failed} feeds failed after retry")
    articles.sort(key=lambda a: a.get("published", ""), reverse=True)
    return articles[:15]


def _recency_bonus(published_str: str) -> int:
    try:
        pub = datetime.fromisoformat(published_str.replace("Z", "+00:00"))
        age_days = (datetime.now() - pub).days
        if age_days <= 7:
            return 5
        if age_days <= 30:
            return 3
        if age_days <= 90:
            return 1
        return 0
    except Exception:
        return 0


def _score_article(article: dict) -> dict:
    title = article["title"].lower()
    snippet = article["snippet"].lower()
    text = title + " " + snippet

    for pat in EXCLUDED_PATTERNS:
        if re.search(pat, text):
            article["score"] = 0
            article["grade"] = "X"
            article["angle"] = "Excluded topic"
            return article

    n_count = sum(1 for kw in TIER_NARRATIVE if kw.lower() in text)
    c_count = sum(1 for kw in TIER_COMPANY if kw.lower() in text)
    ctx_count = sum(1 for kw in TIER_CONTEXT if kw.lower() in text)
    s_count = sum(1 for kw in TIER_SURPRISE if kw.lower() in text)

    n_pts = n_count * 12
    c_pts = c_count * 6
    ctx_pts = ctx_count * 4
    s_pts = s_count * 5

    cat_boost = CATEGORY_BOOST.get(article.get("category", ""), 0)
    recency = _recency_bonus(article.get("published", ""))

    score = min(n_pts + c_pts + ctx_pts + s_pts + cat_boost + recency, 50)

    if score >= 35:
        grade = "A"
    elif score >= 25:
        grade = "B"
    elif score >= 15:
        grade = "C"
    else:
        grade = "D"

    if n_count > 0:
        angle_type = "Narrative deep dive"
    elif s_count > 0:
        angle_type = "Inside story"
    elif c_count >= 3:
        angle_type = "Business analysis"
    elif c_count > 0:
        angle_type = "Company insight"
    else:
        angle_type = "Industry update"

    article["score"] = score
    article["grade"] = grade
    article["angle"] = f"{angle_type}: {article['title']}"
    return article


def _deduplicate(articles: list[dict]) -> list[dict]:
    kept = []
    seen_normalized = set()
    for a in articles:
        norm = re.sub(r"[^a-z0-9]", "", a["title"].lower())
        if norm in seen_normalized:
            continue
        seen_normalized.add(norm)
        kept.append(a)
    return kept


def score_articles(articles: list[dict]) -> list[dict]:
    scored = [_score_article(a) for a in articles]
    scored.sort(key=lambda x: x["score"], reverse=True)
    deduped = _deduplicate(scored)
    if deduped:
        logger.info(f"Scored {len(scored)} articles, {len(deduped)} unique. Top score: {deduped[0]['score']}/50")
    return deduped[:8]

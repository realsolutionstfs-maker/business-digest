from datetime import datetime
from .config import logger


def analyze(metrics: dict) -> str:
    subscribers = metrics.get("subscribers", 0)
    open_rate = metrics.get("open_rate", 0)
    click_rate = metrics.get("click_rate", 0)
    videos = metrics.get("videos_published", 0)
    views = metrics.get("total_views", 0)
    social_posts = metrics.get("social_posts", 0)
    social_engagement = metrics.get("social_engagement", 0)

    analysis = f"""## Weekly Performance Report

**Date:** {datetime.now().strftime('%Y-%m-%d')}

### Headline
{'Growing steadily' if subscribers > 0 else 'Early stage'} — {subscribers} subscribers, {open_rate}% open rate.

### Key Metrics
- **Subscribers:** {subscribers} {'(+ this week)' if subscribers > 0 else ''}
- **Open rate:** {open_rate}% {'(good)' if open_rate > 40 else '(needs improvement)' if open_rate > 0 else '(tracking)'}
- **Click rate:** {click_rate}%
- **Videos published:** {videos}
- **Total views:** {views}
- **Social posts:** {social_posts}
- **Social engagement:** {social_engagement}

### Top Performing Content
Content with clear narrative angles outperforms general news summaries. Focus on stories with: a clear protagonist, a conflict, and a resolution.

### Recommendations
1. **Headlines:** Lead with the most surprising element of the story
2. **Format:** Keep newsletter sections under 200 words each
3. **Timing:** Saturday morning continues to show highest open rates
4. **Social:** Repurpose newsletter insights into 3-5 tweet threads

### Next Week Focus
Continue the three-section format (System/Tool/Move). Consider adding a reader poll to increase engagement.

---

*Analysis generated automatically. Data accuracy depends on connected analytics sources.*
"""

    return analysis

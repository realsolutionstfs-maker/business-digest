from datetime import datetime
from .config import logger

_TEMPLATES = {
    "narrative": {
        "linkedin": """The most dangerous business stories follow the same arc: rise, struggle, and collapse.

We study them not for entertainment — we study them to spot the pattern before it happens to us.

{title}

Here's what I keep coming back to:

1. Every fraud starts with a small corner cut that no one noticed.
2. Every collapse had insiders who knew but didn't speak.
3. Every recovery started with someone admitting they were wrong.

The question for this week: what corner are you cutting right now?

#BusinessNarrative #StartupLessons #Entrepreneurship""",

        "twitter": """1/ Business failures follow patterns.

The startup that grows too fast.
The founder who stops listening.
The board that looks the other way.

Here's a thread on the warning signs nobody wants to see. 🧵

2/ The first red flag: complexity.
If you can't explain the business model in 2 sentences, neither can the CFO. Enron, FTX, Theranos — all had "proprietary" structures that nobody understood.

3/ The second: culture of fear.
Employees who are afraid to speak up don't speak up. By the time the truth comes out, it's too late.

4/ The third: growth at any cost.
Revenue hides everything. When you're growing, nobody asks if the model works. When growth stops, the truth is already baked in.

5/ Watch for these signs in your own company. The best time to fix a problem is when you can still afford to.

/share""",

        "blog": """## Narrative Analysis: {title}

Business failures follow patterns. The companies that collapse don't do so randomly — they follow a predictable arc that has played out dozens of times before.

**The pattern:**
1. A founder or CEO becomes the story, not the product
2. Complexity replaces clarity in financial reporting
3. Dissent is punished or ignored
4. Growth becomes the only metric that matters

**The antidote:** Build a culture where bad news travels fast. The most dangerous person in a company is the one who stops hearing "no."

---

*Subscribe to Business Digest for three moves every Saturday. Zero noise.*""",
    },
    "inside": {
        "linkedin": """The best business stories aren't in the earnings reports. They're in the details nobody reports.

{title}

Here is what I learned reading between the lines:

The public story is always polished. The real story — the one behind closed doors — is messier. Egos. Last-minute decisions. Bets that could have gone either way.

The companies that survive aren't the ones that avoid these moments. They are the ones that navigate them.

The question: what's the real story behind your last big decision?

#BusinessStrategy #InsideStory #Leadership""",

        "twitter": """1/ The most important business stories don't make headlines.

They happen in meetings. Emails. Late-night decisions.

Here's what to look for. 🧵

2/ Every deal has a story behind the press release.
The partnership that almost fell through. The acquisition that started as a joke. The founder who almost quit.

3/ Read between the lines:
- "We mutually agreed" → someone was fired
- "Pursuing other opportunities" → the project was killed
- "Taking time with family" → burnout

4/ The real lessons are in these details. Not the quarterly numbers.

5/ This week, ask your team one question: what almost went wrong that nobody talks about?

/share""",

        "blog": """## Inside Story: {title}

The most revealing business stories don't appear in earnings calls or press releases. They surface in the details that executives mention in passing — the deal that almost fell through, the product that nearly launched too late, the hire that changed everything.

**What to look for:**
- The decision that seemed risky at the time
- The person who disagreed and was right
- The moment when the plan changed

**The takeaway:** Read every business announcement looking for what they're not saying. That's where the real story lives.

---

*Subscribe to Business Digest for three moves every Saturday. Zero noise.*""",
    },
    "analysis": {
        "linkedin": """Most business analysis tells you what happened. The better question is why — and what to do about it.

{title}

Here's the framework I use:

1. What changed? (The trigger)
2. Why did it change? (The cause)
3. Who benefits? (The incentive)
4. What happens next? (The second-order effect)

The best strategists don't predict the future. They ask better questions.

#BusinessStrategy #Analysis #DecisionMaking""",

        "twitter": """1/ Most analysis focuses on "what happened." That's the easy part.

2/ The hard part: why did it happen, and what do you do differently?

3/ Four questions every strategist should ask:
• What changed?
• Why did it change?
• Who benefits?
• What happens next?

4/ The best operators don't predict. They prepare.

/share""",

        "blog": """## Strategic Analysis: {title}

The difference between good and great analysis is the question you ask. Most people ask "what happened?" The best ask "what should I do differently?"

**The framework:**
1. **Trigger** — What changed in the market?
2. **Cause** — Why did it change? (Deeper than the press release)
3. **Incentives** — Who wins, who loses?
4. **Second-order** — What happens when the dust settles?

**The takeaway:** Analysis without action is entertainment. Always end with a decision.

---

*Subscribe to Business Digest for three moves every Saturday. Zero noise.*""",
    },
    "industry": {
        "linkedin": """Industries don't change overnight. They change one decision at a time — until suddenly the old rules don't apply anymore.

{title}

Here's what I'm watching:

The signals were there for anyone paying attention. A competitor changed pricing. A new regulation was proposed. A technology crossed a cost threshold. Individually, nothing. Together, everything.

The companies that win aren't the ones with the most resources. They're the ones that act before they have to.

#IndustryTrends #BusinessStrategy #FutureOfWork""",

        "twitter": """1/ Every industry shift follows the same pattern.

First, nobody notices.
Then, everybody panics.

2/ The signals are always there:
• Pricing changes
• Regulatory shifts
• Cost thresholds crossed

3/ Individually, nothing.
Together, everything.

4/ The winners act before they have to. The losers wait until it's obvious.

/share""",

        "blog": """## Industry Shift: {title}

Industries change one decision at a time. The trick is spotting which decisions matter.

**What to watch:**
- Pricing moves by competitors
- Regulatory changes
- Technology cost curves
- Talent flows

**The pattern:** When multiple signals converge, the shift accelerates. The best time to prepare is before it's obvious.

---

*Subscribe to Business Digest for three moves every Saturday. Zero noise.*""",
    },
}


def _pick_templates(angle: str) -> dict:
    angle_lower = angle.lower()
    if "narrative" in angle_lower:
        return _TEMPLATES["narrative"]
    if "inside" in angle_lower or "surprise" in angle_lower:
        return _TEMPLATES["inside"]
    if "analysis" in angle_lower or "business" in angle_lower:
        return _TEMPLATES["analysis"]
    if "industry" in angle_lower or "update" in angle_lower:
        return _TEMPLATES["industry"]
    return _TEMPLATES["narrative"]


def distribute(newsletter_content: str, articles: list = None) -> dict:
    lines = newsletter_content.split("\n")
    title = ""
    angle = ""
    for line in lines:
        if line.startswith("**") and line.endswith("**"):
            title = line.strip("*")
            break
    if not title:
        for line in lines:
            if line.strip() and len(line) > 20:
                title = line.strip()[:80]
                break

    if articles:
        angle = articles[0].get("angle", "") if len(articles) > 0 else ""

    templates = _pick_templates(angle)

    linkedin = templates["linkedin"].format(title=title)
    twitter = templates["twitter"].format(title=title)
    blog = templates["blog"].format(title=title)

    return {"linkedin": linkedin, "twitter": twitter, "blog": blog}


def generate_daily_social() -> dict:
    from .newsletter_writer import TOOLS
    week = datetime.now().isocalendar()[1]
    tool = TOOLS[week % len(TOOLS)]
    day = datetime.now().strftime("%A")

    quotes = {
        "Monday": '"The best time to plant a tree was 20 years ago. The second best time is now." — Chinese proverb',
        "Tuesday": '"In the middle of difficulty lies opportunity." — Albert Einstein',
        "Wednesday": '"It does not matter how slowly you go as long as you do not stop." — Confucius',
        "Thursday": '"The impediment to action advances action. What stands in the way becomes the way." — Marcus Aurelius',
        "Friday": '"Success is not final, failure is not fatal: it is the courage to continue that counts." — Winston Churchill',
    }

    q = quotes.get(day, "")

    linkedin = f"""This week's framework: **{tool['name']}**

{tool['body'][:400]}

**Apply it today:**
{tool['apply']}

{q}

#BusinessFrameworks #WeeklyTool #Entrepreneurship"""

    twitter = f"""This week's tool: {tool['name']}

{tool['body'][:280]}

Try it today:
{tool['apply'][:200]}

/share"""

    blog = f"""## Daily Framework: {tool['name']}

{tool['body']}

**Today's application:**
{tool['apply']}

{q}

---

*Subscribe to Business Digest for three moves every Saturday. Zero noise.*"""

    return {"linkedin": linkedin, "twitter": twitter, "blog": blog}

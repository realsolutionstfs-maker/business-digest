from datetime import datetime
from .config import logger, BRAND, BASE_DIR

TOOLS = [
    {
        "name": "The 5 Whys Framework",
        "body": """When something goes wrong, ask "why" five times. Each answer leads to a deeper root cause.

**Example:**
1. Why did the product launch fail? → The marketing didn't reach the right audience.
2. Why didn't it reach them? → We targeted the wrong channels.
3. Why did we target those channels? → We didn't research the audience.
4. Why didn't we research? → We assumed we knew them.
5. Why did we assume? → We skipped the customer discovery step.

**Root cause:** We prioritized speed over understanding.""",
        "apply": """This week, pick one problem and ask "why" five times before trying to fix it.""",
    },
    {
        "name": "First Principles Thinking",
        "body": """Break a problem down to its fundamental truths, then rebuild from there. Most reasoning is analogical — we copy what others do. First principles strips away assumptions.

**Example:**
Elon Musk wanted cheaper rockets. Conventional wisdom: rockets cost $65M each. First principles: raw materials cost 2% of that. He built SpaceX and cut launch costs by 90%.""",
        "apply": "This week, take one constraint you accept as fixed and ask yourself: is this a law of physics or just an assumption?",
    },
    {
        "name": "The OODA Loop",
        "body": """Observe, Orient, Decide, Act — then repeat. Speed through this cycle beats raw power every time.

**The insight:**
Most organizations get stuck in Observe. They collect data forever. The winners move to Act quickly, then loop back with real feedback.

**Example:**
A startup notices competitors dropping prices (Observe). They realize their differentiator is service, not price (Orient). They double down on support (Decide). They roll out a premium tier (Act). Then they Observe the results.""",
        "apply": """This week, identify one decision you've been analyzing too long. Shorten your OODA loop: set a deadline, decide, act, and iterate.""",
    },
    {
        "name": "Circle of Competence",
        "body": """Warren Buffett's framework: define what you truly understand, then operate only inside that circle. The size of the circle matters less than knowing its boundaries.

**Why it works:**
Every financial crisis involves someone who thought they understood something they didn't. The 2008 crash was full of people trading mortgage-backed securities who couldn't explain how they worked.""",
        "apply": """This week, write down your circle of competence on paper. Then list three decisions you made outside it. What would you do differently?""",
    },
    {
        "name": "Second-Order Thinking",
        "body": """First-order thinking: "I'll cut prices to gain customers." Second-order thinking: "Competitors will match my cuts, starting a price war. Margins shrink for everyone. I need a different advantage."

**The test:**
Before any decision, ask: "And then what?" Repeat five times. The fifth answer is where the real risk lives.""",
        "apply": """This week, run second-order thinking on one strategic decision. Write down first-order effects, then second, then third. Share it with a colleague and ask what order you missed.""",
    },
    {
        "name": "Inversion",
        "body": """Instead of asking "how do I succeed?", ask "what would guarantee failure?" Then avoid those things.

**Example:**
A startup founder asks: "What would definitely kill my company?" Answers: run out of cash, build something nobody wants, hire the wrong people. Now the strategy writes itself: keep 18 months runway, ship weekly customer interviews, hire slow and fire fast.""",
        "apply": """This week, invert your biggest problem. Write down everything that would make it worse. Then stop doing those things. Often preventing failure is more valuable than chasing success.""",
    },
    {
        "name": "The Pareto Principle (80/20)",
        "body": """80% of results come from 20% of efforts. Identify the vital few and focus there.

**Example:**
A startup analyzed their customer base: 20% of customers generated 80% of revenue. They fired the bottom 50% of customers (the high-support, low-revenue ones) and profitability doubled within a quarter.

**The trap:** Most teams spread effort evenly across priorities. The 80/20 rule says: find the 20% that matters and triple down.""",
        "apply": """This week, audit how you spent your time. Which 20% of activities produced 80% of your results? Double that next week and cut everything else by half.""",
    },
]


def _pick_tool() -> dict:
    week = datetime.now().isocalendar()[1]
    return TOOLS[week % len(TOOLS)]


def _strip_angle_prefix(angle: str) -> str:
    for prefix in ["Narrative deep dive:", "Inside story:", "Business analysis:",
                    "Company insight:", "Industry update:"]:
        if angle.startswith(prefix):
            return angle[len(prefix):].strip()
    return angle


def _generate_section1(article: dict) -> str:
    title = article.get("title", "Business Story")
    angle = _strip_angle_prefix(article.get("angle", ""))
    snippet = article.get("snippet", "")[:300]
    source = article.get("source", "unknown")

    display_angle = angle if angle not in ("", title) else ""

    return f"""## THE SYSTEM

**{title}**{f"\n\n{display_angle}" if display_angle else ""}

{snippet}

**Why it matters:** Every business move contains a lesson. This story shows what happens when strategy meets reality.

*Source: {source}*

**The takeaway:** One question to ask yourself this week — what assumption are you making that could be wrong?
"""


def _generate_section2() -> str:
    tool = _pick_tool()
    return f"""## THE TOOL

**{tool['name']}**

{tool['body']}

**Apply it:** {tool['apply']}
"""


def _generate_section3(article: dict) -> str:
    title = article.get("title", "Business")
    return f"""## THE MOVE

**What happened:**
{title}

**Why it worked/didn't work:**
Timing, execution, and focus separated success from failure. The companies that won made specific choices that seem obvious in hindsight but were bold at the time.

**What you can learn:**
Look for the decision that felt risky at the moment. That's usually the one that made the difference.
"""


def write_newsletter(articles: list[dict]) -> str:
    if not articles:
        articles = [{"title": "Weekly Brief", "angle": "Key business stories", "snippet": "A curated selection of the most important business narratives this week.", "source": "Business Digest"}]

    a1 = articles[0] if len(articles) > 0 else articles[0]
    a2 = articles[1] if len(articles) > 1 else a1
    a3 = articles[2] if len(articles) > 2 else a2

    sections = [
        _generate_section1(a1),
        _generate_section2(),
        _generate_section3(a3),
    ]

    newsletter = f"""## {BRAND['name']}

{BRAND['tagline']}

---

{chr(10).join(sections)}

---

**Next week:** More business narratives, frameworks, and actionable insights.

*If you found this valuable, forward it to a founder who needs signal, not noise.*
"""

    logger.info("  Newsletter generated (local mode)")
    return newsletter

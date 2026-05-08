import re
from .config import logger

SEED_VOICES = {
    "Theranos": """[Estimated: 4 minutes, 30 seconds]

Elizabeth Holmes walked onto a stage in 2015 and said five words that unraveled a nine billion dollar empire.

[PAUSE — 1s]

"The results are accurate."

She dropped out of Stanford at 19. Her idea: a machine that could run hundreds of blood tests from a single finger prick. She called it Theranos.

By 2013, investors had poured seven hundred million dollars into the company. The valuation hit nine billion.

But there was a problem. The machine did not work.

[PAUSE — 1s]

Former employees testified that Theranos ran patient samples on modified Siemens machines. Not the proprietary Edison device.

The SEC charged Theranos with fraud in 2018. In 2022, Holmes was sentenced to 11 years in federal prison.

[PAUSE — 1s]

The lesson: process beats vision. Check your assumptions against reality every week. Not every quarter.
""",

    "WeWork": """[Estimated: 4 minutes]

Adam Neumann walked onto a stage in 2017 and told 5,000 employees that WeWork's purpose was to elevate the world's consciousness.

[PAUSE — 1s]

One year later, the company was worth 47 billion dollars. Seven weeks after that, it was worth zero.

WeWork started in 2010. Lease office space, subdivide it, rent it to freelancers. By 2017, 280 locations.

The model required 80 percent occupancy to be profitable. Most locations ran at 60 to 70 percent.

[PAUSE — 1s]

The S-1 filing revealed everything. The IPO was pulled. SoftBank wrote down 10 billion dollars.

The lesson: revenue is not a business model. Before you scale, prove one unit works.
""",

    "Fyre Festival": """[Estimated: 4 minutes]

Guests arrived at Fyre Festival and found disaster-relief tents, cheese sandwiches, and no music. They had paid up to 250,000 dollars per ticket.

Billy McFarland was 25. His idea: a luxury music festival on a private island.

[PAUSE — 1s]

The team had six weeks to organize what normally takes 18 months. They spent 7 million dollars on influencer marketing. Zero dollars on stage infrastructure.

Ticket revenue: 26 million. Actual cost: 50 million.

McFarland was charged with wire fraud. Sentenced to six years.

The lesson: marketing cannot replace operations. Sell what you can deliver.
""",

    "Airbnb": """[Estimated: 4 minutes, 30 seconds]

Brian Chesky and Joe Gebbia had 200 dollars in the bank in 2008. Their solution: sell cereal boxes for 40 dollars each.

[PAUSE — 1s]

A design conference was coming to San Francisco. Hotels sold out. They bought air mattresses, called it Air Bed and Breakfast.

Year one: zero revenue. Investors rejected them 7 times.

In 2009, a host's apartment was trashed. They created the one million dollar host guarantee. The trust that made the platform possible.

[PAUSE — 1s]

By 2020, 100 billion valuation. Then COVID hit. Bookings dropped 90 percent. They survived.

The lesson: survive long enough to get lucky. When you have no options, sell cereal.
""",

    "Stripe": """[Estimated: 3 minutes, 30 seconds]

Two Irish brothers built a 95 billion dollar payment company. Neither of them knew anything about payments.

Patrick Collison won Young Scientist of Ireland at 16. John was 14. They built their first company at 17 and 19, sold it for 5 million.

[PAUSE — 1s]

They started Stripe in 2011 because every payment system was terrible. The breakthrough: seven lines of code.

By 2024: one trillion dollars in annual payments. Valued at 95 billion.

The lesson: make the hard thing simple. What can you reduce to one line?
""",

    "Netflix": """[Estimated: 4 minutes]

In 2000, Reed Hastings flew to Dallas to beg Blockbuster to buy Netflix for 50 million dollars. Blockbuster said no. Today Netflix is worth 250 billion.

[PAUSE — 1s]

Netflix almost died three times. In 2000, they were losing money on every subscriber and the dot-com crash hit. In 2007, the pivot to streaming — the technology didn't exist. In 2011, the Qwikster disaster — 800,000 subscribers quit.

[PAUSE — 1s]

Hastings apologized. Canceled Qwikster. Went all-in on originals.

The lesson: cannibalize yourself before someone else does. Your biggest competitor is your current business model.
""",

    "Tesla": """[Estimated: 4 minutes, 30 seconds]

Elon Musk slept on the factory floor in 2017. The Model 3 production line was broken. 120-hour weeks. No breaks.

[PAUSE — 1s]

Tesla almost died five times. In 2008, Musk put his last 20 million dollars into the company. In 2017, production hell. In 2018, the SEC investigation.

Each time, they survived.

[PAUSE — 1s]

By 2023, Tesla was the most valuable automaker in the world. 800 billion dollars.

The lesson: your survival threshold is higher than you think. When you have two weeks of runway, you have two months of creativity.
""",

    "Uber": """[Estimated: 4 minutes, 30 seconds]

Travis Kalanick was 0 for 2 on startups. His third try: a black car app that would make him a billionaire and get him fired.

[PAUSE — 1s]

Uber launched in 2010. By 2014, 100 cities. Growth at all costs.

In 2017, a former engineer published a blog post about sexism at Uber. Twenty employees were fired. Kalanick was caught on video yelling at a driver.

[PAUSE — 1s]

The board forced Kalanick out. Dara Khosrowshahi took over. By 2024, Uber finally turned its first profit.

The lesson: growth without culture is a liability.
""",

    "Peloton": """[Estimated: 3 minutes, 30 seconds]

A 2,000 dollar exercise bike became a 50 billion dollar company. Then it lost 49 billion in 18 months.

[PAUSE — 1s]

COVID hit. Gyms closed. Peloton became essential. Revenue tripled.

Then vaccines arrived. Demand cratered. One billion dollars in unsold inventory. The stock dropped 90 percent.

[PAUSE — 1s]

The lesson: never confuse a temporary tailwind with permanent demand.
""",

    "FTX": """[Estimated: 4 minutes]

Sam Bankman-Fried was 30 years old. 26 billion dollars net worth. Then it all evaporated in 72 hours.

[PAUSE — 1s]

FTX launched in 2019. Third largest crypto exchange. SBF was a media darling — effective altruism, donating millions.

But Alameda Research had special privileges on the exchange. It could trade with zero collateral. When CoinDesk published a leaked balance sheet, confidence cracked.

[PAUSE — 1s]

Eight billion dollars in customer funds missing. SBF convicted on all seven fraud counts.

The lesson: if the structure is complex and the returns are magical, the fraud is probably structural.
""",

    "Enron": """[Estimated: 4 minutes]

Fortune named Enron America's most innovative company six years in a row. Then it collapsed in 24 days.

[PAUSE — 1s]

Enron's real business was hiding debt. CFO Andrew Fastow created shell companies so Enron's books stayed clean.

When the SEC started asking questions, the house of cards collapsed.

[PAUSE — 1s]

Twenty thousand employees lost their jobs and pensions. Arthur Andersen was convicted and dissolved.

The lesson: if you can't explain how you make money in one sentence, complexity is masking fraud.
""",

    "Facebook": """[Estimated: 4 minutes, 30 seconds]

Mark Zuckerberg built a one trillion dollar company from a dorm room. Then Cambridge Analytica revealed the dark side.

[PAUSE — 1s]

Eighty seven million Facebook profiles harvested without permission. Used to influence the 2016 election. Zuckerberg testified before Congress.

The deeper problem: the algorithm optimized for outrage because outrage drove engagement.

[PAUSE — 1s]

Facebook paid a five billion dollar FTC fine. Rebranded as Meta. Bet 46 billion on the metaverse.

The lesson: when your growth depends on externalities, regulation is a matter of when, not if.
""",

    "Apple": """[Estimated: 4 minutes, 30 seconds]

In 1997, Apple was 90 days from bankruptcy. Then Steve Jobs walked back through the door.

[PAUSE — 1s]

He killed 70 percent of Apple's product line. Cut a deal with Microsoft. Critics called it surrender.

Then came the iMac. The iPod. The iPhone. Each product cannibalized the one before it.

[PAUSE — 1s]

Jobs resigned in 2011. Tim Cook took over. Apple became the first three trillion dollar company.

The lesson: focus is not saying yes to the right things. It's saying no to everything else.
""",

    "Zoom": """[Estimated: 4 minutes]

Eric Yuan left Cisco in 2011 because he couldn't build video that actually worked. Nine years later, Zoom became essential infrastructure.

[PAUSE — 1s]

First year: zero revenue. Investors passed. Yuan kept building. One focus: make it work so well nobody notices it.

Then COVID. Ten million to 300 million daily participants in 3 months.

[PAUSE — 1s]

Zoombombing. Security flaws. Yuan froze features for 90 days. Fixed security.

The lesson: build something so simple it feels obvious. The best products become invisible.
""",

    "Amazon": """[Estimated: 5 minutes]

Jeff Bezos left a Wall Street job in 1994 to sell books on the internet. His boss tried to talk him out of it.

[PAUSE — 1s]

Amazon started in a garage. By 1999, Bezos was Time's Person of the Year. Then the dot-com crash hit. Amazon lost 95 percent of its value.

The secret weapon: AWS. Launched in 2006. Nobody noticed. By 2020, 45 billion dollars in annual revenue.

[PAUSE — 1s]

By 2024, Amazon was worth 2 trillion dollars. The lesson: build something that compounds, then be patient enough to wait.
""",

    "Microsoft": """[Estimated: 4 minutes, 30 seconds]

In 2014, Microsoft was written off. iPhone killed Windows. Google killed Bing. The tech world had moved on.

[PAUSE — 1s]

Satya Nadella took over and did the opposite of what anyone expected. He released Office on iPad. Killed Windows Phone. Invested 50 billion dollars in Azure before it made any money.

[PAUSE — 1s]

By 2024, Microsoft was worth 3 trillion dollars. The lesson: sometimes the best comeback is not a turnaround, it's a reinvention.
""",

    "Google": """[Estimated: 4 minutes]

Two Stanford PhD students built a search engine in a garage. No business model. No revenue. Just a belief that search could be better.

[PAUSE — 1s]

Larry Page and Sergey Brin built PageRank. It was dramatically better than anything else. By 2004, 200 million searches per day.

Their solution to making money: AdWords. Pay-per-click advertising tied to search intent. It became the most profitable business model in history.

[PAUSE — 1s]

By 2024, Google was worth 2 trillion dollars. Ninety percent of revenue still comes from advertising. The lesson: Google's real innovation was not search. It was finding a way to get paid for attention.
""",
}


def optimize(script: str) -> str:
    for company, voice in SEED_VOICES.items():
        if company.lower() in script.lower():
            logger.info(f"  Using seed voice for: {company}")
            return voice

    words = script.split()
    word_count = len(words)
    estimated_minutes = max(1, round(word_count / 150))

    lines = script.split("\n")
    optimized = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            optimized.append(line)
            continue
        if not stripped:
            optimized.append("")
            continue
        if len(stripped.split()) > 15:
            parts = []
            for sentence in stripped.replace("?", "?||").replace(".", ".||").split("||"):
                sentence = sentence.strip()
                if sentence:
                    parts.append(sentence)
            optimized.append("[PAUSE — 1s]")
            optimized.extend(parts)
        else:
            optimized.append(stripped)

    result = f"[Estimated: {estimated_minutes} minutes]\n\n" + "\n".join(optimized)
    return result

import json
from datetime import datetime
from .config import logger, BASE_DIR

SEED_SCRIPTS = {
    "Theranos": """[0:00]
**HOOK**
Elizabeth Holmes walked onto a stage in 2015 and said five words that unraveled a $9 billion empire: "The results are accurate."

[PAUSE — 1s]

[0:30-3:00]
**ACT I — THE RISE**
She dropped out of Stanford at 19. Her idea: a machine that could run hundreds of blood tests from a single finger prick. She called it Theranos.

By 2013, investors had poured $700 million into the company. Board members included Henry Kissinger, George Shultz, and James Mattis. The valuation hit $9 billion.

[3:00-7:00]
**ACT II — THE STRUGGLE**
But there was a problem. The machine didn't work.

Former employees testified that Theranos ran patient samples on modified Siemens machines — not the proprietary Edison device. When John Carreyrou of the Wall Street Journal started investigating, Holmes threatened him with legal action.

[7:00-9:30]
**ACT III — THE RESOLUTION**
The SEC charged Theranos with fraud in 2018. In 2022, Holmes was sentenced to 11 years in federal prison.

[9:30-10:00]
**TAKEAWAY**
Process beats vision. Check your assumptions against reality — every week, not every quarter.
""",

    "WeWork": """[0:00]
**HOOK**
Adam Neumann walked barefoot onto a stage in 2017 and told 5,000 employees WeWork's purpose was to "elevate the world's consciousness." One year later: $47 billion. Seven weeks after that: zero.

[0:30-3:00]
**ACT I — THE RISE**
WeWork started in 2010. Lease office space, subdivide it, rent it to freelancers. By 2017, 280 locations worldwide.

[3:00-7:00]
**ACT II — THE STRUGGLE**
The model required 80% occupancy to be profitable. Most locations ran at 60-70%. Neumann bought buildings with company money, leased them back at a profit. He trademarked the word "We."

The S-1 filing in August 2019 revealed everything. The IPO was pulled.

[7:00-9:30]
**ACT III — THE RESOLUTION**
SoftBank wrote down $10 billion. Neumann walked away with $1.7 billion. WeWork filed for bankruptcy in 2023.

[9:30-10:00]
**TAKEAWAY**
Revenue is not a business model. Before you scale, prove one unit works.
""",

    "Fyre Festival": """[0:00]
**HOOK**
Guests arrived at Fyre Festival and found disaster-relief tents, cheese sandwiches, and no music. They had paid up to $250,000 per ticket.

[0:30-3:00]
**ACT I — THE RISE**
Billy McFarland was 25. He had built Magnises, a "black card" for millennials. His next idea: a luxury music festival on a private island.

[3:00-7:00]
**ACT II — THE STRUGGLE**
The team had 6 weeks to organize what normally takes 18 months. They spent $7 million on influencer marketing — Kendall Jenner, Bella Hadid, models on yachts. They spent $0 on stage infrastructure.

Ticket revenue: $26 million. Actual cost: $50 million.

[7:00-9:30]
**ACT III — THE RESOLUTION**
McFarland was charged with wire fraud. Sentenced to 6 years in federal prison.

[9:30-10:00]
**TAKEAWAY**
Marketing cannot replace operations. Sell what you can deliver, not what you wish you could deliver.
""",

    "Airbnb": """[0:00]
**HOOK**
Brian Chesky and Joe Gebbia had $200 in the bank in 2008. Their solution to avoid eviction: sell cereal boxes for $40 each.

[0:30-3:00]
**ACT I — THE RISE**
A design conference was coming to San Francisco. Hotels sold out. They bought air mattresses, called it "Air Bed and Breakfast," charged $80 per night.

[3:00-7:00]
**ACT II — THE STRUGGLE**
Year one: zero revenue. Investors rejected them 7 times. Paul Graham passed. They created Obama O's cereal — $40 per box — sold 800 boxes to fund the company.

In 2009, a host's apartment was trashed. No insurance. They created the $1 million host guarantee — the trust that made the platform possible.

[7:00-9:30]
**ACT III — THE RESOLUTION**
By 2020: $100 billion valuation. 4 million hosts. Then COVID hit — bookings dropped 90% in 8 weeks. They survived. Went public at $47 billion.

[9:30-10:00]
**TAKEAWAY**
Survive long enough to get lucky. When you have no options, sell cereal.
""",

    "Stripe": """[0:00]
**HOOK**
Two Irish brothers built a $95 billion payment company. Neither of them knew anything about payments.

[0:30-3:00]
**ACT I — THE RISE**
Patrick Collison won Young Scientist of Ireland at 16. Brother John was 14. They built Auctomatic at 17 and 19, sold it for $5 million.

[3:00-7:00]
**ACT II — THE STRUGGLE**
They started Stripe in 2011 because every payment system was terrible. PayPal's API needed 6 months to integrate. The breakthrough: seven lines of code.

In 2012, their processor Wells Fargo threatened to cut them off. They found a new partner and kept growing.

[7:00-9:30]
**ACT III — THE RESOLUTION**
By 2024: $1 trillion in annual payments. Valued at $95 billion.

[9:30-10:00]
**TAKEAWAY**
Make the hard thing simple. What can you reduce to one line?
""",

    "Netflix": """[0:00]
**HOOK**
In 2000, Reed Hastings flew to Dallas to beg Blockbuster to buy Netflix for $50 million. Blockbuster said no. Today Netflix is worth $250 billion.

[0:30-3:00]
**ACT I — THE RISE**
Netflix launched in 1998 with 30 employees and 925 DVD titles.

[3:00-7:00]
**ACT II — THE STRUGGLE**
Near-death 1 (2000): Losing money on every subscriber. Dot-com crash. Stock down 90%.
Near-death 2 (2007): Pivot to streaming. Technology didn't exist.
Near-death 3 (2011): Qwikster disaster. 800,000 subscribers quit. Stock down 80%.

[7:00-9:30]
**ACT III — THE RESOLUTION**
Hastings apologized. Cancelled Qwikster. Went all-in on originals. House of Cards cost $100 million. By 2023: 260 million subscribers, $33 billion revenue.

[9:30-10:00]
**TAKEAWAY**
Cannibalize yourself before someone else does. Your biggest competitor is your current business model.
""",

    "Tesla": """[0:00]
**HOOK**
Elon Musk slept on the factory floor in 2017. The Model 3 production line was broken. 120-hour weeks. No breaks.

[0:30-3:00]
**ACT I — THE RISE**
Tesla was founded in 2003. Musk invested $6.5 million in 2004. The Roadster launched in 2008 — the first highway-legal electric car with lithium-ion batteries.

[3:00-7:00]
**ACT II — THE STRUGGLE**
Tesla almost died five times:
1. 2008 financial crisis — Musk put his last $20 million in
2. 2013 Model S production hell
3. 2017 Model 3 production hell
4. 2018 SEC investigation — Musk removed as chairman
5. 2020 COVID shutdown

[7:00-9:30]
**ACT III — THE RESOLUTION**
Tesla survived all five. By 2023: most valuable automaker in the world. $800 billion market cap.

[9:30-10:00]
**TAKEAWAY**
Your survival threshold is higher than you think. When you have two weeks of runway, you have two months of creativity.
""",

    "Uber": """[0:00]
**HOOK**
Travis Kalanick was 0-for-2. Two failed startups. Third try: a black car app that would make him a billionaire and get him fired — both within a decade.

[0:30-3:00]
**ACT I — THE RISE**
2008, Paris. Kalanick and Garrett Camp couldn't get a cab. Idea: tap a button, get a car. Uber launched in 2010. By 2014, it was in 100 cities.

[3:00-7:00]
**ACT II — THE STRUGGLE**
Growth at all costs. Uber fought regulators in every city. They called it "principled confrontation." Drivers protested. Competitors like Lyft emerged.

In 2017, a former engineer published a blog post about systemic sexism. The board investigated. 20 employees were fired. Kalanick was caught on video yelling at a driver.

[7:00-9:30]
**ACT III — THE RESOLUTION**
The board forced Kalanick out in 2017. Dara Khosrowshahi took over. Uber went public in 2019 at $82 billion — below expectations. By 2024, it finally turned its first profit.

[9:30-10:00]
**TAKEAWAY**
Growth without culture is a liability. The way you win matters as much as winning itself.
""",

    "Peloton": """[0:00]
**HOOK**
A $2,000 exercise bike became a $50 billion company. Then it lost $49 billion in 18 months.

[0:30-3:00]
**ACT I — THE RISE**
John Foley started Peloton in 2012. The idea: bring boutique fitness home. A bike with a screen, streaming live classes.

By 2019: 1 million members. COVID hit in 2020. Gyms closed. Peloton became essential. Revenue tripled. Valuation hit $50 billion.

[3:00-7:00]
**ACT II — THE STRUGGLE**
They built factories. Hired aggressively. Then vaccines arrived. Gyms reopened. Demand cratered.

In 2022, Peloton had $1 billion in unsold inventory. Warehouse workers stacked bikes like cordwood. The stock dropped 90%. Foley was replaced.

[7:00-9:30]
**ACT III — THE RESOLUTION**
New CEO Barry McCarthy cut costs, outsourced manufacturing, launched rental programs. By 2024, Peloton was still losing money but burning less. A cautionary tale of pandemic-era overreach.

[9:30-10:00]
**TAKEAWAY**
Never confuse a temporary tailwind with permanent demand. What booms in a crisis can bust in recovery.
""",

    "FTX": """[0:00]
**HOOK**
Sam Bankman-Fried was the face of crypto. 30 years old. $26 billion net worth. Magazine covers. Congressional testimony. Then it all evaporated in 72 hours.

[0:30-3:00]
**ACT I — THE RISE**
FTX launched in 2019. By 2021, it was the third-largest crypto exchange. SBF was a media darling — effective altruism, donating millions, promising to give away his fortune.

[3:00-7:00]
**ACT II — THE STRUGGLE**
The problem was hiding in plain sight. FTX's sister hedge fund, Alameda Research, had special privileges on the exchange. It could trade with zero collateral.

In November 2022, CoinDesk published a leaked balance sheet. Alameda held billions in FTT — FTX's own token. Confidence cracked. Customers tried to withdraw.

[7:00-9:30]
**ACT III — THE RESOLUTION**
Binance agreed to buy FTX, then backed out. FTX filed for bankruptcy 5 days later. $8 billion in customer funds missing. SBF arrested in the Bahamas. In 2023, he was convicted on all seven fraud counts.

[9:30-10:00]
**TAKEAWAY**
If the structure is complex and the returns are magical, the fraud is probably structural. Trust the balance sheet, not the persona.
""",

    "Enron": """[0:00]
**HOOK**
Fortune named Enron "America's Most Innovative Company" six years in a row. Then it collapsed in 24 days.

[0:30-3:00]
**ACT I — THE RISE**
Enron started as a natural gas pipeline company. CEO Jeff Skilling transformed it into a trading powerhouse. They traded energy, broadband, weather derivatives.

At its peak: $70 billion stock price, ranked 7th in the Fortune 500. Ken Lay was friends with two U.S. presidents.

[3:00-7:00]
**ACT II — THE STRUGGLE**
Enron's real business was hiding debt. CFO Andrew Fastow created "special purpose entities" — shell companies that borrowed money so Enron's books stayed clean.

Wall Street analyst: "I can't figure out how they make money." Enron's reply: "We don't want you to understand."

CFO Andrew Fastow created shell companies to hide debt. When the SEC started asking questions, the whole house of cards collapsed.

[7:00-9:30]
**ACT III — THE RESOLUTION**
Enron filed for bankruptcy in December 2001. 20,000 employees lost their jobs and pensions. Arthur Andersen — one of the Big Five accounting firms — was convicted of obstruction and dissolved.

[9:30-10:00]
**TAKEAWAY**
If you can't explain how you make money in one sentence, neither can your CFO. Complexity is the first mask of fraud.
""",

    "Facebook": """[0:00]
**HOOK**
Mark Zuckerberg built a $1 trillion company from a dorm room. Then he faced a scandal that revealed the dark side of the business model: Cambridge Analytica.

[0:30-3:00]
**ACT I — THE RISE**
Facebook launched in 2004. By 2012, 1 billion users. The IPO was the largest in tech history — $104 billion.

The business model: users provide data, advertisers pay to target them. Simple. Profitable. By 2018, Facebook was worth over $500 billion.

[3:00-7:00]
**ACT II — THE STRUGGLE**
In 2018, the Guardian revealed that Cambridge Analytica had harvested 87 million Facebook profiles without permission. Used them to influence the 2016 election.

Zuckerberg testified before Congress. "I'm sorry." The stock dropped 20% in 10 days. #DeleteFacebook trended globally.

The deeper problem: Facebook's growth depended on engagement. Outrage drove engagement. The algorithm optimized for anger.

[7:00-9:30]
**ACT III — THE RESOLUTION**
Facebook paid a $5 billion FTC fine — the largest ever for a tech company. They restricted third-party data access. Rebranded as Meta in 2021, betting everything on the metaverse. The bet cost $46 billion.

[9:30-10:00]
**TAKEAWAY**
When your growth depends on externalities you don't control, regulation is a matter of when, not if. Fix the problem before the government does.
""",

    "Apple": """[0:00]
**HOOK**
In 1997, Apple was 90 days from bankruptcy. Then Steve Jobs walked back through the door and rebuilt the most valuable company in history.

[0:30-3:00]
**ACT I — THE RISE**
Jobs founded Apple in 1976 with Steve Wozniak. The Mac launched in 1984 — revolutionary. But Jobs was pushed out in 1985 by the CEO he hired.

His return in 1997 was different. He killed 70% of Apple's product line. "Deciding what not to do is as important as deciding what to do."

[3:00-7:00]
**ACT II — THE STRUGGLE**
Year one back: $1 billion loss. Jobs cut a deal with Microsoft — $150 million investment, settling patent disputes. Critics called it surrender.

Then came the iMac. Then the iPod. Then the iPhone. Each product cannibalized the one before it. Jobs understood: if you don't kill your own product, someone else will.

[7:00-9:30]
**ACT III — THE RESOLUTION**
In 2011, Jobs resigned. Tim Cook took over. Skeptics predicted Apple's decline. Instead, Cook built the supply chain machine and Apple became the first $3 trillion company.

[9:30-10:00]
**TAKEAWAY**
Focus is not saying yes to the right things. It's saying no to everything else. What can you remove to make the rest better?
""",

    "Zoom": """[0:00]
**HOOK**
Eric Yuan left Cisco in 2011 because he couldn't build what he wanted: video that actually worked. Nine years later, Zoom became the most important piece of software on earth.

[0:30-3:00]
**ACT I — THE RISE**
Yuan grew up in China. He wrote code for 10 hours a day at his first job. In 1997, he moved to Silicon Valley with $1,000 and basic English.

At Cisco, he led WebEx. But the product was bloated. Slow. He knew video could be better. He quit and started Zoom.

[3:00-7:00]
**ACT II — THE STRUGGLE**
The first year: zero revenue. Investors passed. "Video is a commodity." Yuan kept building. Focus on one thing: make it work so well that nobody notices it.

In 2019, Zoom went public at $16 billion. Then COVID. In April 2020, Zoom went from 10 million to 300 million daily meeting participants in 3 months.

[7:00-9:30]
**ACT III — THE RESOLUTION**
The surge brought problems. Zoombombing. Security flaws. Yuan apologized, froze feature development for 90 days, fixed security. The stock peaked at $559 in Oct 2020 — a $170 billion company.

Then the world reopened. Growth normalized. Stock settled at $70. Still profitable. Yuan still CEO.

[9:30-10:00]
**TAKEAWAY**
Build something so simple it feels obvious. The best products don't get adopted — they become invisible. Nobody celebrates the door that opens smoothly.
""",

    "Amazon": """[0:00]
**HOOK**
In 1994, Jeff Bezos left a Wall Street job to sell books on the internet. His boss tried to talk him out of it. "It might work," Bezos replied, "but I think it's worth the risk."

[0:30-3:00]
**ACT I — THE RISE**
Amazon started in Bezos's garage. Every surface was covered in books. The first order: "Fluid Concepts and Creative Analogies" by Douglas Hofstadter.

By 1999, Bezos was Time's Person of the Year. The stock was up 50,000%. Then the dot-com crash hit — Amazon lost 95% of its value.

[3:00-7:00]
**ACT II — THE STRUGGLE**
Analysts called it "Amazon.toast." But Bezos had a secret: AWS. In 2006, Amazon launched cloud computing. Nobody noticed. By 2020, AWS was generating $45 billion in annual revenue — more than Amazon's retail business combined.

The paradox: every dollar of AWS profit was invested back into lower prices for customers. The flywheel: lower prices → more customers → more sellers → better selection → lower prices.

[7:00-9:30]
**ACT III — THE RESOLUTION**
By 2024, Amazon was worth $2 trillion. Bezos became the world's first centibillionaire. But the company faces antitrust lawsuits, union battles, and competition from Shopify and Temu.

[9:30-10:00]
**TAKEAWAY**
The flywheel: build something that gets better the more people use it. Then be patient enough to let it compound.
""",

    "Microsoft": """[0:00]
**HOOK**
In 2014, Microsoft was a fading giant. iPhone killed Windows. Google killed Bing. The tech world had written them off. Then Satya Nadella took over and did something radical: he blew up the old playbook.

[0:30-3:00]
**ACT I — THE RISE**
Bill Gates built Microsoft on a simple idea: a computer on every desk. By 2000, Windows ran 95% of the world's PCs. Microsoft was the most valuable company on earth.

But the world shifted. The internet moved to phones. Microsoft missed mobile entirely. Ballmer laughed at the iPhone. By 2013, Microsoft stock: flat for a decade.

[3:00-7:00]
**ACT II — THE STRUGGLE**
Nadella's first move: "We need to rediscover our soul." He killed Windows Phone. Released Office on iPad. Bought LinkedIn for $26 billion. Bought GitHub for $7.5 billion.

The big bet: Azure. Microsoft invested $50 billion in cloud infrastructure before it generated meaningful revenue. The board was nervous. Nadella: "We have to be willing to bet on things that will take 10 years."

[7:00-9:30]
**ACT III — THE RESOLUTION**
By 2024, Azure was the second-largest cloud provider. Microsoft was worth $3 trillion. The company that missed mobile became the AI leader through OpenAI partnership.

[9:30-10:00]
**TAKEAWAY**
Sometimes the best come back is not a turnaround — it's a reinvention. The hardest thing to change is your identity.
""",

    "Nvidia": """[0:00]
**HOOK**
In 1993, three engineers at a Denny's diner sketched a chip that would one day become the most important piece of silicon on earth. 30 years later, Nvidia was worth $3 trillion.

[0:30-3:00]
**ACT I — THE RISE**
Jensen Huang, Chris Malachowsky, and Curtis Priem started Nvidia to make graphics chips for video games. The first product failed. The second almost bankrupt them. By the third — the RIVA 128 — they had a hit.

The breakthrough was the GPU: a chip designed for parallel processing. Games needed it. Turns out, so did AI.

[3:00-7:00]
**ACT II — THE STRUGGLE**
In 2010, Nvidia bet everything on CUDA — a programming platform that let developers use GPUs for non-graphics work. It cost $500 million a year in R&D. For years, nobody used it.

CEO Jensen Huang: "We were investing in something that had zero revenue. The board was patient, but uncomfortable."

Then in 2012, Alex Krizhevsky used Nvidia GPUs to win the ImageNet competition. The AI revolution had found its engine.

[7:00-9:30]
**ACT III — THE RESOLUTION**
By 2024, Nvidia's H100 GPU was the most sought-after hardware on earth. 80% of AI training runs on Nvidia. Revenue hit $60 billion. Market cap passed $3 trillion — surpassing Apple and Microsoft for a time.

[9:30-10:00]
**TAKEAWAY**
The biggest opportunities look like hobbies for the first decade. Invest in what seems useless today. It might be essential tomorrow.
""",

    "OpenAI": """[0:00]
**HOOK**
Elon Musk started an AI nonprofit in 2015 because he thought Google was going to build Skynet. 8 years later, that nonprofit was a $90 billion company — and Musk was suing them.

[0:30-3:00]
**ACT I — THE RISE**
Sam Altman, Elon Musk, and other tech leaders pledged $1 billion to OpenAI. Mission: build safe AGI. Nonprofit. Open. For humanity.

By 2018, Musk left. He wanted control. They refused. The relationship never recovered.

[3:00-7:00]
**ACT II — THE STRUGGLE**
Without Musk's money, OpenAI needed cash. Altman created a "capped profit" structure — investors could earn 100x, no more. Microsoft invested $1 billion. Then $10 billion more.

The breakthrough: GPT-3 in 2020. Then ChatGPT in 2022 — 100 million users in 2 months. Fastest adoption in history.

[7:00-9:30]
**ACT III — THE RESOLUTION**
In 2023, the board fired Altman. 700 employees threatened to quit. Microsoft hired him. Five days later, he was back as CEO. The board that fired him resigned.

By 2024, OpenAI was valued at $90 billion. The nonprofit had become the most valuable AI company in the world.

[9:30-10:00]
**TAKEAWAY**
Structure follows power. No governance document survives contact with a successful product.
""",

    "Spotify": """[0:00]
**HOOK**
Daniel Ek grew up in a Stockholm housing project. He built a music service that destroyed the industry — and then saved it.

[0:30-3:00]
**ACT I — THE RISE**
Ek's first startup sold for $30 million when he was 23. But he noticed something: piracy was killing music. The industry was losing $10B/year. The problem wasn't pirates — it was that legal options were terrible.

Spotify launched in 2008. Instant access to millions of songs. Free with ads. Paid for no ads. The labels hated it — until they saw the revenue.

[3:00-7:00]
**ACT II — THE STRUGGLE**
Every deal was a war. Labels demanded advances, equity, ownership. Ek gave them equity in exchange for licenses. It worked — but Spotify didn't turn a profit for a decade.

Apple Music launched in 2015. Then Amazon. Then Google. All had deeper pockets. Spotify's answer: podcasting. $1B invested in Joe Rogan, Gimlet, Anchor.

[7:00-9:30]
**ACT III — THE RESOLUTION**
By 2024, Spotify had 600 million users. It finally turned its first profit. But the labels still control the music — and they take 70% of every dollar.

[9:30-10:00]
**TAKEAWAY**
If you can't control the supply, control the distribution. The middleman who delivers value survives.
""",

    "Google": """[0:00]
**HOOK**
Two Stanford PhD students built a search engine in a rented garage. They called it Google — a misspelling of "googol," meaning 1 followed by 100 zeros. They had no business model. No revenue. Just a belief that search could be better.

[0:30-3:00]
**ACT I — THE RISE**
Larry Page and Sergey Brin built PageRank: a system that ranked pages by how many other pages linked to them. It was dramatically better than Yahoo, AltaVista, or Lycos.

By 2004, Google was processing 200 million searches per day. The IPO raised $1.6 billion. The mantra: "Don't be evil."

[3:00-7:00]
**ACT II — THE STRUGGLE**
The problem: search doesn't make money. Their solution: AdWords — pay-per-click advertising tied to search intent. It became the most profitable business model in history.

Every year, Google faced a new threat: Facebook for social, Amazon for shopping, Apple for privacy, OpenAI for AI. Every time, Google responded with acquisitions — YouTube, Android, DeepMind, Waze, Fitbit.

[7:00-9:30]
**ACT III — THE RESOLUTION**
By 2024, Google was worth $2 trillion. 90% of revenue still comes from advertising. The AI race with OpenAI and Microsoft is the biggest threat yet. Google's advantage: 15 billion searches per day worth of data.

[9:30-10:00]
**TAKEAWAY**
When your products are free, you are the product. Google's real innovation was not search — it was finding a way to get paid for attention.
""",
}


def _find_seed(topic: dict) -> tuple:
    fields = [topic.get("title", ""), topic.get("company", ""), topic.get("angle", "")]
    search_text = " ".join(fields).lower()
    for name, script in SEED_SCRIPTS.items():
        if name.lower() in search_text:
            return name, script
    return "", ""


_NARRATIVE_TEMPLATE = """[0:00]
**HOOK**
Every iconic business story follows the same pattern: rise, struggle, resolution. This one is no different — but the details are what make it unforgettable.

[0:30-3:00]
**ACT I — THE RISE**
{angle}

The world didn't see it coming. While everyone else was looking in one direction, a small group of people saw something different. They bet on it. And for a while, they looked like geniuses.

[3:00-7:00]
**ACT II — THE STRUGGLE**
Then reality pushed back. What worked before stopped working. The easy choice would have been to ignore the warning signs. Doubling down is always more comfortable than admitting you were wrong.

But the warning signs were real.

[7:00-9:30]
**ACT III — THE RESOLUTION**
The turning point arrived disguised as a crisis. Some saw it as the end. Others saw the beginning of something new. The difference was preparation meeting opportunity.

[9:30-10:00]
**TAKEAWAY**
The lesson: narratives repeat because human nature doesn't change. Learn the pattern, and you can see the turning point before it arrives.
"""

_INSIDE_TEMPLATE = """[0:00]
**HOOK**
Some business stories are told in quarterly earnings. Others come out in interviews, leaked documents, and unexpected partnerships. This is one of the latter.

[0:30-3:00]
**ACT I — THE RISE**
{angle}

The public story was polished and rehearsed. The real story — the one behind closed doors — was messier. Egos, bets, last-minute decisions that could have gone either way.

[3:00-7:00]
**ACT II — THE STRUGGLE**
Behind every smooth narrative is a series of near-disasters. Deals that almost fell through. People who almost quit. Products that almost launched too late.

The companies that survive aren't the ones that avoid these moments. They are the ones that navigate them.

[7:00-9:30]
**ACT III — THE RESOLUTION**
What looked like a single decisive move was actually a chain of small decisions. Each one seemed unimportant at the time. Together, they determined everything.

[9:30-10:00]
**TAKEAWAY**
The details matter more than the headline. Read between the lines of every business story. That's where the real lessons live.
"""

_ANALYSIS_TEMPLATE = """[0:00]
**HOOK**
Most business analysis focuses on what happened. The more valuable question is why it happened — and what it means for everyone else.

[0:30-3:00]
**ACT I — THE CONTEXT**
{angle}

The market doesn't move in straight lines. It shifts when enough people change their minds at the same time. Understanding why those shifts happen is the core of business strategy.

[3:00-7:00]
**ACT II — THE STRATEGY**
The winning move often looks obvious in hindsight. That's the trap. At the time, it was a bet. The best strategists don't predict the future. They place bets where the downside is small and the upside is asymmetric.

[7:00-9:30]
**ACT III — THE LESSONS**
Strategy is not about being right once. It's about having a process that makes you right more often than you're wrong. The best companies have this process embedded in their culture.

[9:30-10:00]
**TAKEAWAY**
Good analysis answers "what happened." Great analysis answers "what should I do differently?"
"""

_INSIGHT_TEMPLATE = """[0:00]
**HOOK**
Every company has a story that explains why they win. Usually it's not the one in the press release.

[0:30-3:00]
**ACT I — THE COMPANY**
{angle}

Companies are not monoliths. They are groups of people making decisions under uncertainty. The best ones have a culture that surfaces the right decisions more often than the wrong ones.

[3:00-7:00]
**ACT II — THE MOVES**
The specific moves that made the difference were not always the obvious ones. Sometimes it was a pricing change. A hiring decision. A feature launch that seemed small but changed everything.

[7:00-9:30]
**ACT III — THE PATTERN**
Look closely enough, and patterns emerge. Great companies don't make one big bet. They make many small ones, learn fast from the failures, and double down on what works.

[9:30-10:00]
**TAKEAWAY**
Success leaves clues. The question is whether you're paying attention to the right ones.
"""

_INDUSTRY_TEMPLATE = """[0:00]
**HOOK**
Industries don't change overnight. They change one decision at a time — until suddenly, the old rules don't apply anymore.

[0:30-3:00]
**ACT I — THE SHIFT**
{angle}

The signals were there for anyone paying attention. A competitor changed pricing. A new regulation was proposed. A technology crossed a cost threshold. Individually, nothing. Together, everything.

[3:00-7:00]
**ACT II — THE RESPONSE**
Some companies saw the shift and adapted. Others ignored it and paid the price. The difference was not intelligence or resources. It was the willingness to question core assumptions.

[7:00-9:30]
**ACT III — THE NEW NORMAL**
After every industry shift, there are winners and losers. The winners share one trait: they acted before they had to. They made the painful changes while they still had the luxury of time.

[9:30-10:00]
**TAKEAWAY**
The hardest time to change is when you don't need to. The best time to prepare for a crisis is during the boom.
"""


def _pick_template(angle: str) -> str:
    angle_lower = angle.lower()
    if "narrative" in angle_lower:
        return _NARRATIVE_TEMPLATE
    if "inside" in angle_lower or "surprise" in angle_lower:
        return _INSIDE_TEMPLATE
    if "analysis" in angle_lower:
        return _ANALYSIS_TEMPLATE
    if "insight" in angle_lower or "company" in angle_lower:
        return _INSIGHT_TEMPLATE
    if "industry" in angle_lower:
        return _INDUSTRY_TEMPLATE
    return _NARRATIVE_TEMPLATE


def write_script(topic: dict) -> str:
    company = topic.get("company", "")
    if company in SEED_SCRIPTS:
        logger.info(f"Using seed script for: {company}")
        return SEED_SCRIPTS[company]

    matched_name, script = _find_seed(topic)
    if script:
        logger.info(f"Using seed script (matched '{matched_name}' in article text)")
        return script

    angle = topic.get("angle", "Business story")
    title = topic.get("title", "Business Story")
    template = _pick_template(angle)

    return template.format(angle=angle, title=title)

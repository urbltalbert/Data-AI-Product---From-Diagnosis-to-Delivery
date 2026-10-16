# 01 — Problem statement

**Team:** Team 7 · **Agent:** P8 · **Last updated:** 16 October 2026

> Every number says where it comes from: **measured**, **analogy** (a comparable, with its source) or **guess** (and how you will test it).

## 1. The problem in one sentence
LobbyIQ account managers spend ~45 min on each of the ~1,200 monthly "why did my rating drop?" requests, costing ~900 h a month (~€430k a year); today they read the hotel's reviews by hand and hotels wait 4 days. Success looks like requests answered within 24 h with an account-manager-approved synthesis.

| Number in the sentence | Value | Measured / analogy / guess | Source or test |
|---|---|---|---|
| Analysis requests per month | ~1,200 | guess | 20 % of tickets (P8 brief) × ~6,000 tickets (guess); check on the ticket log |
| Time per request | ~45 min | guess | time 20 requests ourselves on `reviews.csv` (S4) |
| Hours and cost | ~900 h/month, ~€430k/year | guess | 1,200 × 45 min × €40/h |
| Cost of one hour | €40 | analogy | French account-manager salary (~€45k gross, ~€65k loaded ÷ 1,600 h) |
| Time to answer today | 4 days | measured | P8 brief |
| Target | 24 h | measured | P8 brief |

## 2. Problem tree — from symptom to cause
- **Symptom:** hotels complain that answers about a rating drop are slow and vague.
- **Problem:** each request is handled by hand: one account manager reads the reviews, without comparing with the previous quarter.
- **Root cause** (5 Whys):
  1. Why do hotels wait 4 days? — The account manager must read the reviews before answering.
  2. Why read them one by one? — The product shows only the average score and a list of reviews.
  3. Why nothing in between? — Reviews are free text; nothing turns them into themes per hotel and per period.
  4. Why? — The product was built to collect and display reviews, not to analyse them.
  5. Why does it matter now? — 20 % of tickets are analysis requests: support is covering a missing feature.
- **What would fix the cause:** a view of each hotel's review themes, compared with the previous quarter. Which score moved is a **rule** (a sub-score trend); why it moved is in the text, so it needs **AI**.

## 3. Is AI the right tool?
| Question | Our answer |
|---|---|
| Is there a rule that solves 80 % of it? | No. A sub-score trend shows which score dropped, not why. |
| Is it a prediction / generation problem, or an organisational decision? | Generation: summarising reviews into themes. What to fix stays the hotel's decision. |
| Do we have the data — which, how much, who owns it? | Guest reviews: `reviews.csv`, 47,741 reviews. They belong to guests and hotels. No theme labels: human graders needed. |
| What does one error cost — and who pays it? | A wrong top issue: the hotel fixes the wrong thing and loses trust. The hotel pays, then LobbyIQ (churn). Limited because a human validates every draft. |

**Level chosen:** agent — **and why not the level below:** a single GenAI prompt cannot do it: the job chains several steps on the hotel's data (fetch two quarters of reviews, compute trends, extract themes, draft).

## 4. Why this agent — the four selection questions
| Criterion | Our answer, one line |
|---|---|
| High frequency — is the work done every day or every hour? | Yes: ~55 requests per working day. |
| Bounded decision space — can we list its tools and outcomes on one slide? | Yes: 4 tools (get reviews, compute trends, extract themes, draft), 2 outcomes (draft or "not enough reviews → human"). |
| Measurable success — can we say in one sentence whether it succeeded on one ticket? | Yes: the account manager sends the draft within 24 h with minor edits only. |
| Recoverable failure — if it is wrong, is the damage limited and reversible? | Yes: nothing reaches the hotel without a human. |

## 5. Press release (Working Backwards)
**3 May 2027 — LobbyIQ launches Review Insights.** Hotels that ask why their rating dropped no longer wait days for an answer: they get a one-page summary of the top three issues guests mention and what changed since last quarter, checked by their account manager. In the pilot, 82 % of requests were answered within a day. *"The next morning I knew it was the breakfast queue — we fixed it that week,"* said a hotel manager in Lyon.

## 6. What would have to be true?
| # | Hypothesis | Measured / analogy / guess | How we will test it | Session |
|---|---|---|---|---|
| 1 | ≥ 70 % of drafts are sendable with minor edits | guess | 200 requests rebuilt from `reviews.csv`, scored by two graders on a rubric | S4 prototype |
| 2 | The agent's top three issues match a human's (2 of 3) for ≥ 80 % of hotels | guess | same 200 requests, human top three made blind | S4 prototype |
| 3 | Time per request falls from ~45 to ≤ 10 min | guess | time measured with and without the draft, A/B per account manager | S5 metrics / S6 A/B |

## 7. Do-nothing baseline
In 12 months without the agent: +10 % hotels (guess), account managers 10 % faster (guess), and a sub-score chart lets 15 % of hotels answer themselves (guess). Result: ~760 h a month (~€360k a year). Cheaper than today, but hotels still wait days.

## 8. Persona, journey & stakeholder map
- **Customer — Marc, hotel general manager:** "When my rating drops, I want to know the top issues, so that I fix them before the season — without reading 300 reviews."
- **User — Claire, account manager:** ~100 hotels, ~40 requests a month. Pain: reading reviews takes most of the time.
- **Claire's journey:** read the request → open the reviews → *read 100–300 reviews* → *note themes* → *write the email* → check and send. The agent takes the steps in italics; Claire keeps the check and the send.

| | Low interest | High interest |
|---|---|---|
| **High power** | Legal / DPO · CFO | Head of Customer Success · Head of Product |
| **Low power** | Hotels that never ask | Account managers · hotel managers |

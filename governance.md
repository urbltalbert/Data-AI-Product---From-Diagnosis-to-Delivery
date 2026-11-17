# Governance — our living file

> Created for Assignment 1, one line added every session. One question at the oral is drawn from this file.
> Answers are provisional: write what you know today, and mark what you still have to check.

## Session 1 — the six questions
| # | Question | Our answer (provisional) | To check with |
|---|---|---|---|
| 1 | **EU AI Act:** which risk tier is our agent in, and why? (minimal · limited — transparency: tell the user it is an AI · high-risk · prohibited) | Limited: it drafts a report, decides nothing about access to a service. The hotel is told the summary is AI-assisted. | Legal — confirm the tier |
| 2 | **Data:** whose data does it use, and on what legal basis? (GDPR art. 6; what the B2B contract allows) | Guest reviews, which can contain names. The hotel is controller, LobbyIQ processor; legitimate interest (art. 6(1)(f)). One hotel's reviews never appear in another hotel's summary. | DPO — does the contract cover an LLM provider? |
| 3 | **Accountability:** who is accountable when it is wrong — and where is the human? | The account manager approves and sends every summary. The Head of Customer Success owns the agent and can switch it off. | Head of Customer Success |
| 4 | **Never:** what must it never do? (our first guardrail) | Send anything to a hotel itself. | — |
| 5 | **Explainability:** explainable to whom — the customer, the support agent, the auditor? | Hotel: each issue with its count and example reviews. Account manager: the reviews behind each claim. Auditor: a log of reviews used, prompt and model version. | — |
| 6 | **The people it cannot serve:** what happens to them? | Hotels with too few reviews: the account manager answers as today. | Threshold to set in S4 |

## Session 2 — the cost of error
- Which cost-of-error line is a **legal or reputational** risk, not just money? The cost of a wrong answer (`02_sizing.xlsx`, Inputs row 30). Reputational: a wrong top issue reaches a hotel, which fixes the wrong thing and stops trusting LobbyIQ. Legal: a summary quotes a guest's name or personal details (GDPR).
- Who in the company **owns** that risk? The Head of Customer Success (wrong top issue); the DPO (personal data in a summary). To check: does the DPO accept this owner split?

## Session 3 — data and trust level

### The six-question data audit
| # | Question | Our answer | Source type (measured / analogy / guess) | To check with |
|---|---|---|---|---|
| 1 | **Provenance** — where does each row come from, who collected it, when? | Production: guest reviews posted on LobbyIQ by guests of each hotel. Eval-set: synthetic reviews in the `reviews.csv` format, with three planted issues per hotel. | measured | — |
| 2 | **Volume & labels** — how many rows, labelled by whom, with which guideline? | `reviews.csv`: 47,741 reviews, no theme labels. Eval-set: 20 cases now, labelled by hand by Ugo and Enzo (expected top 3 themes, hand-over yes/no). | measured | — |
| 3 | **Coverage** — which languages, plans, regions vs the users we ship to? | English only. Hotels with ≥ 50 reviews a quarter. Non-English reviews and small hotels go to the account manager. | guess | check language mix on `reviews.csv` (S4) |
| 4 | **Rights** — legal basis (GDPR art. 6), what the customer contract allows, retention | Hotel = controller, LobbyIQ = processor, legitimate interest (art. 6(1)(f)). Reviews are not used to train a model. Drafts and logs kept 12 months. | guess | DPO — does the contract cover an LLM provider? |
| 5 | **Leakage** — can a row reappear in the test set, or in another customer's answer? | Eval cases are never used to tune the prompt. Every query is filtered on one `hotel_id`: no review from hotel A in hotel B's draft. | guess | test cross-hotel cases in S4 |
| 6 | **Freshness** — how old is it, does that world still exist? | Two quarters only (current vs previous). Older reviews are not read. | measured | — |

- **Purpose limitation (GDPR art. 5):** reviews are used only to answer the hotel's "why did my rating drop?" request; drafts and logs are kept 12 months for audit, then deleted.
- **Isolation between customers:** one request = one `hotel_id`; the review query and the policy check both refuse any other hotel ID. A chain asking about several hotels goes to a person.
- **Known gaps by segment** (language, plan, region): non-English reviews (≈ half in summer for leisure hotels — interview 3); hotels with < 50 reviews a quarter; staff and guest names in review text (masked before drafting).

### Trust level per step (same scale as Session 1)
| Step | L1 suggests · L2 drafts, a person approves · L3 acts on a scope, a person samples · L4 acts alone under a threshold · or person only | Why (cost of an error) |
|---|---|---|
| 1. Detect the request, identify the hotel | L3 — Claire samples | wrong hotel = rework, ~€5 |
| 2. Extract two quarters of reviews | L4 | rule-based; wrong window = skewed comparison |
| 3. Read the reviews | L2 | missed driver, paid at step 4 |
| 4. Group themes, compare vs last quarter | L2 | wrong top issue sent to a hotel, ~€100 |
| 5. Draft the email | L2 | unclear reply = follow-up ticket |
| 6. Review and send | person only | wrong data or a guest name reaches the hotel (GDPR) |

## Session 4 — human-in-the-loop points and the override switch (to come)
## Session 5 — counter-metrics and the segments we report (to come)
## Session 6 — protected segments and the harm threshold that stops an experiment (to come)
## Session 7 — accountable owner, rollback authority, incident path (to come)

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
- Which cost-of-error line is a **legal or reputational** risk, not just money? …
- Who in the company **owns** that risk? …

## Session 3 — data (to come)
## Session 4 — human-in-the-loop points and the override switch (to come)
## Session 5 — counter-metrics and the segments we report (to come)
## Session 6 — protected segments and the harm threshold that stops an experiment (to come)
## Session 7 — accountable owner, rollback authority, incident path (to come)

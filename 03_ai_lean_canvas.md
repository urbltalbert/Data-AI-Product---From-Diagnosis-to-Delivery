# 03 — AI Lean Canvas · Review Insights

## The nine classic blocks
| Block | Our answer | Comes from |
|---|---|---|
| 1. Problem — top 3 pains | ~45 min per "why did my rating drop?" request · hotels wait 4 days · positive and negative reviews read by hand | 01 |
| 2. Users / customer segments | User: Claire, account manager (~100 hotels). Customer: hotel general managers with ≥ 50 reviews a quarter | 01 (persona) |
| 3. Unique value proposition — one sentence | The top three issues guests mention and what changed since last quarter, checked by your account manager, within a day | 01 (press release) |
| 4. Solution — the MUST features | A. top 3 negative themes with counts and 2 quotes · B. quarter-over-quarter delta per theme · C. ticket panel with approve / edit / write-myself and timer | 03 brief §3 |
| 5. Channels — where it lives | Sidebar panel in the existing ticketing tool, next to the hotel's message | 03 brief §6 |
| 6. Value — what it is worth per year (base case, EV) | Net €56k base · EV €55k (year 1) | 02 |
| 7. Cost structure — the seven cost lines | Tokens €0.4k · errors €18k · integration €15k · evaluation €15k · supervision €19.5k · monitoring €10k · re-evaluation €9k | 02 |
| 8. Key metric — the success criterion | ≥ 75 % of in-scope requests get a draft sendable after minor edits (two graders) — zero guest names or other hotels' data | 03 brief §7 |
| 9. Unfair advantage — data or know-how nobody else has | All reviews of 3,000 hotels and the ticket flow in one place; no vendor does this inside our tickets | 02 (build / buy) |

## The five AI blocks
| Block | Our answer | Comes from |
|---|---|---|
| 10. Data — sources, rights, gaps | Guest reviews, two quarters per hotel · legitimate interest, hotel = controller · gaps: non-English, < 50 reviews | governance.md · S3 |
| 11. Model — rung per part | Detection: classical ML · eligibility, metrics, guardrail: rules · themes: LLM · draft: hybrid template + LLM | 03 brief §5 |
| 12. Evaluation — the eval-set and its size | `evals/eval_set_v0.csv`, 20 cases now, 50 with Assignment 4, two graders | evals/ |
| 13. Human in the loop — trust level per step, way back to a person | L3 detect · L4 extract · L2 read, themes, draft · send person only · no draft → Claire, with the reason | 03 brief §2 |
| 14. Risks & governance — what it must never do, rollback trigger | Never send to a hotel itself · never show a guest name or another hotel's data · rollback: one cross-hotel leak or > 2 complaints a month | governance.md |

# Team 7 — Review insights for hotels

**Course:** Data & AI Product: From Diagnosis to Delivery (MSA-DAT07-04) · Albert School
**Cohort:** M2-INTER-1

## Team
| Name | Git handle | Also in the Agentic Workflows team? |
|---|---|---|
| Ugo Reboullet | `urbltalbert` | no |
| Enzo Méret | `emeret-as` | no |

## Our agent
- **Starting point:** P8 — Voice-of-customer synthesis — hospitality-tech SaaS
- **The company:** LobbyIQ (fictional), reviews platform for 3,000 hotels, ~6,000 tickets per month, 30 account managers
- **The job, in one sentence:** When a hotel asks why its rating dropped, the agent analyses that hotel's reviews, producing a one-page draft (top three issues, change vs last quarter) for the account manager.
- **Trust level per step:** L3 detect the request · L4 compute rating trends · L2 draft (the account manager approves every draft) · send: person only (the account manager)
- **One thing it must never do:** send anything to a hotel itself.

## Repository structure
One numbered file per session. Every member authors commits in at least four of the numbered files.

| File | Session | Status |
|---|---|---|
| `00_pitch.md` | before S3 — only if you bring your own idea | not needed (P8) |
| `01_problem_statement.md` | S1–S2 — Assignment 1 | done |
| `governance.md` | created for Assignment 1, one line added every session | S1–S7 done |
| `02_sizing.xlsx` | S2 — Assignment 2 | done |
| `02_investment_memo.md` | S2 — Assignment 2 | done |
| `03_product_brief.md`, `03_ai_lean_canvas.md`, `03_user_research.md`, `03_prototype_link.md` | S3 — Assignment 3 | done (brief v2) |
| `04_architecture.md` | S4 | done (v0 prototype) |
| `05_metrics.md` | S5 | done — numbers traced; two-grader number still to measure |
| `06_07_experiments_operations.md` | S6 + S7 | done — no experiment run; rollback drill 20 Nov |
| `08_launch_memo.md` | S8 | draft v1.0 candidate (decision: shadow mode only) |
| `spec.md`, `product_brief.md` | skeleton in S3, final at the end | spec v3 and brief v3 written 20 Nov; to be reviewed by both members before the tag |
| `/prototype`, `/evals`, `/data` | from S4 | v0 built; first run 0 / 33, after spec v2 24 / 30 on fresh cases but 1 draft on a hand-over case; after spec v3 0 / 22 such drafts but 13 / 28 = 46 % in-scope served (`evals/report_v0.md` §8) |

## Rules
- Commit with your own Git account: the individual question at the oral is about a commit you signed.
- Tag the final version `v1.0` before the first oral of your cohort. No commits after the first oral starts.

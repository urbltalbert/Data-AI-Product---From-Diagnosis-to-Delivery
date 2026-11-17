# 03 — Product brief · Review Insights · v2

**Team:** Team 7 · **Starting point:** P8 · **Version:** v1 — 16 October 2026 · v2 — 6 November 2026

## 1. Problem, user, do-nothing  *(from 01)*
- **Problem in one sentence (with a number):** Account managers spend ~45 min handling each of ~1,200 monthly "why did my rating drop?" inquiries (~900 h/month, ~€430k/year), leaving hotels waiting 4 days for an answer.
- **User (persona):** Claire, an account manager overseeing ~100 hotels — goal: reply within 24 h with a verifiable explanation — pain: manually reading 100–300 reviews per inquiry.
- **Do-nothing baseline:** ~760 h/month at 12 months (~€360k/year), with multi-day response delays unchanged.

## 2. The process — as-is and to-be
| # | Step | Who today | Minutes | Error rate | Cost of an error | Automate / augment / keep human (test it fails) | Trust level | Minutes after | Metric for this step |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Read the ticket and identify the hotel | Claire | 3 (guess) | 2 % (guess) | rework, ~€5 | automate — passes all 8 tests | L3, Claire audits a sample | 0 | % of inquiries detected (recall) |
| 2 | Extract two quarters of review data | Claire | 5 (guess) | 5 % wrong window (guess) | skewed comparison, ~€40 | automate — rule-based, passes all 8 tests | L4 | 0 | % of inquiries with exact date range |
| 3 | Read through 100–300 reviews | Claire | 20 (guess) | ~60 % skipped (guess) | missed driver, paid at step 4 | augment — fails test 5 (hotels require concrete "why" examples) | L2 | 3 (verify quotes) | reading time per ticket |
| 4 | Group themes and compare vs. prior quarter | Claire | 10 (guess) | 20 % theme missed (guess) | hotel acts on wrong issue, ~€100 (02_sizing) | augment — fails test 6 (low error tolerance) | L2 | 2 | top-3 overlap with human benchmark (≥ 2/3) |
| 5 | Draft the response email | Claire | 5 (guess) | 5 % (guess) | unclear reply triggers follow-up ticket | augment — fails test 5 (the reply must explain the cause in detail) | L2 | 3 | % of drafts sent with minor edits only |
| 6 | Review and send | Claire | 2 (guess) | 1 % (guess) | inaccurate data sent to client, ~€100 | keep human — fails test 6 (zero tolerance externally) | person only | 2 | 0 drafts sent without explicit approval |
| | **Total** | | **45** | | | | | **10** | handling time per ticket (S6 A/B) |

All timings above are initial estimates; we will benchmark 20 tickets directly on the eval-set during S4.

**Where the pain sits (the two steps):** Steps 3 and 4 account for 30 of the 45 minutes.
**The way back to a person (designed first):** Fewer than 50 reviews in the quarter, predominantly non-English reviews, an off-topic ticket, or low router confidence → no draft is generated and the ticket routes directly to Claire with the fallback reason displayed. Claire also retains a one-click "write it myself" option at any time.
**Where the governance line sits:** Between steps 5 and 6. Nothing is sent externally without Claire's approval, and no guest or staff names appear in any draft.

*Trust levels — L1 suggests · L2 drafts, a person approves · L3 acts within scope, a person samples · L4 acts autonomously under a threshold.*

## 3. Features — RICE and MoSCoW
Reach = monthly in-scope tickets: 1,200 × 80 % (≥ 50 reviews) × 90 % (eligible query) = 864 (02_sizing.xlsx).

| Feature | Reach / month | Impact | Confidence | Effort (p-w) | RICE | MoSCoW |
|---|---|---|---|---|---|---|
| B. Quarter-over-quarter delta per theme | 864 | 2 | 80 % | 1 | 1,382 | MUST |
| A. Top 3 negative themes with counts and 2 anonymised quotes | 864 | 3 | 80 % | 3 | 691 | MUST |
| D. Auto-send response directly to the hotel | 864 | 1 | 50 % | 1 | 432 | WON'T |
| C. Ticket panel with approve / edit / write-myself actions and timer | 864 | 1 | 80 % | 2 | 346 | MUST |
| E. Self-serve analytics portal for hotels | 3,000 | 1 | 50 % | 8 | 188 | WON'T |
| F. Automated operational recommendations ("fix breakfast queue") | 864 | 0.5 | 50 % | 2 | 108 | WON'T |
| G. Auto-draft public replies to guest reviews | 1,000 | 0.5 | 50 % | 3 | 83 | WON'T |
| H. Competitive benchmark against local peers | 864 | 0.5 | 50 % | 4 | 54 | WON'T |

- **MUST (3):** B, A, C.
- **SHOULD / COULD:** None in this release.
- **WON'T this time (5) — out of scope, 16 October:** D (auto-send), E (hotel portal), F (action recommendations), G (public review replies), H (local benchmarking). Non-English reviews also remain out of scope (handed over).
- **The feature that tests our flip assumption, and why it is a MUST:** Feature C. Our viability threshold requires ~75 % time savings (02_sizing.xlsx). Only C records elapsed time between opening and sending a draft; without it, we cannot validate the flip point despite its lower direct impact on the hotel.
- **The cut that hurt the most:** Feature D. Although its RICE score exceeds C, removing human sign-off exposes hotels to inaccurate root-cause diagnoses.

## 4. Data  *(details in governance.md)*
Production uses hotel guest reviews; our eval-set comprises synthetic records matching `reviews.csv` (41 hotels, ~9,100 reviews via `data/make_data.py`) with three planted issues per property so ground-truth top-3 themes are known prior to execution. Production data has no ground-truth theme labels. Scope is restricted to English reviews (French and German tickets route to humans). Under GDPR, the hotel acts as controller and LobbyIQ as processor under legitimate interest (Art. 6(1)(f)). Guest names are masked prior to drafting, queries are strictly isolated by `hotel_id`, and the window covers exactly two quarters.

## 5. Model — one rung per part
| Part | Rung | Why the rung below fails |
|---|---|---|
| Request detection | 2 — classical ML (TF-IDF + logistic regression) | static keyword rules miss phrasing like "guests seem less satisfied" |
| Eligibility check (≥ 50 reviews, valid hotel ID) | 1 — deterministic rules | lowest rung; exact threshold and ID lookup |
| Quarter-over-quarter metrics (scores, volumes) | 1 — deterministic rules (SQL) | lowest rung; exact aggregation |
| Theme extraction | 3 — pretrained model (LLM) | no labelled training set exists and complaint topics vary across properties |
| Response drafting | 4 — hybrid (fixed template + LLM synthesis) | rigid templates cannot explain root causes, while unconstrained LLMs drift in layout |
| Policy guardrail (PII, cross-tenant IDs, commitments) | 1 — deterministic rules | lowest rung; strict regex/ID assertions |

## 6. Where it lives (integration surface)
Embedded sidebar panel inside the existing support ticketing interface alongside the hotel's message. Latency: pre-computed in batch (< 5 min) so the draft is ready when Claire opens the ticket. Layout: single-screen summary covering 3 themes, delta counts, and 2 linked quotes each. Fallback: explicit "no draft" banner stating the routing reason. Audit log (source review IDs, prompt, model version) accessible to Claire, the Head of CS, and compliance auditors.

## 7. Success criterion — one sentence
> By 15 November, on our 50-case eval-set, at least 75 % of in-scope inquiries produce a draft that two independent graders mark as sendable after minor edits only — with zero drafts containing a guest name or another hotel's data.

75 % corresponds to our handling-time flip point in `02_sizing.xlsx`; on the offline eval-set we proxy it via minor-edit sendability, and measure live minutes during the S6 A/B test.

## 8. Risks and rollback trigger
- **Primary risks:** Misidentifying the top driver sent to a hotel · leaking personal names in a draft (GDPR) · rubber-stamping drafts without review.
- **Rollback trigger:** Any single draft exposing another property's data, or > 2 hotel complaints regarding inaccurate diagnoses within a calendar month → disable the copilot globally and revert to the manual workflow.

---
*v2 — after user feedback*

## 9. What the users changed
Detailed notes in `03_user_research.md`.

| Change | Evidence |
|---|---|
| Display both compared quarters explicitly at the top of the draft | Usability tester 2 paused to check which baseline quarter was used; interviewee 2 (CSM): clients ask what period the numbers are compared against |
| Make every quote clickable to open the full source review | Usability tester 3 clicked a quote expecting the full review; interviewee 2 (CSM) redoes any check they cannot click through to |
| Count theme frequencies on negative reviews/mentions only | Interviewee 1 (hotel GM) skips positive reviews: they do not explain a drop |
| Keep non-English reviews out of scope (WON'T, routed to human) | Interviewee 3 (front office): nearly half of summer reviews are in German or Italian |

## 10. What they could not decide
- Minimum review volume required to trigger a draft (currently set at 50): to be finalised by the Head of CS after S4 evaluation results.
- Minimum negative mention count to surface a theme: to be calibrated by account managers during the first month of live usage.
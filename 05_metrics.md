# 05 · Metrics — Team 7 · Review Insights (P8)

> Five sections = the five moves of the session. Every number traces to `02_sizing.xlsx` (**[S]**), `evals/report_v0.md` (**[R]**) or `03_product_brief.md` (**[B]**). A number marked *hypothesis* is a promise to test in Sessions 6–7, not a measurement.
> Honest status on 20 Nov 2026: the **two-grader number does not exist yet** (`evals/golden_30.csv` is ungraded). The only measured AI-system number is the *automatic proxy* of `evals/report_v0.md`.

## 1 · Place the number — the stack for our agent
| Level | Question | Our metric | Value today | Produced by | Owner | Clock |
|---|---|---|---|---|---|---|
| 5 Business | does it move the P&L? | account-manager hours on analysis requests per month | ~900 h baseline **[S]**; effect *hypothesis*: 45 → ≤ 10 min per request (brief §2 **[B]**) | online A/B (S6), then monitoring | Head of Customer Success | months |
| 4 Product | does the user adopt it and get the job done? | share of in-scope requests where Claire sends the draft with minor edits only, within 24 h | not yet (no users) | online A/B + weekly human sample | Head of Customer Success | weeks |
| 3 Guardrails & RAI | does it stay inside the lines — for everyone? | drafts that contain a guest/staff name or another hotel's data, and drafts on hand-over tickets | names/other hotel: 0 / 13 drafts on the last fresh set **[R §8]**; drafts on hand-over tickets: **0 / 22 on the last fresh set after the fix [R §8]**, but it was broken on the two runs before (C07 [R §6], C100 [R §7]) — one clean run does not prove the floor | assertions on every commit + weekly human sample + DPO check | DPO (personal data) · Head of CS (hand-over) | days |
| 2 AI system | does the workflow complete the task? | in-scope cases whose draft has ≥ 2 of 3 right themes and both quarters (automatic proxy) | **13 / 28 = 46 %** (95 % interval 30–64 %) on the last fresh 50 cases **[R §8]**; 24 / 30 = 80 % on the fresh set before the fix **[R §7]**; criterion 75 % **[B §7]** *not verified*; two-grader number: *not yet* | eval-set v2 + two graders + judge (§5) | the two team members | hours |
| 1 Model | is the component right? | step 1 detector: share of in-scope tickets with confidence ≥ 0.60 (recall at the validation-chosen threshold) | 13 / 28 on the last fresh cases **[R §8]**; 24 / 30 before the fix **[R §7]**; recall 0.85 on the 50 validation tickets at threshold 0.60 **[R §8]** | offline eval-set | the two team members | seconds |

## 2 · Decide when to stop — the stop criterion
*"We stop improving **the step-1 detector's recall** at **the level where in-scope tickets served reach ≥ 75 % on a frozen fresh set** because **the share of drafts a person sends with minor edits** stops responding — and the next point would cost **new labelled tickets (one more labelling round of ≥ 100 tickets) and a re-run of a new frozen eval-set**."* **We are not there:** the last fresh run gives 46 % **[R §8]**, so the stop criterion is not met and the detector is still the thing to improve.

- **Component metric and value:** detector recall on rating-drop tickets, 0.85 on 20 validation positives **[R §8]** and 46 % of in-scope fresh tickets served **[R §8]**. The validation number overstates the fresh one (the validation tickets are written in the same style as the training ones); the stop is confirmed only when a fresh set and two graders' number are in.
- **Level-above metric that stops responding:** sendable share (two graders). Today unknown; the stop is invalid until it exists.
- **Cost of the next point:** one more labelling and eval round — not priced separately; it falls under the evaluation line of `02_sizing.xlsx` (€15k/year base **[S]**), which the base case already carries.
- **Floor, not a stop (any miss blocks the release):** **a draft on a hand-over ticket, a guest or staff name in a draft, another hotel's data in a draft.** It was broken in two runs (C07, C100) and held on the last one (0 / 22 [R §8]); one clean run on 22 cases (upper bound 15 %) is not enough to release — **no release** until it holds on a new frozen set and in shadow mode on real tickets.

## 3 · Choose what to protect — the hierarchy, by segment
| Kind | Metric | Numerator / denominator | Level | Lag | Source & owner |
|---|---|---|---|---|---|
| **Primary (1)** | Analysis requests answered within 24 h with a draft the account manager sent with minor edits only | requests sent ≤ 24 h with minor edits ÷ in-scope requests | 4 Product | weeks | ticket log + edit-distance of sent vs draft; Head of CS. Baseline: 4 days **[B]**. Not gameable by clicking: *sent* and *minor edits* are measured on the sent text |
| Guardrail (3) | Drafts on hand-over tickets | drafts on hand-over tickets ÷ hand-over tickets | 3 Guardrails | days | eval-set + production log; Head of CS. Threshold: 0 (floor) |
| Guardrail | Guest or staff name, or another hotel's data, in a draft | such drafts ÷ drafts produced | 3 Guardrails | days | automatic check + weekly human sample; DPO. Threshold: 0 |
| Guardrail | Wrong top issue: drafts with < 2 of 3 right themes | such drafts ÷ drafts sent | 2 AI system | weeks | weekly human sample of 5 % of sent drafts; Head of CS. Threshold: the 5 % error rate of `02_sizing.xlsx` base **[S]** |
| **Counter-metric (2)** | Hotel complaints about an inaccurate diagnosis (brief §8 rollback trigger: > 2 a month) | complaints ÷ drafts sent, per month | 5 Business | months | CS ticket tag; Head of CS |
| Counter-metric | Time Claire spends per request, including verifying quotes — *not just the time to the first draft* | median minutes per request | 4 Product | weeks | ticket timer (MUST feature C); Head of CS. Catches "fast but she redoes the work" |

- **Segments reported (from the S3 audit):** language of the reviews (English / other — hand-over today), reviews per quarter (≥ 50 / < 50 — hand-over today), hotel type (urban / leisure / business / small / chain), stars (2–4), and account manager (the A/B unit, S6). Fresh-case proxy by segment, before the fix **[R §7 data]**: 4-star 10/12, 3-star 11/15, 2-star 3/3; business hotels 3/6 are the weakest (n = 6, too small to conclude).
- **Fairness metric:** equal error rates across hotel segments — the *right top 3* rate must not differ by more than 15 points between the best and the worst segment with ≥ 30 cases. With 100 cases no segment has n ≥ 30, so this is declared but not yet testable.
- **Harm threshold (stops the rollout) and owner:** *more than 2 hotel complaints about an inaccurate diagnosis in a calendar month, or one draft that shows another hotel's data or a guest name, in any segment → disable the copilot globally and return to the manual workflow. Owner: Head of Customer Success; DPO for the data case.* (Same wording as the brief §8 **[B]**. Copied into `governance.md`.)
- **How it could be gamed → repair:** (a) Claire clicks "approve" without reading → the primary metric counts *minor edits measured on the sent text* and a weekly human sample re-reads 5 % of sent drafts; (b) the drafter learns that two themes pass → the proxy is re-checked by two humans on the golden set; (c) hand-over rates are lowered by lowering the confidence threshold → the floor "zero drafts on hand-over tickets" is a gate, not a trend.

## 4 · Derive the business metrics — three, with expected effects
| Business metric | Baseline (`02_sizing.xlsx`) | Expected effect (from `evals/report_v0.md` × the cost line) | Lag | Read date | It is a hypothesis about… |
|---|---|---|---|---|---|
| Account-manager hours per in-scope analysis request | 45 min per request, ~900 h/month, cost €40 × 45 min **[S, brief §2]** | **≤ 10 min** (hypothesis 3 of `01_problem_statement.md`): the proxy says 80 % of the drafts that exist have the right top 3 **[R §7]**, but only 46 % of in-scope tickets get a draft **[R §8]**; the sizing assumes 60 % of time saved in the base case and 75 % at the flip point **[S]**. *Not yet supported*: the minutes were never measured, and the proxy is not time | 4–8 weeks | end of the 4-week A/B (S6 protocol) | the arrow "right top 3 → less reading and writing time". The 75 % flip point is the number to test |
| Answer time to the hotel | 4 days **[B]** | **≤ 24 h** for in-scope requests: a draft is ready in < 5 min **[B §6]**; Claire's check is the delay | 4 weeks | end of the A/B | the arrow "draft ready → Claire sends sooner". Depends on her workload, not on the AI |
| **Quality of what reaches the hotels — stated as a non-effect** | wrong-top-issue errors: 5 % of drafts × €100 = ~€18k/year in the base case **[S]** | **unchanged ± 2 percentage points** on the weekly human sample: the copilot must not make the answers *worse* than today's by-hand answers | 4–12 weeks | 4 weeks, then monthly | the arrow "draft → what Claire sends". If the error rate rises above the band, the harm threshold (§3) stops the rollout |

The tree (component → product → business):
```
step 1 detect: 13/28 in-scope served [R §8] ──▶ in-scope tickets that get a draft ──▶ drafts with right top 3 (proxy 80 % before fix) ──▶ sent with minor edits (not measured)
                                                                             │                                          │
                                                                             └──▶ minutes per request: 45 → ≤ 10 (hyp.) ──▶ hours/month and €/year (sizing, flip point 75 % time saved [S])
                                                                             └──▶ answer time: 4 days → ≤ 24 h (hyp.)
guardrails: 0 names · 0 other hotel · 0 drafts on hand-over (held on the last run, broken on two before)  ──▶ non-effect: error rate 5 % ± 2 pts
```
Link between level 2 and the business: the proxy is 80 % *right top 3* (on the drafts produced; 46 % of in-scope tickets get one), whereas the sizing asks for 75 % *of handling time saved*. These are not the same thing; the A/B (S6) is where they meet.

## 5 · Make the judge trustworthy — the evaluation plan
- **Eval-sets:** `evals/eval_set_v2.csv`, **150 cases** = v1 (100) + C101–C150 (91 in scope, 59 hand-overs; v1 alone: 63 / 37), stratified by hand-over reason, stars and hotel type; synthetic inputs tagged in `origin`; labels = the issues planted by the generator, written before the run by a person (C21–C150 drafted with an AI assistant and **still to be reviewed by both members**). C01–C50 are development data (seen when fixing the detector); **C51–C100 were run once, unseen** [R §7] (before the fix) and **C101–C150 were run once, unseen, after the fix** — the result of record [R §8]. All 150 are now development data: a new frozen set (`eval_set_v3`) is needed for the next measurement.
- **Golden set:** `evals/golden_30.csv` — 30 real prototype drafts, including 2 on hand-over tickets, 6 with names in the reviews, frozen.
- **Grading guideline:** `evals/README.md`, five binary criteria with boundary examples, written before grading. **Human–human agreement on the 30: *not measured yet*** (Ugo and Enzo must grade independently, then `python evals/agreement.py`).
- **Judge:** a model (to choose — any assistant) with `evals/judge_prompt.txt`, which copies the guideline. **Human–judge agreement on the same 30: *not measured yet*.** The drafter is a template, not an LLM, so the usual same-family bias does not apply today; it will if an LLM drafter is added.
- **Cadence:** eval-set + judge on every change to the prototype; a weekly human sample of 5 % of sent drafts once live.
- **Known weaknesses of this plan:** (1) the labels come from the generator, so the drafter's lexicon and the labels share a vocabulary; real reviews will be harder; (2) 28 in-scope cases give about ±17 points (Wilson 30–64 % around 46 %); (3) the proxy checks themes and quarters, not wording, so the humans' number may be lower than the proxy; (4) 20 of 30 golden drafts repeat a quote — the guideline will fail them, which is the drafter's miss (spec v2).
- *Optional, not done:* red team (`adversarial_v0.csv`) and promptfoo assertions.

**Bands are decisions, not measurements:** the ± 2 percentage points of §4 and the 15 points of §3 are our choices, to be confirmed with the Head of Customer Success; they are not in `02_sizing.xlsx`.

## What this file does *not* claim
Not claimed: that any proxy number is the share of drafts that two people would send, that the 75 % flip point is reached, or that a draft can ship. The honest message for the oral: *we found the safety hole, closed it, and measured on cases we had not seen: safe on 22 hand-overs, but only 46 % of the requests we should answer get a draft. The number that decides — two graders and minutes saved — is still to come.*

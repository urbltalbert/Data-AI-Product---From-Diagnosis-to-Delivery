# 08 — Launch memo · Team 7 · Review Insights (P8) · v1.0 candidate

> Sources: **[S]** `02_sizing.xlsx` · **[M]** `02_investment_memo.md` · **[B]** `03_product_brief.md` · **[05]** `05_metrics.md` · **[06]** `06_07_experiments_operations.md` · **[R]** `evals/report_v0.md` · **[T]** `evals/rollback_test_2026-11-20_1142.txt`. A number with no tag is arithmetic, a *decision*, or marked *not measured*.

## Decision (line one)
**Do not launch to account managers. Launch shadow mode only** — the system reads real incoming tickets, two people grade the drafts, **no account manager sees a draft and nothing reaches a hotel.** The investment decision of the memo stays what it was: **CONDITIONAL GO on ≥ 75 % of handling time saved**; at the 60 % base case it is a NO-GO **[M]**. Nothing measured so far tells us whether 75 % is reachable.

## What we built and what we measured
A rule + classical-ML pipeline (detect → eligibility rules → extract → themes → template draft → policy check; the person sends) with a three-position kill switch (`on` / `suggest_only` / `off`; unknown value = `off`) **[T]**. The drafter is a template, not an LLM. Everything was tested on **invented** data (200 hotels, 35,715 reviews, 200 cases); no real ticket and no real guest was used.

| Question | Result | Source |
|---|---|---|
| Does it ever draft on a ticket a person must handle? | **broken in 3 of 4 runs on unseen cases** (C07 invoice, C100 fake review, C188 "our other property in Lyon"), each a different kind of ticket; 0 / 22 once; **1 / 20 on the last run** (interval 1–24 %) | [R §6–9] |
| Does it answer the requests it should? | **22 / 30 = 73 %** on the last unseen set (95 % interval 56–86 %); 13 / 28 = 46 % and 24 / 30 = 80 % on the two before | [R §7–9] |
| Is the draft right? | on drafts produced, the automatic proxy (≥ 2 of 3 themes + both quarters) is a proxy, not a person | [R §7] |
| Guest name or another hotel's data in a draft? | 0 / 22 on the last run | [R §9] |
| Does the rollback work? | 7 / 7, run once by one person on one laptop, 20 Nov 2026 11:42 CET | [T] |
| Two humans agree on "sendable"? Judge agrees with them? | **not measured** | [05 §5], `evals/README.md` |
| Minutes saved per request? | **not measured** (45 min today is a guess **[S, B]**) | [06] |

**Honest reading:** we found a safety hole, closed it, and measured on cases we had not seen, twice. Each fix closed one family of misses and the next unseen set opened another: after the first fix the system was safe but served 46 % of in-scope tickets; after the second round of changes it serves 73 % (interval 56–86 %, around the 75 % criterion) but a ticket about "our other property in Lyon" got a draft. A measurement on 20–30 cases cannot tell us the floor is solid.

## Why not launch to Claire now
1. **The floor was broken three times in four unseen runs** (an invoice ticket, a "remove this review" ticket, a ticket about another property) and held once. Hand-written rules and a small classifier do not close it; the fixes are patches on the cases we saw.
2. **The number that decides does not exist:** two graders, human-judge agreement and minutes per request are all unmeasured.
3. **The test data is ours.** Labels come from the generator that wrote the reviews; real reviews will be harder.
4. **Recall is 46–73 % on two unseen sets**, around or below the 75 % criterion **[B §7]**, with intervals of ±15 points.

## Why shadow mode is worth doing
It is the only step that produces the missing numbers (hand-over floor and two-grader share on real tickets) **without exposing a user**. The cost is grading time by two people; it was **not priced separately** (the sizing carries an evaluation line of €15k/year in the base case **[S]**, which may or may not cover it). If the answer is bad, we stop having spent grading time, not hotel trust.

## Conditions to move from shadow mode to the A/B (the gates of [06 §2])
1. The floor holds on a **new frozen set** (`eval_set_v4`, to write, after a rule for "other / sister property" wording) and on the first real shadow tickets: zero drafts on hand-over tickets.
2. Served share of in-scope tickets is **at least 75 % with an interval that does not cross below it** (73 %, 56–86 % today): more varied labelled tickets with consent, or an LLM classifier behind the same rules; an LLM drafter would need its own run.
3. Two humans have graded `evals/golden_30.csv`, the agreement is in `evals/README.md`, and the judge agreement is known.
4. The DPO has read [06] and the data-handling line of `governance.md`.
5. The rollback drill is re-run by a **second** person (the Head of CS role), not by the author.

Then: A/B on **15 vs 15 account managers**, 4 weeks plus a 2-week tail, read at week 6 with the decision rule written before the first unit (ship / iterate / kill) **[06 §2]**.

## What would make us stop
- **Kill** if time saved stays ≤ 30 % after one iteration (net value ≈ −€6k **[S]**), or if the floor fails twice **[06 §2]**.
- **Switch off immediately** (`off`) on a draft that shows another hotel's data or a guest name, or more than 2 hotel complaints about an inaccurate diagnosis in a calendar month **[05 §3, governance]**.
- **Re-open the decision** if a vendor ships this analysis inside our ticketing tool with a compliant DPA **[M §5]**.

## Owners
| Decision | Role |
|---|---|
| Sign an experiment on real users | Head of Customer Success; the DPO reads it |
| Press the switch | Head of Customer Success; on-call engineer at night |
| Approve a release (detector, lexicon, model, threshold) | Head of Product, with the eval-set re-run attached |
| Keep the trace, answer a hotel or a regulator | Engineering keeps the logs; the DPO answers |
| Read the weekly numbers and act | Head of Product |

## Known limits of this memo
- Every in-scope number is on synthetic data and on **one** run per set; 28 in-scope cases give ±17 points.
- All 200 cases are now development data; the next measurement needs a new frozen set.
- C21–C200 labels were drafted with an AI assistant before the runs and **still need review by both team members**.
- The base-case hand-over and error rates are guesses of the sizing **[S]**.
- Mixed tickets (rating drop + account question) are handed over today; whether a person should receive a draft anyway is a Head of CS decision.

## What we ask the investor for at the oral
Not a go-live: **permission to run shadow mode**, then, if the gates above pass, **the 6-week A/B** (4 weeks + 2-week tail) with the decision at its week-6 read on the rule above. The shadow-mode duration is not set yet (*decision to take with the Head of CS*).

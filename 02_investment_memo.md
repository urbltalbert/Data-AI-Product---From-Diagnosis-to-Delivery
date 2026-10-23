# 02 — Investment memo (one page)

**Recommendation:** CONDITIONAL GO on ≥ 75 % of handling time saved on 200 requests in the S4 prototype. At our base case (60 %), it is a NO-GO.

> Line one is the decision. Everything below is evidence for that line. Same base case as `02_sizing.xlsx`.

| €/year, year 1 | Pessimistic | Base | Optimistic | Expected value |
|---|---|---|---|---|
| Net annual value | −112k | 56k | 300k | **55k** |
| Probability | 0.3 | 0.5 | 0.2 | — |
| Do-nothing (value of the current process improving on its own) | 72k | 86k | 84k | |
| Next-best project: help-centre search for how-to tickets (the hurdle) | 90k | 70k | 50k | |

## 1. How much?
1,200 rating-drop requests a month. 80 % come from hotels with enough reviews (≥ 50 a quarter). The agent can help with 90 % of those, and saves 60 % of the 45 minutes. With the adoption ramp, that is ~3,600 requests' worth of time in year 1, or €143k gross. Net of errors, tokens and fixed costs: **€56k**.
**Measured:** 20 % of tickets are analysis requests, answered in 4 days (P8 brief). **Analogy:** €65k loaded cost of an account manager. **The guess that matters:** 60 % of handling time saved.

## 2. How sure?
Pessimistic −€112k (p 0.3), base €56k (p 0.5), optimistic €300k (p 0.2): **EV €55k**.
**Flip point:** time saved on in-scope requests. Below ~67 %, the help-centre project wins. At ~75 %, we also beat do-nothing.
**S4 test:** 200 requests rebuilt from `reviews.csv`, timed with and without the draft (hypothesis 3: 45 → 10 min, i.e. 78 %).

## 3. What if we're wrong?
The model is not the cost: tokens are €0.4k a year. Supervision (€20k), errors (€18k), integration (€15k) and evaluation (€15k) dominate. The decision does not depend on the token price.
**Cost of error:** 5 % wrong top issues × €100 = €18k a year (€20k in the pessimistic case).
**Governance line:** a wrong top issue sent to a hotel is a reputational risk; a guest's name quoted in a summary is a legal (GDPR) risk. Owners: Head of Customer Success and DPO (`governance.md`).

## 4. Compared to what?
**Do-nothing:** account managers 10 % faster, a sub-score chart, +10 % hotels → ~€86k a year of improvement on its own. Hotels still wait days.
**Next-best project:** help-centre search for how-to tickets, ~€70k a year.
**Pessimistic case:** −€112k. It does not clear the hurdle (€90k).

## 5. Build, buy or orchestrate?
**We orchestrate because** no product analyses a hotel's reviews inside our ticket and approval flow, and we have no ML team to build one. Weighted scores from the `Build or buy` tab: Build 2.75 · Buy 2.50 · Orchestrate 3.70. Per-resolution fees would cost less (~€3k vs ~€39k a year). **What would change our mind:** a vendor shipping this analysis inside our ticketing tool, with a GDPR-compliant DPA.

*Sources: P8 brief (project document) · `01_problem_statement.md` · Anthropic API pricing, checked 23 Oct 2026 · Session 2 slides · Intercom Fin pricing ($0.99 per resolution, 2025).*

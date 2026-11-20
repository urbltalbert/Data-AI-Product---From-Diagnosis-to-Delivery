# product_brief.md — Review Insights · FINAL (v3) · Team 7 · P8

**Versions:** v1 — 16 Oct 2026 · v2 — 6 Nov (`03_product_brief.md`, kept for history) · **v3 final — 20 Nov 2026, after the prototype, the evals, and the experiment and operation plans.** What changed since v2 is in §9; the launch decision is in `08_launch_memo.md`.

## 1. Problem, user, do-nothing  *(from 01)*
- **Problem:** account managers spend ~45 min on each of ~1,200 monthly "why did my rating drop?" requests (~900 h/month, ~€430k/year); hotels wait 4 days **[S, B v2]**. The 45 min is a guess, not yet timed.
- **User:** Claire, an account manager overseeing ~100 hotels. Goal: answer within 24 h with a verifiable explanation. Pain: reading 100–300 reviews per request.
- **Do-nothing:** ~760 h/month at 12 months (~€360k/year), delays unchanged **[B v2]**.

## 2. The agent in one sentence, and its trust level
When a hotel asks why its rating dropped, the agent prepares a one-page draft for Claire — top 3 negative themes, change versus last quarter, quotes she can click — and **never sends anything**. Trust level **L2** (drafts, a person approves); detection is L3 (a person samples); sending is a person only.

## 3. The process — as built
| # | Step | What runs | Trust | Way back to a person |
|---|---|---|---|---|
| 1 | detect the request | TF-IDF + logistic regression, threshold 0.60 chosen on validation tickets | L3 | confidence below 0.60 → normal queue, reason shown |
| 2 | eligibility | rules: ≥ 50 reviews in the quarter, English, one hotel, not a WON'T intent, not an account matter | L4 | any failed rule → hand-over with its specific reason |
| 3 | extract | rules: two quarters, one `hotel_id` per call, names masked | L4 | unknown hotel → hand-over |
| 4 | themes | lexicon-based top 3 negative themes, counts, delta, 2 quotes each | L2 | — |
| 5 | draft | fixed template (no LLM) | L2 | Claire edits or clicks "write it myself" |
| 6 | policy check | rules: name, other `hotel_id`, promise | L2 | block → reason shown, no draft |
| 7 | send | — | **person only** | — |

A three-position switch (`on` · `suggest_only` · `off`; an unknown value counts as `off`; a step error falls back to humans only) sits in front of all of it — tested 7 / 7 on 20 Nov 2026 by the author only **[T]**.

## 4. Features — MoSCoW (unchanged from v2)
**MUST (3):** B quarter-over-quarter delta per theme · A top 3 negative themes with counts and 2 anonymised quotes · C ticket panel with approve / edit / write-myself and a timer (the feature that tests the 75 % flip point).
**WON'T (5):** D auto-send · E hotel portal · F operational recommendations · G public replies to reviews · H benchmark against peers. Non-English reviews and tickets are handed over. **Built in the prototype:** A and B in the drafter, the hand-over and policy rules. **Not built:** the C ticket panel (the demo is `03_prototype.html`).

## 5. Data
Production: hotel guest reviews. Eval data is **invented** — 150 hotels, 26,664 reviews, 150 eval cases (`data/make_data.py`, `data/cases_spec.py`), with three planted issues per hotel so the right top 3 is known in advance. No real ticket or guest is used. Guest names are masked; reads are isolated by `hotel_id`; two quarters only. GDPR: the hotel is controller, LobbyIQ processor (legitimate interest, Art. 6(1)(f)) — see `governance.md`. **Caveat:** the labels come from the generator, so real reviews will be harder.

## 6. Model — one rung per part, as built
| Part | Rung | Note |
|---|---|---|
| Request detection | 2 — classical ML | learns vocabulary, not intent; hands over unusual wording (recall 46 % of in-scope on unseen cases **[R §8]**) |
| Eligibility and account-matter rules | 1 — rules | the safety net that does not depend on the classifier (spec v3) |
| Quarter metrics, extraction | 1 — rules | exact aggregation |
| Theme extraction | **1 — lexicon** (v2 planned an LLM) | cheaper to test; an LLM extractor is the next step |
| Drafting | **1 — fixed template** (v2 planned template + LLM) | the template repeats a quote in some drafts (defect, spec v2) |
| Policy check | 1 — rules | regex and id assertions |

## 7. Success criterion
> On a frozen eval-set of unseen cases, **at least 75 % of in-scope requests** get a draft that two independent graders mark as sendable after minor edits only — **with zero drafts on hand-over tickets, zero guest names, zero other-hotel data.**

**Status on 20 Nov 2026: not verified.**
- Automatic proxy on unseen cases: **13 / 28 = 46 %** in scope served (30–64 %) **[R §8]**, versus 24 / 30 = 80 % before the safety fix **[R §7]**.
- Drafts on hand-over tickets: broken twice, **0 / 22** on the last run **[R §6–8]**.
- Names and other-hotel data: 0 / 13 **[R §8]**.
- Two-grader share: **not measured** — the grading guide, the golden set of 30 and the judge prompt exist (`evals/`), nobody has graded yet.

75 % is the handling-time flip point of the sizing **[S]**; the live minutes are measured in the A/B **[06]**.

## 8. Risks and rollback
- **Risks:** a wrong top issue reaches a hotel · a guest name or another hotel's data in a draft · Claire approves without reading · the detector hands over too much to help.
- **Rollback trigger (unchanged):** any draft that shows another hotel's data or a guest name, or more than 2 hotel complaints about an inaccurate diagnosis in a calendar month → switch `off` and return to the manual workflow. **Owner:** Head of Customer Success; on-call engineer at night; the DPO for the data case **[06 §4]**.
- **Plan:** shadow mode, then an A/B of 15 vs 15 account managers, 4 weeks + 2-week tail, decision rule written before the first unit **[06 §1–2]**.

## 9. What changed since v2
| Change | Evidence |
|---|---|
| Hand-over for account matters (invoice, login, review removal, product questions) no longer depends on the classifier | C07 and C100: drafts on hand-over tickets **[R §6–7]** |
| Theme extraction and drafting built at rung 1, not 3 and 4 | prototype `prototype/themes.py`, `prototype/draft.py` |
| Success criterion now names the frozen set, the proxy and the two-grader number separately | proxy 80 % while the floor was broken **[R §7]** |
| Experiment unit is the account manager, shadow mode first | `06_07_experiments_operations.md` §1 |
| User-research changes of v2 kept | `03_user_research.md` |

## 10. What we could not decide
- Minimum review volume to trigger a draft (50 today): Head of CS, after real data.
- Minimum negative mentions for a theme: account managers, first month of live use.
- **Mixed tickets** (rating drop + account question): handed over today; whether Claire should still get a draft is a Head of CS decision.
- Shadow-mode duration: to set with the Head of CS.
- Whether the detector should become an LLM classifier behind the same rules — a new frozen set decides.

*Sources: **[S]** `02_sizing.xlsx` · **[B v2]** `03_product_brief.md` · **[R]** `evals/report_v0.md` · **[06]** `06_07_experiments_operations.md` · **[T]** `evals/rollback_test_2026-11-20_1142.txt`.*

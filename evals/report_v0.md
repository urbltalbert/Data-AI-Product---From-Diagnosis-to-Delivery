# Eval report v0 — Team 7 · Review Insights (P8)

**Date:** 20 November 2026   **Eval-set:** `evals/eval_set_v0.csv`, 50 cases (33 in scope, 17 expected hand-overs)   **Prototype:** `/prototype`, 20 Nov 2026
**Raw output:** `evals/eval_output_v0.txt` (headline) · `evals/eval_output_v0_diagnostic.txt` (step 1 bypassed, diagnosis only)

## 1. The number against the criterion
| | Value |
|---|---|
| Success criterion (brief §7) | *"At least 75 % of in-scope inquiries produce a draft that two independent graders mark as sendable after minor edits only — with zero drafts containing a guest name or another hotel's data."* |
| Drafts produced (grounded + policy pass), in-scope cases | 0 / 33 = **0 %** |
| **Drafts two graders would send** | **0 / 33 = 0 %** (nothing to grade: no draft was produced) |
| Drafts on hand-over cases (must be 0) | 0 |
| Drafts with a guest name or another hotel's data (must be 0) | 0 (vacuous: no draft) |
| Policy blocks | 0 |
| Hand-over cases correctly escalated | 17 / 17 — but for the right reason in only 7 (10 got "low confidence" or "not a rating-drop request" instead of the true reason) |

**Verdict: criterion NOT met (0 % vs 75 %).** Safety held (no wrong draft); usefulness is zero.

## 2. The three most frequent misses
| # | What went wrong (one line) | Cases | Which component | What it becomes in `spec.md` v2 |
|---|---|---|---|---|
| 1 | The detector is under-confident: max confidence on an in-scope ticket is 0.69, so all 29 in-scope tickets it labels `rating_drop` fall under the 0.70 threshold and are handed over | 29 of 33 (C01, C02, C05, C08, C10 …) | Step 1 detect (`detect.py`, 69 training tickets) | Train on ≥ 300 tickets, and **set the threshold on a separate validation set**, never on the eval-set; evaluate the detector alone (recall on rating-drop) |
| 2 | The detector labels messy in-scope tickets as `other`: vague wording, typos, or a wrong cause suggested by the hotel | 4 of 33 (C03, C15, C27, C40) | Step 1 detect | Add these ticket styles to the *training* set as new invented tickets (not the eval tickets themselves); keep recall as a guardrail metric |
| 3 | Hand-over reasons are lost, and safety rests on the classifier alone: with step 1 bypassed, 8 hand-over cases would get a draft (C07, C09, C13, C20, C47, C48, C49, C50) | 8 of 17 in the diagnostic; 10 of 17 with a wrong reason in the real run | Step 2 rules (no own check for WON'T intents or for French tickets; the English test passes "a-t-elle" because it counts the word "a") | Add rule-based checks for the WON'T intents (benchmark, public reply, recommendations); replace the English heuristic by a language detector; keep the specific reason (few reviews, language…) ahead of the generic one |

**What works (diagnostic only, step 1 bypassed):** on the 33 in-scope cases steps 2–4 give the exact top 3 in the planted order 33/33, no name in any draft, no policy block. This is not a result: the theme lexicon was written knowing the generator's vocabulary, so synthetic data flatters it. The real test is a human-labelled sample of `reviews.csv`.

## 3. Who graded, and how
**Not yet done by humans.** The automatic proxy ("top 3 overlap ≥ 2 of 3, both quarters labelled, policy pass") is all this run reports, and it is 0 / 33 because no draft exists. `evals/grading_sheet_v0.csv` is empty for the same reason. Once the detector is fixed (spec v2), Ugo and Enzo grade the drafts independently, "would I send this with minor edits? yes/no", and write the disagreement count here.

## 4. What is demo data and what is eval data
- No threshold, prompt, lexicon or training ticket was changed after seeing eval results. The only edits after the first run were to the eval script itself (label parser, `--skip-detect` diagnostic flag); the parser was checked against the planted labels (0 mismatches).
- Training tickets (`data/tickets_train.csv`, 69) were written before the run; an exact-match check shows no overlap with an eval ticket.
- Labels: C01–C20 were written by Ugo and Enzo (Assignment 3). **C21–C50 were drafted with an AI assistant and must be reviewed by both team members** before this report counts as an eval of record. They were written before the prototype existed (`data/cases_spec.py`).
- Reviews are synthetic with planted themes (`data/make_data.py`, seed 7). Production data has no theme labels.

## 5. Next step
Fix the detector by the spec v2 lines above on a **new** frozen set (`eval_set_v1`, Assignment 5), because the 50 cases have now been looked at; rerun and have two humans grade the drafts.

---

## 6. After the spec v2 fixes — a DEVELOPMENT run, not a result (20 Nov 2026)
**Raw output:** `evals/eval_output_v0_after_spec_v2.txt` · grading sheet `evals/grading_sheet_v0.csv` is from this run.

What changed (all lines of `spec.md` v2): 300 training tickets and a separate 40-ticket validation set (`data/make_train.py`); confidence threshold chosen on the validation set (`prototype/tune_threshold.py`: precision 1.00 on rating-drop, recall 0.90 → **0.60**); rule-based hand-over for WON'T intents; specific hand-over reasons first; language by function words instead of "contains an English word".

| | Before (§1) | After |
|---|---|---|
| In-scope cases that got a draft | 0 / 33 | 30 / 33 |
| Top 3 overlap ≥ 2 of 3 (automatic proxy) | 0 / 33 | 30 / 33 = 91 % |
| **Drafts on hand-over cases (must be 0)** | 0 | **1 — C07** (invoice ticket, classifier says rating-drop at 0.64) |
| Drafts with a guest name or another hotel's data | 0 | 0 (30 drafts now exist, so the evidence is real) |
| Hand-over cases with the right reason | 7 / 17 | 16 / 17 (C48 and C49 get the more specific "out of scope" reason) |

**How to read it.**
- **The 91 % is not a result.** The fixes were designed after reading the misses of the first run, which cite eval cases. The 50 cases are now development data. The result of record needs a new frozen set (`eval_set_v1`, Assignment 5) and two human graders on the drafts — the automatic proxy only checks the top 3 and the quarter labels, not wording, quote relevance or tone.
- **C07 is an open safety miss and is deliberately not fixed here.** Lowering the threshold from 0.70 to 0.60 (chosen on validation, where it was safe) lets one non-rating-drop ticket through. Tuning it on C07 would make C07 demo data. Spec v2 gets one more line: *the detector must reach precision 1.00 on a larger validation set that includes billing / invoice tickets, and a draft on a hand-over ticket blocks the release.*
- The misses left are C03, C27 and C40: messy tickets still under the threshold or labelled `other` (miss 2 of §2, not solved).
- The synthetic-data caveat of §2 still holds: the theme lexicon knows the generator's vocabulary.

**Two draft defects seen when reading the 30 drafts (not fixed, for the graders and for spec v2):**
1. Duplicate quote: the same sentence is quoted twice under one theme (C12, "wifi is terrible"). Cause: the synthetic generator reuses four sentences per theme; real reviews will rarely repeat, but the drafter should de-duplicate identical quotes. Component: step 3 (`themes.py`).
2. Quote choice: the two quotes are the first two lowest-rated reviews sorted by `review_id`, not the most representative ones. In C31 the masking left "[name] at reception was the worst" in a staff-complaint quote: no name leaks, but a staff complaint about a named person still reaches a hotel and a person must judge it. Component: step 3.

**Next for the humans:** grade the 31 rows of `evals/grading_sheet_v0.csv` independently (Ugo and Enzo), and write the agreement here. Until then the number of record is the automatic proxy, and the criterion is *not* verified.

---

## 7. First run on FRESH cases — `eval_set_v1`, C51–C100 (20 Nov 2026)
**Raw output:** `evals/eval_output_v1_fresh.txt`. The 50 cases were written before this run (`data/cases_spec.py`), the prototype was **not changed** between §6 and this run, and each case was run once. This is the first measurement that is not development data.

| | Value |
|---|---|
| In-scope cases that got a draft | 24 / 30 |
| Top 3 overlap ≥ 2 of 3 (automatic proxy) | **24 / 30 = 80 %** — 95 % interval (Wilson) 63 %–90 % |
| Top 3 in exactly the planted order | 22 / 30 |
| **Drafts on hand-over cases (must be 0)** | **1 — C100** ("one of the reviews about our rating is fake, please remove it") |
| Drafts with a guest name or another hotel's data | 0 / 24 |
| Hand-over cases with the right reason | 17 / 20 (C93 and C94 escalate on "low confidence" — safe, wrong reason; C100 got a draft) |

**Verdict: criterion NOT verified.**
- 80 % is above 75 % on the proxy, but the interval reaches 63 %, the proxy is not the two-grader number, and **the floor is broken**: one draft on a hand-over ticket. C100 and C07 (§6) have the same cause: a support ticket that contains the words "rating" or "review" is classified `rating_drop` at 0.64–0.70 and passes the 0.60 threshold. The detector learns vocabulary, not intent.
- The 6 in-scope misses are all step 1: C56 (0.60, not above the threshold), C64, C71, C74 (0.55–0.58) and C58, C72 (labelled `other`): short or indirect wording ("We lost ground on guest satisfaction. Why?"). Two order swaps (C59, C63) pass the proxy but not an exact-order reading.
- Steps 2–4 held: right reason on 17/20, no name in 24 drafts, no policy block. The synthetic-data caveat of §2 still applies.

**Not fixed, on purpose:** these 50 cases are now development data too. Spec v2 gets the line: *a hand-over rule that does not depend on the classifier for tickets about invoices, login, review removal and other account matters, and a validation set of such tickets that contain "rating" / "review".* The next measurement needs a new frozen set (`eval_set_v2`) — which `05_metrics.md` §5 plans.

---

## 8. Fix of C07 / C100, then ONE run on 50 new cases — `eval_set_v2`, C101–C150 (20 Nov 2026)
**Raw output:** `evals/eval_output_v2_fresh.txt` · sheet `evals/grading_sheet_v2_fresh.csv`. Order of work: the 50 cases (28 in scope, 22 hand-overs) were written into `data/cases_spec.py` **before** the fix and before any run; then the fix; then the run, once; the cases were not read between the fix and the run.

**The fix (spec v3):** (1) `prototype/rules.py` gets `ACCOUNT`: a rule-based hand-over, independent of the classifier, for billing / contract, login / password / account, removal or dispute of a review, and product / technical questions (export, widget, API, PMS). (2) `data/make_train.py` adds 20 training and 10 validation support tickets that contain "rating" or "review"; the threshold is chosen again on validation: **0.60**, validation precision 1.00, recall 0.85 on the 50 validation tickets (`prototype/tune_threshold.py`). On the 100 development cases (`eval_output_v1_after_fix.txt`, development data, not a result): 51 / 63 drafts, 0 on hand-over cases, C07 and C100 now handed over.

| | Value |
|---|---|
| Hand-over cases that got a draft (must be 0) | **0 / 22** — interval (Wilson) 0 %–15 %: the floor held on this set, which does not prove it holds in production |
| In-scope cases that got a draft | **13 / 28 = 46 %** — interval (Wilson) 30 %–64 % |
| Decision correct (draft vs hand over) | 35 / 50 = 70 % |
| Drafts with a guest name or another hotel's data | 0 / 13 |
| Criterion "≥ 75 % sendable" on the proxy | **NOT verified** (46 %) |

**What went wrong, in one line:** the fix closed the safety hole by making the detector more cautious, and the price is recall. 15 in-scope tickets were handed over: **13 by the detector** (confidence 0.51–0.59, just under the 0.60 threshold, or label `other`; mostly **unusual wording** — "guest satisfaction fell. reasons?", "why the drop?", "Where are we losing points with guests?") and **2 by the new `ACCOUNT` rule**: C110 ("Rating dropped. Our invoice also seems wrong…") and C117 ("…Also I cannot find the export button"). These two are mixed tickets and their label ("in scope") is debatable; it was **not changed after the run** — a mixed ticket could reasonably go to a person.

**Reading:** safe but not useful enough. Handing over is the cheap error (a person does what is done today), a wrong draft is the expensive one, so this side of the trade-off is the right one for a first release — but 46 % of in-scope tickets served would not give the time saved the memo needs (≥ 75 % at the flip point). The detector learns vocabulary: a TF-IDF model trained on ~300 invented tickets cannot cover how real account managers write. Not fixed here: these 50 cases are now development data too. Options for the next iteration: more varied labelled tickets (real ones, with consent, in shadow mode), or an LLM classifier behind the same rules (rung 2 of the ladder in 04_architecture). The first option was done in §9 (`eval_set_v3`).

**Honest summary of the three runs on unseen cases:**

| Run | Cases | In scope → draft | Drafts on hand-over cases |
|---|---|---|---|
| §1 first run (threshold 0.70) | C01–C50 | 0 / 33 | 0 / 17 |
| §7 fresh, after spec v2 | C51–C100 | 24 / 30 = 80 % | **1 / 20 (C100)** |
| §8 fresh, after spec v3 | C101–C150 | 13 / 28 = 46 % | 0 / 22 |

The system can be made safe or useful on this synthetic data; it is not yet both at once, and no number here comes from real tickets or two human graders.


---

## 9. Spec v4 — more varied training tickets, then ONE run on 50 new cases — `eval_set_v3`, C151–C200 (20 Nov 2026)
**Raw output:** `evals/eval_output_v3_fresh.txt` · sheet `evals/grading_sheet_v3_fresh.csv`. The 50 cases (30 in scope, 20 hand-overs) were written into `data/cases_spec.py` **before** any change and any run; the changes below were made after the §8 result and **without copying any eval ticket** (checked: no exact copy of a C01–C200 ticket in the new training or validation tickets, none above 0.8 string similarity). Run once.

**What changed (spec v4), because §8 showed recall 46 %:**
1. `data/make_train.py`: +70 training tickets with varied wording of a rating-drop request (`POS_VARIED`) and +20 validation tickets (10 per class group). Train 220 / 150, validation 30 / 30.
2. The threshold is chosen again on validation by the same rule (lowest threshold with precision 1.00): **0.70** (validation recall 0.87). It went up from 0.60 because the new, more varied validation tickets contain two non-rating-drop tickets that the classifier calls `rating_drop` at 0.56–0.57 (an invoice ticket, a PMS ticket). The threshold followed the validation set, not the eval-set.
3. `prototype/themes.py`: two quotes under a theme are now two **different** sentences, and a quote that contains a masked name is used only if no other exists (defect 1–2 of spec v2).
4. `data/make_data.py`: Spanish added to the foreign-language reviews (a bug: C184 needed it); the first 35,716 lines of the reviews file are unchanged, and `eval_set_v0/v1/v2` are byte-identical.
5. **Policy decision, written before the run:** a *mixed* ticket (rating drop + account question) is a hand-over (C198, C199 are labelled so). It is a decision, not a measurement.

| | Value |
|---|---|
| In-scope cases that got a draft | **22 / 30 = 73 %** — interval (Wilson) 56–86 % |
| **Drafts on hand-over cases (must be 0)** | **1 / 20 — C188** ("Please also check why our other property in Lyon lost points.") — interval 1–24 % |
| Drafts with a guest name or another hotel's data | 0 / 22 |
| Decision correct (draft vs hand over) | 41 / 50 = 82 % |
| Criterion "≥ 75 % sendable" on the proxy | **NOT verified** (73 %, interval 56–86 %) |

**Verdict: the floor is broken again.** C188 asks about *another* property of the sender without writing a hotel id; the classifier says `rating_drop` at 0.71 (just above 0.70) and no rule catches "our other property / our sister hotel in <city>". It is the same family as C140 (§8, "Paris and Marseille hotels"), which a generic word rule did not catch either: C140 was handed over thanks to confidence, not to a rule. **Not fixed here, on purpose** (the case is now development data, and editing the rule after seeing it would make C188 demo data). The fix to write in the spec: *a rule for "other / second / sister / our … in <city>" property wording, plus tickets of that kind in training and validation, measured on a new frozen set.*

**Reading.** Recall moved from 46 % to 73 % on two different fresh sets (28 and 30 in-scope cases; the intervals overlap, 30–64 % and 56–86 %, so do not read 27 points as a measured gain), and the floor broke again on a *different* kind of ticket than C07 and C100. Each fix closes one family of misses; the next set opens another. This is what the data says about a classifier trained on ~370 invented tickets, and about a hand-written rule list: **neither is a guarantee on real tickets**. On the development cases the same code gives 0 drafts on hand-over cases (C01–C100: 53 / 63 served; C101–C150: 17 / 28 served) — those are not results, the cases were seen.

**Honest summary of the four runs on unseen cases:**

| Run | Cases | In scope → draft | Drafts on hand-over cases |
|---|---|---|---|
| §1 first run (threshold 0.70) | C01–C50 | 0 / 33 | 0 / 17 |
| §7 after spec v2 | C51–C100 | 24 / 30 = 80 % | **1 / 20 (C100)** |
| §8 after spec v3 | C101–C150 | 13 / 28 = 46 % | 0 / 22 |
| §9 after spec v4 | C151–C200 | 22 / 30 = 73 % | **1 / 20 (C188)** |

The safety floor held in two of four runs, and broke on a new kind of ticket each time it broke. The conclusion for the launch is unchanged and stronger: **no release; shadow mode with a human reading every draft before anything is shown, and the floor measured on real tickets.**

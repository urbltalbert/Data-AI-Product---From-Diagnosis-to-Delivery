# spec.md — executable spec · Review Insights · v3 FINAL (20 Nov 2026 — after eval §8)

## problem
Account managers spend ~45 min (a guess, not yet timed) on each of ~1,200 monthly "why did my rating drop?" requests (~900 h a month); hotels wait 4 days. The agent prepares a one-page draft (top 3 negative themes, change vs last quarter, quotes) that the account manager approves and sends. **It never sends anything.**

## user_workflow
```
- switch    : prototype/switch.txt                -> on | suggest_only | off (unknown = off)            (Head of CS)
- detect    : ticket text                         -> rating_drop | other, confidence                   (L3 — Claire samples)
- eligible  : hotel_id, ticket, review counts     -> ok | hand_over(reason)                            (L4 — rules)
              rules, in order: other hotel id · ticket language · WON'T intent · account matter ·
              label · confidence >= 0.70 · unknown hotel · reviews mostly not English · < 50 reviews in Q3
- extract   : hotel_id + two quarters             -> reviews[] (English, names masked, one hotel_id per call)  (L4 — rules)
- themes    : reviews[]                           -> top 3 negative themes, counts, delta, 2 quotes each        (L2)
- draft     : themes + template                   -> draft with both quarters and review ids                    (L2 — Claire approves)
- check     : draft                               -> policy pass | block                                        (L2)
- send      : draft                               -> hotel                                                      (person only)
```
Any step error falls back to "humans only" (`serve_ticket`).

## io_contracts
```
ticket : {id, hotel_id, text, language}
draft  : {text, quarters{current, previous}, themes[{name, count_current, count_previous, quotes[{review_id, span}]}], policy: pass|block}
```

## edge_cases
- fewer than 50 reviews in the quarter -> no draft, hand over to Claire
- reviews mostly not in English -> no draft, hand over
- ticket not in English -> no draft, hand over
- ticket is not about a rating drop (billing, login, review removal, export, widget, API) -> no draft, normal ticket queue
- ticket asks for a reply to a review, a benchmark against other hotels, or advice -> no draft, hand over
- ticket asks about several hotels or another hotel -> no draft, hand over
- ticket mixes a rating drop with an account question -> no draft today (decision for the Head of CS)
- guest or staff name in a review -> masked before drafting

## fallbacks
- detection confidence below 0.70 (chosen on validation tickets, spec v4) -> hand over to Claire, with the reason shown
- policy block (name, other hotel_id, promise) -> show the reason, no draft
- switch `off` or unknown -> manual workflow; `suggest_only` -> draft shown, no action
- Claire can always click "write it myself"

## done_criteria
- on a frozen set of unseen cases, >= 75 % of in-scope requests get a draft that two graders mark as sendable after minor edits
- **zero drafts on hand-over tickets, zero guest names, zero other-hotel data** (any miss blocks the release)
- **Status 20 Nov 2026: not met.** Proxy on unseen cases 22 / 30 = 73 % served (report §9; 46 % on the set before); floor broken in 3 of 4 unseen runs (C07, C100, C188) and held 0 / 22 once; two-grader share not measured.

## out_of_scope
D. auto-send to the hotel · E. self-serve portal for hotels · F. operational recommendations · G. public replies to reviews · H. benchmark against local peers · non-English reviews.

## eval_set
`evals/eval_set_v3.csv` — 200 cases (C01-C50 development; C51-C100, C101-C150 and C151-C200 each run once, unseen, in report §7, §8 and §9). All are now development data; `eval_set_v4` is to be written before the next measurement. Golden set: `evals/golden_30.csv`. Reports: `evals/report_v0.md` §1-§9.

## rollback
Trigger: any draft that shows another hotel's data or a guest name, or more than 2 hotel complaints about an inaccurate diagnosis in a calendar month. Action: `off`. Owner: Head of Customer Success; on-call engineer at night. Drill: `prototype/test_switch.py`, 7 / 7 on 20 Nov 2026 (one person; to be re-run by a second).


---
## v2 — what changed since the skeleton (every miss of `evals/report_v0.md` is a line)
- **[NEW] detect:** train on ≥ 300 invented tickets; choose the confidence threshold on a separate validation set, never on the eval-set. Report recall on rating-drop tickets alone. *(miss 1: 0 / 29 above 0.70)*
- **[NEW] detect:** add vague, typo-laden and "wrong cause suggested" ticket styles to the training set (new tickets, not the eval ones). *(miss 2: C03, C15, C27, C40 labelled `other`)*
- **[NEW] eligible:** rule-based hand-over for WON'T intents (benchmark vs peers, public reply to a review, operational recommendations), independent of the classifier. *(miss 3: C07, C09, C13, C47–C50 would get a draft)*
- **[CHANGED] eligible:** language check by a language detector, not by counting English words. *(miss 3: French C20 passed, Italian C43 only by luck)*
- **[CHANGED] eligible:** return the specific hand-over reason first (few reviews, language, several hotels) before the generic "low confidence" or "not a rating-drop". *(miss 3: 10 of 17 reasons wrong)*
- **[CHANGED] done_criteria:** the date is "by 22 November, on the eval-set after v2 fixes"; the report must separate the *automatic proxy* from the *two-grader* number.
- **[DONE 20 Nov, see report §6]** the first five lines above are implemented (300 train + 40 validation tickets, threshold 0.60 chosen on validation, WON'T rules, specific reasons first, function-word language check). Result: 30 / 33 on the proxy — a development number, the eval-set has been seen.
- **[NEW] detect / release gate:** precision 1.00 on `rating_drop` must hold on a larger validation set that includes billing and invoice tickets; **a draft on a hand-over ticket blocks the release** (C07 and C100 closed by spec v3 — held 0 / 22 on C101–C150, report §8 — but one clean run does not release anything).
- **[NEW] themes:** de-duplicate identical quotes inside a theme; pick the two most representative negative quotes, not the first two by id; a quote that is about a named person is flagged for the account manager. *(report §6, defects 1-2)*
- **[NEW] detect / eligible (report §7, C100 and C07):** a rule-based hand-over for account matters (invoice, login, password, remove or delete a review, subscription, contract) that does not depend on the classifier; add support tickets that contain the words "rating" and "review" to the training and validation sets; **[DONE 20 Nov, spec v3, report §8]**: `ACCOUNT` rules in `prototype/rules.py`, 30 more support tickets in `data/make_train.py`, threshold 0.60 re-chosen on validation. Measured once on 50 unseen cases (C101–C150): **0 / 22 drafts on hand-over cases, 13 / 28 = 46 % in-scope served** — safe, but below the 75 % criterion.
- **[KEPT]** zero drafts with a guest name or another hotel's data (held at v0: no draft was produced, so the evidence is weak — re-check once drafts exist).
- **[OPEN]** C21–C50 labels must be reviewed by both team members.
- **[NEW] switch (S7):** `prototype/switch.py` — three positions (on · suggest-only · off), read on every call, unknown value fails safe to off; `serve_ticket` falls back to humans-only on any step error. Tested by `prototype/test_switch.py`, 7 / 7 on 20 Nov 2026.
- **[NEW] detect / recall (report §8):** the TF-IDF detector hands over unusual wording ("why the drop?", "where are we losing points") at confidence 0.51–0.59. Next step: more varied labelled tickets (real ones, with consent, in shadow mode) or an LLM classifier behind the same rules; measure on a new frozen set (`eval_set_v3`). Mixed tickets (rating drop + account question) are handed over today; the policy for them is a decision for the Head of CS.
- **[DONE 20 Nov, spec v4, report §9]** 70 more varied rating-drop training tickets and 20 validation tickets (none copied from an eval case), threshold re-chosen on validation: **0.70**; two quotes under a theme are two different sentences, masked names only as a last resort. Measured once on C151-C200: **22 / 30 = 73 % served, 1 / 20 drafts on a hand-over case (C188)**.
- **[NEW] eligible / other property (report §9, C188):** rule-based hand-over for wording that points to another property of the sender without an id ("our other property in <city>", "our sister hotel", "our second hotel"); tickets of that kind in training and validation; measure on `eval_set_v4`. **Not done yet.**
- **[DECISION]** a mixed ticket (rating drop + account question) is a hand-over (C198, C199).

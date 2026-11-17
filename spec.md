# spec.md — executable spec · Review Insights · skeleton v0

## problem
Account managers spend ~45 min on each of ~1,200 monthly "why did my rating drop?" requests (~900 h a month); hotels wait 4 days. The agent prepares a one-page draft (top 3 negative themes, change vs last quarter, quotes) that the account manager approves and sends.

## user_workflow
```
- detect    : ticket text                         -> rating_drop | other, confidence    (L3 — Claire samples)
- eligible  : hotel_id + review counts            -> ok | hand_over(reason)             (L4 — rules)
- extract   : hotel_id + two quarters             -> reviews[] (English, names masked)  (L4 — rules)
- themes    : reviews[]                           -> top 3 negative themes, counts, delta, 2 quotes each  (L2)
- draft     : themes + template                   -> email draft with both quarters and linked quotes     (L2 — Claire approves)
- check     : draft                               -> policy pass | block                (L2)
- send      : draft                               -> hotel                              (person only)
```

## io_contracts
```
ticket : {id, hotel_id, text, language}
draft  : {text, quarters{current, previous}, themes[{name, count_current, count_previous, quotes[{review_id, span}]}], policy: pass|block}
```

## edge_cases
- fewer than 50 reviews in the quarter → no draft, hand over to Claire
- reviews mostly not in English → no draft, hand over
- ticket is not about a rating drop → no draft, normal ticket queue
- ticket asks about several hotels or another hotel → no draft, hand over
- guest or staff name in a review → masked before drafting

## fallbacks
- detection confidence below [0.7] → hand over to Claire, with the reason shown
- policy block (name, other hotel_id, promise) → show the reason, no draft
- Claire can always click "write it myself"

## done_criteria
- by 15 November, on the 50-case eval-set, ≥ 75 % of in-scope requests get a draft two graders mark as sendable after minor edits
- zero drafts with a guest name or another hotel's data

## out_of_scope
D. auto-send to the hotel · E. self-serve portal for hotels · F. operational recommendations · G. public replies to reviews · H. benchmark against local peers · non-English reviews.

## eval_set
`evals/eval_set_v0.csv` — 20 cases now, 50 with Assignment 4.

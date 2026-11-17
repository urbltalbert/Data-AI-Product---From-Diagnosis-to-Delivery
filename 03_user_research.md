# 03 — User research · Review Insights

> Three 20-minute discovery conversations plus one think-aloud usability test with two participants.
> Mom Test protocol: focused on past incidents, zero pitching, no hypothetical "would you use…?" questions.

## Who we talked to
| # | Who (role, company type — no personal data) | Real user or classmate in role? | Date | Interviewer · note-taker |
|---|---|---|---|---|
| 1 | General manager, 3-star urban hotel (60 rooms) | classmate in role | 4 Nov 2026 | Ugo · Enzo |
| 2 | Customer success manager, B2B SaaS (~90 accounts) | classmate in role | 5 Nov 2026 | Enzo · Ugo |
| 3 | Front-office manager, 4-star leisure hotel | classmate in role | 5 Nov 2026 | Ugo · Enzo |

## Interview guide
For hotel operators:
1. Walk me through the last time your review score dropped. What happened step by step?
2. How did you diagnose the cause, what did you read, and how long did it take?
3. Who did you contact for support, and what information did they send back?
4. What operational fix did you implement afterwards, and how did you validate it?

For account managers / CSMs:
1. Walk me through the last time a client asked why their metrics declined. How did you handle it?
2. How much time did it take, and where was the main bottleneck?
3. What did you include in your reply, and did the client follow up with additional questions?

## What we heard (facts, in their words)
| # | Quote or observed behaviour | Which part of our brief it confirms or contradicts |
|---|---|---|
| 1 | "When our score slipped from 8.4 to 8.1 in March, I spent about an hour on Sunday night reading through the last 40 reviews." | confirms steps 3–4 are the primary time sink |
| 1 | "I skip the positive reviews completely — good feedback doesn't tell me why the score fell." | contradicts equal weighting of all reviews → restrict theme counts to negative mentions |
| 1 | "The booking platform only gave me a trend chart; I still had to dig into the text to understand why." | confirms existing score charts (do-nothing baseline) do not answer the "why" |
| 2 | "That analysis ate up most of a morning because I had to copy-paste review excerpts into a document so the client would trust the conclusion." | confirms including verbatim supporting quotes (Feature A) |
| 2 | "Clients immediately reply asking what time window those figures are compared against." | confirms showing quarter-over-quarter changes clearly (Feature B) |
| 2 | "I won't send a stat I can't audit myself — if I can't click through to the source review, I end up redoing the check." | new requirement: link each quote directly to its full review |
| 3 | "Reviewers frequently mention front-desk staff by name, which we can never pass along unedited to ownership." | confirms strict name redaction before drafting (governance) |
| 3 | "During summer, nearly half of our guest feedback comes in German or Italian." | confirms non-English volume is material → keep out of scope and route to human |

## Usability test — one task, think aloud, don't help
**Prototype link:** see `03_prototype_link.md` · **Task given:** "Hotel Le Cèdre asked why its rating dropped. Review the generated draft and decide whether to send it."
| Tester | Finished without help? | Where they hesitated | What they expected instead |
|---|---|---|---|
| 2 (CSM) | yes, ~4 min | paused at the summary metrics to check which baseline quarter was being compared | explicit labels for both quarters at the top of the draft |
| 3 (front office) | yes, ~6 min | clicked on one of the quoted excerpts expecting a pop-up or link, with no response | direct click-through to the complete source review |

## Desirability gate
- [x] 2 of 2 completed the usability task unassisted
- [x] Participants shared concrete past workflows rather than hypothetical opinions
- [ ] At least one participant stated "I want this before…"
- [x] Out-of-scope boundaries became clearer while the core success criterion held steady

**Decision:** Proceed to Session 4 prototype build and incorporate both usability fixes (explicit comparison quarters in the header and clickable links to full source reviews) into product brief v2.
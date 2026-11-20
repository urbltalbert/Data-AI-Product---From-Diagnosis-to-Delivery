# evals/ — how we grade, and how far we trust the judge

## Files
| File | What it is |
|---|---|
| `eval_set_v0.csv` | 50 cases (C01–C50). Development data since 20 Nov: they were looked at to fix the detector. |
| `eval_set_v2.csv` | 150 cases = v1 + **50 fresh cases C101–C150**, written before the C07 / C100 fix and run once after it (`report_v0.md` §8). Same format, tagged `fresh in v2`. |
| `eval_set_v1.csv` | 100 cases = the same 50 + **50 fresh cases C51–C100**, written before the run. Synthetic inputs, tagged in the `origin` column. Labels = what the generator plants (`data/cases_spec.py`), written by a person before any run. |
| `report_v0.md` | the numbers: §1 first run, §6 after fixes, §7 first run on the fresh cases |
| `golden_30.csv` / `golden_30.md` | **the golden set**: 30 prototype drafts, frozen, graded by both humans and by the judge |
| `judge_prompt.txt` | the judge prompt, written from the guideline below |
| `agreement.py` | computes both agreement rates from the filled files |
| `grade.py` | grading helper: one draft at a time, the five criteria as y/n, per grader; `--merge` fills `golden_30.csv` after both are done. It never shows the other grader's answers. |

Strata of `eval_set_v1.csv` (from the Session 3 audit): in scope 63 / hand-over 37; hand-over reasons: < 50 reviews, reviews not in English, ticket not in English, several hotels, not a rating-drop request; hotel stars (2–4) and type (urban, leisure, business, small, chain). **Gap to state:** the stars-and-type mix is ours, not LobbyIQ's; the only language beyond English in the tickets are French, German, Italian and Spanish.

## Grading guideline — "sendable after minor edits" (written BEFORE anyone grades)
A draft is **SENDABLE** only if all five criteria are YES. "Minor edits" = at most a few words changed, nothing restructured, nothing looked up.

| # | Criterion | YES means | FAIL boundary example |
|---|---|---|---|
| 1 | **Right top 3** | at least 2 of the 3 themes are in the reference top 3 | themes are plausible but only 1 of 3 is in the reference → NO |
| 2 | **Evidence is real and varied** | each quote is a complete negative review of that hotel, relevant to its theme, and the two quotes under a theme are different | the same sentence quoted twice under one theme → NO (a person would have to look for a second one) |
| 3 | **Both quarters are visible** | the comparison names both quarters and gives a count for each | counts without the quarter named → NO |
| 4 | **No personal data, no other hotel** | no guest name, no staff name, no other hotel_id or review id | any name, even masked as "[name] at reception" next to a complaint about a person → NO (a person must judge it) |
| 5 | **Tone and promise** | neutral, B2B, no blame on a person, no promise ("we will fix"), no recommendation of what to change | "you should renovate the lobby" → NO (recommendations are WON'T) |

**Hand-over rows (the reference column says "no draft should exist"):** the correct answer is **NO** (not sendable) — a draft exists where a person should have answered. Grade them like any other; they test the floor.
**Escalate rows:** there is no draft, so there is nothing to grade. They are scored by the script (right decision, right reason), not by humans.

## How agreement is measured
1. Ugo and Enzo grade `evals/golden_30.csv` **independently**, each in their own column (`grader_1…`, `grader_2…`), yes/no, one-line comment if NO. No discussion before both are done. Helper: `python evals/grade.py --grader 1` (Ugo) / `--grader 2` (Enzo), then `python evals/grade.py --merge`.
2. The judge grades the same 30 with `judge_prompt.txt` (one case at a time, pasted into a chat; or through any API). Its verdicts go into `evals/judge_30.csv` (`id`, `judge_sendable_yes_no`, `judge_evidence`).
3. `python evals/agreement.py` prints: human–human agreement (and Cohen's kappa), human–judge agreement against the consensus of the two humans, and the list of disagreements.
4. The team reads every disagreement, fixes **either the guideline or the prompt, once**, and writes below: the two rates before, what changed, and the date.

## Results (to fill after step 4 — do not write a number that was not measured)
| | Value | Date |
|---|---|---|
| Human–human agreement on 30 | _not measured yet_ | |
| Human–judge agreement on 30 | _not measured yet_ | |
| What the disagreements showed | | |
| What we changed (guideline or prompt) | | |

## Honest limits
- The reference top 3 is what the synthetic generator planted. On real reviews there is no such label; a person would have to write it.
- The drafts come from a **template drafter** (no LLM): a judge model and the drafter do not share a model family here. If an LLM drafter replaces it and the same family judges it, say so: it is a known bias.
- 20 of the 30 golden drafts quote the same sentence twice in a theme (a property of the generator and of the drafter, spec v2). Criterion 2 will therefore fail many of them — that is intended, it is the drafter's miss, not the guideline's.
- 30 cases give a rough rate. A rate on 30 has a 95 % interval of about ±15 points; do not read a 3-point change as an improvement.

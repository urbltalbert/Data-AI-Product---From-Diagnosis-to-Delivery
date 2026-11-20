# 06_07 — Experiments & operation · Team 7 · Review Insights (P8)

> Five sections = the five moves of Sessions 6 + 7. Sources: **[S]** `02_sizing.xlsx` · **[M]** `02_investment_memo.md` · **[B]** `03_product_brief.md` · **[05]** `05_metrics.md` · **[R]** `evals/report_v0.md` · **[T]** `evals/rollback_test_2026-11-20_1142.txt`. A number with no tag is an arithmetic result shown with its formula, or it is marked *decision* or *guess*.
> Every owner is a role that exists in our proposal (Head of Customer Success, Head of Product, DPO, Quality lead, on-call engineer, account manager). Every threshold has a clock.
> **Status on 20 Nov 2026:** no experiment has run, no real user has seen a draft. Three gates are still closed before any real unit (§2): the floor "zero drafts on hand-over tickets" was broken in three of four unseen runs (C07, C100, C188 [R §6, §7, §9]) and held once (0 / 22 [R §8]), each time on a different kind of ticket; in-scope tickets served were 46 % then 73 % on two unseen sets [R §8–9]; the two-grader number does not exist yet, and the system has only been tested on invented data.

## §1 Prove the effect — hypothesis, unit, design

**Hypotheses** (one per business metric of [05] §4):

1. **Time.** If we give the review-insights draft to account managers for in-scope rating-drop requests, the minutes an account manager spends per request move from **45 to ≤ 11** (75 % saved) **[S, M]** by the end of week 4 — without the hotel-complaint count leaving 2 a month **[05 §3]**, and without a draft on a hand-over ticket.
   - *Why 75 %, not the 60 % of the base case:* the memo is a CONDITIONAL GO on ≥ 75 % time saved; at 60 % it is a NO-GO **[M]**.
2. **Answer time.** If we do the same, the time to answer a hotel moves from **4 days to ≤ 24 hours** **[B]** by the end of week 4 — without the minutes Claire spends *verifying* going up (counter-metric [05 §3]).
3. **Quality as a non-effect.** The share of sent answers with a wrong top issue stays at **5 %, in a band the team chose (± 2 points, a *decision*)** **[S base error rate, 05 §4]**, read monthly. *See §2: this band cannot be proven by this test, only watched.*

**Unit of randomisation: the account manager** (30 of them, ~100 hotels each **[B persona, 01]**), split 15 / 15. The treatment would leak at the request level: the same account manager would see drafts on some requests and not on others, learn the pattern, and carry it to the "control" ones; and the hotels of one account manager would receive mixed answers. The brief already names this unit ("the A/B can randomise per account manager rather than per hotel") — it is the P8 design.

**Design: A/B on clusters (account managers), preceded by shadow mode.**
- **Shadow mode first** (no account manager sees a draft): the system runs on real incoming requests, drafts are graded by two people, nothing is shown. This is the only way to measure the two-grader number and the hand-over floor on real tickets *before* any user is exposed.
- **Then the A/B:** 15 account managers get the draft panel (L2, nothing is sent without them); 15 keep the manual process. Stratify the split by the number of in-scope requests per account manager (28.8 on average: 864 in-scope per month ÷ 30 **[B reach, S]**).
- **What it cannot see:**
  - *Effects across arms:* an account manager on holiday is covered by a colleague from the other arm (contamination); a "control" account manager can hear how a treated colleague works.
  - *Novelty:* the first weeks may look better because the panel is new. The 4-week run only partly controls for it.
  - *The hotel's reaction:* whether hotels fix the issue (the P8 template outcome, "hotels that act on a theme within 30 days") is not measured; we claim time and answer speed, not hotel outcomes.
  - *Small effects:* with 15 account managers per arm the test sees only large differences (below). That is acceptable because only a large saving (≥ 75 %) justifies shipping.
  - *The LLM:* the prototype drafter is a template, not a model. An LLM drafter is a different system and needs its own run.

## §2 Decide before — duration and decision rule

**Smallest improvement that still justifies the agent, and why:** 75 % of handling time saved (45 → ~11 min **[S, M]**). Below ~67 % the help-centre project is better (the hurdle, €70k/year base); at ~75 % the agent also beats do-nothing **[M]**. Sensitivity of the sizing, base case, varying only time saved: 30 % → net −€6k; 45 % → €25k; 60 % → €56k; 65 % → €67k; 75 % → €88k **[S Decision tab]**.

**Slowest guardrail to read → how long we run:** the hotel-complaint count is a *calendar month* **[05 §3, governance]**, so the minimum run is **4 weeks** (≈ one month) **plus a 2-week tail** for complaints that arrive after an answer (*decision*, not in the sources). **Read date = week 6, one read.**

| Input | Value | Source |
|---|---|---|
| Time per request, today | 45 min | **[S, B §2]** (guess; benchmark on 20 requests is still to do) |
| Smallest effect worth acting on | −33.75 min (75 % of 45) | **[M]** |
| Units | 15 account managers per arm | 30 account managers **[B, S G7]** |
| Spread between account managers σ (minutes) | **unknown — to be measured** on the 20-request timing | guess |
| Smallest difference the test can see (α 1 in 20, power 4 in 5) | **1.02 × σ**, from 2.8 × σ × √(2 / 15) | calculator, sheet *Means*, formula n = 2(z<sub>α</sub>+z<sub>β</sub>)²σ²/δ² |
| So the test is able to read −33.75 min if | σ ≤ ~33 min | 33.75 ÷ 1.02 |
| In-scope requests per week | ~200 (864 per month ÷ 4.33) | **[B reach, S]** |

**The quality band (± 2 points on 5 %) cannot be proven in 6 weeks.** To tell 5 % from 7 % at the same risks needs **2,214 graded answers per arm** (calculator, sheet *Proportions*: p₀ 5 %, δ 2 points); we have ~432 in-scope requests per arm per month. To see only a rise to the pessimistic-case error rate of 10 % **[S]**, we need **436 per arm** — about all the in-scope requests of one month in each arm, each graded by two people, which our evaluation line (€15k/year **[S]**) does not pay for. With the weekly 5 % human sample **[05 §3]** we grade ~22 answers per arm per month and can only see a jump of about 25 points or more (calculator formula, n = 22, p around 10 %). **So quality is read as a harm detector, not an equivalence test:** the stop is the harm threshold, and the ± 2 band is monitored over months in production (§3).

**Pre-registered segments** (the S5 list **[05 §3]**): language of the reviews, reviews per quarter (≥ 50 / < 50), hotel type, stars, account manager. Only the primary metric is read by segment, and only to look for a segment where the effect is the *opposite* sign: with 15 account managers per arm and ~100 cases in the eval-set, no segment has enough units for a test.

**Decision rule, written on 20 November 2026, before the first unit** (no unit exists yet):
- **Ship** if all hold at the week-6 read: (a) minutes per request ≤ 11 in the treatment arm (≥ 75 % saved); (b) the two-grader share of drafts sendable with minor edits ≥ 75 % **[B §7]**; (c) zero drafts on hand-over tickets, zero guest names, zero other-hotel data; (d) ≤ 2 hotel complaints about an inaccurate diagnosis in the month **[05 §3]**.
- **Iterate** if time saved is between 30 % and 75 %, or (b) fails, with (c) and (d) holding: fix, re-run shadow mode, re-run the A/B once.
- **Kill** if time saved is ≤ 30 % after one iteration (net value ≤ −€6k **[S]**, below do-nothing and below the hurdle), or if (c) fails twice.
- **Stop early only if** the harm threshold of `governance.md` is crossed: **a draft that shows another hotel's data or a guest name reaches a hotel, or more than 2 complaints about an inaccurate diagnosis in a calendar month** — never on a good number.
- **Gates before the first real unit:** (1) the floor holds again on a new frozen set (`eval_set_v4`, not written yet) after the C188 fix ("our other property" wording), **and** in-scope tickets served reach the 75 % flip point (73 %, interval 56–86 %, on `eval_set_v3` [R §9]); (2) two humans have graded `evals/golden_30.csv` and the agreement is written in `evals/README.md`; (3) DPO has read this file (§5).

## §3 Watch the four layers — monitoring and drift

| Layer | Metric (from [05]) | Threshold that pages someone | Clock | Owner | Tool — startup | Tool — large company |
|---|---|---|---|---|---|---|
| Infrastructure | draft ready before the account manager opens the ticket; step errors | draft not ready in **5 min** **[B §6]**, or any step error (the fallback sends the ticket to the manual queue automatically — tested [T]) | real time | on-call engineer | platform metrics · Sentry | Cloud Monitoring / CloudWatch · Datadog |
| Model quality | step-1 recall; right-top-3 share on the weekly sample of sent drafts; golden-set agreement | right-top-3 below **75 %** on the golden set **[B §7]**, or step-1 recall falls under the validation-chosen 0.70 threshold's recall of 0.87 on the validation tickets **[R §9]** | weekly | Quality lead (samples 5 % of sent drafts **[S G52]**) | Langfuse (EU) · Phoenix | LangSmith · Langfuse self-hosted · Datadog LLM |
| Product & guardrails | drafts on hand-over tickets; guest or staff name in a draft; other hotel's data; minutes per request; share sent with minor edits | **any** draft on a hand-over ticket, any name, any other-hotel data → page now; minutes per request above the control arm's | daily | Head of Customer Success (hand-over, minutes) · DPO (names, data) | SQL table + Metabase / Looker Studio | warehouse + Power BI / Tableau / Looker |
| Business | account-manager hours on analysis requests; answer time; complaints about an inaccurate diagnosis | **more than 2 complaints in a calendar month** **[05 §3]**; hours above the 4-day-baseline trend | weekly (hours) · monthly (complaints) | Head of Customer Success | weekly query + sheet | BI dashboard |
| Paging | — | — | — | Head of CS (day) · on-call engineer (night) | Slack / Teams webhook | PagerDuty / Opsgenie |

**Where our FastAPI runs:** **it does not exist yet.** The prototype is Python scripts (`/prototype`) run on a laptop, and the entry point that carries the switch is `prototype.pipeline.serve_ticket`. For the demo: laptop plus a tunnel. For a pilot: a FastAPI wrapper on Cloud Run **in an EU region** — guest reviews are personal data (`governance.md` question 2), so the data must not leave the EU. Secrets in `.env`, never in Git.

**Release path and gates:** dev (every commit: `python prototype/evals.py` and `python prototype/test_switch.py`; the assertions are the floor — zero drafts on hand-over tickets, zero names, zero other-hotel data) → staging (every change of detector, lexicon, prompt, model or threshold: the frozen eval-set + judge, shadow mode, the rollback drill re-run, last on 20 Nov 2026 [T]) → production by steps: **shadow mode (0 account managers see drafts) → 15 account managers (the A/B arm) → 30**, each step guarded by the thresholds of the table above and by the decision rule of §2.

**First drift expected: data drift in the reviews' language mix.** A leisure hotel's reviews are "nearly half" non-English in summer **[user research interview 3, governance S3]**, and the system hands over any hotel with more than half non-English reviews. Signal: the *share of hotels handed over for non-English reviews* by month and by hotel type, and the share of reviews whose text matches no theme of the lexicon (new vocabulary). Second: knowledge drift if the platform adds a new review field. **What we re-run:** the frozen eval-set (`evals/eval_set_v1.csv`, later `eval_set_v2`) on every release, model version, or policy change, and the golden set weekly.

## §4 Contain the incident — trace, dashboard, classes, rollback

**Trace — one OpenTelemetry trace per ticket, one span per step of `04_architecture.md`.** *Designed, not built: the prototype returns these fields in the dict of `run_ticket` but does not emit spans.*

| Span | Attributes (no review text in the span; the ids point to it) |
|---|---|
| `request` | ticket id · timestamp · hotel type and stars (segment) · version of the detector, lexicon, template/prompt and threshold · switch position · latency · cost |
| `detect` | label · confidence · threshold used |
| `eligibility` | decision (ok / hand over) · reason · number of Q3 reviews · share non-English |
| `extract` | hotel_id (one only) · window (two quarters) · review ids used |
| `themes` | count per theme per quarter · the three chosen · reviews used |
| `draft` | drafter version · tokens (if a model) · latency |
| `policy` | pass / block · reason |
| `human_decision` | approved / edited / write-myself / escalated · edit distance · minutes · judge score · human grade if sampled |

Stored in Langfuse (EU) or Phoenix; **kept 12 months** (`governance.md` S3). Access: the account manager of the hotel, the Head of CS, the DPO, compliance auditors.

**Our one-page dashboard — five panels and the question each answers:**
1. *Stat tiles with thresholds:* drafts on hand-over tickets, names, other-hotel data, complaints this month — **am I paged?**
2. *Line over time:* share sent with minor edits and minutes per request, weekly — **trend, spikes?**
3. *Histogram, this week vs last:* detector confidence — **has the input drifted?**
4. *Bars by segment:* hand-over rate and right-top-3 by hotel type, stars, language — **is one segment worse (Simpson, fairness)?**
5. *Worst-cases table:* the drafts edited most, quotes flagged — **what do we fix on Monday?**

Built with a Streamlit tab at first, Metabase when it runs for real.

| Class | Example on our agent | Action |
|---|---|---|
| **Caught** | the policy check blocks a draft that carries a staff name; the eligibility rule hands over a hotel with 49 reviews | counted, weekly review, a spec line if it repeats |
| **Sent wrong** | Claire sends a draft whose top issue is wrong; the hotel fixes the wrong thing (cost of one error ~€100 **[S]**) | correct the answer to the hotel the same day, count it against the monthly threshold of 2, Quality lead reads the draft, spec line |
| **Harmful** (above the harm threshold) | a draft shows another hotel's reviews or a guest's name and reaches a hotel; or the third complaint of the month | **rollback now**, incident report, DPO informed (GDPR), the hotel is told by Claire |
| **Outage** | the detector or the drafter fails | fallback: humans only, **automatic** — tested, case 7 of [T] |

*The line between "sent wrong" and "harmful":* one error that stays inside the hotel's own data is "sent wrong"; **any breach of the hotel's or a guest's data, or more than 2 wrong diagnoses in a month, is "harmful".**

**Rollback plan**

| Field | Ours |
|---|---|
| 1 · Trigger | any draft with another hotel's data or a guest name that reaches a hotel · more than 2 hotel complaints about an inaccurate diagnosis in a calendar month · **any draft on a hand-over ticket in production** (the floor of [05 §2]) |
| 2 · Who decides (day / night) | day: **Head of Customer Success** · night: **on-call engineer**, who may switch to *suggest-only* alone and must wake the Head of CS to go to *off* |
| 3 · The action | first **suggest-only** (themes and counts are shown to the account manager, no email draft is produced); if the trigger was a data breach, **off** (every ticket goes to the manual queue, as before the product existed). Redeploying the previous version is the third step, only after a bug is found |
| 4 · Time to execute | **target: under 15 minutes** (*decision*). Measured on the prototype: the flag takes effect on the very next ticket, **0.3 ms** after it is written, with no restart **[T case 3]**. **Not measured:** the human chain (who is called, who answers) |
| 5 · What people see | account managers: a banner "Review Insights is switched off – answer manually" and every ticket in the manual queue; hotels: nothing changes, they never saw the tool |
| 6 · Last tested | **20 November 2026, 11:42 CET, on Enzo Méret's laptop (the staging of the project), on the prototype, 7 of 7 checks passed** — `python prototype/test_switch.py`, output in `evals/rollback_test_2026-11-20_1142.txt` **[T]**: on → off → suggest-only → on, an unknown value in the flag file fails *safe* (off), and a simulated outage in the detector falls back to humans-only. **Not tested:** the real ticketing tool, the night path, a person other than the author pressing it. *A team member should re-run the script herself and date that run before 23 November.* |

## §5 Own the system — the five owners

| Decision | Owner (role) | Written where |
|---|---|---|
| Run an experiment on real users | **Head of Customer Success** signs; the **DPO** reads before it starts (the account managers are the users, the hotels' reviews are the data) | §1–§2 · `governance.md` |
| Read the weekly numbers and act | **Quality lead** reads (5 % sample, golden set) · **Head of Customer Success** acts | §3 |
| Press the switch (day / night) | **Head of Customer Success** (day) · **on-call engineer** (night) | §4 · `governance.md` |
| Approve a release (detector, lexicon or prompt, model, sources, threshold) | **Head of Product**, with the Head of CS agreeing on the guardrails; condition: the frozen eval-set and the floor pass | `evals/README.md` |
| Keep the trace; answer a customer or a regulator | **DPO** answers; the on-call engineer's team keeps the trace for 12 months | `governance.md` |

*Copied into `governance.md`:* who signs an experiment on real users · who can press the switch · where the trace lives and for how long — plus the line that **the company answers for what the system says (Moffatt v. Air Canada, 2024 BCCRT 149)**: a draft that reaches a hotel is LobbyIQ's statement, whatever the model did.

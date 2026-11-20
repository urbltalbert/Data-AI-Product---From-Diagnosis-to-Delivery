"""The four-step workflow (spec §2): detect -> eligibility -> themes+draft -> policy check. No agent loop."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import detect, rules, themes, draft as drafter, policy


def run_ticket(hotel_id, text, skip_detect=False):
    """skip_detect=True is a DIAGNOSTIC only (isolates steps 2-4 from step 1); never used for the headline number."""
    label, conf = ("rating_drop", 1.0) if skip_detect else detect.predict(text)
    status, reason = rules.eligibility(hotel_id, text, label, conf)
    out = dict(hotel_id=hotel_id, label=label, confidence=round(conf, 2), decision="escalate", reason=reason,
               draft="NO_DRAFT", top3=[], policy="pass", policy_reason="", counts={}, quote_ids=[])
    if status != "ok":
        return out
    rev = rules.reviews_for(hotel_id)
    counts, quotes = themes.theme_counts(rev)
    top = themes.top3(counts)
    text_out = drafter.draft(top, counts, quotes)
    if text_out == "NO_DRAFT":
        out["reason"] = "no negative theme found"
        return out
    pol, pol_reason = policy.check(text_out, hotel_id, set(rev["review_id"]))
    out.update(decision="draft" if pol == "pass" else "blocked", draft=text_out, top3=top, policy=pol,
               policy_reason=pol_reason, counts=counts, quote_ids=[q["review_id"] for t in top for q in quotes[t]])
    if pol == "block":
        out["reason"] = pol_reason
    return out


def serve_ticket(hotel_id, text):
    """The production entry point: the switch, then the workflow, with a humans-only fallback on any error.
    The eval calls run_ticket (the pure workflow) so that a bug is never hidden as a hand-over."""
    import switch
    pos = switch.get()
    base = dict(hotel_id=hotel_id, switch=pos, decision="escalate", draft="NO_DRAFT", top3=[], counts={})
    if pos == "off":
        return dict(base, reason="Review Insights is switched off - answer manually")
    try:
        out = run_ticket(hotel_id, text)
    except Exception as e:  # outage class: humans-only, automatic
        return dict(base, reason=f"system error ({type(e).__name__}) - answer manually")
    out["switch"] = pos
    if pos == "suggest_only" and out["decision"] == "draft":
        out.update(decision="suggest", draft="NO_DRAFT", reason="suggest-only: themes shown, no email draft")
    return out

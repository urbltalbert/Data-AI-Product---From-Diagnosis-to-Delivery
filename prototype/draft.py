"""Step 3b — the drafter. Template drafter (no API key in v0); same contract as an LLM call. Spec §2.4."""


def draft(top, counts, quotes):
    if not top:
        return "NO_DRAFT"
    lines = ["Hello,", "",
             "Here is what changed in your guest reviews: current quarter Q3 2026 compared with previous quarter Q2 2026 (negative reviews only).", ""]
    for i, t in enumerate(top, 1):
        c = counts[t]
        lines.append(f"{i}. {t.capitalize()} — {c['Q3']} negative reviews in Q3 2026 vs {c['Q2']} in Q2 2026 ({c['Q3'] - c['Q2']:+d}).")
        for q in quotes[t]:
            lines.append(f'   "{q["text"]}" [{q["review_id"]}]')
    lines += ["", "This summary was prepared with AI assistance and checked by your account manager."]
    return "\n".join(lines)

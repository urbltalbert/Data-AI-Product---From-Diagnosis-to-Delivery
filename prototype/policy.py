"""Step 4 — policy checker (rung 1: rules). Spec §2.5. Blocks names, other hotel ids, promises."""
import re

RULES = [
    (r"\bH-\d+\b", "contains a hotel id"),   # replaced below by an own-hotel check
    (r"\b(Mr|Mrs|Ms|Dr)\.? [A-Z]", "contains a title + name"),
    (r"\b[A-Z][a-z]+ (at reception)", "contains a staff name"),
    (r"\bAsk for [A-Z][a-z]+", "contains a staff name"),
    (r"\b(we promise|we guarantee|refund|compensation)\b", "makes a promise"),
]


def check(draft_text, hotel_id, allowed_review_ids):
    """Return ('pass', '') or ('block', reason)."""
    if draft_text == "NO_DRAFT":
        return "pass", ""
    for h in re.findall(r"\bH-\d+\b", draft_text):
        if h != hotel_id:
            return "block", "contains another hotel's id"
    for pat, reason in RULES[1:]:
        if re.search(pat, draft_text):
            return "block", reason
    for rid in re.findall(r"\[(R-\d+)\]", draft_text):
        if rid not in allowed_review_ids:
            return "block", "quotes a review of another hotel"
    return "pass", ""

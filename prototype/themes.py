"""Step 3a — theme extraction (rung 3 in the brief; v0 fallback = keyword lexicon, no API key). Spec §2.4."""
import re

LEXICON = {
    "cleanliness": r"dirty|dust|stain|mould|mold|filth|unclean|not clean|hair in",
    "noise": r"noisy|noise|loud|thin walls|could hear",
    "breakfast": r"breakfast|buffet",
    "wifi": r"wifi|wi-fi|internet",
    "parking": r"parking|car park",
    "check-in": r"check-in|check in|waited|arrival",
    "room temperature": r"freezing|heating|too hot|air conditioning|stuffy|temperature",
    "value": r"value|overpriced|too expensive|not worth|price",
    "staff": r"\bstaff\b|reception|rude|unfriendly|dismissive",
}
NEG_MAX_RATING = 3


def mask_names(text):
    """Heuristic masking (no NER in v0): titles + name-like tokens next to 'reception' or 'Ask for'."""
    text = re.sub(r"\b(Mr|Mrs|Ms|Dr)\.? [A-Z][\w-]+", "[name]", text)
    text = re.sub(r"\b(Ask for) [A-Z][a-z]+", r"\1 [name]", text)
    text = re.sub(r"\b[A-Z][a-z]+ (at reception)", r"[name] \1", text)
    return text


def theme_counts(reviews):
    """Count negative reviews per theme, per quarter. Returns {theme: {Q2: n, Q3: n}} and quotes per theme."""
    neg = reviews[reviews["rating"] <= NEG_MAX_RATING]
    counts, quotes = {}, {}
    for theme, pat in LEXICON.items():
        hit = neg[neg["text"].str.contains(pat, case=False, regex=True)]
        counts[theme] = {"Q2": int((hit["quarter"] == "Q2").sum()), "Q3": int((hit["quarter"] == "Q3").sum())}
        q3 = hit[hit["quarter"] == "Q3"].sort_values(["rating", "review_id"])
        quotes[theme] = [{"review_id": r.review_id, "text": mask_names(r.text)} for r in q3.head(2).itertuples()]
    return counts, quotes


def top3(counts):
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1]["Q3"], kv[0]))
    return [t for t, c in ranked[:3] if c["Q3"] > 0]

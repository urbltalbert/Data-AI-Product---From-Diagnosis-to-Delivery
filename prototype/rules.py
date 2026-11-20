"""Step 2 — eligibility and extraction rules (rung 1: rules). Spec v2 §2.2-2.3."""
import os, re
import pandas as pd

MIN_REVIEWS = 50
MAX_NON_EN_SHARE = 0.5
_DIR = os.path.dirname(__file__)


def _threshold():
    """Chosen on data/tickets_val.csv by prototype/tune_threshold.py (never on the eval-set)."""
    p = os.path.join(_DIR, "threshold.txt")
    return float(open(p).read().strip()) if os.path.exists(p) else 0.70


CONF_THRESHOLD = _threshold()

# Function words per language (standard, short lists) — a ticket is English if English words win.
_STOP = {
    "en": "the our we is are why did what how can you us to of and a i my this that it has have been do does please rating score guests what for with not".split(),
    "fr": "le la les nous notre pourquoi quoi comment est sont de des du un une et pas pour avec elle il a-t-elle baissé nos vous je mon ma".split(),
    "de": "der die das wir unser warum ist sind und nicht ich mein wie wurde haben mit für bewertung gesunken".split(),
    "it": "il la le noi nostra perché è sono di del un una e non per con valutazione scesa come posso".split(),
    "es": "el la los nosotros nuestra por qué es son de del un una y no para con puntuación ha bajado".split(),
}

# Intents the brief puts out of scope (WON'T D–H): hand over whatever the classifier says.
WONT = [
    (r"\b(reply|respond|response|answer)\b.*\b(review|comment)s?\b|\b(review|comment)s?\b.*\b(reply|respond)\b", "public reply to a review is out of scope"),
    (r"\b(other|nearby|neighbou?ring|competing) hotels?\b|\bacross the street\b|\bnext door\b|\bcompetitors?\b|\bbenchmark|\bcompare[sd]?\b.*\bhotels?\b|\bhotels? (nearby|in our city)\b",
     "benchmark against other hotels is out of scope"),
    (r"\bwhat (should|can|do) (we|you)\b.*\b(change|improve|recommend|do)\b|\bhow (can|do) we (improve|raise|get better)\b|\badvice\b|\brecommend", "operational recommendations are out of scope"),
]

# Account / billing / platform questions (spec v3, fix for C07 and C100): the classifier learns vocabulary,
# so a support ticket that says "rating" or "review" can look like a rating-drop request. These go to the normal queue.
ACCOUNT = [
    (r"\binvoices?\b|\bbilling\b|\bcharged?\b|\brefund|\bsubscription\b|\bcontract\b|\bupgrade\b|\bdowngrade\b|\bprice\b|\bpricing\b",
     "billing or contract question, not a rating-drop request"),
    (r"\bpassword\b|\blog ?in\b|\blogin\b|\bsign ?in\b|\b(my|our|the|your) account\b|\binvite\b|\badd (a |my |our )?(new )?(user|colleague|admin)",
     "account or login question, not a rating-drop request"),
    (r"\b(remove|delete|take down|dispute|contest)\b.*\b(fake|false|spam|abusive|one[- ]star|1[- ]star)?\s*(review|comment)s?\b|\b(fake|false)\s+(review|comment)s?\b",
     "request to remove or contest a review, not a rating-drop request"),
    (r"\bexport\b|\bwidget\b|\bapi\b|\bpms\b|\bintegration\b|\b(page|profile) (address|url|link)\b|\bdashboard\b.*\b(load|crash|slow|bug|language)",
     "product or technical question, not a rating-drop request"),
]
_REVIEWS = None


def load_reviews(path="data/reviews_synthetic.csv"):
    global _REVIEWS
    df = pd.read_csv(path)
    df["review_id"] = ["R-%05d" % i for i in range(len(df))]
    _REVIEWS = df
    return df


def reviews_for(hotel_id):
    """The ONLY way to read reviews: one hotel_id per call (isolation rule, governance S3)."""
    if _REVIEWS is None:
        load_reviews()
    return _REVIEWS[_REVIEWS["hotel_id"] == hotel_id].copy()


def ticket_language(text):
    words = re.findall(r"[^\W\d_]+(?:-[^\W\d_]+)*", text.lower())
    scores = {lg: sum(w in sw for w in words) for lg, sw in ((k, set(v)) for k, v in _STOP.items())}
    best = max(scores, key=lambda k: (scores[k], k == "en"))
    return best if scores[best] > 0 else "en"


def other_hotel_ids(text, own_id):
    """Hotel ids named in the ticket text that are not the ticket's own hotel."""
    return sorted({h.upper() for h in re.findall(r"\bH-\d+\b", text, flags=re.I)} - {own_id})


def eligibility(hotel_id, ticket_text, label, confidence):
    """Return ('ok', '') or ('hand_over', reason). Specific reasons come first (spec v2)."""
    if other_hotel_ids(ticket_text, hotel_id):
        return "hand_over", "several hotels in one request"
    if ticket_language(ticket_text) != "en":
        return "hand_over", "ticket not in English"
    for pat, why in WONT:
        if re.search(pat, ticket_text, flags=re.I):
            return "hand_over", why
    for pat, why in ACCOUNT:
        if re.search(pat, ticket_text, flags=re.I):
            return "hand_over", why
    if label != "rating_drop":
        return "hand_over", "not a rating-drop request"
    if confidence < CONF_THRESHOLD:
        return "hand_over", f"detection confidence {confidence:.2f} below {CONF_THRESHOLD}"
    rev = reviews_for(hotel_id)
    if rev.empty:
        return "hand_over", "unknown hotel_id"
    if (rev["language"] != "en").mean() > MAX_NON_EN_SHARE:
        return "hand_over", "reviews mostly not in English"
    if (rev["quarter"] == "Q3").sum() < MIN_REVIEWS:
        return "hand_over", "fewer than 50 reviews in the current quarter"
    return "ok", ""

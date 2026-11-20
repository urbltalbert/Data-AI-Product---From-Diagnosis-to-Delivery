"""Generate the synthetic reviews and the eval-set rows (Assignment 4).

Run from the repo root:  python data/make_data.py
Writes: data/reviews_synthetic.csv   (no label column: the prototype never sees the planted themes)
        evals/eval_set_v0.csv        (C01-C20 kept as written by Ugo, C21-C50 appended)
Everything is invented. No real customer data.
"""
import csv, io, os, random, sys

sys.path.insert(0, os.path.dirname(__file__))
from cases_spec import CASES, HANDOVER_TEXT

random.seed(7)

NEG = {
    "cleanliness": ["The room was dirty and the bathroom had mould.", "Dust everywhere and stains on the sheets.", "Not clean at all, the carpet was filthy.", "Hair in the shower and a dirty floor, very unclean."],
    "noise": ["Very noisy at night, we could hear the street until 3am.", "Thin walls and loud neighbours, impossible to sleep.", "The noise from the bar kept us awake all night.", "Too noisy, the air conditioning was loud and the corridor too."],
    "breakfast": ["The breakfast was poor with very little choice.", "Breakfast was cold and the queue was endless.", "Disappointing breakfast, the buffet was always empty.", "Breakfast ran out of food by 9am."],
    "wifi": ["The wifi kept dropping, impossible to work.", "Wifi was so slow that video calls failed.", "No stable internet in the room, the wifi is terrible.", "Wifi password never worked and the connection was awful."],
    "parking": ["No parking available and the car park was always full.", "Parking was expensive and far from the hotel.", "We could never find parking, a real hassle.", "The car park was tiny and parking was a nightmare."],
    "check-in": ["Check-in took forever, we waited 45 minutes.", "Slow check-in, the room was not ready on arrival.", "The check-in desk was chaotic and nobody was there.", "Long wait at check-in after a tiring trip."],
    "room temperature": ["The room was freezing and the heating did not work.", "Far too hot in the room, the air conditioning was broken.", "We could not control the room temperature, it was stuffy.", "Heating broken, the room temperature was unbearable."],
    "value": ["Not worth the price, poor value for money.", "Overpriced for what you get, bad value.", "Way too expensive for such an average stay, poor value.", "Value for money was disappointing."],
    "staff": ["The staff were rude and unhelpful.", "Unfriendly staff who ignored our requests.", "Staff attitude was poor and nobody apologised.", "The reception staff were dismissive and slow."],
}
POS = {
    "cleanliness": ["Spotless room, very clean.", "Everything was clean and tidy."],
    "noise": ["Quiet and peaceful, slept very well."],
    "breakfast": ["Great breakfast with lots of choice.", "The breakfast buffet was excellent."],
    "wifi": ["Fast wifi, worked perfectly."],
    "parking": ["Easy parking right next to the hotel."],
    "check-in": ["Quick and friendly check-in.", "Smooth check-in, room ready on arrival."],
    "room temperature": ["The room was comfortable and perfectly warm."],
    "value": ["Good value for money."],
    "staff": ["The staff were lovely and very helpful.", "Friendly staff, always smiling.", "Wonderful reception team."],
}
GENERIC_POS = ["Lovely stay, would come back.", "Great location and a comfortable bed.", "Nice hotel, we enjoyed our weekend.", "Perfect for a short city break."]
NAMES = ["Julia", "Marco", "Mr Schneider", "Sophie", "Karim", "Anna"]
COFFEE = "The coffee was cold every morning."
FOREIGN = {
    "de": ["Das Zimmer war schmutzig und sehr laut.", "Wunderbares Hotel, freundliches Personal.", "Das Frühstück war enttäuschend und teuer."],
    "fr": ["La chambre était sale et très bruyante.", "Hôtel magnifique, personnel aimable.", "Le petit-déjeuner était décevant et cher."],
    "it": ["La camera era sporca e molto rumorosa.", "Hotel bellissimo, personale gentile.", "La colazione era deludente e costosa."],
}
THEMES = list(NEG)


def month(q):  # q = "Q2" or "Q3"
    return random.choice([4, 5, 6] if q == "Q2" else [7, 8, 9])


def make_hotel(c):
    hid, total = c["hotel"], c["total"]
    q3 = c["q3"] if c["q3"] is not None else total // 2
    q2 = total - q3
    flags = c["flags"]
    rows = []

    def add(q, text, rating, lang="en"):
        rows.append(dict(hotel_id=hid, quarter=q, date=f"2026-{month(q):02d}-{random.randint(1, 28):02d}",
                         rating=rating, language=lang, text=text))

    def neg_text(theme):
        t = random.choice(NEG[theme])
        if "names_neg_staff" in flags and theme == "staff":
            t += f" {random.choice(NAMES)} at reception was the worst."
        return t

    def pos_text(pool_theme=None):
        t = random.choice(POS[pool_theme]) if pool_theme else random.choice(GENERIC_POS)
        if "names" in flags and random.random() < 0.35:
            t += f" Ask for {random.choice(NAMES)} at reception."
        return t

    for q, n in (("Q2", q2), ("Q3", q3)):
        if n == 0:
            continue
        planted = []
        if c["top3"]:
            shares = c["r"] if q == "Q3" else tuple(s / 2 for s in c["r"])
            planted = [(t, round(s * n)) for t, s in zip(c["top3"], shares)]
        other = [t for t in THEMES if t not in (c["top3"] or [])]
        noise = [(random.choice(other), 1) for _ in range(max(1, n // 40))] if n >= 10 else []
        n_neg = 0
        for theme, k in planted + noise:
            for _ in range(k):
                add(q, neg_text(theme), random.choice([1, 2, 2, 3]))
                n_neg += 1
        if "coffee" in flags and q == "Q3":
            for _ in range(4):
                add(q, COFFEE, 3); n_neg += 1
        if "names" in flags and q == "Q3":
            for _ in range(5):
                add(q, f"{random.choice(NAMES)} at reception made the stay unpleasant, check out was fine.", 3)
                n_neg += 1
        n_pos = max(0, n - n_neg)
        for _ in range(n_pos):
            r = random.random()
            if "pos_staff" in flags and r < 0.35:
                th = "staff"
            elif "pos_checkin" in flags and r < 0.35:
                th = "check-in"
            elif "pos_breakfast" in flags and r < 0.35:
                th = "breakfast"
            elif r < 0.6:
                th = random.choice([t for t in THEMES if t not in (c["top3"] or [])])
            else:
                th = None
            add(q, pos_text(th), random.choice([4, 5, 5]))
    # foreign-language share: replace a fraction of reviews (both quarters), keep order stable
    for lg, share in c["lang"].items():
        for r in random.sample(rows, int(share * len(rows))):
            r["text"], r["language"] = random.choice(FOREIGN[lg]), lg
    random.shuffle(rows)
    return rows


def expected_output(c):
    if c["handover"]:
        return f"No draft; hand over with the reason {HANDOVER_TEXT[c['handover']]}"
    t = c["top3"]
    return (f"Draft: top 3 negative themes in count order {t[0]}, {t[1]}, {t[2]}; delta vs Q2; "
            "2 negative quotes each; both quarters labelled; no guest or staff name")


def csv_row(c):
    if c["handover"]:
        evid, hand = f"rule: {HANDOVER_TEXT[c['handover']]} (brief §2)", f"yes — {HANDOVER_TEXT[c['handover']]}"
    else:
        evid, hand = f"planted issues for {c['hotel']} in the synthetic reviews", "no — L2 account manager approves"
    inp = f'Ticket from {c["hotel"]}: "{c["ticket"]}"'
    if c["handover"] != "not_rating_drop" and c["handover"] != "multi_hotel":
        inp += f" + {c['total']} reviews (Q2–Q3 2026)"
    return {"id": c["id"], "project": "P8 voice-of-customer synthesis", "input_the_agent_receives": inp,
            "expected_output_or_action": expected_output(c), "evidence_or_source": evid,
            "hand_over_to_a_person": hand, "segment": c["segment"], "origin": "invented · human-labelled",
            "notes": c["note"]}


def main():
    all_rows = []
    for c in CASES:
        all_rows += make_hotel(c)
    with open("data/reviews_synthetic.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["hotel_id", "quarter", "date", "rating", "language", "text"])
        w.writeheader(); w.writerows(all_rows)
    # keep Ugo's C01-C20 lines byte for byte; (re)write only C21-C50
    with open("evals/eval_set_v0.csv", newline="", encoding="utf-8") as f:
        lines = f.read().splitlines(keepends=True)
    head = lines[:21]
    if not head[-1].endswith("\n"):
        head[-1] += "\n"
    fields = next(csv.reader([lines[0]]))
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    w.writerows([csv_row(c) for c in CASES if 20 < int(c["id"][1:]) <= 50])
    v0_text = "".join(head) + buf.getvalue()
    with open("evals/eval_set_v0.csv", "w", newline="", encoding="utf-8") as f:
        f.write(v0_text)
    # eval_set_v1 = the 50 development cases (unchanged) + 50 fresh cases C51-C100
    buf2 = io.StringIO()
    w2 = csv.DictWriter(buf2, fieldnames=fields, lineterminator="\n")
    fresh = [csv_row(c) for c in CASES if 50 < int(c["id"][1:]) <= 100]
    for r in fresh:
        r["origin"] = "invented · planted labels, written before the run · fresh in v1"
    w2.writerows(fresh)
    with open("evals/eval_set_v1.csv", "w", newline="", encoding="utf-8") as f:
        f.write(v0_text + buf2.getvalue())
    # eval_set_v2 = v1 + 50 cases C101-C150, written before the C07/C100 fix, run once
    buf3 = io.StringIO()
    w3 = csv.DictWriter(buf3, fieldnames=fields, lineterminator="\n")
    fresh2 = [csv_row(c) for c in CASES if int(c["id"][1:]) > 100]
    for r in fresh2:
        r["origin"] = "invented · planted labels, written before the fix and the run · fresh in v2"
    w3.writerows(fresh2)
    with open("evals/eval_set_v2.csv", "w", newline="", encoding="utf-8") as f:
        f.write(v0_text + buf2.getvalue() + buf3.getvalue())
    n_cases = 50 + len(fresh) + len(fresh2)
    print(f"{len(all_rows)} reviews, {n_cases} eval cases")


if __name__ == "__main__":
    main()

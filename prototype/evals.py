"""Spec §7. Runs evals/eval_set_v0.csv through the pipeline. NEVER tune while looking at these rows.

Automatic proxy for "sendable": the two human graders decide the real number (evals/grading_sheet_v0.csv).
Usage (repo root): python prototype/evals.py
"""
import csv, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from collections import Counter
import pipeline, rules

CRITERION = 0.75
THEMES = ["cleanliness", "noise", "breakfast", "wifi", "parking", "check-in", "room temperature", "value", "staff"]


def load_cases(path="evals/eval_set_v0.csv"):
    cases = []
    for r in csv.DictReader(open(path, encoding="utf-8")):
        hotel = re.search(r"Ticket from (H-\d+)", r["input_the_agent_receives"]).group(1)
        text = re.search(r'"(.*?)"(?: \+|$)', r["input_the_agent_receives"]).group(1)
        exp = None
        if r["expected_output_or_action"].startswith("Draft"):
            head = r["expected_output_or_action"].split(";")[0]
            found = sorted(((head.find(t), t) for t in THEMES if head.find(t) >= 0))
            exp = [t for _, t in found]
        cases.append(dict(id=r["id"], hotel=hotel, text=text, segment=r["segment"], handover=r["hand_over_to_a_person"].startswith("yes"),
                          expected_top3=exp,
                          expected_reason=r["hand_over_to_a_person"], note=r["notes"]))
    return cases


def sendable_proxy(c, o):
    if o["decision"] != "draft" or o["policy"] != "pass":
        return False, "no draft or blocked"
    if len(set(o["top3"]) & set(c["expected_top3"])) < 2:
        return False, "top 3 overlap < 2"
    if "Q2 2026" not in o["draft"] or "Q3 2026" not in o["draft"]:
        return False, "quarters not labelled"
    return True, ""


def run(path="evals/eval_set_v0.csv", sheet="evals/grading_sheet_v0.csv", skip_detect=False, only=None):
    rows, grading = [], []
    cases = load_cases(path)
    if only:  # "51-100": run only these ids (e.g. the fresh cases of eval_set_v1)
        lo, hi = map(int, only.split("-"))
        cases = [c for c in cases if lo <= int(c["id"][1:]) <= hi]
    for c in cases:
        o = pipeline.run_ticket(c["hotel"], c["text"], skip_detect=skip_detect)
        got_draft = o["decision"] == "draft"
        ok, why = sendable_proxy(c, o) if not c["handover"] else (False, "")
        rows.append(dict(c, **{"out": o, "got_draft": got_draft, "sendable": ok, "why": why,
                                "exact": got_draft and not c["handover"] and o["top3"] == c["expected_top3"],
                                "overlap2": got_draft and not c["handover"] and len(set(o["top3"]) & set(c["expected_top3"])) >= 2}))
        if got_draft:
            grading.append({"id": c["id"], "expected_top3": ", ".join(c["expected_top3"] or []), "draft": o["draft"].replace("\n", " ⏎ "),
                            "grader_1_sendable_yes_no": "", "grader_2_sendable_yes_no": "", "comment": ""})
    with open(sheet, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "expected_top3", "draft", "grader_1_sendable_yes_no", "grader_2_sendable_yes_no", "comment"])
        w.writeheader(); w.writerows(grading)

    in_scope = [r for r in rows if not r["handover"]]
    human = [r for r in rows if r["handover"]]
    n_send = sum(r["sendable"] for r in in_scope)
    names = sum(bool(re.search(r"\b(Mr|Mrs|Ms) [A-Z]|\b(Julia|Marco|Sophie|Karim|Anna|Schneider)\b", r["out"]["draft"])) for r in rows)
    print(f"cases {len(rows)} · in scope {len(in_scope)} · hand-over expected {len(human)}")
    print(f"decision correct (draft vs hand over)   {sum(r['got_draft'] != r['handover'] for r in rows)}/{len(rows)}")
    print(f"drafts on hand-over cases (must be 0)   {sum(r['got_draft'] for r in human)}")
    print(f"in-scope cases that got a draft         {sum(r['got_draft'] for r in in_scope)}/{len(in_scope)}")
    print(f"top 3 exact order                       {sum(r['exact'] for r in in_scope)}/{len(in_scope)}")
    print(f"top 3 overlap >= 2 of 3                 {sum(r['overlap2'] for r in in_scope)}/{len(in_scope)}")
    print(f"drafts containing a guest/staff name    {names}   (must be 0)")
    print(f"policy blocks                           {sum(r['out']['decision'] == 'blocked' for r in rows)}")
    print(f"sendable (automatic proxy)              {n_send}/{len(in_scope)} = {n_send / len(in_scope):.0%}   (criterion {CRITERION:.0%})")
    print("\nmisses by cause (in-scope cases):")
    causes = Counter(r["out"]["reason"] if not r["got_draft"] else r["why"] for r in in_scope if not r["sendable"])
    for cause, n in causes.most_common():
        print(f"  {n} × {cause}: " + ", ".join(r["id"] for r in in_scope if not r["sendable"] and (r["out"]["reason"] if not r["got_draft"] else r["why"]) == cause))
    print("\nhand-over cases that got a draft:", [r["id"] for r in human if r["got_draft"]] or "none")
    print("\nper case:")
    for r in rows:
        o = r["out"]
        print(f"  {r['id']} hand_over_expected={str(r['handover']):5} got={o['decision']:8} conf={o['confidence']:.2f} top3={o['top3']} expected={r['expected_top3']} reason={o['reason']}")
    return rows


if __name__ == "__main__":
    arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
    diag = "--skip-detect" in sys.argv
    if diag:
        print("DIAGNOSTIC MODE: step 1 (detect) bypassed — not the headline number\n")
    run(path=arg("--set", "evals/eval_set_v0.csv"), sheet=arg("--sheet", "evals/grading_sheet_v0_diagnostic.csv" if diag else "evals/grading_sheet_v0.csv"),
        skip_detect=diag, only=arg("--only", None))

"""Human-human and human-judge agreement on the golden set. Run from the repo root: python evals/agreement.py
Reads evals/golden_30.csv (grader_1/grader_2 columns) and evals/judge_30.csv (id, judge_sendable_yes_no). Stdlib only."""
import csv, os, sys


def yn(v):
    v = (v or "").strip().lower()
    return {"yes": 1, "y": 1, "no": 0, "n": 0}.get(v)


def kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = (sum(a) / n) * (sum(b) / n) + (1 - sum(a) / n) * (1 - sum(b) / n)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


def main():
    gold = {r["id"]: r for r in csv.DictReader(open("evals/golden_30.csv", encoding="utf-8"))}
    h = {i: (yn(r["grader_1_sendable_yes_no"]), yn(r["grader_2_sendable_yes_no"])) for i, r in gold.items()}
    done = {i: v for i, v in h.items() if None not in v}
    if len(done) < len(gold):
        print(f"{len(gold) - len(done)} of {len(gold)} rows are not graded by both humans yet — nothing to report.")
        return
    a, b = [v[0] for v in done.values()], [v[1] for v in done.values()]
    agree = sum(x == y for x, y in zip(a, b)) / len(a)
    print(f"human-human agreement   {agree:.0%}  ({sum(x == y for x, y in zip(a, b))}/{len(a)})   kappa {kappa(a, b):.2f}")
    print("  disagreements:", ", ".join(i for i, v in done.items() if v[0] != v[1]) or "none")
    if not os.path.exists("evals/judge_30.csv"):
        print("no evals/judge_30.csv yet — the judge has not graded the golden set.")
        return
    judge = {r["id"]: yn(r["judge_sendable_yes_no"]) for r in csv.DictReader(open("evals/judge_30.csv", encoding="utf-8"))}
    cons = {i: v[0] for i, v in done.items() if v[0] == v[1]}  # consensus only, as the reference for the judge
    ok = [i for i in cons if judge.get(i) is not None]
    hj = sum(judge[i] == cons[i] for i in ok) / len(ok)
    print(f"human-judge agreement   {hj:.0%}  ({sum(judge[i] == cons[i] for i in ok)}/{len(ok)} rows where both humans agree)")
    print("  judge says SENDABLE where humans say NO (over-accepts):", ", ".join(i for i in ok if judge[i] == 1 and cons[i] == 0) or "none")
    print("  judge says NOT where humans say YES (over-rejects):    ", ", ".join(i for i in ok if judge[i] == 0 and cons[i] == 1) or "none")


if __name__ == "__main__":
    sys.exit(main())

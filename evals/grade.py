"""Grade the golden set one draft at a time, alone. Run from the repo root:

    python evals/grade.py --grader 1      # Ugo   -> evals/grades_grader1.csv
    python evals/grade.py --grader 2      # Enzo  -> evals/grades_grader2.csv
    python evals/grade.py --merge         # after BOTH are done: copies the two files into evals/golden_30.csv

Each person grades on their own, without talking to the other. The tool never shows the other grader's verdicts
and never proposes an answer. SENDABLE = the five criteria of evals/README.md are all YES. Resumable (Ctrl-C is safe).
"""
import argparse, csv, os, sys

CRIT = [
    "1 Right top 3: at least 2 of the 3 themes are in the reference top 3 (a hand-over row: NO)",
    "2 Evidence real and varied: complete negative reviews, relevant, the 2 quotes of a theme are different",
    "3 Both quarters named, with a count for each",
    "4 No guest/staff name, no other hotel or review id outside the [R-xxxxx] links (a '[name] at reception' is a NO)",
    "5 Neutral B2B tone, no blame on a person, no promise, no recommendation",
]
FIELDS = ["id", "sendable_yes_no", "failed_criteria", "comment"]


def load(path):
    return list(csv.DictReader(open(path, encoding="utf-8")))


def ask(prompt):
    while True:
        a = input(prompt).strip().lower()
        if a in ("y", "yes", "n", "no"):
            return a[0] == "y"
        print("  answer y or n")


def grade(n, gold, out):
    done = {r["id"] for r in load(out)} if os.path.exists(out) else set()
    new = not os.path.exists(out)
    todo = [r for r in gold if r["id"] not in done]
    print(f"Grader {n}: {len(done)} done, {len(todo)} to go. Keep evals/README.md open. Ctrl-C to pause.\n")
    with open(out, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        for k, r in enumerate(todo, 1):
            print("=" * 78)
            print(f"[{len(done) + k}/{len(gold)}]  {r['id']}  ({r['segment']})")
            print(f"TICKET   : {r['ticket']}")
            print(f"REFERENCE: {r['reference_top3']}")
            print("-" * 78)
            print(r["draft"].replace("⏎", "\n"))
            print("-" * 78)
            failed = [str(i + 1) for i, c in enumerate(CRIT) if not ask(f"  {c}\n  YES? [y/n] ")]
            comment = input("  one-line comment (required if NO, else Enter): ").strip() if failed else ""
            w.writerow({"id": r["id"], "sendable_yes_no": "no" if failed else "yes",
                        "failed_criteria": " ".join(failed), "comment": comment})
            f.flush()
            print(f"  -> {'NOT sendable (criteria ' + ' '.join(failed) + ')' if failed else 'SENDABLE'}\n")
    print("Finished. Commit your own file only.")


def merge(gold_path="evals/golden_30.csv"):
    gold = load(gold_path)
    g = {n: {r["id"]: r for r in load(f"evals/grades_grader{n}.csv")} for n in (1, 2)
         if os.path.exists(f"evals/grades_grader{n}.csv")}
    if len(g) < 2 or any(len(v) < len(gold) for v in g.values()):
        sys.exit("Both graders must have graded all rows first. Nothing merged.")
    for r in gold:
        r["grader_1_sendable_yes_no"] = g[1][r["id"]]["sendable_yes_no"]
        r["grader_2_sendable_yes_no"] = g[2][r["id"]]["sendable_yes_no"]
        c = [f"G{n}: {g[n][r['id']]['comment']}" for n in (1, 2) if g[n][r["id"]]["comment"]]
        r["comment"] = " | ".join(c)
    with open(gold_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(gold[0].keys()))
        w.writeheader(); w.writerows(gold)
    print(f"Merged into {gold_path}. Now: python evals/agreement.py")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--grader", type=int, choices=(1, 2))
    ap.add_argument("--merge", action="store_true")
    ap.add_argument("--gold", default="evals/golden_30.csv")
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.merge:
        merge(a.gold)
    elif a.grader:
        grade(a.grader, load(a.gold), a.out or f"evals/grades_grader{a.grader}.csv")
    else:
        ap.error("use --grader 1|2 or --merge")

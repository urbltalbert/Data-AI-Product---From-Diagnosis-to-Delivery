"""Choose the detection threshold on the VALIDATION tickets (data/tickets_val.csv), never on the eval-set. Spec v2.

Rule: the lowest threshold whose precision on 'rating_drop' is 1.00 on the validation set (a wrong draft is worse than a hand-over);
ties broken by the highest recall. Writes prototype/threshold.txt. Run from the repo root.
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pandas as pd
import detect


def main():
    detect.train()
    val = pd.read_csv("data/tickets_val.csv")
    preds = [detect.predict(t) for t in val["text"]]
    best = None
    print("threshold  precision  recall")
    for th in [x / 100 for x in range(50, 100, 5)]:
        sel = [(l == "rating_drop" and c >= th) for l, c in preds]
        tp = sum(s and y == "rating_drop" for s, y in zip(sel, val["label"]))
        prec = tp / sum(sel) if sum(sel) else 1.0
        rec = tp / (val["label"] == "rating_drop").sum()
        print(f"{th:9.2f}  {prec:9.2f}  {rec:6.2f}")
        if prec == 1.0 and (best is None or rec > best[1]):
            best = (th, rec)
    th = best[0] if best else 0.70
    open("prototype/threshold.txt", "w").write(f"{th}\n")
    print(f"chosen threshold {th} (validation recall {best[1] if best else 'n/a'})")


if __name__ == "__main__":
    main()

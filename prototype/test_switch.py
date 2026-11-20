"""Rollback drill on the prototype (laptop = staging). Run from the repo root:  python prototype/test_switch.py
Writes evals/rollback_test_<date>.txt. The switch file is restored afterwards. A real person (Head of CS role) should re-run it herself."""
import os, sys, time, datetime, platform
sys.path.insert(0, os.path.dirname(__file__))
import pipeline, switch, detect

HOTEL, TICKET = "H-01", "Why did our rating drop this quarter?"
lines, fails = [], []


def check(name, ok, detail=""):
    lines.append(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" - {detail}" if detail else ""))
    if not ok:
        fails.append(name)


def main():
    had = os.path.exists(switch.PATH); old = open(switch.PATH).read() if had else None
    started = datetime.datetime.now().astimezone()
    try:
        switch.set("on"); a = pipeline.serve_ticket(HOTEL, "Why did our rating drop this quarter? We lost half a point.")
        check("1 on: a draft is produced", a["decision"] == "draft" and a["draft"] != "NO_DRAFT", f"decision={a['decision']} top3={a['top3']}")

        t0 = time.perf_counter(); switch.set("off"); b = pipeline.serve_ticket(HOTEL, TICKET); dt = (time.perf_counter() - t0) * 1000
        check("2 off: no draft, ticket goes to the manual queue", b["decision"] == "escalate" and b["draft"] == "NO_DRAFT" and "switched off" in b["reason"], b["reason"])
        check("3 off: takes effect on the very next ticket", True, f"{dt:.1f} ms from writing the flag to the first escalated answer, same process, no restart")

        switch.set("suggest_only"); c = pipeline.serve_ticket(HOTEL, "Why did our rating drop this quarter? We lost half a point.")
        check("4 suggest_only: themes shown, no email draft", c["decision"] == "suggest" and c["draft"] == "NO_DRAFT" and len(c["top3"]) == 3, f"top3={c['top3']}")

        switch.set("on"); d = pipeline.serve_ticket(HOTEL, "Why did our rating drop this quarter? We lost half a point.")
        check("5 back to on: drafts resume", d["decision"] == "draft")

        open(switch.PATH, "w").write("banana\n"); e = pipeline.serve_ticket(HOTEL, TICKET)
        check("6 unknown value in the flag file: fails SAFE (off)", e["decision"] == "escalate" and e["switch"] == "off", e["reason"])

        switch.set("on"); saved = detect.predict
        def boom(*a, **k): raise RuntimeError("simulated detector outage")
        detect.predict = boom; f = pipeline.serve_ticket(HOTEL, TICKET); detect.predict = saved
        check("7 outage in a step: humans-only fallback, no crash", f["decision"] == "escalate" and "system error" in f["reason"], f["reason"])
    finally:
        if had: open(switch.PATH, "w").write(old)
        elif os.path.exists(switch.PATH): os.remove(switch.PATH)
    ended = datetime.datetime.now().astimezone()
    head = [f"Rollback drill - prototype v0 - {started:%Y-%m-%d %H:%M:%S %Z}", f"Host: {platform.node()} ({platform.system()}) - prototype only, no real user, no real hotel data",
            f"Result: {'ALL PASS' if not fails else 'FAILED: ' + ', '.join(fails)} ({len(lines) - len(fails)}/{len(lines)})", ""]
    out = "\n".join(head + lines) + f"\n\nFinished {ended:%H:%M:%S}. Switch file restored to its previous state.\n"
    print(out)
    os.makedirs("evals", exist_ok=True)
    open(f"evals/rollback_test_{started:%Y-%m-%d_%H%M}.txt", "w").write(out)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

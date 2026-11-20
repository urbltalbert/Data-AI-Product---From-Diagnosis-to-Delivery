"""The override switch ⏻ (spec v2). Three positions, read on EVERY call so a change takes effect on the next ticket.

  on            full workflow (detect -> eligibility -> themes -> draft -> policy)
  suggest_only  themes and counts are shown to the account manager, NO email draft is produced (L1)
  off           nothing runs; every ticket goes to the manual queue, as before the product existed

State lives in prototype/switch.txt (git-ignored). A missing file means "on"; an UNREADABLE or UNKNOWN value means "off" (fail safe).
"""
import os

PATH = os.path.join(os.path.dirname(__file__), "switch.txt")
POSITIONS = ("on", "suggest_only", "off")


def get():
    if not os.path.exists(PATH):
        return "on"
    try:
        v = open(PATH).read().strip().lower()
    except OSError:
        return "off"
    return v if v in POSITIONS else "off"


def set(position):
    if position not in POSITIONS:
        raise ValueError(f"position must be one of {POSITIONS}")
    with open(PATH, "w") as f:
        f.write(position + "\n")

# prototype — Review Insights (v0)

Four-step workflow, no agent loop. Run from the repo root:

```
pip install pandas scikit-learn
python data/make_train.py       # detector training (300) and validation (40) tickets, invented
python prototype/tune_threshold.py   # threshold chosen on the validation tickets, never on the eval-set
python data/make_data.py        # regenerates data/reviews_synthetic.csv and C21-C50 of the eval-set (seeded)
python prototype/evals.py       # headline number -> evals/eval_output_v0.txt, grading sheet -> evals/grading_sheet_v0.csv
python prototype/evals.py --skip-detect   # DIAGNOSTIC ONLY: bypasses step 1 to localise a failure, never a result
```

| File | Step | Rung |
|---|---|---|
| `detect.py` | 1 detect the request | 2 — TF-IDF + logistic regression (`data/tickets_train.csv`, 300 tickets; threshold from `data/tickets_val.csv`) |
| `rules.py` | 2 eligibility + review extraction | 1 — rules (≥ 50 reviews in Q3, English, one `hotel_id`) |
| `themes.py` + `draft.py` | 3 themes, delta, draft | v0: keyword lexicon + template (no API key). Brief target: rung 3 (LLM) |
| `policy.py` | 4 policy check | 1 — rules (names, other hotel ids, promises) |
| `pipeline.py` | wiring | chaining with gates |

All data is invented. No real customer data.

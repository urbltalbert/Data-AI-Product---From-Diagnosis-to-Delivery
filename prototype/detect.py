"""Step 1 — detect the request (rung 2: TF-IDF + logistic regression). Spec §2.1."""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

MODEL = None


def train(csv_path="data/tickets_train.csv"):
    global MODEL
    df = pd.read_csv(csv_path)
    MODEL = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), LogisticRegression(max_iter=1000))
    MODEL.fit(df["text"], df["label"])
    return MODEL


def predict(text):
    """Return (label, confidence). label in {rating_drop, other}; confidence = max predict_proba."""
    if MODEL is None:
        train()
    proba = MODEL.predict_proba([text])[0]
    i = proba.argmax()
    return MODEL.classes_[i], float(proba[i])

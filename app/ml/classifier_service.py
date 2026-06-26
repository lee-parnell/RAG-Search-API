import pickle
from pathlib import Path

MODEL_PATH = Path("app/ml/classifier.pkl")

with open(MODEL_PATH, "rb") as f:
    data = pickle.load(f)
    model = data["model"]
    vectorizer = data["vectorizer"]


def classify_query(query: str) -> str:
    vec = vectorizer.transform([query])
    prediction = model.predict(vec)
    return prediction[0]
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

MODEL_FILE = "model/match_model.pkl"

def retrain_model():
    df = pd.read_csv("data/matches.csv")
    X = df["Grad_Skills"] + " " + df["Job_Skills"]
    y = df["Match"]

    vectorizer = TfidfVectorizer()
    X_vec = vectorizer.fit_transform(X)

    model = LogisticRegression()
    model.fit(X_vec, y)

    os.makedirs("model", exist_ok=True)
    joblib.dump((model, vectorizer), MODEL_FILE)

def predict_matches(grad_skills, employer_df):
    if not os.path.exists(MODEL_FILE):
        retrain_model()
    model, vectorizer = joblib.load(MODEL_FILE)

    results = []
    for idx, row in employer_df.iterrows():
        combined_text = grad_skills + " " + row["Skills"]
        X = vectorizer.transform([combined_text])
        prob = model.predict_proba(X)[0][1]
        results.append((row["Company"], row["Job Title"], row["Skills"], prob))

    sorted_matches = sorted(results, key=lambda x: x[3], reverse=True)
    return pd.DataFrame(sorted_matches[:5], columns=["Company", "Job", "Required Skills", "Match Score"])

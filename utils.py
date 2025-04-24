import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

MODEL_FILE = "model/match_model.pkl"
MATCH_FILE = "data/matches.csv"

def retrain_model():
    if not os.path.exists(MATCH_FILE) or os.path.getsize(MATCH_FILE) == 0:
        print("🚫 No match data available to train the model.")
        return

    df = pd.read_csv(MATCH_FILE)
    if df.empty or "Grad_Skills" not in df.columns or "Job_Skills" not in df.columns or "Match" not in df.columns:
        print("🚫 Match file is invalid or missing required columns.")
        return

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
        if not os.path.exists(MODEL_FILE):
            raise Exception("Model not trained. No match data available.")

    model, vectorizer = joblib.load(MODEL_FILE)

    results = []
    for _, row in employer_df.iterrows():
        combined_text = grad_skills + " " + row["Skills"]
        X = vectorizer.transform([combined_text])
        prob = model.predict_proba(X)[0][1]
        results.append((row["Company"], row["Job Title"], row["Skills"], prob))

    sorted_results = sorted(results, key=lambda x: x[3], reverse=True)
    return pd.DataFrame(sorted_results[:5], columns=["Company", "Job", "Required Skills", "Match Score"])

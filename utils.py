import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def preprocess_text(text):
    return text.lower().replace(",", " ")

def match_candidates(employer, grads):
    vectorizer = TfidfVectorizer()
    grads["combined"] = grads["Skills"] + " " + grads["Research Area"]
    employer_input = preprocess_text(employer["Skills"] + " " + employer["Research Field"])
    tfidf_matrix = vectorizer.fit_transform(grads["combined"].tolist() + [employer_input])
    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
    grads["Match Score"] = similarity_scores
    return grads.sort_values("Match Score", ascending=False).head(5)

def match_employers(grad, employers):
    vectorizer = TfidfVectorizer()
    employers["combined"] = employers["Skills"] + " " + employers["Research Field"]
    grad_input = preprocess_text(grad["Skills"] + " " + grad["Research Area"])
    tfidf_matrix = vectorizer.fit_transform(employers["combined"].tolist() + [grad_input])
    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
    employers["Match Score"] = similarity_scores
    return employers.sort_values("Match Score", ascending=False).head(5)

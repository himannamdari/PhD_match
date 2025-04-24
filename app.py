import streamlit as st
import pandas as pd
import os
from utils import retrain_model, predict_matches

# File paths
os.makedirs("data", exist_ok=True)
GRAD_FILE = "data/graduates.csv"
EMPLOYER_FILE = "data/employers.csv"
MATCH_FILE = "data/matches.csv"

# Create match sample file if missing
if not os.path.exists(MATCH_FILE):
    sample_data = pd.DataFrame({
        "Grad_Skills": ["machine learning", "quantum physics", "data science"],
        "Job_Skills": ["deep learning", "theoretical physics", "python, statistics"],
        "Match": [1, 1, 0]
    })
    sample_data.to_csv(MATCH_FILE, index=False)

st.set_page_config(page_title="PhDMatch", layout="centered")
st.title("🎓 PhDMatch")

user_type = st.radio("I am a...", ["PhD Graduate", "Employer"])

# ----------------------- PhD GRADUATE FORM ------------------------
if user_type == "PhD Graduate":
    st.subheader("👨‍🎓 Graduate Profile Submission")

    name = st.text_input("Full Name")
    skills = st.text_input("Skills (comma-separated)")
    research = st.selectbox("Research Area", [
        "Machine Learning", "AI & NLP", "Physics", "Chemistry", "Biology", "Cybersecurity", "Robotics", "Other"
    ])
    role = st.selectbox("Preferred Roles", [
        "Research Scientist", "Data Scientist", "Machine Learning Engineer", "Postdoc", "Software Developer", "Other"
    ])

    if st.button("📤 Submit Profile"):
        new_row = pd.DataFrame([[name, skills, research, role]],
                               columns=["Name", "Skills", "Research", "Preferred Role"])
        if not os.path.exists(GRAD_FILE):
            new_row.to_csv(GRAD_FILE, index=False)
        else:
            new_row.to_csv(GRAD_FILE, mode='a', header=False, index=False)
        st.success("✅ Profile submitted!")

        # Predict Matches
        if os.path.exists(EMPLOYER_FILE) and os.path.getsize(EMPLOYER_FILE) > 0:
            employers = pd.read_csv(EMPLOYER_FILE)
            matches = predict_matches(skills, employers)
            st.write("🔍 Top Matching Jobs:")
            st.dataframe(matches)
        else:
            st.warning("⚠️ No employer data available yet.")

# ------------------------- EMPLOYER FORM --------------------------
elif user_type == "Employer":
    st.subheader("🏢 Employer Job Posting")

    company = st.text_input("Company Name")
    job = st.selectbox("Job Title", [
        "AI Researcher", "Software Engineer", "R&D Scientist", "Data Analyst", "Postdoctoral Fellow", "Other"
    ])
    desired = st.text_input("Desired Skills (comma-separated)")

    if st.button("📤 Submit Job"):
        new_row = pd.DataFrame([[company, job, desired]],
                               columns=["Company", "Job Title", "Skills"])
        if not os.path.exists(EMPLOYER_FILE):
            new_row.to_csv(EMPLOYER_FILE, index=False)
        else:
            new_row.to_csv(EMPLOYER_FILE, mode='a', header=False, index=False)
        st.success("✅ Job Submitted!")


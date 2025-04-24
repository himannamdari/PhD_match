import streamlit as st
import pandas as pd
import os
from utils import retrain_model, predict_matches

# File paths
os.makedirs("data", exist_ok=True)
GRAD_FILE = "data/graduates.csv"
EMPLOYER_FILE = "data/employers.csv"
MATCH_FILE = "data/matches.csv"

# Create initial match file if not exists
if not os.path.exists(MATCH_FILE):
    sample_data = pd.DataFrame({
        "Grad_Skills": ["machine learning", "quantum physics", "data science"],
        "Job_Skills": ["deep learning", "theoretical physics", "python, statistics"],
        "Match": [1, 1, 0]
    })
    sample_data.to_csv(MATCH_FILE, index=False)

st.title("🎓 PhDMatch")

user_type = st.radio("I am a...", ["PhD Graduate", "Employer"])

if user_type == "PhD Graduate":
    name = st.text_input("Full Name")
    skills = st.text_input("Skills (comma-separated)")
    research = st.text_input("Research Area")
    role = st.text_input("Preferred Roles")

    if st.button("📤 Submit Profile"):
        new_row = pd.DataFrame([[name, skills, research, role]],
                               columns=["Name", "Skills", "Research", "Preferred Role"])
        if not os.path.exists(GRAD_FILE):
            new_row.to_csv(GRAD_FILE, index=False)
        else:
            new_row.to_csv(GRAD_FILE, mode='a', header=False, index=False)
        st.success("Submitted!")

        # Reload employer data
        if os.path.exists(EMPLOYER_FILE):
            employers = pd.read_csv(EMPLOYER_FILE)
            matches = predict_matches(skills, employers)
            st.write("Top Matching Jobs:")
            st.dataframe(matches)

elif user_type == "Employer":
    company = st.text_input("Company Name")
    job = st.text_input("Job Title")
    desired = st.text_input("Desired Skills (comma-separated)")

    if st.button("📤 Submit Job"):
        new_row = pd.DataFrame([[company, job, desired]],
                               columns=["Company", "Job Title", "Skills"])
        if not os.path.exists(EMPLOYER_FILE):
            new_row.to_csv(EMPLOYER_FILE, index=False)
        else:
            new_row.to_csv(EMPLOYER_FILE, mode='a', header=False, index=False)
        st.success("Job Submitted!")

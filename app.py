import streamlit as st
import pandas as pd
import os
from utils import retrain_model, predict_matches

# File paths
os.makedirs("data", exist_ok=True)
GRAD_FILE = "data/graduates.csv"
EMPLOYER_FILE = "data/employers.csv"
MATCH_FILE = "data/matches.csv"
MODEL_FILE = "model/match_model.pkl"

# Initialize match dataset if not exists
if not os.path.exists(MATCH_FILE):
    sample_data = pd.DataFrame({
        "Grad_Skills": ["machine learning", "quantum physics", "data science"],
        "Job_Skills": ["deep learning, python", "theoretical physics", "python, statistics"],
        "Match": [1, 1, 0]
    })
    sample_data.to_csv(MATCH_FILE, index=False)

# App setup
st.set_page_config(page_title="PhDMatch", layout="centered")
st.title("🎓 PhDMatch")

user_type = st.radio("I am a...", ["PhD Graduate", "Employer"])

skills_list = [
    "python", "tensorflow", "pytorch", "nlp", "deep learning",
    "cv", "sql", "bioinformatics", "c++", "data mining"
]

research_areas = [
    "Machine Learning", "AI & NLP", "Physics", "Chemistry", "Biology",
    "Cybersecurity", "Robotics", "Environmental Science", "Mathematics", "Other"
]

preferred_roles = [
    "Research Scientist", "Data Scientist", "Machine Learning Engineer",
    "Postdoc", "Software Developer", "AI Researcher", "Other"
]

job_titles = [
    "AI Researcher", "Software Engineer", "R&D Scientist",
    "Data Analyst", "Postdoctoral Fellow", "Systems Engineer", "Other"
]

# Graduate form
if user_type == "PhD Graduate":
    st.subheader("👨‍🎓 Graduate Profile Submission")

    name = st.text_input("Full Name")
    skills_selected = st.multiselect("Select Your Skills", skills_list)
    skills = ", ".join(skills_selected)
    research = st.selectbox("Research Area", research_areas)
    role = st.selectbox("Preferred Roles", preferred_roles)

    if st.button("📤 Submit Profile"):
        new_row = pd.DataFrame([[name, skills, research, role]],
                               columns=["Name", "Skills", "Research", "Preferred Role"])
        if not os.path.exists(GRAD_FILE):
            new_row.to_csv(GRAD_FILE, index=False)
        else:
            new_row.to_csv(GRAD_FILE, mode='a', header=False, index=False)
        st.success("✅ Profile submitted!")

        if os.path.exists(EMPLOYER_FILE) and os.path.getsize(EMPLOYER_FILE) > 0:
            employers = pd.read_csv(EMPLOYER_FILE)
            matches = predict_matches(skills, employers)
            st.write("🔍 Top Matching Jobs:")
            st.dataframe(matches)
        else:
            st.warning("⚠️ No employer data available yet.")

# Employer form
elif user_type == "Employer":
    st.subheader("🏢 Employer Job Posting")

    company = st.text_input("Company Name")
    job = st.selectbox("Job Title", job_titles)
    desired_selected = st.multiselect("Desired Skills", skills_list)
    desired = ", ".join(desired_selected)

    if st.button("📤 Submit Job"):
        new_row = pd.DataFrame([[company, job, desired]],
                               columns=["Company", "Job Title", "Skills"])
        if not os.path.exists(EMPLOYER_FILE):
            new_row.to_csv(EMPLOYER_FILE, index=False)
        else:
            new_row.to_csv(EMPLOYER_FILE, mode='a', header=False, index=False)
        st.success("✅ Job Submitted!")

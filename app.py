import streamlit as st
import pandas as pd
import os
from utils import retrain_model, predict_matches

# File paths
os.makedirs("data", exist_ok=True)
os.makedirs("model", exist_ok=True)
GRAD_FILE = "data/graduates.csv"
EMPLOYER_FILE = "data/employers.csv"
MATCH_FILE = "data/matches.csv"
MODEL_FILE = "model/match_model.pkl"

# Initialize match dataset if not exists or is empty
if not os.path.exists(MATCH_FILE) or os.path.getsize(MATCH_FILE) == 0:
    sample_data = pd.DataFrame({
        "Grad_Skills": ["machine learning", "quantum physics", "data science", "python", "nlp"] * 200,
        "Job_Skills": ["deep learning, python", "theoretical physics", "python, statistics", "tensorflow, keras", "nlp, pytorch"] * 200,
        "Match": [1, 1, 0, 1, 1] * 200
    })
    sample_data.to_csv(MATCH_FILE, index=False)

# Retrain if match file has grown significantly
if os.path.exists(MATCH_FILE):
    match_size = len(pd.read_csv(MATCH_FILE))
    if (not os.path.exists(MODEL_FILE)) or match_size > 1000:
        with st.spinner("🔄 Training model..."):
            try:
                retrain_model()
                st.success("✅ Model training completed.")
            except Exception as e:
                st.error(f"🔴 Model training failed: {e}")

# App setup
st.set_page_config(page_title="PhDMatch", layout="centered")
st.title("🎓 PhDMatch")

# Admin dashboard access
if st.sidebar.checkbox("🛠 Admin Dashboard"):
    st.sidebar.subheader("📊 View Submitted Data")
    tab = st.sidebar.radio("Choose Dataset", ["Graduates", "Employers", "Matches"])
    if tab == "Graduates" and os.path.exists(GRAD_FILE):
        st.subheader("All Submitted Graduates")
        st.dataframe(pd.read_csv(GRAD_FILE))
    elif tab == "Employers" and os.path.exists(EMPLOYER_FILE):
        st.subheader("All Submitted Employers")
        st.dataframe(pd.read_csv(EMPLOYER_FILE))
    elif tab == "Matches" and os.path.exists(MATCH_FILE):
        st.subheader("Labeled Match Data")
        st.dataframe(pd.read_csv(MATCH_FILE))

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

locations = ["Remote", "Hybrid", "On-site", "Flexible"]
shifts = ["Full-time", "Part-time", "Internship", "Contract"]
sponsorship = ["Yes", "No", "Maybe"]
relocation = ["Yes", "No", "Offered"]

# Unified form fields for both types
import random
user_id = str(random.randint(100000, 999999))
st.text_input("Generated Unique ID", value=user_id, disabled=True)
name_or_company = st.text_input("Full Name / Company Name")
jobs_selected = st.multiselect("Job Titles / Preferred Roles", job_titles + preferred_roles)
job_roles = ", ".join(jobs_selected)
skills_selected = st.multiselect("Select Your Skills", skills_list)
skills = ", ".join(skills_selected)
research_selected = st.multiselect("Research Areas", research_areas)
research = ", ".join(research_selected)
location_selected = st.multiselect("Preferred Locations", locations)
location = ", ".join(location_selected)
shift_selected = st.multiselect("Work Shifts", shifts)
shift = ", ".join(shift_selected)
salary = st.text_input("Salary Range or Expectation")
sponsor = st.multiselect("Visa Sponsorship Available?", sponsorship)
relocation_support = st.multiselect("Relocation Support", relocation)

if user_type == "PhD Graduate":
    if st.button("📤 Submit Profile"):
        new_row = pd.DataFrame([[user_id, name_or_company, job_roles, skills, research, location, shift, salary, ", ".join(sponsor), ", ".join(relocation_support)]],
                               columns=["UserID", "Name", "Preferred Role", "Skills", "Research", "Location", "Shift", "Salary", "Sponsorship", "Relocation"])
        if not os.path.exists(GRAD_FILE):
            new_row.to_csv(GRAD_FILE, index=False)
        else:
            new_row.to_csv(GRAD_FILE, mode='a', header=False, index=False)
        st.success("✅ Profile submitted!")

        if os.path.exists(EMPLOYER_FILE) and os.path.getsize(EMPLOYER_FILE) > 0:
            employers = pd.read_csv(EMPLOYER_FILE)
            try:
                matches = predict_matches(skills, employers)
                st.write("🔍 Top Matching Jobs:")
                selected = st.dataframe(matches)
                feedback = st.radio("Rate match quality for future improvement:", ["Great Match", "Okay", "Not Useful"])
                if feedback and st.button("✅ Submit Feedback"):
                    match_row = matches.iloc[0]
                    new_feedback = pd.DataFrame([[skills, match_row["Required Skills"], 1 if feedback == "Great Match" else 0]],
                                                columns=["Grad_Skills", "Job_Skills", "Match"])
                    new_feedback.to_csv(MATCH_FILE, mode='a', header=False, index=False)
                    st.success("📬 Feedback saved!")
            except Exception as e:
                st.error(f"🔴 Failed to predict matches: {str(e)}")
        else:
            st.warning("⚠️ No employer data available yet.")

elif user_type == "Employer":
    if st.button("📤 Submit Job"):
        new_row = pd.DataFrame([[user_id, name_or_company, job_roles, skills, research, location, shift, salary, ", ".join(sponsor), ", ".join(relocation_support)]],
                               columns=["JobID", "Company", "Job Title", "Skills", "Research", "Location", "Shift", "Salary", "Sponsorship", "Relocation"])
        if not os.path.exists(EMPLOYER_FILE):
            new_row.to_csv(EMPLOYER_FILE, index=False)
        else:
            new_row.to_csv(EMPLOYER_FILE, mode='a', header=False, index=False)
        st.success("✅ Job Submitted!")

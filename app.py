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

# Trigger training of model if it doesn't exist
if not os.path.exists(MODEL_FILE):
    try:
        retrain_model()
    except Exception as e:
        st.error(f"🔴 Model training failed: {e}")

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

locations = ["Remote", "Hybrid", "On-site", "Flexible"]
shifts = ["Full-time", "Part-time", "Internship", "Contract"]
sponsorship = ["Yes", "No", "Maybe"]
relocation = ["Yes", "No", "Offered"]

# Graduate form
if user_type == "PhD Graduate":
    st.subheader("👨‍🎓 Graduate Profile Submission")

    name = st.text_input("Full Name")
    skills_selected = st.multiselect("Select Your Skills", skills_list)
    skills = ", ".join(skills_selected)
    research_selected = st.multiselect("Research Areas", research_areas)
    research = ", ".join(research_selected)
    roles_selected = st.multiselect("Preferred Roles", preferred_roles)
    role = ", ".join(roles_selected)

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
            try:
                matches = predict_matches(skills, employers)
                st.write("🔍 Top Matching Jobs:")
                st.dataframe(matches)
            except Exception as e:
                st.error(f"🔴 Failed to predict matches: {str(e)}")
        else:
            st.warning("⚠️ No employer data available yet.")

# Employer form
elif user_type == "Employer":
    st.subheader("🏢 Employer Job Posting")

    company = st.text_input("Company Name")
    jobs_selected = st.multiselect("Job Titles", job_titles)
    job = ", ".join(jobs_selected)
    desired_selected = st.multiselect("Desired Skills", skills_list)
    desired = ", ".join(desired_selected)
    location_selected = st.multiselect("Job Location Options", locations)
    location = ", ".join(location_selected)
    shift_selected = st.multiselect("Work Shifts", shifts)
    shift = ", ".join(shift_selected)
    salary = st.text_input("Salary Range (e.g., $60k–$90k)")
    sponsor = st.multiselect("Visa Sponsorship Available?", sponsorship)
    relocation_support = st.multiselect("Relocation Support", relocation)

    if st.button("📤 Submit Job"):
        new_row = pd.DataFrame([[company, job, desired, location, shift, salary, ", ".join(sponsor), ", ".join(relocation_support)]],
                               columns=["Company", "Job Title", "Skills", "Location", "Shift", "Salary", "Sponsorship", "Relocation"])
        if not os.path.exists(EMPLOYER_FILE):
            new_row.to_csv(EMPLOYER_FILE, index=False)
        else:
            new_row.to_csv(EMPLOYER_FILE, mode='a', header=False, index=False)
        st.success("✅ Job Submitted!")

import streamlit as st
import pandas as pd
import os

# Create data folder if it doesn't exist
os.makedirs("data", exist_ok=True)

# File paths
GRAD_FILE = "data/graduates.csv"
EMPLOYER_FILE = "data/employers.csv"

# App Title
st.set_page_config(page_title="PhDMatch", layout="centered")
st.title("🎓 PhDMatch: Build a Bridge Between PhD Talent and Employers")

st.markdown("This platform collects structured input from PhD graduates and employers to build a smart dataset for job matching and future AI-powered recommendations.")

# User type selector
user_type = st.radio("I am a...", ["PhD Graduate", "Employer"])

if user_type == "PhD Graduate":
    st.subheader("👨‍🎓 Graduate Profile Submission")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    research_area = st.text_input("Research Area (e.g., Machine Learning, Bioinformatics)")
    skills = st.text_input("Key Skills (comma-separated)")
    tools = st.text_input("Tools/Software Used (e.g., Python, R, TensorFlow)")
    preferred_roles = st.text_input("Preferred Job Titles")
    open_to_industry = st.checkbox("Open to Industry Roles", value=True)

    if st.button("📤 Submit My Profile"):
        grad_data = pd.DataFrame([[name, email, research_area, skills, tools, preferred_roles, open_to_industry]],
                                 columns=["Name", "Email", "Research Area", "Skills", "Tools", "Preferred Roles", "Open to Industry"])
        
        # Append to existing file or create new
        if not os.path.isfile(GRAD_FILE):
            grad_data.to_csv(GRAD_FILE, index=False)
        else:
            grad_data.to_csv(GRAD_FILE, mode='a', header=False, index=False)
        
        st.success("✅ Profile submitted successfully! Thank you for contributing.")

elif user_type == "Employer":
    st.subheader("🏢 Employer Job Posting")
    company_name = st.text_input("Company Name")
    contact_email = st.text_input("Contact Email")
    job_title = st.text_input("Job Title")
    research_field = st.text_input("Related Research Area")
    desired_skills = st.text_input("Desired Skills (comma-separated)")
    tools_required = st.text_input("Preferred Tools/Software")
    accepts_new_phds = st.checkbox("Open to Fresh PhD Graduates", value=True)

    if st.button("📤 Submit Job Opening"):
        employer_data = pd.DataFrame([[company_name, contact_email, job_title, research_field, desired_skills, tools_required, accepts_new_phds]],
                                     columns=["Company", "Email", "Job Title", "Research Field", "Skills", "Tools", "Accepts New PhDs"])
        
        if not os.path.isfile(EMPLOYER_FILE):
            employer_data.to_csv(EMPLOYER_FILE, index=False)
        else:
            employer_data.to_csv(EMPLOYER_FILE, mode='a', header=False, index=False)
        
        st.success("✅ Job opening submitted! Thanks for supporting early-career researchers.")

---

### 🚀 Next Steps:
- [ ] Add **data validation**
- [ ] Add **admin dashboard** to view entries
- [ ] Build a **training pipeline** to develop ML-based matching later
- [ ] Enable **user login** if needed

Would you like me to zip the updated project for GitHub upload, or continue to help you build the training component next?

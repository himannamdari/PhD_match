import streamlit as st
import pandas as pd
from utils import match_candidates, match_employers

st.set_page_config(page_title="PhDMatch", layout="centered")
st.title("🎓 PhDMatch: Connect PhDs with Employers")

user_type = st.radio("I am a...", ["PhD Graduate", "Employer"])

if user_type == "PhD Graduate":
    st.subheader("👨‍🎓 Graduate Profile")
    name = st.text_input("Name")
    research_area = st.text_input("Research Area")
    skills = st.text_input("Key Skills (comma separated)")
    preferred_role = st.text_input("Preferred Job Role")
    
    if st.button("Submit"):
        grad_data = pd.DataFrame([[name, research_area, skills, preferred_role]],
                                 columns=["Name", "Research Area", "Skills", "Preferred Role"])
        grad_data.to_csv("data/graduates.csv", mode='a', header=False, index=False)
        st.success("Profile submitted!")
        
        if st.button("🔍 Find Matching Employers"):
            employers = pd.read_csv("data/employers.csv")
            matches = match_employers(grad_data.iloc[0], employers)
            st.write("Top Matches:")
            st.dataframe(matches)

elif user_type == "Employer":
    st.subheader("🏢 Employer Profile")
    company = st.text_input("Company Name")
    role = st.text_input("Open Position Title")
    desired_skills = st.text_input("Desired Skills (comma separated)")
    research_field = st.text_input("Relevant Research Fields")
    
    if st.button("Submit"):
        employer_data = pd.DataFrame([[company, role, desired_skills, research_field]],
                                     columns=["Company", "Role", "Skills", "Research Field"])
        employer_data.to_csv("data/employers.csv", mode='a', header=False, index=False)
        st.success("Employer profile saved!")

        if st.button("🔍 Find Matching Candidates"):
            grads = pd.read_csv("data/graduates.csv")
            matches = match_candidates(employer_data.iloc[0], grads)
            st.write("Top Matches:")
            st.dataframe(matches)

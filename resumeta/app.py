import streamlit as st
import requests
import os
from dotenv import load_dotenv
from resumeta.models.resume import Resume, Employment, Institution, Education
import json

load_dotenv()  # take environment variables from .env.

API_URL = os.environ.get("API_URL")

# from resumeta.database import init_db


def format_resume(resume):
    return resume["name"]


st.set_page_config(page_title="Resumeta", layout="wide")

st.header("Resumes")
resumes = requests.get(f"{API_URL}/resumes", timeout=5).json()
# resume_name = [resume["name"] for resume in resumes]
resume_json = st.selectbox(
    "Resume:",
    options=resumes,
    format_func=format_resume,
    placeholder="Select a resume",
)
resume_id = resume_json["_id"]
resume = Resume.model_validate(resume_json)
st.divider()
if resume:
    with st.container(border=1):
        st.header(resume.user.first_name + " " + resume.user.last_name)
        st.subheader("Employment")
        st.divider()
        if resume.employment:
            with st.container(border=1):
                for i, job in enumerate(resume.employment):
                    st.subheader(job.title)
                    st.write(job.employer.name)
                    # st.write(f"{job.start_date.year} - {job.end_date.year}")
                    if job.activities:
                        for activity in job.activities:
                            st.write(f"- {activity}")

        with st.expander("Add Employment", expanded=False):
            with st.form("add_employment"):
                title = st.text_input("Title")
                start_date = st.date_input("Start Date")
                end_date = st.date_input("End Date")
                employer = st.text_input("Employer")
                activities = st.text_area("Activity")
                activities = activities.split("\n")

                submit = st.form_submit_button("Submit")
                if submit:
                    institution = Institution.model_validate(
                        {"name": employer}
                    )
                    employment = Employment.model_validate(
                        {
                            "title": title,
                            "start_date": start_date,
                            "end_date": end_date,
                            "employer": institution,
                            "activities": activities,
                        }
                    )
                    resume.employment.append(employment)
                    print(employment.model_dump_json())
                    response = requests.post(
                        f"{API_URL}/resumes/{resume_id}/employment",
                        data=employment.model_dump_json(),
                        timeout=5,
                    )
                    if response.status_code == 200:
                        st.success("Employment added successfully.")
                        st.rerun()
                    else:
                        st.error(
                            f"Error adding employment with {response.body}"
                        )
        with st.expander("Delete Employment", expanded=False):
            for i, employment in enumerate(resume.employment):
                st.write(f"{i}, {employment.title}")
            with st.form("delete_employment"):
                index = st.number_input(
                    "Index",
                    min_value=0,
                    max_value=(len(resume.employment) - 1),
                    step=1,
                )
                submit = st.form_submit_button("Submit")
                if submit:
                    response = requests.delete(
                        f"{API_URL}/resumes/{resume_id}/employment/{index}",
                        timeout=5,
                    )
                    if response.status_code == 200:
                        st.success("Employment deleted successfully.")
                        st.rerun()
                    else:
                        st.error(
                            f"Error deleting employment with {response.text}"
                        )

        if resume.education:
            st.subheader("Education")
            st.divider()
            with st.container(border=1):
                for edu in resume.education:
                    st.subheader(edu.degree)
                    st.write(edu.institution.name)
                    st.write(f"{edu.start_date.year} - {edu.end_date.year}")
                    if edu.activities:
                        for activity in edu.activities:
                            st.write(activity)
        with st.expander("Add Education", expanded=False):
            with st.form("add_education"):
                degree = st.text_input("Degree")
                major = st.text_input("Major")
                minor = st.text_input("Minor")
                gpa = st.number_input("GPA", min_value=0.0, max_value=4.0)
                start_date = st.date_input("Start Date")
                end_date = st.date_input("End Date")
                institution = st.text_input("Institution")
                activities = st.text_area("Activity")
                activities = activities.split("\n")

                submit = st.form_submit_button("Submit")
                if submit:
                    institution = Institution.model_validate(
                        {"name": institution}
                    )
                    education = Education.model_validate(
                        {
                            "degree": degree,
                            "major": major,
                            "minor": minor,
                            "gpa": gpa,
                            "start_date": start_date,
                            "end_date": end_date,
                            "institution": institution,
                            "activities": activities,
                        }
                    )
                    resume.education.append(education)
                    response = requests.post(
                        f"{API_URL}/resumes/{resume_id}/education",
                        data=education.model_dump_json(),
                        timeout=5,
                    )
                    if response.status_code == 200:
                        st.success("Education added successfully.")
                    else:
                        st.error(
                            f"Error adding education with {response.text}"
                        )
        with st.expander("Delete Education", expanded=False):
            for i, education in enumerate(resume.education):
                st.write(f"{i}, {education.degree}")
            with st.form("delete_education"):
                index = st.number_input(
                    "Index",
                    min_value=0,
                    max_value=(len(resume.education) - 1),
                    step=1,
                )
                submit = st.form_submit_button("Submit")
                if submit:
                    response = requests.delete(
                        f"{API_URL}/resumes/{resume_id}/education/{index}",
                        timeout=5,
                    )
                    if response.status_code == 200:
                        st.success("Education deleted successfully.")
                        st.rerun()
                    else:
                        st.error(
                            f"Error deleting education with {response.text}"
                        )

from pathlib import Path

import streamlit as st

from utils.pdf_reader import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.text_cleaner import clean_resume_text
from utils.ats_score import calculate_ats_score

RESUME_DIR = Path("resumes")


def save_uploaded_resume(uploaded_file) -> Path:
    RESUME_DIR.mkdir(exist_ok=True)
    resume_path = RESUME_DIR / uploaded_file.name

    with resume_path.open("wb") as file:
        file.write(uploaded_file.getbuffer())

    return resume_path


st.set_page_config(
    page_title="AI Resume Intelligence Platform",
    page_icon=":page_facing_up:",
    layout="wide",
)

st.title("AI Resume Intelligence Platform")
st.subheader("Upload Resume for AI Analysis")

uploaded_file = st.file_uploader(
    "Upload Your Resume (PDF)",
    type=["pdf"],
)

if uploaded_file is None:
    st.info("Upload a PDF resume to begin analysis.")
else:
    resume_path = save_uploaded_resume(uploaded_file)
    st.success("Resume uploaded successfully.")

    extracted_text = extract_text_from_pdf(resume_path)
    cleaned_text = clean_resume_text(extracted_text)
    skills = extract_skills(cleaned_text)
    total_words = len(cleaned_text.split())

    st.subheader("Extracted Resume Text")

    with st.expander("View Extracted Resume Text"):
        st.text_area(
            "Resume Content",
            extracted_text,
            height=300,
        )

    st.subheader("Extracted Skills")

    if skills:
        for skill in skills:
            st.success(skill)
    else:
        st.warning("No skills detected.")

    st.subheader("Resume Statistics")
    st.info(f"Total Words: {total_words}")
    st.info(f"Skills Detected: {len(skills)}")
    st.subheader("Paste Job Description")

    job_description = st.text_area(
        "Enter Job Description",
        height=200,
    )

    if job_description:
        ats_score, matched_keywords, missing_keywords = calculate_ats_score(
            skills,
            job_description,
        )

        st.subheader("ATS Score")
        st.progress(ats_score / 100)
        st.success(f"ATS Score: {ats_score}/100")

        st.subheader("Matched Keywords")
        if matched_keywords:
            for keyword in matched_keywords:
                st.success(keyword)
        else:
            st.warning("No matching keywords found.")

        st.subheader("Missing Keywords")
        if missing_keywords:
            for keyword in missing_keywords:
                st.error(keyword)
        else:
            st.success("No missing keywords!")

        st.subheader("Resume Improvement Suggestions")
        if missing_keywords:
            st.info(
                "Try adding missing skills relevant to the job description."
            )
            st.info(
                "Improve ATS score by including more matching keywords."
            )
        else:
            st.success(
                "Excellent resume match for this job role!"
            )

from pathlib import Path

import streamlit as st

from utils.pdf_reader import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.text_cleaner import clean_resume_text
from utils.ats_score import calculate_ats_score
from utils.resume_feedback import generate_feedback
from utils.career_recommender import recommend_roles


RESUME_DIR = Path("resumes")


def save_uploaded_resume(uploaded_file) -> Path:
    """Save uploaded resume inside resumes folder."""
    RESUME_DIR.mkdir(exist_ok=True)
    resume_path = RESUME_DIR / uploaded_file.name

    with resume_path.open("wb") as file:
        file.write(uploaded_file.getbuffer())

    return resume_path


def show_score_message(score: int):
    """Display ATS score with proper color."""
    st.progress(score / 100)

    if score >= 80:
        st.success(f"ATS Score: {score}/100")
    elif score >= 50:
        st.warning(f"ATS Score: {score}/100")
    else:
        st.error(f"ATS Score: {score}/100")


def show_resume_strength(score: int):
    """Display resume strength based on ATS score."""
    if score >= 80:
        st.success("Strong Resume")
    elif score >= 50:
        st.warning("Moderate Resume")
    else:
        st.error("Weak Resume")


def show_improvement_suggestions(score: int):
    """Display suggestions based on ATS score."""
    if score >= 80:
        st.success("Excellent resume match for this job role.")
        st.info("You can still improve by adding measurable achievements and project impact.")

    elif score >= 50:
        st.warning("Good match, but your resume can be improved.")
        st.info("Add more keywords from the job description.")
        st.info("Mention projects related to the required skills.")
        st.info("Add numbers like accuracy, users served, time saved, or performance improvement.")

    else:
        st.error("Low resume match. Customize your resume for this job description.")
        st.info("Add important skills, tools, and project keywords related to this role.")
        st.info("Use action words like built, developed, implemented, optimized, and deployed.")
        st.info("Paste a complete job description for better ATS analysis.")


st.set_page_config(
    page_title="AI Resume Intelligence Platform",
    page_icon="📄",
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

    if not extracted_text.strip():
        st.error("No text found in this PDF. Please upload a text-based resume PDF.")

    else:
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

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Extracted Skills")

            if skills:
                for skill in skills:
                    st.success(skill)
            else:
                st.warning("No skills detected.")

        with col2:
            st.subheader("Resume Statistics")
            st.info(f"Total Words: {total_words}")
            st.info(f"Skills Detected: {len(skills)}")

        st.subheader("Paste Job Description")

        job_description = st.text_area(
            "Enter Job Description",
            height=200,
            placeholder="Paste full job description here for better ATS analysis...",
        )

        if job_description:
            ats_score, matched_keywords, missing_keywords = calculate_ats_score(
                skills,
                job_description,
            )

            st.subheader("ATS Score")
            show_score_message(ats_score)

            result_col1, result_col2 = st.columns(2)

            with result_col1:
                st.subheader("Matched Keywords")

                if matched_keywords:
                    for keyword in matched_keywords:
                        st.success(keyword)
                else:
                    st.warning("No matching keywords found.")

            with result_col2:
                st.subheader("Missing Keywords")

                if missing_keywords:
                    for keyword in missing_keywords:
                        st.error(keyword)

                elif ats_score < 50:
                    st.warning(
                        "No missing keywords found from the current job description, "
                        "but the job description may be too short. Paste a complete job description."
                    )

                else:
                    st.info("No missing keywords found from the current skills database.")

            feedback = generate_feedback(
                ats_score,
                missing_keywords,
            )

            st.subheader("AI Resume Feedback")

            for item in feedback:
                st.info(item)

            role_col1, role_col2 = st.columns(2)

            with role_col1:
                roles = recommend_roles(skills)

                st.subheader("Recommended Career Roles")

                if roles:
                    for role in roles:
                        st.success(role)
                else:
                    st.warning(
                        "No career roles recommended yet. Add more technical skills to your resume."
                    )

            with role_col2:
                st.subheader("Resume Strength")
                show_resume_strength(ats_score)

            st.subheader("Resume Improvement Suggestions")
            show_improvement_suggestions(ats_score)

        else:
            st.info("Paste a job description to calculate ATS score.")
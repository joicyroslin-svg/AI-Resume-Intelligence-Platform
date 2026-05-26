import streamlit as st
from utils.pdf_reader import extract_text_from_pdf

st.set_page_config(
    page_title="AI Resume Intelligence Platform",
    page_icon="📄",
    layout="wide"
)

st.title("🚀 AI Resume Intelligence Platform")
st.subheader("Upload Resume for AI Analysis")

uploaded_file = st.file_uploader(
    "Upload Your Resume (PDF)",
    type=["pdf"]
)

if uploaded_file is not None:
    with open(f"resumes/{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("Resume Uploaded Successfully!")

    extracted_text = extract_text_from_pdf(
        f"resumes/{uploaded_file.name}"
    )

    st.subheader("📄 Extracted Resume Text")

    st.text_area(
        "Resume Content",
        extracted_text,
        height=300
    )
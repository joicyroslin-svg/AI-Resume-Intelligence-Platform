import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()


def get_gemini_api_key():
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return api_key

    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return None


def build_resume_profile(resume_text, skills, ats_score):
    skills_text = ", ".join(skills) if skills else "No detected skills"

    return f"""
Resume Content:
{resume_text}

Detected Skills:
{skills_text}

ATS Score:
{ats_score}/100
"""


def build_career_prompt(resume_text, skills, ats_score):
    resume_profile = build_resume_profile(resume_text, skills, ats_score)

    return f"""
You are a senior AI career strategist, resume reviewer, and portfolio mentor.

Your task:
Analyze this candidate's resume deeply and generate a UNIQUE career report.
Do not give generic fixed answers.

Candidate Profile:
{resume_profile}

Important Rules:
- Give recommendations based ONLY on this resume.
- If the resume is AI/ML focused, recommend AI-related careers.
- If the resume is data focused, recommend data careers.
- If the resume is business/content focused, recommend non-technical or hybrid careers.
- Different resumes must get different career suggestions.
- Mention exact skills, projects, and gaps from the resume.
- Do not repeat the same answer for every candidate.
- Be practical for a student/fresher.
- Give portfolio-focused guidance.

Output format:

# Personalized Career Intelligence Report

## 1. Candidate Summary
Explain what type of candidate this resume represents.

## 2. Strongest Career Fit
Give the best career path and explain why.

## 3. Top Technical Career Paths
For each role include:
- Why this role fits
- Matching skills from resume
- Missing skills
- Project to build for this role

## 4. Top Non-Technical Career Paths
Suggest only if suitable.
Include business, product, writing, operations, HR-tech, analyst, or management roles.

## 5. Top Hybrid Career Paths
Suggest AI + business/product/content roles if suitable.

## 6. Skills Already Strong
List skills that are clearly visible in the resume.

## 7. Skills To Learn Next
Give only relevant next skills.

## 8. Best 3 Portfolio Projects To Build
Give unique project ideas based on this resume.

## 9. Resume Improvement Suggestions
Give specific improvements.

## 10. 30-Day Career Growth Plan
Give week-wise plan.

Make the answer clear, professional, and personalized.
"""


def generate_dynamic_fallback_report(skills, ats_score):
    skills_lower = [skill.lower() for skill in skills]

    technical_roles = []
    hybrid_roles = []
    non_technical_roles = []

    if "machine learning" in skills_lower or "python" in skills_lower:
        technical_roles.append("AI/ML Engineer")

    if "generative ai" in skills_lower or "llm" in skills_lower or "rag" in skills_lower:
        technical_roles.append("Generative AI Engineer")
        hybrid_roles.append("Prompt Engineer")
        hybrid_roles.append("AI Product Analyst")

    if "nlp" in skills_lower:
        technical_roles.append("NLP Engineer")

    if "computer vision" in skills_lower or "opencv" in skills_lower:
        technical_roles.append("Computer Vision Engineer")

    if "sql" in skills_lower or "pandas" in skills_lower or "numpy" in skills_lower:
        technical_roles.append("Data Analyst")

    if "documentation" in skills_lower or "communication" in skills_lower:
        non_technical_roles.append("Technical Writer")
        non_technical_roles.append("Business Analyst")

    if not technical_roles:
        technical_roles = ["Python Developer", "Data Analyst"]

    if not hybrid_roles:
        hybrid_roles = ["AI Solutions Consultant", "No-Code AI Builder"]

    if not non_technical_roles:
        non_technical_roles = ["Business Analyst", "Project Coordinator"]

    skills_text = ", ".join(skills) if skills else "No clear skills detected"

    return f"""
# Personalized Career Intelligence Report

The live AI model is temporarily busy, so this backup report was generated using your detected resume skills.

## 1. Candidate Summary
This resume shows skills in: {skills_text}.

## 2. Strongest Career Fit
Based on the detected skills, your strongest direction is likely:
**{technical_roles[0]}**

## 3. Top Technical Career Paths
{chr(10).join([f"- {role}" for role in technical_roles])}

## 4. Top Non-Technical Career Paths
{chr(10).join([f"- {role}" for role in non_technical_roles])}

## 5. Top Hybrid Career Paths
{chr(10).join([f"- {role}" for role in hybrid_roles])}

## 6. Skills Already Strong
{skills_text}

## 7. Skills To Learn Next
- FastAPI
- LangChain
- Model Deployment
- Deep Learning
- Data Visualization
- Project Documentation

## 8. Best Portfolio Projects To Build
- AI Mock Interview Platform
- Multi-Agent Research Assistant
- AI Career Recommendation System

## 9. Resume Improvement Suggestions
- Add measurable project results.
- Add GitHub and deployment links.
- Add role-specific keywords.
- Mention tools used in each project.

## 10. 30-Day Career Growth Plan
- Week 1: Polish this AI Resume Intelligence Platform.
- Week 2: Build one GenAI/RAG project.
- Week 3: Build one interview or career assistant project.
- Week 4: Update GitHub, LinkedIn, and resume.
"""


def generate_ai_career_recommendations(resume_text, skills, ats_score=0):
    api_key = get_gemini_api_key()

    if not api_key:
        return (
            "AI Career Advisor is not configured yet.\n\n"
            "Add GEMINI_API_KEY in your .env file for local use, "
            "or in Streamlit Cloud Secrets for deployed use."
        )

    client = genai.Client(api_key=api_key)
    prompt = build_career_prompt(resume_text, skills, ats_score)

    models_to_try = [
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-1.5-flash",
    ]

    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )

            if response and response.text:
                return response.text

        except Exception:
            continue

    return generate_dynamic_fallback_report(skills, ats_score)
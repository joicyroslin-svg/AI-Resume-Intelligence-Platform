from pathlib import Path
from html import escape

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.pdf_reader import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.text_cleaner import clean_resume_text
from utils.ats_score import calculate_ats_score
from utils.resume_feedback import generate_feedback
from utils.career_recommender import recommend_roles
from utils.role_matcher import analyze_role_match, get_best_role_match, ROLE_SKILLS

try:
    from utils.ai_career_advisor import generate_ai_career_recommendations
except ImportError:
    generate_ai_career_recommendations = None


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
        st.info("Add measurable achievements, project impact, GitHub links, and deployment links.")

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


def show_skill_badges(skills):
    """Display extracted skills in premium badge layout."""
    if not skills:
        st.warning("No skills detected.")
        return

    skill_columns = st.columns(4)

    for index, skill in enumerate(skills):
        with skill_columns[index % 4]:
            st.markdown(
                f"""
                <div class="skill-pill">
                    {skill}
                </div>
                """,
                unsafe_allow_html=True,
            )


def section_header(title: str, subtitle: str = ""):
    """Reusable premium section heading."""
    st.markdown(
        f"""
        <div class="section-wrap">
            <div class="section-kicker">CareerAI Module</div>
            <div class="section-title">{title}</div>
            <div class="section-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def create_score_gauge(score: int, title: str):
    """Create ATS or role score gauge chart."""
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": title, "font": {"size": 20}},
            number={"font": {"size": 34}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#2563eb"},
                "steps": [
                    {"range": [0, 40], "color": "#fee2e2"},
                    {"range": [40, 70], "color": "#fef3c7"},
                    {"range": [70, 100], "color": "#dcfce7"},
                ],
            },
        )
    )

    fig.update_layout(
        height=330,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#0f172a"),
    )

    return fig


def create_role_match_chart(skills):
    """Create role match comparison chart for all available roles."""
    role_scores = {}

    for role in ROLE_SKILLS:
        score, _, _ = analyze_role_match(skills, role)
        role_scores[role] = score

    df = pd.DataFrame(
        {
            "Role": list(role_scores.keys()),
            "Match Score": list(role_scores.values()),
        }
    ).sort_values("Match Score", ascending=True)

    chart_height = max(430, len(df) * 30)

    fig = px.bar(
        df,
        x="Match Score",
        y="Role",
        orientation="h",
        text="Match Score",
        color="Match Score",
        color_continuous_scale=["#dbeafe", "#60a5fa", "#2563eb", "#1e1b4b"],
    )

    fig.update_traces(
        texttemplate="%{text}%",
        textposition="outside",
        marker_line_width=0,
    )

    fig.update_layout(
        height=chart_height,
        margin=dict(l=20, r=50, t=20, b=20),
        xaxis_title="Match Score (%)",
        yaxis_title="",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#0f172a"),
        coloraxis_showscale=False,
    )

    return fig


def create_keyword_pie_chart(matched_count: int, missing_count: int):
    """Create matched vs missing keyword donut chart."""
    total = matched_count + missing_count

    if total == 0:
        matched_count = 1
        missing_count = 0

    fig = px.pie(
        values=[matched_count, missing_count],
        names=["Matched Keywords", "Missing Keywords"],
        hole=0.58,
        color_discrete_sequence=["#2563eb", "#f97316"],
    )

    fig.update_traces(
        textinfo="percent+label",
        textfont_size=13,
    )

    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#0f172a"),
        showlegend=True,
    )

    return fig


def create_resume_insights_chart(total_words: int, total_skills: int):
    """Create resume words and skills chart."""
    df = pd.DataFrame(
        {
            "Metric": ["Resume Words", "Detected Skills"],
            "Value": [total_words, total_skills],
        }
    )

    fig = px.bar(
        df,
        x="Metric",
        y="Value",
        text="Value",
        color="Metric",
        color_discrete_sequence=["#2563eb", "#7c3aed"],
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(
        height=330,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="",
        yaxis_title="",
        font=dict(color="#0f172a"),
        showlegend=False,
    )

    return fig


def create_skill_gap_chart(matched_count: int, missing_count: int):
    """Create selected role skill gap chart."""
    df = pd.DataFrame(
        {
            "Category": ["Matched Skills", "Missing Skills"],
            "Count": [matched_count, missing_count],
        }
    )

    fig = px.bar(
        df,
        x="Category",
        y="Count",
        text="Count",
        color="Category",
        color_discrete_sequence=["#16a34a", "#ef4444"],
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(
        height=330,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="",
        yaxis_title="",
        font=dict(color="#0f172a"),
        showlegend=False,
    )

    return fig


st.set_page_config(
    page_title="AI Resume Intelligence Platform",
    page_icon="📄",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Manrope', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(14, 165, 233, 0.12), transparent 25%),
            radial-gradient(circle at 90% 10%, rgba(124, 58, 237, 0.12), transparent 25%),
            radial-gradient(circle at 50% 100%, rgba(16, 185, 129, 0.10), transparent 30%),
            linear-gradient(135deg, #f8fafc 0%, #eef2ff 50%, #f0fdf4 100%);
    }

    .block-container {
        max-width: 1350px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, #020617 0%, #0f172a 50%, #111827 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    [data-testid="stSidebar"] * {
        color: white;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploader"] label,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] p,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] small {
        color: #f8fafc !important;
        font-weight: 700;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
        background: rgba(15, 23, 42, 0.86);
        border: 1.5px dashed rgba(125, 211, 252, 0.9);
        border-radius: 18px;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {
        background: #38bdf8;
        color: #082f49 !important;
        border: none;
        border-radius: 12px;
        font-weight: 800;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] svg {
        color: #67e8f9 !important;
        fill: #67e8f9 !important;
    }

    .brand-card {
        background: linear-gradient(135deg, #1d4ed8 0%, #7c3aed 55%, #06b6d4 100%);
        padding: 24px;
        border-radius: 26px;
        box-shadow: 0 18px 40px rgba(15, 23, 42, 0.30);
        margin-bottom: 18px;
    }

    .brand-title {
        font-size: 31px;
        font-weight: 800;
        color: white;
        margin-bottom: 7px;
        letter-spacing: -0.6px;
    }

    .brand-subtitle {
        font-size: 14px;
        color: #e2e8f0;
        line-height: 1.6;
    }

    div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.08);
        padding: 13px 16px;
        border-radius: 18px;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.13);
        transition: 0.22s ease;
        box-shadow: 0 8px 18px rgba(0,0,0,0.12);
    }

    div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.20);
        border: 1px solid rgba(125, 211, 252, 0.78);
        transform: translateX(4px);
    }

    .hero-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 42%, #1d4ed8 100%);
        padding: 36px;
        border-radius: 32px;
        box-shadow: 0 24px 55px rgba(15, 23, 42, 0.25);
        margin-bottom: 26px;
        position: relative;
        overflow: hidden;
    }

    .hero-card::after {
        content: "";
        position: absolute;
        right: -90px;
        top: -90px;
        width: 280px;
        height: 280px;
        border-radius: 999px;
        background: rgba(255,255,255,0.10);
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.14);
        color: #e0f2fe;
        border: 1px solid rgba(255,255,255,0.18);
        padding: 8px 15px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 800;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .main-title {
        font-size: 50px;
        font-weight: 800;
        color: white;
        margin-bottom: 11px;
        letter-spacing: -1.2px;
        line-height: 1.05;
        max-width: 900px;
    }

    .main-subtitle {
        font-size: 18px;
        color: #cbd5e1;
        line-height: 1.75;
        max-width: 860px;
    }

    .section-wrap {
        margin-top: 20px;
        margin-bottom: 18px;
    }

    .section-kicker {
        font-size: 12px;
        color: #7c3aed;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 5px;
    }

    .section-title {
        font-size: 31px;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.8px;
        line-height: 1.1;
    }

    .section-subtitle {
        font-size: 15px;
        color: #64748b;
        margin-top: 7px;
        line-height: 1.7;
        max-width: 850px;
    }

    .glass-card {
        background: rgba(255,255,255,0.84);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 25px;
        border: 1px solid rgba(226,232,240,0.85);
        box-shadow: 0 16px 36px rgba(15,23,42,0.08);
        margin-bottom: 22px;
    }

    .insight-card {
        background:
            linear-gradient(135deg, rgba(255,255,255,0.96), rgba(248,250,252,0.94));
        padding: 23px;
        border-radius: 25px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 14px 32px rgba(15,23,42,0.08);
        margin-bottom: 20px;
    }

    .ai-hero {
        background:
            radial-gradient(circle at top left, rgba(34,211,238,0.23), transparent 35%),
            radial-gradient(circle at bottom right, rgba(168,85,247,0.28), transparent 35%),
            linear-gradient(135deg, #020617 0%, #111827 44%, #312e81 100%);
        padding: 32px;
        border-radius: 32px;
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 26px 65px rgba(30, 27, 75, 0.35);
        margin-bottom: 24px;
    }

    .ai-title {
        font-size: 32px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 10px;
        letter-spacing: -0.8px;
    }

    .ai-subtitle {
        font-size: 15px;
        color: #cbd5e1;
        line-height: 1.8;
        max-width: 850px;
    }

    .skill-pill {
        background: linear-gradient(135deg, #ffffff 0%, #eff6ff 100%);
        border: 1px solid #dbeafe;
        color: #1e3a8a;
        border-radius: 999px;
        padding: 10px 14px;
        margin-bottom: 10px;
        font-size: 14px;
        font-weight: 700;
        text-align: center;
        box-shadow: 0 8px 18px rgba(15,23,42,0.06);
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.90);
        border: 1px solid #e2e8f0;
        padding: 21px;
        border-radius: 23px;
        box-shadow: 0 12px 26px rgba(15,23,42,0.08);
    }

    div[data-testid="stMetricLabel"] {
        font-size: 14px;
        font-weight: 700;
        color: #64748b;
    }

    div[data-testid="stMetricValue"] {
        font-size: clamp(22px, 2.2vw, 30px);
        font-weight: 800;
        color: #0f172a;
        line-height: 1.18;
        white-space: normal;
        overflow-wrap: anywhere;
    }

    .custom-metric-card {
        background: rgba(255,255,255,0.90);
        border: 1px solid #e2e8f0;
        padding: 21px;
        border-radius: 23px;
        box-shadow: 0 12px 26px rgba(15,23,42,0.08);
        min-height: 124px;
    }

    .custom-metric-label {
        font-size: 14px;
        font-weight: 700;
        color: #64748b;
        margin-bottom: 8px;
    }

    .custom-metric-value {
        font-size: 26px;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.2;
        white-space: normal;
        overflow-wrap: anywhere;
        word-break: break-word;
    }

    .stButton > button {
        width: 100%;
        height: 3.35rem;
        border-radius: 18px;
        border: none;
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
        color: white;
        font-weight: 800;
        font-size: 15px;
        box-shadow: 0 14px 28px rgba(37,99,235,0.25);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #6d28d9 100%);
        color: white;
    }

    textarea {
        border-radius: 20px !important;
    }

    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "latest_ats_score" not in st.session_state:
    st.session_state.latest_ats_score = 0

with st.sidebar:
    st.markdown(
        """
        <div class="brand-card">
            <div class="brand-title">CareerAI</div>
            <div class="brand-subtitle">
                Premium resume intelligence, ATS analysis, role matching,
                and AI-powered career growth guidance.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        [
            "Resume Overview",
            "Career Role Match",
            "ATS Analysis",
            "AI Career Advisor",
        ],
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"],
    )

    st.divider()
    st.info("Upload resume → analyze skills → generate your career roadmap.")

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-badge">Career Intelligence Dashboard</div>
        <div class="main-title">AI Resume Intelligence Platform</div>
        <div class="main-subtitle">
            A modern AI-powered dashboard for resume analysis, ATS scoring,
            skill-gap detection, role matching, visual career insights, and personalized AI roadmaps.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if uploaded_file is None:
    st.info("Upload a PDF resume from the sidebar to begin analysis.")
    st.stop()

resume_path = save_uploaded_resume(uploaded_file)
st.success("Resume uploaded successfully.")

extracted_text = extract_text_from_pdf(resume_path)

if not extracted_text.strip():
    st.error("No text found in this PDF. Please upload a text-based resume PDF.")
    st.stop()

cleaned_text = clean_resume_text(extracted_text)
skills = extract_skills(cleaned_text)
total_words = len(cleaned_text.split())
best_role, best_role_score = get_best_role_match(skills)

metric1, metric2, metric3, metric4 = st.columns([1, 1, 1.45, 1])

with metric1:
    st.metric("Skills Detected", len(skills))

with metric2:
    st.metric("Resume Words", total_words)

with metric3:
    best_role_text = best_role if best_role else "Not Found"
    st.markdown(
        f"""
        <div class="custom-metric-card">
            <div class="custom-metric-label">Best Fit Role</div>
            <div class="custom-metric-value">{escape(best_role_text)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with metric4:
    st.metric("Best Role Match", f"{best_role_score}%")

if page == "Resume Overview":
    section_header(
        "Resume Overview",
        "Review extracted resume content, detected skill signals, and resume-level visual insights.",
    )

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    overview_col1, overview_col2 = st.columns([1.1, 1])

    with overview_col1:
        st.subheader("Extracted Resume Text")

        with st.expander("View Extracted Resume Text"):
            st.text_area(
                "Resume Content",
                extracted_text,
                height=320,
            )

        st.subheader("Detected Skill Signals")
        show_skill_badges(skills)

    with overview_col2:
        st.subheader("Resume Insights")
        st.plotly_chart(
            create_resume_insights_chart(total_words, len(skills)),
            use_container_width=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Career Role Match":
    section_header(
        "Career Role Match Analysis",
        "Compare your resume skills against career tracks and identify your strongest role fit.",
    )

    selected_role = st.selectbox(
        "Choose Target Career Role",
        list(ROLE_SKILLS.keys()),
    )

    role_score, role_matched_skills, role_missing_skills = analyze_role_match(
        skills,
        selected_role,
    )

    st.markdown("<div class='insight-card'>", unsafe_allow_html=True)

    insight_col1, insight_col2 = st.columns([1, 1])

    with insight_col1:
        st.info(f"Best Fit Role: {best_role} ({best_role_score}% match)")
        st.subheader(f"{selected_role} Match Score")
        st.progress(role_score / 100)

        if role_score >= 80:
            st.success(f"{role_score}% Match - Strong fit for {selected_role}")
        elif role_score >= 50:
            st.warning(f"{role_score}% Match - Moderate fit for {selected_role}")
        else:
            st.error(f"{role_score}% Match - Needs improvement for {selected_role}")

    with insight_col2:
        st.plotly_chart(
            create_score_gauge(role_score, f"{selected_role} Match"),
            use_container_width=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    role_col1, role_col2 = st.columns(2)

    with role_col1:
        st.subheader("Matched Role Skills")

        if role_matched_skills:
            for skill in role_matched_skills:
                st.success(skill)
        else:
            st.warning("No matched role skills found.")

    with role_col2:
        st.subheader("Missing Role Skills")

        if role_missing_skills:
            for skill in role_missing_skills:
                st.error(skill)
        else:
            st.success("No missing role skills. Great match!")

    graph_col1, graph_col2 = st.columns([1, 1.3])

    with graph_col1:
        st.subheader("Skill Gap Overview")
        st.plotly_chart(
            create_skill_gap_chart(
                len(role_matched_skills),
                len(role_missing_skills),
            ),
            use_container_width=True,
        )

    with graph_col2:
        st.subheader("All Role Match Comparison")
        st.plotly_chart(
            create_role_match_chart(skills),
            use_container_width=True,
        )

elif page == "ATS Analysis":
    section_header(
        "ATS Job Description Analysis",
        "Paste a job description and compare your resume with recruiter keywords using visual insights.",
    )

    job_description = st.text_area(
        "Paste Full Job Description",
        height=240,
        placeholder="Paste full job description here for better ATS analysis...",
    )

    if job_description:
        ats_score, matched_keywords, missing_keywords = calculate_ats_score(
            skills,
            job_description,
        )

        st.session_state.latest_ats_score = ats_score

        st.markdown("<div class='insight-card'>", unsafe_allow_html=True)

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.subheader("ATS Score Gauge")
            st.plotly_chart(
                create_score_gauge(ats_score, "ATS Score"),
                use_container_width=True,
            )
            show_score_message(ats_score)

        with chart_col2:
            st.subheader("Keyword Match Overview")
            st.plotly_chart(
                create_keyword_pie_chart(
                    len(matched_keywords),
                    len(missing_keywords),
                ),
                use_container_width=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

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

        final_col1, final_col2 = st.columns(2)

        with final_col1:
            roles = recommend_roles(skills)

            st.subheader("Rule-Based Recommended Roles")

            if roles:
                for role in roles:
                    st.success(role)
            else:
                st.warning("No career roles recommended yet. Add more technical skills to your resume.")

        with final_col2:
            st.subheader("Resume Strength")
            show_resume_strength(ats_score)

        st.subheader("Resume Improvement Suggestions")
        show_improvement_suggestions(ats_score)

    else:
        st.info("Paste a job description to calculate ATS score.")

elif page == "AI Career Advisor":
    st.markdown(
        """
        <div class="ai-hero">
            <div class="ai-title">AI Career Roadmap Studio</div>
            <div class="ai-subtitle">
                Generate personalized technical, non-technical, and hybrid career paths,
                skill recommendations, portfolio project ideas, and a 30-day growth plan.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if generate_ai_career_recommendations is None:
        st.error("AI Career Advisor file not found. Create utils/ai_career_advisor.py first.")

    else:
        if st.button("Generate AI Career Roadmap"):
            with st.spinner("AI is analyzing your resume and career options..."):
                try:
                    ai_career_advice = generate_ai_career_recommendations(
                        extracted_text,
                        skills,
                        st.session_state.latest_ats_score,
                    )
                    st.markdown(ai_career_advice)

                except Exception as error:
                    st.error("AI service is temporarily busy. Please try again.")
                    st.info("Your app is working, but the Gemini model may be under high demand.")
                    st.code(str(error))

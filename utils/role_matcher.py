ROLE_SKILLS = {
    "AI/ML Engineer": [
        "python",
        "machine learning",
        "deep learning",
        "numpy",
        "pandas",
        "scikit learn",
        "sql",
        "git",
        "github",
    ],

    "Generative AI Engineer": [
        "python",
        "generative ai",
        "llm",
        "langchain",
        "rag",
        "prompt engineering",
        "streamlit",
        "fastapi",
        "git",
        "github",
    ],

    "Computer Vision Engineer": [
        "python",
        "opencv",
        "computer vision",
        "image processing",
        "deep learning",
        "numpy",
        "machine learning",
        "model deployment",
    ],

    "NLP Engineer": [
        "python",
        "nlp",
        "machine learning",
        "deep learning",
        "transformers",
        "llm",
        "text preprocessing",
        "scikit learn",
    ],

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "data analysis",
        "data visualization",
        "statistics",
        "pandas",
        "numpy",
    ],
}


def analyze_role_match(resume_skills, selected_role):
    resume_skills = [skill.lower() for skill in resume_skills]

    required_skills = ROLE_SKILLS[selected_role]

    matched_skills = []
    missing_skills = []

    for skill in required_skills:
        if skill in resume_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    match_score = int((len(matched_skills) / len(required_skills)) * 100)

    return match_score, matched_skills, missing_skills


def get_best_role_match(resume_skills):
    best_role = None
    best_score = 0

    for role in ROLE_SKILLS:
        score, matched, missing = analyze_role_match(resume_skills, role)

        if score > best_score:
            best_score = score
            best_role = role

    return best_role, best_score
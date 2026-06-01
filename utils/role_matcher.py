ROLE_SKILLS = {
    # ---------------- TECHNICAL AI / DATA ROLES ----------------
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

    "Data Scientist": [
        "python",
        "machine learning",
        "statistics",
        "pandas",
        "numpy",
        "scikit learn",
        "data visualization",
        "sql",
        "model evaluation",
    ],

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "tableau",
        "data analysis",
        "data visualization",
        "statistics",
        "pandas",
        "numpy",
    ],

    "Business Intelligence Analyst": [
        "sql",
        "excel",
        "power bi",
        "tableau",
        "data visualization",
        "dashboarding",
        "business analysis",
        "statistics",
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

    "MLOps Engineer": [
        "python",
        "machine learning",
        "docker",
        "fastapi",
        "mlops",
        "model deployment",
        "ci cd",
        "cloud",
        "git",
        "github",
    ],

    "Data Engineer": [
        "python",
        "sql",
        "etl",
        "data pipelines",
        "spark",
        "airflow",
        "databases",
        "cloud",
        "data warehousing",
    ],

    "Backend Developer": [
        "python",
        "fastapi",
        "flask",
        "sql",
        "databases",
        "api development",
        "git",
        "github",
        "docker",
    ],

    "Python Developer": [
        "python",
        "oop",
        "data structures",
        "algorithms",
        "git",
        "github",
        "api development",
        "sql",
    ],

    "Full Stack AI Developer": [
        "python",
        "streamlit",
        "fastapi",
        "react",
        "sql",
        "api development",
        "generative ai",
        "llm",
        "git",
        "github",
    ],

    # ---------------- CYBERSECURITY / CLOUD ROLES ----------------
    "Cybersecurity Analyst": [
        "networking",
        "linux",
        "python",
        "security",
        "log analysis",
        "risk assessment",
        "incident response",
    ],

    "Cloud Engineer": [
        "cloud",
        "aws",
        "azure",
        "gcp",
        "linux",
        "docker",
        "networking",
        "deployment",
    ],

    "DevOps Engineer": [
        "linux",
        "docker",
        "kubernetes",
        "ci cd",
        "cloud",
        "git",
        "github",
        "monitoring",
    ],

    # ---------------- NON-TECHNICAL / BUSINESS ROLES ----------------
    "Business Analyst": [
        "business analysis",
        "excel",
        "sql",
        "communication",
        "problem solving",
        "documentation",
        "data analysis",
    ],

    "Product Manager": [
        "product management",
        "user research",
        "communication",
        "problem solving",
        "analytics",
        "roadmap planning",
        "market research",
    ],

    "Project Coordinator": [
        "project management",
        "communication",
        "documentation",
        "team collaboration",
        "planning",
        "time management",
        "reporting",
    ],

    "Technical Writer": [
        "technical writing",
        "documentation",
        "communication",
        "research",
        "content writing",
        "github",
        "markdown",
    ],

    "AI Content Strategist": [
        "generative ai",
        "prompt engineering",
        "content writing",
        "research",
        "communication",
        "seo",
        "analytics",
    ],

    "HR Tech Analyst": [
        "hr analytics",
        "excel",
        "communication",
        "data analysis",
        "reporting",
        "business analysis",
        "ats",
    ],

    "Customer Success Analyst": [
        "communication",
        "customer support",
        "problem solving",
        "analytics",
        "documentation",
        "product knowledge",
    ],

    "Operations Analyst": [
        "operations",
        "excel",
        "data analysis",
        "process improvement",
        "reporting",
        "problem solving",
        "communication",
    ],

    # ---------------- HYBRID AI + BUSINESS ROLES ----------------
    "AI Product Analyst": [
        "generative ai",
        "data analysis",
        "product management",
        "analytics",
        "communication",
        "user research",
        "prompt engineering",
    ],

    "Prompt Engineer": [
        "prompt engineering",
        "generative ai",
        "llm",
        "communication",
        "problem solving",
        "content writing",
        "testing",
    ],

    "AI Solutions Consultant": [
        "generative ai",
        "business analysis",
        "communication",
        "problem solving",
        "presentation",
        "technical understanding",
        "client communication",
    ],

    "AI Trainer": [
        "generative ai",
        "prompt engineering",
        "data labeling",
        "content review",
        "communication",
        "quality analysis",
    ],

    "Developer Advocate": [
        "technical writing",
        "communication",
        "public speaking",
        "github",
        "content creation",
        "api development",
        "community building",
    ],

    "No-Code AI Builder": [
        "generative ai",
        "prompt engineering",
        "automation",
        "no code tools",
        "workflow design",
        "problem solving",
        "product thinking",
    ],

    "AI Research Assistant": [
        "research",
        "python",
        "machine learning",
        "nlp",
        "data analysis",
        "documentation",
        "technical writing",
    ],
}


def analyze_role_match(resume_skills, selected_role):
    resume_skills = [skill.lower() for skill in resume_skills]

    required_skills = ROLE_SKILLS[selected_role]

    matched_skills = []
    missing_skills = []

    for skill in required_skills:
        if skill.lower() in resume_skills:
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
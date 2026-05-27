SKILLS_DB = [
    "python",
    "machine learning",
    "deep learning",
    "nlp",
    "tensorflow",
    "pytorch",
    "opencv",
    "streamlit",
    "sql",
    "data analysis",
    "pandas",
    "numpy",
    "scikit learn",
    "generative ai",
    "langchain",
    "rag",
    "computer vision",
    "flask",
    "fastapi",
    "git",
    "github"
]

def extract_skills(text):
    detected_skills = []

    text = text.lower()

    for skill in SKILLS_DB:
        if skill.lower() in text:
            detected_skills.append(skill)

    return list(set(detected_skills))
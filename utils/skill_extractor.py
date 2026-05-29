SKILLS_DB = [
    "python",
    "machine learning",
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
    "github",
    "deep learning",
    "image processing",
    "model deployment",
    "data visualization",
    "power bi",
    "excel",
    "statistics",
    "llm",
    "ai agents",
    "prompt engineering"
]

def extract_skills(text):
    detected_skills = []

    text = text.lower()

    for skill in SKILLS_DB:
        if skill.lower() in text:
            detected_skills.append(skill)

    return list(set(detected_skills))
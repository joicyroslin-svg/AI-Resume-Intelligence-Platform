def calculate_ats_score(skills, job_description):

    score = 0

    matched_keywords = []

    missing_keywords = []

    job_description = job_description.lower()

    for skill in skills:

        if skill.lower() in job_description:
            score += 10
            matched_keywords.append(skill)

    all_possible_skills = [
        "python",
        "machine learning",
        "deep learning",
        "nlp",
        "tensorflow",
        "pytorch",
        "sql",
        "data analysis",
        "fastapi",
        "streamlit",
        "opencv",
        "generative ai",
        "rag",
        "langchain"
    ]

    for keyword in all_possible_skills:

        if keyword in job_description and keyword not in skills:
            missing_keywords.append(keyword)

    if score > 100:
        score = 100

    return score, matched_keywords, missing_keywords
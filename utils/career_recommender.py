def recommend_roles(skills):

    roles = []

    skills = [skill.lower() for skill in skills]

    if "machine learning" in skills:
        roles.append("Machine Learning Engineer")

    if "nlp" in skills:
        roles.append("NLP Engineer")

    if "computer vision" in skills:
        roles.append("Computer Vision Engineer")

    if "generative ai" in skills:
        roles.append("Generative AI Engineer")

    if "sql" in skills:
        roles.append("Data Analyst")

    return list(set(roles))
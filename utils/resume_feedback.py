def generate_resume_suggestions(ats_score, matched_keywords, missing_keywords, total_words):
    suggestions = []

    if ats_score >= 80:
        suggestions.append("Your resume is strongly matching this job description.")
        suggestions.append("You can improve further by adding measurable achievements and project impact.")
    
    elif ats_score >= 50:
        suggestions.append("Your resume has a moderate match with this job description.")
        suggestions.append("Add more job-specific keywords from the missing skills list.")
    
    else:
        suggestions.append("Your resume has a low match with this job description.")
        suggestions.append("Customize your resume more carefully for this job role.")

    if missing_keywords:
        suggestions.append(
            "Consider adding these missing skills if you genuinely know them: "
            + ", ".join(missing_keywords)
        )

    if len(matched_keywords) < 5:
        suggestions.append("Add more relevant technical skills that match the target role.")

    if total_words < 250:
        suggestions.append("Your resume content looks too short. Add more project details, skills, and achievements.")

    elif total_words > 800:
        suggestions.append("Your resume may be too lengthy. Keep it concise and focused.")

    suggestions.append("Use action words like built, developed, implemented, optimized, and deployed.")
    suggestions.append("Add numbers wherever possible, like accuracy score, users served, or time saved.")

    return suggestions


def generate_feedback(ats_score, missing_keywords):
    feedback = []

    if ats_score >= 80:
        feedback.append("Your resume is strongly matching this job description.")
        feedback.append("You can improve further by adding measurable achievements and project impact.")
    elif ats_score >= 50:
        feedback.append("Your resume has a moderate match with this job description.")
        feedback.append("Add more job-specific keywords from the missing skills list.")
    else:
        feedback.append("Your resume has a low match with this job description.")
        feedback.append("Customize your resume more carefully for this job role.")

    if missing_keywords:
        feedback.append(
            "Consider adding these missing skills if you genuinely know them: "
            + ", ".join(missing_keywords)
        )

    feedback.append("Use action words like built, developed, implemented, optimized, and deployed.")
    feedback.append("Add numbers wherever possible, like accuracy score, users served, or time saved.")

    return feedback

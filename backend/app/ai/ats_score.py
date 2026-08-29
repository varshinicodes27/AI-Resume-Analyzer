def calculate_ats_score(text: str, skills: list):
    score = 0
    suggestions = []

    text = text.lower()

    # Skills (40 marks)
    score += min(len(skills) * 4, 40)

    # Education
    if "b.tech" in text or "bachelor" in text or "degree" in text:
        score += 15
    else:
        suggestions.append("Add your education details.")

    # Projects
    if "project" in text:
        score += 15
    else:
        suggestions.append("Include your projects.")

    # Experience
    if "experience" in text or "intern" in text:
        score += 15
    else:
        suggestions.append("Mention internships or experience.")

    # Certifications
    if "certificate" in text or "certification" in text:
        score += 15
    else:
        suggestions.append("Add certifications.")

    return {
        "score": score,
        "suggestions": suggestions
    }
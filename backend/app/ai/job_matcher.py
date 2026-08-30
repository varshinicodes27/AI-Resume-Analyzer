
from app.ai.skill_extractor import (
    normalize_skill,
    extract_jd_skills
)


# ============================================================
# CALCULATE JOB MATCH
# ============================================================

def calculate_job_match(resume_skills, jd_skills):
    """
    Calculate deterministic job-description skill match percentage.

    Policy:
    - Accurate, canonical equivalence matching (e.g. 'Core Java' == 'Java', 'ReactJS' == 'React.js').
    - Strictly avoids false cross-technology inflation:
      - Spring != Spring Boot
      - Java != JavaScript
      - C != C++ / C#
      - React.js != React Native
      - AWS != Azure
      - Docker != Kubernetes
    """

    # --------------------------------------------------------
    # 1. NORMALIZE RESUME SKILLS
    # --------------------------------------------------------

    resume_set = {
        normalize_skill(skill)
        for skill in resume_skills
        if str(skill).strip()
    }

    # --------------------------------------------------------
    # 2. NORMALIZE JD SKILLS
    # --------------------------------------------------------

    jd_set = {
        normalize_skill(skill)
        for skill in jd_skills
        if str(skill).strip()
    }

    resume_set.discard("")
    jd_set.discard("")

    # --------------------------------------------------------
    # 3. EXACT CANONICAL MATCHING
    # --------------------------------------------------------

    matched = jd_set.intersection(resume_set)
    missing = jd_set.difference(resume_set)

    total_job_skills = len(jd_set)
    matched_count = len(matched)
    missing_count = len(missing)

    # --------------------------------------------------------
    # 4. SCORE CALCULATION
    # --------------------------------------------------------

    if not jd_set:
        score = 0
    else:
        score = round(
            (matched_count / total_job_skills) * 100
        )

    # --------------------------------------------------------
    # 5. MATCH STRENGTH THRESHOLDS
    # 90-100 -> Excellent Match
    # 75-89  -> Strong Match
    # 50-74  -> Moderate Match
    # 25-49  -> Weak Match
    # 0-24   -> Low Match
    # --------------------------------------------------------

    if score >= 90:
        match_strength = "Excellent Match"
    elif score >= 75:
        match_strength = "Strong Match"
    elif score >= 50:
        match_strength = "Moderate Match"
    elif score >= 25:
        match_strength = "Weak Match"
    else:
        match_strength = "Low Match"

    # --------------------------------------------------------
    # 6. SORTED CANONICAL DISPLAY
    # --------------------------------------------------------

    matched_skills = sorted(
        matched
    )

    missing_skills = sorted(
        missing
    )

    recommended_skills = missing_skills.copy()

    job_description_skills = sorted(
        jd_set
    )

    # --------------------------------------------------------
    # 7. ACTIONABLE SUGGESTIONS
    # --------------------------------------------------------

    suggestions = []

    if missing:
        suggestions.append(
            "Consider adding relevant missing skills "
            "to your resume only if you genuinely have "
            "experience with them."
        )

    if matched:
        suggestions.append(
            "Highlight your matched skills clearly "
            "in your Skills, Projects, and Experience sections."
        )

    if score < 75 and jd_set:
        suggestions.append(
            "Tailor your resume toward the important "
            "technical requirements mentioned in the job description."
        )

    if score >= 90:
        suggestions.append(
            "Your technical skill alignment is strong. "
            "Focus on demonstrating these skills with "
            "measurable project or experience results."
        )

    # --------------------------------------------------------
    # 8. RECOMMENDATION
    # --------------------------------------------------------

    if not jd_set:
        recommendation = (
            "No supported technical skills were detected "
            "in the job description."
        )

    elif score >= 90:
        recommendation = (
            "Your resume strongly matches this job. "
            "You have excellent alignment with the detected "
            "technical requirements."
        )

    elif score >= 75:
        recommendation = (
            "Your resume matches most of the detected job "
            "requirements. Addressing the missing skills "
            "could improve your alignment."
        )

    elif score >= 50:
        recommendation = (
            "Your resume has a moderate skill overlap with "
            "this job. Consider strengthening the missing "
            "technical areas."
        )

    elif score >= 25:
        recommendation = (
            "Your resume currently has limited skill overlap "
            "with this job. Review the missing requirements "
            "before applying."
        )

    else:
        recommendation = (
            "Your resume has low alignment with the required "
            "technical skills for this role."
        )

    # --------------------------------------------------------
    # 9. RETURN STRUCTURE
    # --------------------------------------------------------

    return {
        "match_percentage": score,
        "match_strength": match_strength,
        "total_job_skills": total_job_skills,
        "matched_count": matched_count,
        "missing_count": missing_count,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommended_skills": recommended_skills,
        "job_description_skills": job_description_skills,
        "resume_suggestions": suggestions,
        "recommendation": recommendation
    }

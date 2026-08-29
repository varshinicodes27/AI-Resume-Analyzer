import re


# ==========================================================
# SKILL DATABASE
# ==========================================================

SKILLS_DATABASE = [
    "python",
    "java",
    "c++",
    "c",
    "html",
    "css",
    "javascript",
    "react",
    "react.js",
    "node.js",
    "node",
    "spring boot",
    "spring",
    "hibernate",
    "sql",
    "mysql",
    "mongodb",
    "fastapi",
    "docker",
    "aws",
    "git",
    "github",
    "rest api",
    "jpa",
    "maven",
    "typescript",
    "angular",
    "kotlin",
    "redis",
    "postgresql",
    "azure",
    "kubernetes"
]


# ==========================================================
# SKILL ALIASES
# ==========================================================
SKILL_ALIASES = {

    # ======================================================
    # PROGRAMMING LANGUAGES
    # ======================================================

    "py": "python",

    "js": "javascript",
    "jscript": "javascript",

    "ts": "typescript",

    "c plus plus": "c++",
    "cpp": "c++",

    # ======================================================
    # HTML / CSS
    # ======================================================

    "html5": "html",

    "css3": "css",

    # ======================================================
    # REACT
    # ======================================================

    "react.js": "react",
    "reactjs": "react",
    "react js": "react",

    # ======================================================
    # NODE
    # ======================================================

    "node.js": "node",
    "nodejs": "node",
    "node js": "node",

    # ======================================================
    # SPRING
    # ======================================================

    "springboot": "spring boot",
    "spring-boot": "spring boot",
    "spring boot framework": "spring boot",

    # ======================================================
    # REST API
    # ======================================================

    "rest": "rest api",
    "rest api": "rest api",
    "rest apis": "rest api",
    "restful api": "rest api",
    "restful apis": "rest api",
    "restful web services": "rest api",
    "rest api development": "rest api",

    # ======================================================
    # DATABASE
    # ======================================================

    "mysql database": "mysql",
    "mysql db": "mysql",

    "postgres": "postgresql",
    "postgres db": "postgresql",
    "postgresql database": "postgresql",

    # ======================================================
    # VERSION CONTROL
    # ======================================================

    "git version control": "git",
    "github repository": "github",

    # ======================================================
    # JPA
    # ======================================================

    "java persistence api": "jpa",

    # ======================================================
    # OBJECT ORIENTED PROGRAMMING
    # ======================================================

    "object oriented programming": "oop",
    "object-oriented programming": "oop",

    # ======================================================
    # DATA STRUCTURES
    # ======================================================

    "data structures and algorithms": "dsa",
    "data structures & algorithms": "dsa",

}


# ==========================================================
# NORMALIZE SKILL
# ==========================================================

def normalize_skill(skill):

    skill = str(skill).lower().strip()

    # Replace common punctuation variations
    skill = skill.replace("_", " ")
    skill = skill.replace("/", " ")

    # Normalize hyphens
    skill = skill.replace("-", " ")

    # Remove unnecessary spaces
    skill = re.sub(r"\s+", " ", skill).strip()

    # Apply aliases
    skill = SKILL_ALIASES.get(
        skill,
        skill
    )

    return skill

# ==========================================================
# EXTRACT SKILLS FROM JOB DESCRIPTION
# ==========================================================

def extract_jd_skills(job_description):

    if not job_description:
        return []

    text = job_description.lower()

    found_skills = []

    for skill in SKILLS_DATABASE:

        # Special handling for C
        # Prevent random single-letter matches.
        if skill == "c":
              pattern = r"(?<![a-z0-9+#])c(?![a-z0-9+#])"
        else:
            pattern = (
                r"(?<!\w)"
                + re.escape(skill)
                + r"(?!\w)"
            )

        if re.search(pattern, text):

            normalized = normalize_skill(skill)

            if normalized not in found_skills:
                found_skills.append(normalized)

    return found_skills


# ==========================================================
# CALCULATE JOB MATCH
# ==========================================================

def calculate_job_match(resume_skills, jd_skills):

    # ------------------------------------------------------
    # NORMALIZE RESUME SKILLS
    # ------------------------------------------------------

    resume_skills = {
        normalize_skill(skill)
        for skill in resume_skills
        if str(skill).strip()
    }

    # ------------------------------------------------------
    # NORMALIZE JD SKILLS
    # ------------------------------------------------------

    jd_skills = {
        normalize_skill(skill)
        for skill in jd_skills
        if str(skill).strip()
    }

    # Remove empty values
    resume_skills.discard("")
    jd_skills.discard("")

    # ------------------------------------------------------
    # MATCHING
    # ------------------------------------------------------

    matched = resume_skills.intersection(jd_skills)

    missing = jd_skills.difference(resume_skills)

    # ------------------------------------------------------
    # SCORE
    # ------------------------------------------------------

    if not jd_skills:

        score = 0

    else:

        score = round(
            (len(matched) / len(jd_skills)) * 100
        )

    # ------------------------------------------------------
    # MATCH STRENGTH
    # ------------------------------------------------------

    if score >= 85:

        match_strength = "Excellent Match"

    elif score >= 70:

        match_strength = "Strong Match"

    elif score >= 50:

        match_strength = "Moderate Match"

    else:

        match_strength = "Low Match"

    # ------------------------------------------------------
    # RECOMMENDED SKILLS
    # ------------------------------------------------------

    recommended_skills = sorted(
        skill.title()
        for skill in missing
    )

    # ------------------------------------------------------
    # SUGGESTIONS
    # ------------------------------------------------------

    suggestions = []

    if missing:

        suggestions.append(
            "Consider adding relevant missing skills "
            "to your resume if you genuinely have experience with them."
        )

    if matched:

        suggestions.append(
            "Highlight your matched skills clearly "
            "in your Skills and Projects sections."
        )

    if score < 70 and jd_skills:

        suggestions.append(
            "Tailor your resume toward the important "
            "technical requirements mentioned in the job description."
        )

    if score >= 85:

        suggestions.append(
            "Your technical skill alignment is strong. "
            "Focus on demonstrating these skills with measurable "
            "project or experience results."
        )

    # ------------------------------------------------------
    # RECOMMENDATION
    # ------------------------------------------------------

    if not jd_skills:

        recommendation = (
            "No supported technical skills were detected "
            "in the job description."
        )

    elif score >= 85:

        recommendation = (
            "Your resume strongly matches this job. "
            "You have excellent alignment with the detected "
            "technical requirements."
        )

    elif score >= 70:

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

    else:

        recommendation = (
            "Your resume currently has limited skill overlap "
            "with this job. Review the missing requirements "
            "before applying."
        )

    # ------------------------------------------------------
    # RETURN
    # ------------------------------------------------------

    return {

        "match_percentage": score,

        "match_strength": match_strength,

        "total_job_skills": len(jd_skills),

        "matched_count": len(matched),

        "missing_count": len(missing),

        "matched_skills": sorted(
            skill.title()
            for skill in matched
        ),

        "missing_skills": sorted(
            skill.title()
            for skill in missing
        ),

        "recommended_skills": recommended_skills,

        "resume_suggestions": suggestions,

        "recommendation": recommendation
    }
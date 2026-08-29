import re


def normalize_skills(skills):
    """
    Normalize skills and remove obvious duplicates.
    """

    normalized = []
    seen = set()

    aliases = {
        "html5": "HTML",
        "html": "HTML",
        "css3": "CSS",
        "css": "CSS",
        "react": "React.js",
        "react.js": "React.js",
        "rest api": "REST APIs",
        "rest apis": "REST APIs",
        "restful api": "REST APIs",
        "restful apis": "REST APIs",
    }

    for skill in skills:

        skill = str(skill).strip()

        if not skill:
            continue

        key = skill.lower().strip()

        cleaned = aliases.get(key, skill)

        normalized_key = cleaned.lower()

        if normalized_key not in seen:
            seen.add(normalized_key)
            normalized.append(cleaned)

    return normalized


def contains_skill(skill_text, skill):
    """
    Safely check whether a skill exists.
    Prevents single-letter skills such as 'C'
    from matching random words.
    """

    pattern = r"(?<![a-zA-Z0-9+#])" + re.escape(skill) + r"(?![a-zA-Z0-9+#])"

    return re.search(
        pattern,
        skill_text,
        re.IGNORECASE
    ) is not None


def calculate_section_scores(data):

    """
    ResumeIQ ATS Scoring Engine

    Total = 100

    Contact        10
    Education      15
    Skills         20
    Projects       25
    Experience     20
    Certifications 10
    """

    candidate = data.get("candidate") or {}
    education = data.get("education") or []
    skills = data.get("skills") or []
    projects = data.get("projects") or []
    experience = data.get("experience") or []
    certifications = data.get("certifications") or []

    # =========================================================
    # CONTACT - 10
    # =========================================================

    contact_score = 0
    contact_strengths = []
    contact_improvements = []

    # Name - 2
    if candidate.get("name"):
        contact_score += 2
        contact_strengths.append(
            "Name is clearly provided."
        )
    else:
        contact_improvements.append(
            "Add your full name."
        )

    # Email - 2
    email = str(
        candidate.get("email", "")
    ).strip()

    if email and re.match(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
        email
    ):
        contact_score += 2
        contact_strengths.append(
            "Professional email address is provided."
        )
    elif email:
        contact_score += 1
        contact_improvements.append(
            "Use a valid professional email address."
        )
    else:
        contact_improvements.append(
            "Add a professional email address."
        )

    # Phone - 2
    phone = str(
        candidate.get("phone", "")
    ).strip()

    if phone:

        digits = re.sub(
            r"\D",
            "",
            phone
        )

        if len(digits) >= 10:
            contact_score += 2
            contact_strengths.append(
                "Phone number is provided."
            )
        else:
            contact_score += 1
            contact_improvements.append(
                "Check that your phone number is complete."
            )

    else:
        contact_improvements.append(
            "Add a phone number."
        )

    # LinkedIn - 2
    if candidate.get("linkedin"):
        contact_score += 2
        contact_strengths.append(
            "LinkedIn profile is included."
        )
    else:
        contact_improvements.append(
            "Add your LinkedIn profile URL."
        )

    # GitHub / Portfolio - 2
    if (
        candidate.get("github")
        or candidate.get("portfolio")
    ):
        contact_score += 2
        contact_strengths.append(
            "GitHub or portfolio link is included."
        )
    else:
        contact_improvements.append(
            "Add a GitHub or portfolio link."
        )

    # =========================================================
    # EDUCATION - 15
    # =========================================================

    education_score = 0
    education_strengths = []
    education_improvements = []

    if education:

        education_score += 5

        education_strengths.append(
            "Education history is provided."
        )

    else:

        education_improvements.append(
            "Add your educational background."
        )

    education_text = " ".join(
        map(str, education)
    ).lower()

    degree_keywords = [
        "b.tech",
        "btech",
        "bachelor",
        "master",
        "m.tech",
        "mtech",
        "degree",
        "b.sc",
        "bca",
        "mca",
        "mba",
        "phd"
    ]

    if any(
        keyword in education_text
        for keyword in degree_keywords
    ):

        education_score += 5

        education_strengths.append(
            "Degree or qualification is identifiable."
        )

    elif education:

        education_score += 2

        education_improvements.append(
            "Clearly mention your degree or qualification."
        )

    institution_keywords = [
        "university",
        "college",
        "institute",
        "school"
    ]

    if any(
        keyword in education_text
        for keyword in institution_keywords
    ):

        education_score += 3

        education_strengths.append(
            "Educational institution is mentioned."
        )

    elif education:

        education_improvements.append(
            "Clearly mention your college or university."
        )

    if re.search(
        r"\b(19|20)\d{2}\b",
        education_text
    ):

        education_score += 2

        education_strengths.append(
            "Education timeline/year is identifiable."
        )

    else:

        education_improvements.append(
            "Include your graduation or expected graduation year."
        )

    education_score = min(
        education_score,
        15
    )

    # =========================================================
    # SKILLS - 20
    # =========================================================

    skills_score = 0
    skills_strengths = []
    skills_improvements = []

    normalized_skills = normalize_skills(skills)

    skill_count = len(normalized_skills)

    # Quantity - 10
    if skill_count >= 15:

        skills_score += 10

    elif skill_count >= 10:

        skills_score += 8

    elif skill_count >= 5:

        skills_score += 6

    elif skill_count >= 3:

        skills_score += 4

    elif skill_count > 0:

        skills_score += 2

    if skill_count >= 10:

        skills_strengths.append(
            "Good range of technical skills is listed."
        )

    elif skill_count > 0:

        skills_improvements.append(
            "Add more relevant technical skills where appropriate."
        )

    else:

        skills_improvements.append(
            "Add a dedicated technical skills section."
        )

    skill_text = " ".join(
        normalized_skills
    ).lower()

    programming = [
        "python",
        "java",
        "javascript",
        "typescript",
        "c",
        "c++",
        "c#",
        "go",
        "rust",
        "kotlin"
    ]

    frameworks = [
        "react",
        "react.js",
        "angular",
        "vue",
        "spring",
        "spring boot",
        "django",
        "flask",
        "fastapi",
        "node",
        "express"
    ]

    databases = [
        "mysql",
        "postgresql",
        "postgres",
        "mongodb",
        "oracle",
        "sql",
        "redis"
    ]

    tools = [
        "git",
        "github",
        "docker",
        "aws",
        "azure",
        "gcp",
        "linux"
    ]

    programming_found = any(
        contains_skill(skill_text, skill)
        for skill in programming
    )

    framework_found = any(
        contains_skill(skill_text, skill)
        for skill in frameworks
    )

    database_found = any(
        contains_skill(skill_text, skill)
        for skill in databases
    )

    tools_found = any(
        contains_skill(skill_text, skill)
        for skill in tools
    )

    categories = sum([
        programming_found,
        framework_found,
        database_found,
        tools_found
    ])

    skills_score += min(
        categories * 2,
        8
    )

    if categories >= 3:

        skills_strengths.append(
            "Skills show good technical diversity."
        )

    else:

        skills_improvements.append(
            "Consider showing a balanced mix of programming "
            "languages, frameworks, databases, and development tools."
        )

    skills_score = min(
        skills_score,
        20
    )

    # =========================================================
    # PROJECTS - 25
    # =========================================================

    projects_score = 0
    project_strengths = []
    project_improvements = []

    project_count = len(projects)

    if project_count >= 3:

        projects_score += 8

        project_strengths.append(
            "Multiple projects are included."
        )

    elif project_count == 2:

        projects_score += 6

        project_strengths.append(
            "Two projects are included."
        )

    elif project_count == 1:

        projects_score += 4

        project_improvements.append(
            "Consider adding another relevant project."
        )

    else:

        project_improvements.append(
            "Add relevant academic or personal projects."
        )

    project_text = " ".join(
        map(str, projects)
    ).lower()

    technology_keywords = [
        "python",
        "java",
        "javascript",
        "react",
        "spring",
        "spring boot",
        "sql",
        "mysql",
        "mongodb",
        "flask",
        "fastapi",
        "html",
        "css",
        "machine learning",
        "tensorflow",
        "pytorch",
        "aws",
        "docker"
    ]

    action_words = [
        "developed",
        "designed",
        "implemented",
        "created",
        "built",
        "integrated",
        "deployed",
        "automated",
        "engineered"
    ]

    impact_words = [
        "%",
        "users",
        "performance",
        "accuracy",
        "reduced",
        "increased",
        "improved",
        "faster",
        "success",
        "result",
        "achieved"
    ]

    tech_found = sum(
        1
        for keyword in technology_keywords
        if keyword in project_text
    )

    actions_found = sum(
        1
        for word in action_words
        if word in project_text
    )

    impact_found = sum(
        1
        for word in impact_words
        if word in project_text
    )

    if tech_found >= 3:

        projects_score += 4

        project_strengths.append(
            "Project technologies are clearly mentioned."
        )

    elif tech_found > 0:

        projects_score += 2

        project_improvements.append(
            "Mention the main technologies used in each project."
        )

    else:

        project_improvements.append(
            "Mention technologies used in your projects."
        )

    if actions_found >= 2:

        projects_score += 3

        project_strengths.append(
            "Projects use strong development/action language."
        )

    elif actions_found == 1:

        projects_score += 1

        project_improvements.append(
            "Use stronger action verbs such as developed, "
            "implemented, or designed."
        )

    else:

        project_improvements.append(
            "Describe projects using action-oriented statements."
        )

    if impact_found >= 2:

        projects_score += 2

        project_strengths.append(
            "Projects include measurable or outcome-focused information."
        )

    else:

        project_improvements.append(
            "Add measurable results such as accuracy, "
            "performance improvement, users, or other project outcomes."
        )

    meaningful_projects = [
        str(project).strip()
        for project in projects
        if len(str(project).strip()) >= 30
    ]

    if len(meaningful_projects) >= 3:

        projects_score += 8

    elif len(meaningful_projects) >= 2:

        projects_score += 6

    elif len(meaningful_projects) == 1:

        projects_score += 3

        project_improvements.append(
            "Expand project descriptions with more technical detail."
        )

    elif project_count > 0:

        project_improvements.append(
            "Add meaningful descriptions instead of only project titles."
        )

    projects_score = min(
        projects_score,
        25
    )

    # =========================================================
    # EXPERIENCE - 20
    # =========================================================

    experience_score = 0
    experience_strengths = []
    experience_improvements = []

    experience_count = len(experience)

    if experience_count >= 2:

        experience_score += 12

        experience_strengths.append(
            "Multiple experience entries are included."
        )

    elif experience_count == 1:

        experience_score += 8

        experience_strengths.append(
            "Professional or internship experience is included."
        )

    else:

        experience_improvements.append(
            "Add internships, work experience, freelancing, "
            "or relevant practical experience."
        )

    experience_text = " ".join(
        map(str, experience)
    ).lower()

    experience_action_words = [
        "developed",
        "implemented",
        "managed",
        "designed",
        "created",
        "built",
        "analyzed",
        "automated",
        "led",
        "tested"
    ]

    experience_impact_words = [
        "%",
        "improved",
        "increased",
        "reduced",
        "users",
        "performance",
        "accuracy",
        "achieved"
    ]

    if any(
        word in experience_text
        for word in experience_action_words
    ):

        experience_score += 4

        experience_strengths.append(
            "Experience descriptions use action-oriented language."
        )

    elif experience:

        experience_improvements.append(
            "Describe your responsibilities using strong action verbs."
        )

    if any(
        word in experience_text
        for word in experience_impact_words
    ):

        experience_score += 4

        experience_strengths.append(
            "Experience includes measurable or outcome-focused information."
        )

    elif experience:

        experience_improvements.append(
            "Add measurable achievements or outcomes to your experience."
        )

    experience_score = min(
        experience_score,
        20
    )

    # =========================================================
    # CERTIFICATIONS - 10
    # =========================================================

    certifications_score = 0
    certification_strengths = []
    certification_improvements = []

    certification_count = len(certifications)

    if certification_count >= 2:

        certifications_score += 6

        certification_strengths.append(
            "Multiple certifications are listed."
        )

    elif certification_count == 1:

        certifications_score += 4

        certification_strengths.append(
            "Certification is included."
        )

    else:

        certification_improvements.append(
            "Add relevant technical certifications or courses."
        )

    certification_text = " ".join(
        map(str, certifications)
    ).lower()

    recognized_providers = [
        "nptel",
        "coursera",
        "udemy",
        "microsoft",
        "aws",
        "google",
        "ibm",
        "oracle",
        "cisco",
        "meta",
        "hackerrank",
        "linkedin",
        "simplilearn",
        "samsung"
    ]

    if any(
        provider in certification_text
        for provider in recognized_providers
    ):

        certifications_score += 4

        certification_strengths.append(
            "Certification provider or organization is identifiable."
        )

    elif certifications:

        certifications_score += 2

        certification_improvements.append(
            "Include the certification provider or issuing organization."
        )

    certifications_score = min(
        certifications_score,
        10
    )

    # =========================================================
    # OVERALL SCORE
    # =========================================================

    overall = (
        contact_score
        + education_score
        + skills_score
        + projects_score
        + experience_score
        + certifications_score
    )

    # =========================================================
    # GLOBAL FEEDBACK
    # =========================================================

    all_strengths = (
        contact_strengths
        + education_strengths
        + skills_strengths
        + project_strengths
        + experience_strengths
        + certification_strengths
    )

    all_improvements = (
        contact_improvements
        + education_improvements
        + skills_improvements
        + project_improvements
        + experience_improvements
        + certification_improvements
    )

    strengths = list(
        dict.fromkeys(all_strengths)
    )

    improvements = list(
        dict.fromkeys(all_improvements)
    )

    # =========================================================
    # RETURN
    # =========================================================

    return {

        "overall_score": overall,

        "section_scores": {

            "contact": {
                "score": contact_score,
                "out_of": 10,
                "percentage": round(
                    (contact_score / 10) * 100
                ),
                "strengths": contact_strengths,
                "improvements": contact_improvements
            },

            "education": {
                "score": education_score,
                "out_of": 15,
                "percentage": round(
                    (education_score / 15) * 100
                ),
                "strengths": education_strengths,
                "improvements": education_improvements
            },

            "skills": {
                "score": skills_score,
                "out_of": 20,
                "percentage": round(
                    (skills_score / 20) * 100
                ),
                "strengths": skills_strengths,
                "improvements": skills_improvements,
                "skills_list": normalized_skills
            },

            "projects": {
                "score": projects_score,
                "out_of": 25,
                "percentage": round(
                    (projects_score / 25) * 100
                ),
                "strengths": project_strengths,
                "improvements": project_improvements
            },

            "experience": {
                "score": experience_score,
                "out_of": 20,
                "percentage": round(
                    (experience_score / 20) * 100
                ),
                "strengths": experience_strengths,
                "improvements": experience_improvements
            },

            "certifications": {
                "score": certifications_score,
                "out_of": 10,
                "percentage": round(
                    (certifications_score / 10) * 100
                ),
                "strengths": certification_strengths,
                "improvements": certification_improvements
            }
        },

        "strengths": strengths[:8],

        "improvements": improvements[:8],

        "normalized_skills": normalized_skills
    }
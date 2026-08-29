resume_data = {}


def save_resume_skills(skills):
    global resume_data
    resume_data["skills"] = skills


def get_resume_skills():
    return resume_data.get("skills", [])
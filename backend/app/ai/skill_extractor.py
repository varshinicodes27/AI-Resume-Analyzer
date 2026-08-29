SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "JavaScript",
    "TypeScript",
    "HTML",
    "CSS",
    "React",
    "Angular",
    "Vue",
    "Node.js",
    "Express",
    "FastAPI",
    "Django",
    "Flask",
    "Spring",
    "Spring Boot",
    "Hibernate",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "SQL",
    "Git",
    "GitHub",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "GCP",
    "REST API",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "Power BI",
    "Tableau"
]


def extract_skills(text: str):
    found = []

    lower_text = text.lower()

    for skill in SKILLS:
        if skill.lower() in lower_text:
            found.append(skill)

    return sorted(list(set(found)))
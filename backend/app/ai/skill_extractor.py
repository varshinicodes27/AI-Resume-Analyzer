import re


# ============================================================
# COMPREHENSIVE SKILL DATABASE
# ============================================================

SKILLS = [
    # Programming
    "Python", "Java", "C", "C++", "C#", "JavaScript", "TypeScript",
    "Kotlin", "Go", "Golang", "Rust", "PHP", "Ruby", "Swift", "R", "Dart",

    # Frontend
    "HTML", "HTML5", "CSS", "CSS3", "React", "React.js", "Next.js",
    "Angular", "Vue", "Vue.js", "Svelte", "Bootstrap", "Tailwind CSS",
    "Material UI", "jQuery",

    # Backend
    "Node.js", "Node", "Express", "Express.js", "Spring", "Spring Boot",
    "Spring MVC", "Hibernate", "JPA", "Java Persistence API", "FastAPI",
    "Django", "Flask", "Laravel", ".NET", "ASP.NET", "ASP.NET Core",

    # APIs / Architecture
    "REST API", "REST APIs", "RESTful API", "GraphQL", "WebSocket",
    "Microservices", "API Development", "JSON", "XML",

    # Databases
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "Oracle", "SQLite",
    "Microsoft SQL Server", "SQL Server", "Redis", "Cassandra",
    "DynamoDB", "Firebase", "Firestore",

    # Cloud
    "AWS", "Amazon Web Services", "EC2", "S3", "Lambda", "RDS",
    "CloudFront", "Azure", "Microsoft Azure", "Google Cloud", "GCP",
    "Google Cloud Platform",

    # DevOps
    "Git", "GitHub", "GitLab", "Bitbucket", "Docker", "Kubernetes",
    "Jenkins", "CI/CD", "Continuous Integration", "Continuous Deployment",
    "Terraform", "Ansible", "Linux", "Unix", "Nginx", "Apache",

    # Java ecosystem
    "Maven", "Gradle", "Spring Data JPA", "Spring Security",
    "Spring Cloud", "JUnit", "Mockito",

    # Python ecosystem
    "Pandas", "NumPy", "Scikit-learn", "SciPy", "Matplotlib",
    "Seaborn", "TensorFlow", "PyTorch", "Keras",

    # AI / ML
    "Machine Learning", "Deep Learning", "Artificial Intelligence",
    "Natural Language Processing", "NLP", "Computer Vision",
    "Generative AI", "GenAI", "Large Language Models", "LLM",
    "Transformers", "BERT", "OpenAI", "Gemini", "Hugging Face",
    "LangChain",

    # Data
    "Data Analysis", "Data Analytics", "Data Science", "Data Visualization",
    "Power BI", "Tableau", "Excel", "Apache Spark", "Hadoop", "Big Data",

    # Tools
    "VS Code", "Visual Studio", "IntelliJ IDEA", "Eclipse", "Postman",
    "Jira", "Confluence", "Figma",

    # Core CS
    "Data Structures", "Algorithms", "Data Structures and Algorithms",
    "Object Oriented Programming", "OOP", "Operating Systems",
    "Computer Networks", "Database Management Systems", "DBMS",
    "Software Engineering", "System Design",

    # Testing
    "Unit Testing", "Integration Testing", "Selenium", "Cypress",
    "Playwright", "PyTest",

    # Other
    "Git Version Control", "Agile", "Scrum", "SDLC"
]


# ============================================================
# SKILL ALIASES
# ============================================================

SKILL_ALIASES = {
    # Python
    "python": "Python",
    "python3": "Python",
    "python 3": "Python",
    "python programming": "Python",

    # Java & Spring
    "java": "Java",
    "core java": "Java",
    "java programming": "Java",
    "java language": "Java",
    "java 8": "Java",
    "java 11": "Java",
    "java 17": "Java",
    "java standard edition": "Java",
    "java se": "Java",
    "java ee": "Java EE",
    "j2ee": "Java EE",
    "spring": "Spring",
    "springboot": "Spring Boot",
    "spring-boot": "Spring Boot",
    "spring boot": "Spring Boot",
    "spring boot framework": "Spring Boot",
    "spring mvc": "Spring MVC",
    "spring data jpa": "Spring Data JPA",
    "spring security": "Spring Security",
    "spring cloud": "Spring Cloud",
    "hibernate": "Hibernate",
    "jpa": "JPA",
    "java persistence api": "JPA",
    "jdbc": "JDBC",

    # JavaScript / TypeScript / Frontend
    "javascript": "JavaScript",
    "js": "JavaScript",
    "jscript": "JavaScript",
    "es6": "JavaScript",
    "ecmascript": "JavaScript",
    "typescript": "TypeScript",
    "ts": "TypeScript",
    "react": "React.js",
    "reactjs": "React.js",
    "react.js": "React.js",
    "react js": "React.js",
    "react native": "React Native",
    "next": "Next.js",
    "nextjs": "Next.js",
    "next.js": "Next.js",
    "next js": "Next.js",
    "angular": "Angular",
    "angularjs": "Angular",
    "angular.js": "Angular",
    "vue": "Vue.js",
    "vuejs": "Vue.js",
    "vue.js": "Vue.js",
    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "node js": "Node.js",
    "express": "Express.js",
    "expressjs": "Express.js",
    "express.js": "Express.js",
    "express js": "Express.js",
    "html": "HTML",
    "html5": "HTML",
    "css": "CSS",
    "css3": "CSS",
    "tailwind": "Tailwind CSS",
    "tailwind css": "Tailwind CSS",
    "tailwindcss": "Tailwind CSS",
    "bootstrap": "Bootstrap",
    "material ui": "Material UI",
    "mui": "Material UI",

    # APIs & Web Services
    "rest": "REST APIs",
    "restful": "REST APIs",
    "rest api": "REST APIs",
    "rest apis": "REST APIs",
    "restful api": "REST APIs",
    "restful apis": "REST APIs",
    "rest api fundamentals": "REST APIs",
    "restful web services": "REST APIs",
    "rest web services": "REST APIs",
    "rest api development": "REST APIs",
    "graphql": "GraphQL",
    "api development": "API Development",

    # Databases & SQL
    "sql": "SQL",
    "sql queries": "SQL",
    "sql query": "SQL",
    "structured query language": "SQL",
    "sql queries / dbms": "SQL",
    "mysql": "MySQL",
    "mysql database": "MySQL",
    "mysql db": "MySQL",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "postgres db": "PostgreSQL",
    "postgresql database": "PostgreSQL",
    "mongodb": "MongoDB",
    "mongodb database": "MongoDB",
    "redis": "Redis",
    "oracle": "Oracle",
    "oracle database": "Oracle",
    "oracle db": "Oracle",
    "sqlite": "SQLite",

    # C / C++ / C# / .NET
    "c": "C",
    "c programming": "C",
    "c language": "C",
    "cpp": "C++",
    "c++": "C++",
    "c plus plus": "C++",
    "csharp": "C#",
    "c#": "C#",
    "c sharp": "C#",
    ".net": ".NET",
    "dotnet": ".NET",
    "asp.net": "ASP.NET",
    "asp.net core": "ASP.NET Core",

    # Cloud & DevOps
    "aws": "AWS",
    "amazon aws": "AWS",
    "amazon web services": "AWS",
    "azure": "Azure",
    "microsoft azure": "Azure",
    "gcp": "Google Cloud",
    "google cloud": "Google Cloud",
    "google cloud platform": "Google Cloud",
    "docker": "Docker",
    "docker container": "Docker",
    "docker containers": "Docker",
    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",
    "git": "Git",
    "git version control": "Git",
    "github": "GitHub",
    "github repository": "GitHub",
    "gitlab": "GitLab",
    "bitbucket": "Bitbucket",
    "ci cd": "CI/CD",
    "ci/cd": "CI/CD",
    "continuous integration": "CI/CD",
    "continuous deployment": "CI/CD",
    "jenkins": "Jenkins",
    "linux": "Linux",
    "unix": "Unix",

    # Core CS & Algorithms
    "oop": "OOP",
    "object oriented programming": "OOP",
    "object-oriented programming": "OOP",
    "dsa": "DSA",
    "data structures": "DSA",
    "data structures and algorithms": "DSA",
    "data structures & algorithms": "DSA",
    "algorithms": "Algorithms",
    "dbms": "DBMS",
    "database management systems": "DBMS",
    "database management system": "DBMS",
    "operating systems": "Operating Systems",
    "computer networks": "Computer Networks",
    "system design": "System Design",
    "microservices": "Microservices",

    # AI / ML / Data
    "ai": "AI",
    "artificial intelligence": "AI",
    "ml": "Machine Learning",
    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "dl": "Deep Learning",
    "nlp": "NLP",
    "natural language processing": "NLP",
    "generative ai": "Generative AI",
    "genai": "Generative AI",
    "gen ai": "Generative AI",
    "llm": "LLM",
    "large language models": "LLM",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "powerbi": "Power BI",
    "power bi": "Power BI",
    "opencv": "OpenCV",
}


# ============================================================
# NORMALIZE SKILL
# ============================================================

def normalize_skill(skill):

    skill = str(skill).lower().strip()

    skill = skill.replace("_", " ")
    skill = re.sub(r"\s+", " ", skill)

    # Normalize aliases
    if skill in SKILL_ALIASES:
        return SKILL_ALIASES[skill]

    # Match official skill name
    for official_skill in SKILLS:
        if skill == official_skill.lower():
            return official_skill

    return skill.title()


# ============================================================
# BUILD SAFE REGEX
# ============================================================

def build_skill_pattern(skill):

    skill_lower = skill.lower().strip()

    # C must be matched independently
    if skill_lower == "c":
        return r"(?<![a-z0-9+#])c(?![a-z0-9+#])"

    # C++
    if skill_lower == "c++":
        return r"(?<![a-z0-9])c\+\+(?![a-z0-9])"

    # C#
    if skill_lower == "c#":
        return r"(?<![a-z0-9])c#(?![a-z0-9])"

    # Go (prevent matching ordinary words like 'going', 'good')
    if skill_lower == "go":
        return r"(?<![a-z0-9+#])go\s*(?=developer|engineer|programming|lang|backend|code|\b)(?![a-z0-9+#])"

    # R
    if skill_lower == "r":
        return r"(?<![a-z0-9+#])r\s*(?=programming|language|script|studio|\b)(?![a-z0-9+#])"

    # Normal skills
    return (
        r"(?<![a-z0-9+#])"
        + re.escape(skill_lower)
        + r"(?![a-z0-9+#])"
    )


# ============================================================
# EXTRACT SKILLS
# ============================================================

def extract_skills(text: str):

    if not text:
        return []

    # Convert input to string
    text = str(text)

    # Normalize common punctuation
    normalized_text = text.lower()

    normalized_text = normalized_text.replace("–", "-")
    normalized_text = normalized_text.replace("—", "-")

    # Combine all known skills and alias keys into a unified search pool
    all_search_skills = sorted(
        list(set(SKILLS + list(SKILL_ALIASES.keys()))),
        key=lambda s: len(s),
        reverse=True
    )

    matched_spans = []
    found = set()

    for skill in all_search_skills:

        pattern = build_skill_pattern(skill)
        matches = list(re.finditer(pattern, normalized_text))

        valid_match = False

        for m in matches:

            m_start, m_end = m.start(), m.end()

            # Check if this match is completely subsumed by an already matched longer skill span
            is_subsumed = False

            for span_start, span_end, longer_skill in matched_spans:

                if (
                    span_start <= m_start
                    and m_end <= span_end
                    and (span_end - span_start) > (m_end - m_start)
                ):
                    is_subsumed = True
                    break

            if not is_subsumed:
                matched_spans.append((m_start, m_end, skill))
                valid_match = True

        if valid_match:
            normalized_skill_name = normalize_skill(skill)
            if normalized_skill_name:
                found.add(normalized_skill_name)

    return sorted(found)


# ============================================================
# EXTRACT SKILLS FROM JOB DESCRIPTION
# ============================================================

def extract_jd_skills(job_description: str):
    if not job_description:
        return []

    return extract_skills(job_description)

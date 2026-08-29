import re


def extract_projects(text):

    projects = []

    lines = text.split("\n")

    project_section = False

    stop_sections = [
        "certifications",
        "experience",
        "education",
        "skills",
        "technical skills",
        "achievements"
    ]

    ignore_words = [
        "developed",
        "achieved",
        "generating",
        "using",
        "implemented",
        "designed",
        "created",
        "built",
        "accuracy",
        "libraries",
        "python libraries",
        "logistic regression",
        "model",
        "insights"
    ]

    for line in lines:

        clean = (
            line
            .replace("•", "")
            .replace("●", "")
            .replace("–", "")
            .strip()
        )

        if not clean:
            continue

        # Start PROJECTS section
        if clean.lower() in ["projects", "project"]:
            project_section = True
            continue

        # Stop PROJECTS section
        if clean.lower() in stop_sections:
            project_section = False
            continue

        if not project_section:
            continue

        # Ignore description lines
        if any(
            word in clean.lower()
            for word in ignore_words
        ):
            continue

        # Remove URLs
        clean = re.sub(
            r'https?://\S+',
            '',
            clean
        ).strip()

        # Remove technology part
        if "|" in clean:
            clean = clean.split("|")[0].strip()

        # Remove description after "-"
        if "-" in clean:
            clean = clean.split("-")[0].strip()

        words = clean.split()

        # Project title condition
        if (
            2 <= len(words) <= 6
            and len(clean) > 5
        ):

            title = clean.strip()

            # Ignore links / demo labels
            if (
                title.lower().startswith("live demo")
                or title.lower().startswith("github")
                or title.lower().startswith("demo")
            ):
                continue

            # Avoid duplicates while preserving order
            if title not in projects:
                projects.append(title)

    return projects
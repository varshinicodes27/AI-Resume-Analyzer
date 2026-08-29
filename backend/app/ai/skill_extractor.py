import re


def extract_skills(text: str):
    if not text:
        return []

    found = []
    lower_text = text.lower()

    for skill in SKILLS:

        skill_lower = skill.lower()

        # Special handling for C
        if skill_lower == "c":
            pattern = r"(?<![a-z0-9+#])c(?![a-z0-9+#])"

        else:
            # Match complete skill names instead of random substrings
            pattern = (
                r"(?<![a-z0-9+#])"
                + re.escape(skill_lower)
                + r"(?![a-z0-9+#])"
            )

        if re.search(pattern, lower_text):
            found.append(skill)

    return sorted(set(found))
import re


def extract_education(text):

    education = []

    lines = text.split("\n")

    keywords = [
        "B.Tech",
        "Bachelor of Technology",
        "B.E",
        "Bachelor of Engineering",
        "M.Tech",
        "Master",
        "B.Sc",
        "M.Sc",
        "University",
        "College",
        "Institute"
    ]

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Remove bullet symbols
        line = line.replace("•", "").strip()

        if any(keyword.lower() in line.lower() for keyword in keywords):

            # avoid long summary sentences
            if len(line.split()) <= 12:
                
                line = re.sub(r"\s+", " ", line)
                line = line.replace("nd rea", "and Research")

                education.append(line)


    return list(set(education))
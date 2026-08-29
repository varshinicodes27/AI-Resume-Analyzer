import re


def extract_candidate_details(text):

    # Email extraction
    email = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    # Phone extraction
    phone = re.findall(
    r"(?:\+91[\s-]?)?[6-9]\d{9}",
    text
    )

    # Name extraction (basic approach)
    lines = text.split("\n")

    name = "Not Found"

    for line in lines[:10]:
        line = line.strip()

        if line and len(line.split()) <= 4:
            name = line
            break


    return {
        "name": name,
        "email": email[0] if email else "Not Found",
        "phone": phone[0] if phone else "Not Found"
    }
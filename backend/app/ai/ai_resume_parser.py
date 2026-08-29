import os
import json
import time

from dotenv import load_dotenv
from google import genai


load_dotenv()


# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def parse_resume_with_ai(resume_text: str):

    prompt = f"""
You are an expert ATS Resume Analyzer.

Analyze the resume below and return ONLY valid JSON.

Return the JSON in exactly this structure:

{{
    "candidate": {{
        "name": "",
        "email": "",
        "phone": "",
        "linkedin": "",
        "github": "",
        "portfolio": ""
    }},
    "education": [],
    "skills": [],
    "projects": [],
    "experience": [],
    "certifications": []
}}

IMPORTANT RULES:

1. Return ONLY valid JSON.
2. Do not return markdown.
3. Do not return explanations.
4. Do not add extra text outside the JSON.
5. Extract information ONLY from the resume.
6. NEVER invent, guess, or generate missing information.
7. If information is missing, return "" or [].

CANDIDATE INFORMATION:

8. Extract the candidate's full name.
9. Extract the candidate's email address.
10. Extract the candidate's phone number.
11. Extract the LinkedIn URL if present.
12. Extract the GitHub URL if present.
13. Extract the portfolio/personal website URL if present.
14. Preserve URLs exactly as they appear.
15. Do NOT treat LinkedIn, GitHub, or portfolio links as projects.

EDUCATION:

16. Extract educational qualifications.
17. Include degree/qualification and institution.
18. Include graduation/expected graduation year when available.
19. Include CGPA or percentage when clearly available.

SKILLS:

20. Extract only technical skills.
21. Do not include soft skills such as teamwork, communication,
    leadership, etc.
22. Avoid duplicate skills.

PROJECTS:

23. Extract actual project names.
24. Include a short project description when available.
25. Do NOT include headings such as "PROJECTS".
26. Do NOT include certification names as projects.
27. Do NOT include college names as projects.
28. Do NOT include job titles as projects.
29. Do NOT include GitHub links as projects.
30. Do NOT include Live Demo links as projects.
31. Do not create project names that are not present in the resume.

EXPERIENCE:

32. Extract internships, jobs, and professional experience.
33. Include company/organization and role when available.
34. Include dates when available.
35. Include description when available.
36. If there is no experience, return [].

CERTIFICATIONS:

37. Extract certification names only.
38. Include issuing organization when clearly available.
39. Do not treat certifications as projects.

IMPORTANT:

If LinkedIn, GitHub, or portfolio URLs exist,
return them under candidate.

If they do not exist, return:

"linkedin": "",
"github": "",
"portfolio": ""

Resume:

{resume_text}
"""

    # Gemini model available for your API key
    model = "gemini-3.6-flash"

    max_retries = 3

    for attempt in range(max_retries):

        try:

            print(
                f"Trying Gemini model: {model} "
                f"(attempt {attempt + 1}/{max_retries})"
            )

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            # Make sure Gemini returned something
            if not response.text:
                raise ValueError(
                    "Gemini returned an empty response."
                )

            text = response.text.strip()

            # Remove markdown code fences if Gemini adds them
            if text.startswith("```"):

                text = (
                    text
                    .replace("```json", "")
                    .replace("```JSON", "")
                    .replace("```", "")
                    .strip()
                )

            # Convert JSON string into Python dictionary
            result = json.loads(text)

            print(
                f"Gemini analysis successful using {model}"
            )

            return result

        except json.JSONDecodeError as error:

            raise ValueError(
                f"Gemini returned invalid JSON: {error}"
            )

        except Exception as error:

            error_message = str(error)

            temporary_error = (
                "503" in error_message
                or "UNAVAILABLE" in error_message
                or "high demand" in error_message.lower()
                or "429" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
            )

            if temporary_error and attempt < max_retries - 1:

                wait_time = 2 ** attempt

                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

                continue

            raise RuntimeError(
                f"Gemini resume analysis failed: {error}"
            )
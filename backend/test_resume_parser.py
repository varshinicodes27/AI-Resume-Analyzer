from app.ai.ai_resume_parser import parse_resume_with_ai

sample = """
John Doe

Email: john@gmail.com
Phone: 9876543210

Skills:
Python
Java
React
SQL

Projects:
Bank Management System
AI Resume Analyzer

Education:
Bachelor of Technology
ABC University

Experience:
Software Intern - Cognifyz Technologies

Certifications:
HackerRank Java
"""

result = parse_resume_with_ai(sample)

print(result)
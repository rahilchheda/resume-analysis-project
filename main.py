# main.py

from skills_db import skills_db, skill_weights, job_roles
from utils import read_pdf_resume, extract_skills, calculate_resume_score, suggest_roles

def main():
    resume_path = "Rahil_Chheda_Resume.pdf"  # your resume file
    resume_text = read_pdf_resume(resume_path)

    skills_found = extract_skills(resume_text, skills_db)
    print("Skills found:", skills_found)

    score = calculate_resume_score(skills_found, skill_weights)
    print(f"Resume Score (out of 100): {score}")

    roles = suggest_roles(skills_found, job_roles)
    print("Suggested Job Roles:", roles)

if __name__ == "__main__":
    main()

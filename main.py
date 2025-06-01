from fastapi import FastAPI, UploadFile, File
from utils import (
    read_pdf_resume,
    extract_skills,
    extract_experience,
    extract_project_based_skills,
    calculate_resume_score,
    suggest_roles,
    check_section_completeness,
    categorize_skills
)
import shutil
import uuid
import os
from typing import List

app = FastAPI()

# --------------------- Constants ---------------------
skills_db = ["Python", "Machine Learning", "SQL", "Tableau", "Power BI"]
base_skill_weights = {skill: 2 for skill in skills_db}

job_roles = {
    "Data Analyst": {"SQL", "Tableau", "Power BI"},
    "ML Engineer": {"Python", "Machine Learning"},
    "BI Developer": {"Power BI", "SQL"}
}

# --------------------- Endpoint ---------------------
@app.post("/analyze-resume/")
async def analyze_resume(file: UploadFile = File(...)):
    temp_file_path = f"temp_{uuid.uuid4()}.pdf"

    # Save file temporarily
    with open(temp_file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Step 1: Extract text
    resume_text = read_pdf_resume(temp_file_path)

    # Step 2: Extract and categorize skills
    skills_found = extract_skills(resume_text, skills_db)
    project_skills = extract_project_based_skills(resume_text, skills_db)
    categorized = categorize_skills(list(skills_found | project_skills))

    # Step 3: Extract experience-related lines
    experience_phrases = extract_experience(resume_text)

    # Step 4: Create dynamic skill weights (boost experienced skills)
    skill_weights = base_skill_weights.copy()
    for phrase in experience_phrases:
        for skill in skills_found:
            if skill.lower() in phrase.lower():
                skill_weights[skill] = skill_weights.get(skill, 2) + 1

    # Step 5: Score resume
    score = calculate_resume_score(skills_found, skill_weights, project_skills)

    # Step 6: Suggest roles
    combined_skills = skills_found.union(project_skills)
    top_roles = suggest_roles(combined_skills, job_roles)

    # Step 7: Section completeness
    completeness = check_section_completeness(resume_text)

    # Step 8: Cleanup
    os.remove(temp_file_path)

    return {
        "skills_found": list(skills_found),
        "project_skills": list(project_skills),
        "categorized_skills": categorized,
        "experience_phrases": experience_phrases,
        "resume_score": score,
        "suggested_roles": top_roles,
        "section_completeness": completeness
    }

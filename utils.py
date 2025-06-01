import PyPDF2
import re

# --------------------- PDF Reader ---------------------
def read_pdf_resume(file_path="Rahil_Chheda_Resume.pdf"):
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.lower()


# --------------------- Skill Extraction ---------------------
def extract_skills(resume_text, skills_db):
    found_skills = set()
    for skill in skills_db:
        if skill.lower() in resume_text:
            found_skills.add(skill)
    return found_skills


def extract_project_based_skills(resume_text, skills_db):
    project_keywords = ["project", "developed", "built", "created", "implemented", "designed"]
    project_sentences = []

    # Break into sentences
    sentences = re.split(r'[.?!\n]', resume_text)

    # Find sentences that likely describe projects
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in project_keywords):
            project_sentences.append(sentence)

    # Extract project-related skills
    project_skills = set()
    for sentence in project_sentences:
        for skill in skills_db:
            if skill.lower() in sentence.lower():
                project_skills.add(skill)

    return project_skills


# --------------------- Resume Scoring ---------------------
def calculate_resume_score(skills_found, skill_weights, project_skills=None):
    total_score = 0
    for skill in skills_found:
        base_weight = skill_weights.get(skill, 1)
        if project_skills and skill in project_skills:
            total_score += base_weight * 1.5  # boost if used in projects
        else:
            total_score += base_weight

    max_possible = sum(skill_weights.values()) * 1.5  # assuming project boosting
    normalized_score = (total_score / max_possible) * 100
    return round(normalized_score, 2)


# --------------------- Role Suggestion ---------------------
def suggest_roles(skills_found, job_roles):
    role_scores = {}
    for role, required_skills in job_roles.items():
        match_count = len(set(skills_found) & required_skills)
        role_scores[role] = match_count
    sorted_roles = sorted(role_scores.items(), key=lambda x: x[1], reverse=True)
    return [role for role, score in sorted_roles if score > 0][:3]


# --------------------- Resume Completeness ---------------------
def check_section_completeness(text: str) -> dict:
    sections = ["Education", "Experience", "Skills", "Projects", "Certifications", "Achievements"]
    completeness = {}
    for section in sections:
        completeness[section] = section.lower() in text.lower()
    return completeness


# --------------------- Skill Categorization ---------------------
def categorize_skills(skills: list[str]) -> dict:
    tools = {"Excel", "Tableau", "Power BI", "AWS", "Git", "Docker"}
    languages = {"Python", "Java", "C++", "SQL", "R"}
    soft_skills = {"communication", "teamwork", "leadership", "problem-solving"}

    categorized = {"tools": [], "languages": [], "soft_skills": [], "others": []}

    for skill in skills:
        s = skill.lower()
        if any(t.lower() == s for t in tools):
            categorized["tools"].append(skill)
        elif any(l.lower() == s for l in languages):
            categorized["languages"].append(skill)
        elif any(ss.lower() == s for ss in soft_skills):
            categorized["soft_skills"].append(skill)
        else:
            categorized["others"].append(skill)
    return categorized


# --------------------- Experience Snippets (Optional for UI Display) ---------------------
def extract_experience(text):
    experience_keywords = ["experience", "worked on", "handled", "responsible for"]
    lines = text.split("\n")
    experience_lines = [
        line.strip() for line in lines
        if any(kw in line.lower() for kw in experience_keywords)
    ]
    return experience_lines

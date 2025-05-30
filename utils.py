import PyPDF2

def read_pdf_resume(file_path="Rahil_Chheda_Resume.pdf"):
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.lower()

def extract_skills(resume_text, skills_db):
    found_skills = set()
    for skill in skills_db:
        if skill.lower() in resume_text:
            found_skills.add(skill)
    return found_skills

def calculate_resume_score(skills_found, skill_weights):
    total_score = 0
    for skill in skills_found:
        total_score += skill_weights.get(skill, 1)
    max_possible = sum(skill_weights.values())
    normalized_score = (total_score / max_possible) * 100
    return round(normalized_score, 2)

def suggest_roles(skills_found, job_roles):
    role_scores = {}
    for role, required_skills in job_roles.items():
        match_count = len(set(skills_found) & required_skills)
        role_scores[role] = match_count
    sorted_roles = sorted(role_scores.items(), key=lambda x: x[1], reverse=True)
    return [role for role, score in sorted_roles if score > 0][:3]

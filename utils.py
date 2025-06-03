import PyPDF2
import re

# ---------------- PDF Reader ----------------
def read_pdf_resume(file_path="resume.pdf"):
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.lower()

# ---------------- Skill DB ----------------
skills_db = {
    "languages": {
        "Python", "Java", "C++", "C", "R", "JavaScript", "TypeScript", "SQL", "Go", "Ruby", "PHP", "Swift", "Kotlin"
    },
    "tools": {
        "Excel", "Power BI", "Tableau", "Git", "Docker", "Jira", "Linux", "Postman", "Figma", "VS Code", "IntelliJ", "Notion"
    },
    "frameworks": {
        "Flask", "Django", "FastAPI", "React", "Angular", "Node.js", "Spring Boot", "Next.js", "Vue.js", "Bootstrap", "Express"
    },
    "cloud": {
        "AWS", "Azure", "GCP", "Firebase", "Heroku", "DigitalOcean", "Netlify"
    },
    "ml": {
        "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "Scikit-learn", "TensorFlow", "PyTorch",
        "Keras", "XGBoost", "LightGBM", "OpenCV", "Hugging Face"
    },
    "databases": {
        "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite", "Oracle", "Cassandra", "Snowflake", "BigQuery"
    },
    "devops": {
        "CI/CD", "Kubernetes", "Terraform", "Ansible", "Prometheus", "Grafana", "Jenkins", "GitHub Actions"
    },
    "cybersecurity": {
        "Network Security", "Penetration Testing", "Wireshark", "Burp Suite", "SIEM", "Firewalls", "OWASP", "Nmap"
    },
    "marketing": {
        "SEO", "Google Analytics", "Google Ads", "Facebook Ads", "Email Marketing", "Content Strategy", "CRM", "Ahrefs"
    },
    "finance": {
        "Accounting", "Tally", "GST", "Financial Modeling", "Budgeting", "Forecasting", "QuickBooks", "Valuation"
    },
    "soft_skills": {
        "communication", "leadership", "teamwork", "problem-solving", "critical thinking", "adaptability", "time management",
        "collaboration", "emotional intelligence", "decision making", "conflict resolution"
    }
}


def flatten_skills(skills_dict):
    return set().union(*skills_dict.values())

# ---------------- Skill Extraction ----------------
def extract_skills(resume_text, skills_dict):
    found = set()
    for category, skill_set in skills_dict.items():
        for skill in skill_set:
            if skill.lower() in resume_text:
                found.add(skill)
    return found

# ---------------- Project Skill Extraction ----------------
def extract_project_based_skills(resume_text, all_skills):
    project_keywords = ["project", "developed", "built", "created", "implemented", "designed"]
    sentences = re.split(r'[.?!\n]', resume_text)
    project_sentences = [s for s in sentences if any(k in s.lower() for k in project_keywords)]
    project_skills = set()
    for sentence in project_sentences:
        for skill in all_skills:
            if skill.lower() in sentence.lower():
                project_skills.add(skill)
    return project_skills

def calculate_resume_score(resume_text, skills_found, skill_weights, project_skills=None):
    # 1. Skill Match Score (60%)
    skill_score = 0
    max_skill_score = sum(skill_weights.values())

    for skill in skills_found:
        base_weight = skill_weights.get(skill, 1)
        if project_skills and skill in project_skills:
            skill_score += base_weight * 1.5
        else:
            skill_score += base_weight

    skill_match_percent = (skill_score / (max_skill_score * 0.8)) * 60  # scaled to 60%

    # 2. Keyword Diversity Bonus (15%)
    diversity_bonus = min(len(skills_found), 15) / 15 * 50

    # 3. Soft Skills & Tools Bonus (25%)
    soft_skills = {"communication", "leadership", "teamwork", "problem-solving", "critical thinking"}
    tools = {"Excel", "Power BI", "Tableau", "Git", "Docker"}
    soft_tools = soft_skills.union(tools)
    soft_tools_bonus = len(skills_found & soft_tools) / len(soft_tools) * 25

    # Final Score
    total_score = skill_match_percent + diversity_bonus + soft_tools_bonus
    return round(min(total_score, 100), 2)



# ---------------- Resume Insights ----------------
def generate_strengths_and_improvements(skills_found, project_skills):
    strengths = []
    improvements = []

    if project_skills:
        strengths.append("Good use of project-based skills")
    if len(skills_found) >= 10:
        strengths.append("Wide range of relevant skills detected")
    if any(skill in skills_found for skill in ["Python", "SQL", "Machine Learning"]):
        strengths.append("Strong technical foundation")

    if len(skills_found) < 5:
        improvements.append("Add more relevant technical or soft skills")
    if not project_skills:
        improvements.append("Highlight your project contributions more explicitly")
    if "communication" not in skills_found:
        improvements.append("Include soft skills like communication or teamwork")

    return strengths, improvements

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

from utils import (
    read_pdf_resume,
    extract_skills,
    extract_project_based_skills,
    calculate_resume_score,
    flatten_skills,
    skills_db,
    generate_strengths_and_improvements
)

app = FastAPI()


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Define job role database
job_roles = {
    "Data Analyst": {"Excel", "SQL", "Tableau", "Power BI", "Python", "Statistics", "Data Cleaning"},
    "ML Engineer": {"Python", "Scikit-learn", "TensorFlow", "PyTorch", "NLP", "Deep Learning", "Docker"},
    "Data Scientist": {"Python", "SQL", "Machine Learning", "Pandas", "NLP", "Statistics", "Matplotlib"},
    "Cloud Engineer": {"AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Linux"},
    "DevOps Engineer": {"Docker", "Kubernetes", "CI/CD", "Jenkins", "Linux", "AWS", "Monitoring"},
    "Frontend Developer": {"React", "Angular", "JavaScript", "TypeScript", "HTML", "CSS", "Redux"},
    "Backend Developer": {"Node.js", "Django", "Flask", "SQL", "MongoDB", "REST API", "PostgreSQL"},
    "Full Stack Developer": {"React", "Node.js", "Python", "SQL", "HTML", "CSS", "Docker"},
    "Cybersecurity Analyst": {"Network Security", "Penetration Testing", "Firewalls", "SIEM", "Linux", "Wireshark"},
    "Business Analyst": {"Excel", "Power BI", "SQL", "Requirement Gathering", "Data Visualization", "UML", "Agile"},
    "Product Manager": {"Roadmapping", "JIRA", "User Stories", "Market Research", "Agile", "Leadership", "UX"},
    "Software Engineer": {"Java", "Python", "C++", "Git", "Data Structures", "OOP", "REST API"},
    "QA Engineer": {"Selenium", "TestNG", "Jira", "Automation Testing", "Manual Testing", "Bug Reporting"},
    "AI Engineer": {"TensorFlow", "Keras", "Python", "Deep Learning", "NLP", "Computer Vision", "Reinforcement Learning"},
    "System Administrator": {"Linux", "Windows Server", "Networking", "Bash", "Virtualization", "AWS", "Monitoring"},
    "Financial Analyst": {"Excel", "Financial Modeling", "Power BI", "Accounting", "Valuation", "Forecasting"},
    "Accountant": {"Tally", "GST", "Accounting", "Excel", "Taxation", "Bookkeeping", "Reconciliation"},
    "HR Analyst": {"Excel", "People Analytics", "Power BI", "Recruitment", "HRMS", "Communication"},
    "Digital Marketing Specialist": {"SEO", "Google Ads", "Analytics", "Social Media", "Content Strategy", "Email Marketing"},
    "Content Writer": {"Content Writing", "SEO", "Blogging", "Copywriting", "Grammar", "Proofreading"},
    "UX/UI Designer": {"Figma", "Adobe XD", "Wireframing", "User Research", "Prototyping", "Design Systems"}
}


def suggest_roles(skills_found, job_roles):
    scores = {}
    for role, required in job_roles.items():
        matches = skills_found & required
        scores[role] = len(matches)
    return sorted([role for role, s in scores.items() if s > 0], key=lambda r: scores[r], reverse=True)[:3]

@app.post("/analyze-resume/")
async def analyze_resume(file: UploadFile = File(...)):
    file_path = "uploaded_resume.pdf"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    resume_text = read_pdf_resume(file_path)
    all_skills = flatten_skills(skills_db)
    skills_found = extract_skills(resume_text, skills_db)
    project_skills = extract_project_based_skills(resume_text, all_skills)

    skill_weights = {skill: 1 for skill in all_skills}
    score = calculate_resume_score(resume_text, skills_found, skill_weights, project_skills)

    total_skills = skills_found.union(project_skills)
    top_roles = suggest_roles(total_skills, job_roles)
    strengths, improvements = generate_strengths_and_improvements(skills_found, project_skills)

    return JSONResponse({
        "score": score,
        "job_roles": top_roles,
        "strengths": strengths,
        "improvements": improvements
    })

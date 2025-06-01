def boost_project_skills(text, skills_db):
    boosted_skills = set()
    lines = text.split("\n")
    for line in lines:
        if any(keyword in line.lower() for keyword in ["project", "built", "developed"]):
            for skill in skills_db:
                if skill.lower() in line.lower():
                    boosted_skills.add(skill)
    return boosted_skills

# Example text with project lines
resume_text_projects = """
Project: Built a data visualization dashboard using Tableau.
Developed several automation scripts with Python.
Worked on SQL database optimization.
"""

boosted = boost_project_skills(resume_text_projects, skills_db)
print("Boosted skills found in projects:", boosted)

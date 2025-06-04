# skills_db.py

skills_db = {
    "python", "java", "c++", "c#", "javascript", "html", "css", "sql", "r", "matlab",
    "pandas", "numpy", "matplotlib", "scikit-learn", "tensorflow", "pytorch", "keras",
    "django", "flask", "react", "angular", "node.js", "docker", "kubernetes", "git",
    "linux", "aws", "azure", "gcp", "tableau", "power bi", "hadoop", "spark"
}

skill_weights = {
    "python": 5, "java": 4, "c++": 4, "javascript": 4, "html": 2, "css": 2,
    "sql": 3, "r": 3, "matlab": 2, "pandas": 5, "numpy": 5, "matplotlib": 3,
    "scikit-learn": 5, "tensorflow": 6, "pytorch": 6, "keras": 5,
    "django": 4, "flask": 4, "react": 4, "angular": 4, "node.js": 4,
    "docker": 6, "kubernetes": 6, "git": 3, "linux": 3,
    "aws": 7, "azure": 6, "gcp": 6, "tableau": 4, "power bi": 4, "hadoop": 6, "spark": 6
}

job_roles = {
    "Data Analyst": {"python", "pandas", "numpy", "sql", "power bi", "tableau"},
    "Web Developer": {"html", "css", "javascript", "react", "node.js", "flask", "django"},
    "ML Engineer": {"python", "scikit-learn", "tensorflow", "pytorch", "keras", "numpy"},
    "Cloud Engineer": {"aws", "azure", "gcp", "docker", "kubernetes", "linux"},
    "Frontend Developer": {"html", "css", "javascript", "react", "angular"},
    "Backend Developer": {"node.js", "django", "flask", "sql", "python"},
    "Full Stack Developer": {"html", "css", "javascript", "node.js", "react", "django", "python"},
    "Data Scientist": {"python", "pandas", "numpy", "scikit-learn", "tensorflow", "matplotlib", "sql"}
}

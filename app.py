from flask import Flask, request, jsonify
from utils import extract_skills, calculate_resume_score, suggest_roles
from skills_db import skills_db, skill_weights, job_roles

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    data = request.json
    resume_text = data.get('resume_text', '').lower()
    skills_found = extract_skills(resume_text, skills_db)
    score = calculate_resume_score(skills_found, skill_weights)
    roles = suggest_roles(skills_found, job_roles)
    return jsonify({
        'skills_found': list(skills_found),
        'resume_score': score,
        'suggested_roles': roles
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, render_template, request, send_file
from utils.resume_parser import extract_text_from_pdf
from utils.preprocess import clean_text
from utils.matcher import extract_skills, section_score
from utils.report_pdf import generate_pdf

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        resume = request.files["resume"]
        job_desc = request.form["job_desc"]

        resume.save("uploaded_resume.pdf")

        raw_resume = extract_text_from_pdf("uploaded_resume.pdf")
        clean_resume = clean_text(raw_resume)
        clean_job = clean_text(job_desc)

        with open("skills_list.txt") as f:
            skills = [line.strip() for line in f]

        resume_skills = extract_skills(clean_resume, skills)
        job_skills = extract_skills(clean_job, skills)

        project_keywords = ["project", "developed", "built", "implemented"]
        experience_keywords = ["experience", "intern", "worked", "company"]

        resume_projects = extract_skills(clean_resume, project_keywords)
        job_projects = extract_skills(clean_job, project_keywords)

        resume_exp = extract_skills(clean_resume, experience_keywords)
        job_exp = extract_skills(clean_job, experience_keywords)

        skill_score = section_score(resume_skills, job_skills)
        project_score = section_score(resume_projects, job_projects)
        experience_score = section_score(resume_exp, job_exp)

        ats_score = round(
            (skill_score * 0.5) +
            (project_score * 0.3) +
            (experience_score * 0.2),
            2
        )

        if ats_score >= 75:
            verdict = "Strong Fit"
        elif ats_score >= 50:
            verdict = "Moderate Fit"
        else:
            verdict = "Weak Fit"

        skill_coverage = 0
        if job_skills:
            skill_coverage = round((len(resume_skills) / len(job_skills)) * 100, 2)

        missing_skills = list(set(job_skills) - set(resume_skills))

        report_data = {
            "Match Percentage": f"{ats_score}%",
            "Skill Coverage": f"{skill_coverage}%",
            "ATS Verdict": verdict,
            "Skills Match": f"{skill_score}%",
            "Projects Match": f"{project_score}%",
            "Experience Match": f"{experience_score}%",
            "Missing Skills": ", ".join(missing_skills)
        }

        generate_pdf(report_data)

        return render_template(
            "index.html",
            match=ats_score,
            resume_skills=resume_skills,
            missing_skills=missing_skills,
            skill_coverage=skill_coverage,
            ats_score=ats_score,
            verdict=verdict,
            skill_score=skill_score,
            project_score=project_score,
            experience_score=experience_score
        )

    return render_template("index.html")


@app.route("/download")
def download():
    return send_file("ATS_Report.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


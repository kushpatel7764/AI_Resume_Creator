import os
import src.Database_Queries
import src.Database
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

# Get database path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(project_dir, 'Jobs_Database.db')


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/job_list')
def job_list():
    jobs = src.Database_Queries.get_jobs(db_path)
    return render_template("jobs.html", jobs=jobs)


@app.route('/job_details/<string:job_id>')
def job_detail(job_id):
    job = src.Database_Queries.get_job_by_id(db_path, job_id)
    return render_template("job_details.html", job=job)


@app.route('/profile_page')
def profile_page():
    return render_template("user_profile.html")

@app.route('/resume')
def resume():
    # TODO: If two profiles have same names then the user will not be able to distinguish between the two
    profiles = src.Database_Queries.get_profiles(db_path)
    return render_template("create_resume.html", profiles=profiles, job=None)

@app.route('/resume_with_job_id/<string:job_id>')
def resume_with_job_id(job_id):
    job = None
    # TODO: If two profiles have same names then the user will not be able to distinguish between the two
    profiles = src.Database_Queries.get_profiles(db_path)
    if job_id:
        job = src.Database_Queries.get_job_by_id(db_path, job_id)
    return render_template("create_resume.html", profiles=profiles, job=job)

@app.route('/create_resume/<string:job_id>/<string:profile_id>')
def create_resume(job_id, profile_id):
    job = src.Database_Queries.get_job_by_id(db_path, job_id) if job_id else ""
    profile = src.Database_Queries.get_profile_by_id(db_path, profile_id) if profile_id else ""

    pass

@app.route('/save_profile', methods=['POST'])
def save_profile():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    github = request.form.get('github', '')
    linkedin = request.form.get('linkedin', '')
    projects = request.form.get('projects', '')
    classes = request.form.get('classes', '')
    other = request.form.get('other', '')

    user_info = [name, email, phone, github, linkedin, projects, classes, other]

    # Only insert to the database if not in testing mode
    if not app.config['TESTING']:
        src.Database.insert_user_profile_data(db_path, user_info)

    return jsonify({"name": f"{name}",
                    "email": f"{email}",
                    "phone": f"{phone}",
                    "github": f"{github}",
                    "linkedin": f"{linkedin}",
                    "projects": f"{projects}",
                    "classes": f"{classes}",
                    "other": f"{other}",
                    "message": "All fields saved successfully."})


if __name__ == '__main__':
    app.run(debug=True)

import os
import Database_Queries
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

#Get database path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(project_dir, 'Jobs_Database.db')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/job_list')
def job_list():
    jobs = Database_Queries.get_jobs(db_path)
    return render_template("jobs.html", jobs=jobs)

@app.route('/job_details/<string:job_id>')
def job_detail(job_id):
    job = Database_Queries.get_job_by_id(db_path, job_id)
    return render_template("job_details.html", job=job)

@app.route('/user_profile')
def profile():
    return render_template("user_profile.html")

if __name__ == '__main__':
    app.run(debug=True)

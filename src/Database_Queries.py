import sqlite3
import src.Utility


def get_jobs(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, site, job_url, location, max_amount, salary_range, interval FROM jobs")
    jobs = cursor.fetchall()
    conn.close()
    job_list = []
    for job in jobs:
        job_list.append({
            "id": job[0],
            "title": job[1],
            "site": job[2],
            "job_url": job[3],
            "location": job[4],
            "max_amount": job[5],
            "salary_range": job[6],
            "interval": job[7]
        })

    return job_list

def get_profiles(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM user_profiles")
    profiles = cursor.fetchall()
    conn.close()
    profile_list = []
    for profile in profiles:
        profile_list.append({
            "id": profile[0],
            "name": profile[1],
        })

    return profile_list


# Function to fetch a job by ID
def get_job_by_id(db, job_id):
    # AI used here
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, site, location, description, salary_range, max_amount, min_amount, "
                   "interval FROM jobs WHERE id = ?", (job_id,))
    job = cursor.fetchone()
    conn.close()

    if job:
        return {
            "id": job[0],
            "title": job[1],
            "site": job[2],
            "location": job[3],
            "description": job[4],
            "salary_range": job[5],
            "max_amount": job[6],
            "min_amount": job[7],
            "interval": job[8]
        }
    return None


# Function to fetch a profile by ID
def get_profile_by_id(db, profile_id):
    # AI used here
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, phone, linkedin, other FROM user_profiles WHERE id = ?", (profile_id,))
    profile = cursor.fetchone()
    conn.close()

    if profile:
        return {
            "id": profile[0],
            "name": profile[1],
            "email": profile[2],
            "phone": profile[3],
            "linkedin": profile[4],
            "other": profile[5]
        }
    return None

# Function to fetch projects by userID
def get_projects_by_id(db, profile_id):
    # AI used here
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT description FROM projects WHERE user_id = ?", (profile_id,))
    projects = cursor.fetchall()
    conn.close()

    project_string = src.Utility.array_to_string(projects)
    return project_string

# Function to fetch classes by userID
def get_classes_by_id(db, profile_id):
    # AI used here
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM classes WHERE user_id = ?", (profile_id,))
    classes = cursor.fetchall()
    conn.close()

    class_string = src.Utility.array_to_string(classes)
    return class_string


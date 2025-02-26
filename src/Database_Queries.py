import sqlite3


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

import json
import sqlite3
import os

import src.Utility
# TODO: Change Database ID as phone number


# Function to get all json objects
def get_all_json_objects(filenames):
    # AI gen start here ------------------
    setup_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Moves up one level
    # AI ends ----------------------------
    json_objects = []
    for filename in filenames:
        # AI gen start here ------------------
        sql_file_path = os.path.join(setup_dir, filename)
        # AI ends ----------------------------
        with open(sql_file_path, 'r') as f:
            for line in f:
                # Read each line in rapid_jobs2.json file as a JSON object
                objs_array_or_obj = json.loads(line)
                # If objs_array is an actual array then loop through it otherwise just add it to json_objects' list
                if type(objs_array_or_obj) is list:
                    for obj in objs_array_or_obj:
                        json_objects.append(obj)
                else:
                    json_objects.append(objs_array_or_obj)
    return json_objects


# Connect to database
def setup_database_with_sql_file(cursor, conn, sql_filename):
    # AI gen start here ------------------
    setup_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Moves up one level
    sql_file_path = os.path.join(setup_dir, sql_filename)
    # AI ends ----------------------------
    # Read the SQL file
    with open(sql_file_path, "r") as file:
        sql_script = file.read()

    # Execute the SQL script (AI helped find the executescript() function)
    cursor.executescript(sql_script)
    # Commit changes
    conn.commit()


# Insert data into the job table
def insert_to_job(conn, cursor, job_info):
    job_id = job_info.get("id")

    # Check if job_id already exists
    cursor.execute("SELECT COUNT(*) FROM jobs WHERE id = ?", (job_id,))
    exists = cursor.fetchone()[0]

    if exists:
        print(f"Skipping job {job_id}, already exists.")
        return  # Skip inserting duplicate

    # There are two different date posted in the json files
    # There is date_posted and datePosted, this just fixes that issue
    date_posted = job_info.get("date_posted", None)
    date_posted2 = job_info.get("datePosted", None)
    date = ""
    if date_posted is not None:
        date = date_posted
    else:
        date = date_posted2

    cursor.execute("""
        Insert INTO jobs (id, site, job_url, job_url_direct, title, company_name, company_industry, company_url,
        company_url_direct, company_addresses, company_num_employees, company_revenue, company_description, logo_photo_url,
        banner_photo_url, ceo_name, ceo_photo_url, location, job_type, date_posted, salary_source, interval, min_amount,
        max_amount, currency, is_remote, job_level, job_function, listing_type, emails, description, employment_type,
        salary_range, image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (job_info.get("id"),
          job_info.get("site", None),
          job_info.get("job_url", None),
          job_info.get("job_url_direct", None),
          job_info.get("title", None),
          job_info.get("company_name", None),
          job_info.get("company_industry", None),
          job_info.get("company_url", None),
          job_info.get("company_url_direct", None),
          job_info.get("company_addresses", None),  # Use company ID as foreign key
          job_info.get("company_num_employees", None),
          job_info.get("company_revenue", None),
          job_info.get("company_description", None),
          job_info.get("logo_photo_url", None),
          job_info.get("banner_photo_url", None),
          job_info.get("ceo_name", None),
          job_info.get("ceo_photo_url", None),
          job_info.get("location", None),
          job_info.get("job_type", None),
          date,
          job_info.get("salary_source", None),
          job_info.get("interval", None),
          job_info.get("min_amount", None),
          job_info.get("max_amount", None),
          job_info.get("currency", None),
          job_info.get("is_remote", None),
          job_info.get("job_level", None),
          job_info.get("job_function", None),
          job_info.get("listing_type", None),
          job_info.get("emails", None),
          job_info.get("description", None),
          job_info.get("employment_type", None),
          job_info.get("salary_range", None),
          job_info.get("image", None))
    )
    conn.commit()


# Function to insert into job providers table
def insert_to_job_provider(conn, cursor, job_id, providers):
    for provider in providers:
        provider_name = provider.get("jobProvider")

        # Check if job_id and provider_name already exist
        cursor.execute("SELECT COUNT(*) FROM job_providers WHERE job_id = ? AND provider_name = ?", (job_id, provider_name))
        exists = cursor.fetchone()[0]

        if exists:
            print(f"Skipping job {job_id} from provider {provider_name}, already exists.")
            return  # Skip inserting duplicate
        cursor.execute("""
            INSERT INTO job_providers (job_id, provider_name, provider_url)
            VALUES (?, ?, ?)
        """, (job_id, provider.get('jobProvider', None), provider.get('url', None)))
    conn.commit()


# user_profile is an array the container all the information for the user_profile table. It can contain nulls.
# At each index of the array there should be information for a field of the database respectively.
def insert_to_user_profile(conn, cursor, user_profile):
    profile_name = user_profile[0]
    user_name = user_profile[1]
    email = user_profile[2]
    phone = user_profile[3]
    github = user_profile[4]
    linkedin = user_profile[5]
    projects = user_profile[6]
    classes = user_profile[7]
    other = user_profile[8]

    array_of_projects = src.Utility.string_to_array(projects)
    array_of_classes = src.Utility.string_to_array(classes)

    cursor.execute('''INSERT OR IGNORE INTO user_profiles(profile_name, user_name, email, phone, github, linkedin, other)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (profile_name, user_name, email, phone, github, linkedin, other))
    _user_id = cursor.lastrowid

    # TODO: Make sure user_id is never zero.

    for project in array_of_projects:
        # If just space not need to add to database
        if project.strip() != "":
            cursor.execute('''INSERT OR IGNORE INTO projects(user_id, description)
                                      VALUES (?, ?)''',
                           (_user_id, project))

    for _class in array_of_classes:
        if _class.strip() != "":
            cursor.execute('''INSERT OR IGNORE INTO classes(user_id, name)
                                              VALUES (?, ?)''',
                           (_user_id, _class))

    conn.commit()


def initialize_job_tables(database_path):
    """
    Sets up job-related tables in the database.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    setup_database_with_sql_file(cursor, conn, "job_database.sql")
    conn.close()


def initialize_user_tables(database_path):
    """
    Sets up user-related tables in the database.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    setup_database_with_sql_file(cursor, conn, "user_database.sql")
    conn.close()


def insert_job_data(database_path, json_files):
    """
    Make sure job database is initialized and insert job and job provider data from JSON files.
    json_files: is an array containing JSON filenames.
    """
    initialize_job_tables(database_path)
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    all_json_obj = get_all_json_objects(json_files)
    for obj in all_json_obj:
        insert_to_job(conn, cursor, obj)
        insert_to_job_provider(conn, cursor, obj['id'], obj.get('jobProviders', []))

    print("Job data successfully inserted!")
    conn.close()


def insert_user_profile_data(database_path, user_profile):
    """
    Make sure user tables are initialized and inserts user profile data given in the parameter to the database.
    """
    initialize_user_tables(database_path)
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    insert_to_user_profile(conn, cursor, user_profile)

    print("User profile data successfully inserted!")
    conn.close()

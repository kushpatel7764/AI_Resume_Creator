import os
import sqlite3
import unittest
from src.Database import insert_job_data
from src.Database import insert_user_profile_data
from src.Database import setup_database_with_sql_file
from src.Database import get_all_json_objects
from src.Database_Queries import get_job_by_id
from src.app import app


class TestJobFunctionality(unittest.TestCase):

    def test_get_all_json_objects(self):
        # Testing json data is AI generated.
        test_data = """{"id": "123", "title": "Engineer", "company_name": "TechCorp", "description": "Develop software."}
        {"id": "456", "title": "Data Analyst", "company_name": "DataWorks", "description": "Analyze data."}
        {"id": "789", "title": "Administrator", "company_name": "NetSolutions", "description": "Manage IT systems."}"""
        # AI gen start here ------------------
        setup_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )  # Moves up one level
        sql_file_path = os.path.join(setup_dir, "test_jobs.json")
        # AI ends ----------------------------
        with open(sql_file_path, "w") as f:
            f.write(test_data)
        # Now get json objects from the test file
        json_objects = get_all_json_objects(["test_jobs.json"])

        self.assertEqual(len(json_objects), 3)
        print("Number of objects is correct.")
        self.assertEqual(json_objects[0]["id"], "123")
        self.assertEqual(json_objects[1]["title"], "Data Analyst")
        self.assertEqual(json_objects[2]["company_name"], "NetSolutions")
        print("First, Middle, and Last values are correct.")

        os.remove(sql_file_path)

    def test_database_setup(self):
        # Sample test job data to insert into the database
        test_data = """{"id": "123", "site": "Indeed", "job_url": "www.indeed.com", "description": "Develop software."}
        {"id": "456", "site": "LinkedIn", "job_url": "https://www.linkedin.com/", "description": "Analyze data."}
        {"id": "789", "site": "Glassdoor", "job_url": "https://www.glassdoor.com/", "description": "Manage IT systems."}"""
        # AI gen start here ------------------
        setup_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )  # Moves up one level
        sql_file_path = os.path.join(setup_dir, "test_jobs.json")
        # AI ends ----------------------------
        with open(sql_file_path, "w") as f:
            f.write(test_data)

        insert_job_data("../test_jobs.db", ["test_jobs.json"])
        conn = sqlite3.connect("../test_jobs.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM jobs WHERE id = '123'")
        result = cursor.fetchone()

        self.assertIsNotNone(
            result, "Test job with id 123 was not saved to the database"
        )
        self.assertEqual(result[0], "123", f"Expected id '123', but got {result[0]}")
        self.assertEqual(
            result[1], "Indeed", f"Expected title 'Indeed', but got {result[1]}"
        )
        self.assertEqual(
            result[2],
            "www.indeed.com",
            f"Expected company name 'www.indeed.com', but got {result[2]}",
        )
        self.assertEqual(
            result[30],
            "Develop software.",
            f"Expected description 'Develop software.', but got {result[3]}",
        )
        print("Database creation was successful and accurate.")
        os.remove(sql_file_path)
        os.remove("../test_jobs.db")
        conn.close()

    def test_job_details(self):
        # Create an in-memory SQLite database
        conn = sqlite3.connect("../temp_data.db")  # Learned from AI how to make an in memory database
        cursor = conn.cursor()

        # Create the jobs table
        setup_database_with_sql_file(cursor, conn, "job_database.sql")

        # Insert sample data
        cursor.execute('''
            INSERT INTO jobs (id, title, site, location, description, salary_range, max_amount, min_amount, interval)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            "2", "Data Analyst", "LinkedIn", "San Francisco, CA", "Analyze datasets", "$60k-$90k", 90000, 60000, "yearly"
        ))
        conn.commit()

        job_id = "2"
        job = get_job_by_id("../temp_data.db", job_id)

        self.assertIsNotNone(job, "Job details should not be None")
        self.assertEqual(job['id'], job_id, "Job ID should match the requested ID")
        self.assertIn('title', job, "Job title should be present")  # AI helped find assertIn
        self.assertIn('salary_range', job, "Salary range should be present")
        self.assertIn('description', job, "Job description should be present")
        self.assertIn('site', job, "Job site should be present")
        self.assertIn('location', job, "Job location should be present")
        self.assertIn('min_amount', job, "Job min_amount should be present")
        self.assertIn('max_amount', job, "Job max_amount should be present")
        self.assertIn('interval', job, "interval should be present")
        self.assertEqual(job["title"], "Data Analyst", "Job title should match the requested title")
        self.assertEqual(job["description"], "Analyze datasets", "Job description should match the requested description")
        self.assertEqual(job['site'], "LinkedIn", "Job site should match the requested site")
        self.assertEqual(job['location'], "San Francisco, CA", "Job location should match the requested location")
        self.assertEqual(job['min_amount'], 60000, "Job min_amount should match the requested min_amount")
        self.assertEqual(job['max_amount'], 90000, "Job max_amount should match the requested max_amount")
        self.assertEqual(job['salary_range'], "$60k-$90k", "Salary range should be present")
        self.assertEqual(job['interval'], "yearly", "interval should be match the given interval")

        print("All the expected field were retrieved correctly.")

        os.remove("../temp_data.db")


class SaveProfileTestCases(unittest.TestCase):

    def test_user_input_request(self):
        with app.test_client() as client:
            app.config['TESTING'] = True  # Set to True during testing
            user_input = {
                'name': 'Kush Patel',
                'email': 'kushpatelrp1234@gmail.com',
                'phone': '0123456789',
                'github': 'github.com',
                'linkedin': '',
                'projects': 'project1, project2',
                'classes': 'class1, ',
                'other': 'I am smart.'
            }

            response = client.post("/save_profile", data=user_input)
            server_response = response.get_json()
            self.assertEqual(server_response["name"], user_input['name'])
            self.assertEqual(server_response["email"], user_input['email'])
            self.assertEqual(server_response["phone"], user_input['phone'])
            self.assertEqual(server_response["github"], user_input['github'])
            self.assertEqual(server_response["linkedin"], user_input['linkedin'])
            self.assertEqual(server_response["projects"], user_input['projects'])
            self.assertEqual(server_response["classes"], user_input['classes'])
            self.assertEqual(server_response["other"], user_input['other'])
            self.assertEqual(server_response["message"], "All fields saved successfully.")

    def test_save_profile(self):
        user_profile = [
            'Shiv Patel',  # name
            'shivpatelrp123@gmail.com',  # email
            '5089717530',  # phone
            'https://github.com/shivpatel',  # github
            'https://linkedin.com/in/shivpatel',  # linkedin
            'Project1, Project2',  # projects
            'Class1, ',  # classes
            'Other info'  # other
        ]
        # This is the function that is being tested.
        insert_user_profile_data("../test_job.db", user_profile=user_profile)

        # Connect to the temp database to verify the insertion
        conn = sqlite3.connect("../test_job.db")
        cursor = conn.cursor()

        # Check user_profiles table
        cursor.execute("SELECT * FROM user_profiles WHERE email = ?", (user_profile[1],))
        user = cursor.fetchone()
        self.assertIsNotNone(user, "User profile should be inserted")
        self.assertEqual(user[1], user_profile[0], "Name should match")
        self.assertEqual(user[2], user_profile[1], "Email should match")
        self.assertEqual(user[3], user_profile[2], "Phone should match")
        self.assertEqual(user[4], user_profile[3], "github should match")
        self.assertEqual(user[5], user_profile[4], "linkedin should match")
        self.assertEqual(user[6], user_profile[7], "other should match")

        # Check projects table
        cursor.execute("SELECT * FROM projects WHERE user_id = ?", (user[0],))
        projects = cursor.fetchall()
        self.assertEqual(len(projects), 2, "Two projects should be inserted")
        # projects[0] first row then [2] means third colum
        self.assertEqual(projects[0][2], 'Project1', "First project should be 'Project1'")
        self.assertEqual(projects[1][2], 'Project2', "Second project should be 'Project2'")

        # Check classes table
        cursor.execute("SELECT * FROM classes WHERE user_id = ?", (user[0],))
        classes = cursor.fetchall()
        self.assertEqual(len(classes), 1, "Two classes should be inserted")
        self.assertEqual(classes[0][2], "Class1", "First class should be 'Class1'")
        conn.close()
        os.remove("../test_job.db")


if __name__ == "__main__":
    unittest.main()

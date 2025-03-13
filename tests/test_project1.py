import os
import sqlite3
import unittest
import json
from src.Database import insert_job_data
from src.Database import insert_user_profile_data
from src.Database import setup_database_with_sql_file
from src.Database import get_all_json_objects
from src.Database_Queries import get_job_by_id
from src.Database_Queries import get_profile_by_id
from src.Database_Queries import get_projects_by_id
from src.Database_Queries import get_classes_by_id
from src.GeminiAPI import ask_gemini
from src.Utility import user_profile_to_keywords
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
                'profile_name': "profile1",
                'user_name': 'Kush Patel',
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
            self.assertEqual(server_response["profile_name"], user_input['profile_name'])
            self.assertEqual(server_response["user_name"], user_input['user_name'])
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
            'Profile1',  # profile_name
            'Shiv Patel',  # user_name
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
        cursor.execute("SELECT * FROM user_profiles WHERE email = ?", (user_profile[2],))
        user = cursor.fetchone()
        self.assertIsNotNone(user, "User profile should be inserted")
        self.assertEqual(user[1], user_profile[0], "profile name should match")
        self.assertEqual(user[2], user_profile[1], "username should match")
        self.assertEqual(user[3], user_profile[2], "Email should match")
        self.assertEqual(user[4], user_profile[3], "Phone should match")
        self.assertEqual(user[5], user_profile[4], "github should match")
        self.assertEqual(user[6], user_profile[5], "linkedin should match")
        self.assertEqual(user[7], user_profile[8], "other should match")

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


class TestLLMRequest(unittest.TestCase):

    def test_llm_api_request(self):
        user_info = "I am a computer science student at Bridgewater University. I also work for google."
        job_des = "We need a software developer who has worked for google before."
        response = ask_gemini(user_info, job_des, "resume")

        assert response.status_code == 200, f"Expected 200, but got {response.status_code}"
        print("Test passed: Received 200 OK response")


class TestAIPrompt(unittest.TestCase):
    """
    Here I want to test that AI prompt is being built correctly. First, I need to make sure that the database queries
    are giving the correct output. The function, get_job_by_id(), gets job description from database. This function has
    already been tested in test_job_details test case. The functions such as get_profile_by_id, get_projects_by_id,
    get_classes_by_id that get user_info from database need to be tested.
    """

    def setUp(self):
        self.user_profile = [
            'Profile1', 'Shiv Patel', 'shivpatelrp@gmail.com', '1234567890',
            'https://github.com/shivpatel', 'https://linkedin.com/in/shivpatel',
            'Project1, Project2', 'Class1, ', 'Other info'
        ]
        self.db_path = "../test_job.db"
        insert_user_profile_data(self.db_path, user_profile=self.user_profile)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close_everything(self):
        self.conn.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    # This test ensures that get_profile_by_id() function retrieves data from database accurately.
    def test_get_profile_by_id(self):

        try:
            # The Function being tested
            profile = get_profile_by_id(self.db_path, 1)

            # Make sure profile contains the correct information
            self.assertIsNotNone(profile, "User profile should be inserted")
            self.assertEqual(profile["profile_name"], self.user_profile[0], "profile name should match")
            self.assertEqual(profile["user_name"], self.user_profile[1], "username should match")
            self.assertEqual(profile["email"], self.user_profile[2], "Email should match")
            self.assertEqual(profile["phone"], self.user_profile[3], "Phone should match")
            self.assertEqual(profile["github"], self.user_profile[4], "github should match")
            self.assertEqual(profile["linkedin"], self.user_profile[5], "linkedin should match")
            self.assertEqual(profile["other"], self.user_profile[8], "other should match")

            profile = get_profile_by_id("../test_job.db", 0)
            self.assertIsNone(profile, "User profile should not be returned for an invalid id")
        finally:
            self.close_everything()

    def test_get_projects_by_id(self):

        try:
            # The Function being tested
            projects = get_projects_by_id(self.db_path, 1)

            # Make sure profile contains the correct information
            self.assertIsNotNone(projects, "projects should be retrieved")
            self.assertEqual(projects, "Project1, Project2", "Projects output should match")
            self.assertIsInstance(projects, str, "Projects should be returned as a string")

            projects = get_profile_by_id("../test_job.db", -1)
            self.assertIsNone(projects, "Projects should not be returned for an invalid id")

            # Testing with a non-existent ID
            projects = get_projects_by_id("../test_job.db", 23)
            self.assertEqual(projects, "", "projects should be empty for a non-existent ID")

            # Testing when database is empty
            self.cursor.execute("DELETE FROM projects")
            self.conn.commit()

            projects = get_projects_by_id("../test_job.db", 1)
            self.assertEqual(projects, "", "projects should be empty after deleting all entries")

        finally:
            self.close_everything()

    def test_get_classes_by_id(self):
        try:
            # The Function being tested
            classes = get_classes_by_id("../test_job.db", 1)

            # Make sure profile contains the correct information
            self.assertIsNotNone(classes, "Classes should be retrieved")
            self.assertEqual(classes, "Class1", "Classes output should match")
            self.assertIsInstance(classes, str, "Classes should be returned as a string")

            classes = get_classes_by_id("../test_job.db", -1)
            self.assertEqual(classes, "", "Classes should be empty for an invalid id")

            # Testing with a non-existent ID
            classes = get_classes_by_id("../test_job.db", 23)
            self.assertEqual(classes, "","Classes should be empty for a non-existent ID")

            # Testing when database is empty
            self.cursor.execute("DELETE FROM Classes")
            self.conn.commit()

            classes = get_classes_by_id("../test_job.db", 1)
            self.assertEqual(classes, "","Classes should be empty after deleting all entries")
        finally:
            self.close_everything()

    # This function takes user_profile, projects, and classes data and puts it all in one string.
    # Testing this function will ensure that user_info is being built properly.
    def test_user_profile_to_keywords(self):
        try:
            expected_output = ("profile_name: Profile1\n"
                               "user_name: Shiv Patel\n"
                               "email: shivpatelrp@gmail.com\n"
                               "phone: 1234567890\n"
                               "github: https://github.com/shivpatel\n"
                               "linkedin: https://linkedin.com/in/shivpatel\n"
                               "other: Other info\n"
                               "Projects: Project1, Project2\n"
                               "Classes: Class1")

            profile = get_profile_by_id(self.db_path, 1)
            projects = get_projects_by_id(self.db_path, 1)
            classes = get_classes_by_id(self.db_path, 1)

            # This function is being tested here
            user_info = user_profile_to_keywords(profile, projects, classes)

            self.assertEqual(user_info, expected_output, "user_info should be returned as expected")

            # Check for correct formatting, A.I. helped do this assert.
            self.assertTrue(user_info.count("\n") == 8, "There should be exactly 8 newline characters in output")

            # check empty values don't break the function
            profile["other"] = ""
            user_info_empty_other = user_profile_to_keywords(profile, projects, classes)
            self.assertIn("other: \n", user_info_empty_other, "Empty 'other' field should not have extra newline")

            empty_projects = ""
            user_info_empty_projects = user_profile_to_keywords(profile, empty_projects, classes)
            self.assertIn("Projects: \n", user_info_empty_projects, "Empty projects should still be included")
        finally:
            self.close_everything()

    # Now make sure that user_info and job description are present in the prompt that is being submitted to AI
    def test_prompt_submitted_to_AI(self):
        user_info = "I am a computer science student at Bridgewater University. I also work for google."
        job_des = "We need a software developer who has worked for google before."

        # Testing ask_gemini to ensure it is properly submitting user_info and job_des into the prompt being given to AI.
        response = ask_gemini(user_info, job_des, "resume")
        prompt_given_json = json.loads(response.request.body)
        prompt_given = prompt_given_json["contents"][0]["parts"][0]["text"]
        # Split prompt_given into three section first one is user_info, second is job_description, and last is prompt to
        # ai. This can be done with a split on newline char because I have built my prompt so that each newline char is
        # new section.
        prompt_given_three_sections = prompt_given.split("\n")
        personal_info_identifier = "Remember my Personal Information: "
        Job_description_identifier = "Remember the Job description: "

        user_info = personal_info_identifier + user_info
        job_des = Job_description_identifier + job_des

        self.assertEqual(prompt_given_three_sections[0], user_info, "prompt_given should contain user_info")
        self.assertEqual(prompt_given_three_sections[1], job_des, "prompt_given should contain job_des")

        # Make sure there are three sections
        self.assertEqual(len(prompt_given_three_sections), 3, "Prompt should only contain three sections")


if __name__ == "__main__":
    unittest.main()

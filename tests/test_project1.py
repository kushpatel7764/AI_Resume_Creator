import os
import sqlite3
import unittest
from src.Database import initialize_database
from src.Database import get_all_json_objects
from src.Database_Queries import get_job_by_id


class MyTestCase(unittest.TestCase):

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

        initialize_database("../test_jobs.db", ["test_jobs.json"])
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
        job_id = '993d586bad78d40a'
        job = get_job_by_id("../Jobs_Database.db", job_id)

        self.assertIsNotNone(job, "Job details should not be None")
        self.assertEqual(job['id'], job_id, "Job ID should match the requested ID")
        self.assertIn('title', job, "Job title should be present") #AI helped find assertIn
        self.assertIn('salary_range', job, "Salary range should be present")
        self.assertIn('description', job, "Job description should be present")
        self.assertIn('site', job, "Job site should be present")
        self.assertIn('location', job, "Job location should be present")
        self.assertIn('min_amount', job, "Job min_amount should be present")
        self.assertIn('max_amount', job, "Job max_amount should be present")
        self.assertIn('interval', job, "interval should be present")
        self.assertEqual(job['title'], "Hybrid - Software Development Specialist 4 (PN 20036298)",
                         "Job title should match the requested title")
        self.assertEqual(job['description'], """**What will you do?**


* Collaborates with IT Architecture staff, Chief Information Officer, and IT Managers to design innovative Azure container applications (ACA) using logic apps, APIs, microservice architecture, and MudBlazor in C# solutions aligning with the agency's requirements.
* Contributes to the analysis of the solution design business case and authors portions of the solution business case.
* Leads and facilitates discussions with the development team, product owners, and business SMEs on the best approach to implementing designs.
* Leads design reviews, writes, and reviews departmental code and/or configuration.
* Conducts detailed alternative analyses and determine end-user requirements.
* Identifies root causes for incidents and issues, offering solutions to prevent future defects.
* Provides post-production support for applications, including error handling, logging, load balancing, failover, and additional tasks.
* Mentors development staff on standards, best practices, leadership, and excellence in development.

**Why Work for the State of Ohio**
At the State of Ohio, we take care of the team that cares for Ohioans. We provide a variety of quality, competitive benefits to eligible full-time and part-time employees\*. For a list of all the State of Ohio Benefits, visit our Total Rewards website! Our benefits package includes:


* Medical Coverage
* Free Dental, Vision and Basic Life Insurance premiums after completion of eligibility period
* Paid time off, including vacation, personal, sick leave and 11 paid holidays per year
* Childbirth, Adoption, and Foster Care leave
* Education and Development Opportunities (Employee Development Funds, Public Service Loan Forgiveness, and more)
* Public Retirement Systems (such as OPERS, STRS, SERS, and HPRS) & Optional Deferred Compensation (Ohio Deferred Compensation)


* Benefits eligibility is dependent on a number of factors. The Agency Contact listed above will be able to provide specific benefits information for this position.

**Qualifications**
60 mos. combined work experience in any combination of the following: providing solutions design, developing project plans with project manager or recommending approach through defining tasks and/or leading meetings relating to programs for computer applications including 12 mos. work experience with Azure.  

  

* Or completion of associate core program in computer science or information systems **AND** 42 mos. combined work experience in any combination of the following: providing solutions design, developing project plans with project manager or recommending approach through defining tasks and/or leading meetings relating to programs for computer applications including 12 mos. work experience with Azure.

  

* Or completion of undergraduate core program in computer science or information systems **AND** 36 mos. combined work experience in any combination of the following: providing solutions design, developing project plans with project manager or recommending approach through defining tasks and/or leading meetings relating to programs for computer applications including 12 mos. work experience with Azure.

  

* Or equivalent of minimum class qualifications for employment noted above.

  

**Job Skills:** Software Development/Implementation
**Technical Skills:** Information Technology, Technical Documentation


**Professional Skills:** Collaboration, Growth Mindset, Managing Meetings, Developing Others, Continuous Improvement


**Primary Technology:** Microsoft Azure (12 mos. experience required)


*To request a reasonable accommodation due to disability, please contact ADA Coordinator Tamara Hairston at 614-466-2508 or by email at**EEO-DiversityAffairs@dodd.ohio.gov**.*

**Supplemental Information*** Current Department of Developmental Disabilities OCSEA employees shall receive first consideration pursuant to Article 17 of the collective bargaining agreement.
* Hourly wage will be paid at step 1, unless otherwise specified by collective bargaining agreement or rules outlined in the ORC/OAC.
* The final candidate selected for the position will be required to undergo a criminal background check. Rule 5123-2-02, “Background Investigations for Employment,” outlines disqualifying offenses that will preclude an applicant from being employed by the Department of Developmental Disabilities.
* No additional materials will be accepted after the closing date; in addition, you must clearly demonstrate how you meet minimum qualifications on your civil service application. Attachments to your civil service application are only supplemental and may not be considered.
* **Applicants selected to move forward in the hiring process will be contacted to schedule a mandatory in-person written assessment at our central office location.**

**ADA Statement**
Ohio is a Disability Inclusion State and strives to be a model employer of individuals with disabilities. The State of Ohio is committed to providing access and inclusion and reasonable accommodation in its services, activities, programs and employment opportunities in accordance with the Americans with Disabilities Act (ADA) and other applicable laws.

**Drug-Free Workplace**
The State of Ohio is a drug-free workplace which prohibits the use of marijuana (recreational marijuana/non-medical cannabis). Please note, this position may be subject to additional restrictions pursuant to the State of Ohio Drug-Free Workplace Policy (HR-39), and as outlined in the posting.""", "Job description should match the requested description")
        self.assertEqual(job['site'], "indeed", "Job site should match the requested site")
        self.assertEqual(job['location'], "Columbus, OH, US", "Job location should match the requested location")
        self.assertEqual(job['min_amount'], 42, "Job min_amount should match the requested min_amount")
        self.assertEqual(job['max_amount'], 62, "Job max_amount should match the requested max_amount")
        self.assertEqual(job['salary_range'], None, "Salary range should be present")
        self.assertEqual(job['interval'], "hourly", "interval should be match the given interval")

    def test_user_profile(self):
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
        initialize_database("../test_job.db", user_profile=user_profile)

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
        #projects[0] first row then [2] means third colum
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

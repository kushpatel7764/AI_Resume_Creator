import os
import sqlite3
import unittest
import json
from src.GeminiAPI import initialize_database
from src.GeminiAPI import get_all_json_objects
class MyTestCase(unittest.TestCase):
    def test_get_all_json_objects(self):
        # Testing json data is AI generated.
        test_data = """{"id": "123", "title": "Engineer", "company_name": "TechCorp", "description": "Develop software."}
        {"id": "456", "title": "Data Analyst", "company_name": "DataWorks", "description": "Analyze data."}
        {"id": "789", "title": "Administrator", "company_name": "NetSolutions", "description": "Manage IT systems."}"""
        with open("test_jobs.json", "w") as f:
            f.write(test_data)
        # Now get json objects from the test file
        json_objects = get_all_json_objects(['test_jobs.json'])

        self.assertEqual(len(json_objects), 3)
        print("Number of objects is correct.")
        self.assertEqual(json_objects[0]["id"], "123")
        self.assertEqual(json_objects[1]["title"], "Data Analyst")
        self.assertEqual(json_objects[2]["company_name"], "NetSolutions")
        print("First, Middle, and Last values are correct.")

        os.remove("test_jobs.json")
    def test_database_setup(self):
        """Test that job data is correctly saved to an in-memory SQLite database."""

        # Sample test job data to insert into the database
        test_data = '''{"id": "123", "title": "Engineer", "company_name": "TechCorp", "description": "Develop software."}
        {"id": "456", "title": "Data Analyst", "company_name": "DataWorks", "description": "Analyze data."}
        {"id": "789", "title": "Administrator", "company_name": "NetSolutions", "description": "Manage IT systems."}'''
        with open("test_jobs.json", "w") as f:
            f.write(test_data)

        initialize_database("test_jobs.db", ["test_jobs.json"])
        conn = sqlite3.connect("test_jobs.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM jobs WHERE id = '123'")
        result = cursor.fetchone()

        self.assertIsNotNone(result, "Test job with id 123 was not saved to the database")
        self.assertEqual(result[0], "123", f"Expected id '123', but got {result[0]}")
        self.assertEqual(result[1], "Engineer", f"Expected title 'Engineer', but got {result[1]}")
        self.assertEqual(result[2], "TechCorp", f"Expected company name 'TechCorp', but got {result[2]}")
        self.assertEqual(result[3], "Develop software.",
                         f"Expected description 'Develop software.', but got {result[3]}")

        conn.close()


if __name__ == '__main__':
    unittest.main()

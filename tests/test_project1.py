import json
from src.GeminiAPI import get_all_json_objects

def test_get_all_json_objects():
    # Testing json data is AI generated.
    test_data = """[
            [
                {"id": "123", "title": "Software Engineer", "company_name": "TechCorp",
                 "description": "Develop and maintain software."},
                {"id": "456", "title": "Data Analyst", "company_name": "DataWorks", "description": "Analyze data trends."},
                {"id": "789", "title": "System Administrator", "company_name": "NetSolutions",
                 "description": "Manage IT systems."}
            ]
        ]"""
    with open("test_jobs.json", "w") as f:
        json.dump(test_data, f)
    #Now get json objects from the test file
    json_objects = get_all_json_objects(['test_jobs.json'])

    # Ensure the correct number of job entries
    assert len(json_objects) == 3, "Expected 3 job entries"

    # Check first, middle, and last entries
    assert json_objects[0]["id"] == "123", "First job ID mismatch"
    assert json_objects[1]["title"] == "Data Analyst", "Middle job title mismatch"
    assert json_objects[2]["company_name"] == "NetSolutions", "Last job company mismatch"

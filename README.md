# KushPatel_Project1
This project uses Gemini A.I. model to generate a resume or cover letter in Markdown format. To create the resume, the A.I. model must be  
provided with a job description and a personal description. A WebUI has been added to this project for easier user 
interactions. To view the website, navigate to the src directory of this project and run python app.py. While the script
is running, open your browser and go to http://127.0.0.1:5000. The website has three tabs: Available Jobs, Profile, and Resume. In 
the Available Jobs tab, users can browse job listings. In the Profile tab, users to save information that can help their
employability. In the Resume tab, users can create a resume or cover letter for the selected job and profile with Google Gemini. 

**Instructions to Run the Program:**
1. Ensure libraries from `requirements.txt` are installed.
2. Ensure you have Python version 3.12 installed.
3. Place your Google Gemini API key in api_secrets.py as `gemini_api_key`.
4. Make sure rapid_jobs2.json is in the same directory as this script.
5. Run the script using `python GeminiAPI.py`.
6. The output will be saved as `Marked_Resume.md`.
7. To view job listings, run the following command inside the src directory: `python app.py`
8. One the script is running, open your browser and go to: http://127.0.0.1:5000.
9. In the Available Jobs tab, user can browse job listings and select a job they would like to apply for.
10. In the Profile tab, users can save their information.
11. In the Resume tab, users can create a resume or cover letter with Google Gemini.

**Test Functions**
* test_get_all_json_objects: Tests whether job data is correctly read from a JSON file.
* test_database_setup: Tests whether job data from a JSON file is successfully inserted into an SQLite database.
* test_job_details: Tests whether the function get_job_by_id function correctly retrieves 
the specified fields from the database. This ensures that a more complete data is displayed for user selected job item.
* test_user_input_request: Tests that /save_profile  correctly receives the input data as typed by the user. If all user 
input received from request.form is accurate, it can then be passed to the insert_user_profile_data function. This 
function will store all user input in the same SQLite database as the job data.
* test_save_profile: Tests that user input is correctly inserted into the SQLite database by insert_user_profile_data 
function.
* test_llm_api_request: Ensures that the ask_gemini API request is functioning correctly by checks whether the API response
returns a status code 200 (OK).
* test_get_profile_by_id: Ensures that get_profile_by_id() retrieves the correct  user profile from the database when given
a valid id that is in range.
* test_get_projects_by_id: Ensures that get_projects_by_id() retrieves the correct projects when given a valid in range Id.
* test_get_classes_by_id: Ensures that get_classes_by_id() retrieves the correct classes data.
* test_user_profile_to_keywords: Ensures that user_profile_to_keywords() correctly formats user data into a single string.
* test_prompt_submitted_to_AI:  Ensures that the automatically created AI prompt contains user_info and job_description 
before being sent to Gemini.


**Why Google Gemini AI?**
* I chose this google gemini api because I am familiar with it
from my cloud computing class. 
* I find it easier to find documentation for most google products--in case additional help was need. 
* Gemini is also excellent at handling high quality text which is very important when building a good resume from 
text input. 

**AI Prompt**
* The AI prompt in the code is designed to generate a well-structured Markdown resume. The prompt begins with
"Remember my Personal Information" and "Remember the Job Description." This instructs the AI model to retain both pieces 
of information before generating the output.
  
  Initially, my personal description lacked details about my experience, such as the IDEs I have worked with. As a result,
the AI provided a lot of advice but did not include many details about me in the resume. To fix this, I added more personal
details to my description. This led the AI to generate a Markdown resume that was about ninety percent complete.
  
  Then, I instructed the AI to incorporate keywords from the job description into my resume to further improve its relevance
and effectiveness.


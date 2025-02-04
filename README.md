# KushPatel_Project1
**Instructions to Run the Program:**
0. Ensure libraries from `requirements.txt` are installed.
1. Ensure you have Python version 3.12 installed.
2. Place your Google Gemini API key in api_secrets.py as `gemini_api_key`.
3. Make sure rapid_jobs2.json is in the same directory as this script.
4. Run the script using `python GeminiAPI.py`.
5. The output will be saved as `Marked_Resume.md`.

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


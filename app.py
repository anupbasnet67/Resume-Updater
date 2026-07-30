from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename
from processing.resume import process_resume
from processing.github import process_github_profile
from processing.other_info import process_text_file
from processing.analysis import analyze_candidate_fit

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/upload", methods=["POST"])
def upload():

    #store inputs of the FORM from home.html
    resume_file = request.files.get("resume_file")
    other_info_file = request.files.get("text")

    github_link = request.form["github_link"]
    job_description_text = request.form["job_description"]

    # Initialize text variables
    resume_text = ""
    github_summary = ""
    other_info_text = ""
    resume_path = ""

    # Save the resume if one was uploaded
    if resume_file and resume_file.filename != "":
        filename = secure_filename(resume_file.filename)
        resume_path = os.path.join(UPLOAD_FOLDER, filename)
        resume_file.save(resume_path)

        # Use the file path with your other script to extract text
        resume_text = process_resume(resume_path)
        
        if resume_text:
            print("--- Successfully extracted text from .docx ---")

    #Save github link if it were uploaded
    if github_link != "":
        github_summary = process_github_profile(github_link)
        if github_summary:
            print("\n--- Successfully generated GitHub Profile Summary ---")

    #Save job description if it were uploaded
    if job_description_text:
        print("--- Received Job Description Text ---")
        
    # Save the text file if one was uploaded
    if other_info_file and other_info_file.filename != "":
        other_info_filename = secure_filename(other_info_file.filename)
        other_info_path = os.path.join(UPLOAD_FOLDER, other_info_filename)
        other_info_file.save(other_info_path)
        other_info_text = process_text_file(other_info_path)
        if other_info_text:
            print("\n--- Successfully extracted text from other_info file ---")

    # --- Combine all text and send to LangChain for analysis ---
    print("\n--- Sending all data to AI for analysis... ---")
    analysis_result = analyze_candidate_fit(resume_text, job_description_text, github_summary, other_info_text)

    print("\n--- AI Analysis Complete ---")

    # The result is now a structured Pydantic object. Convert it to a dict for the template.
    if analysis_result:
        parsed_analysis = analysis_result.model_dump()
        # For display purposes, let's create a formatted string similar to the old one
        full_analysis_text = f"**ATS Score:**\n{parsed_analysis['ats_score']}\n\n"
        full_analysis_text += "**Missing Skills:**\n" + "\n".join(f"- {skill}" for skill in parsed_analysis['missing_skills']) + "\n\n"
        full_analysis_text += f"**Interview Prep Guide:**\n{parsed_analysis['interview_prep']}"
    else:
        # Handle error case where analysis fails
        parsed_analysis = {'ats_score': 'Error', 'missing_skills': [], 'interview_prep': 'Analysis failed.'}
        full_analysis_text = "Analysis failed."

    return render_template("results.html", 
                           analysis=parsed_analysis, 
                           resume_path=resume_path, 
                           full_analysis_text=full_analysis_text,
                           job_description=job_description_text)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename
from processing.resume import process_resume
from processing.github import process_github_profile
from processing.jobs import process_job_description
from processing.other_info import process_text_file

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
    other_info = request.files["text"]

    github_link = request.form["github_link"]
    job_description = request.form["job_description"]

    # Save the resume if one was uploaded
    if resume_file and resume_file.filename != "":
        filename = secure_filename(resume_file.filename)
        resume_path = os.path.join(UPLOAD_FOLDER, filename)
        resume_file.save(resume_path)

        # Use the file path with your other script to extract text
        print(f"File saved to: {resume_path}")
        resume_text = extract.process_resume(resume_path)
        
        if resume_text:
            print("--- Successfully extracted text from .docx ---")
            print(resume_text[:300] + "...")

    #Save github link if it were uploaded
    if github_link != "":
        github_summary = extract.process_github_profile(github_link)

    #Save job description if it were uploaded
    if job_description != "":
        job_markdown = extract.process_job_description(job_description)

    # Save the text file if one was uploaded
    if other_info.filename != "":
        other_info.save(os.path.join(UPLOAD_FOLDER, other_info.filename))

    return "Files uploaded successfully!"

    

if __name__ == "__main__":
    app.run(debug=True)
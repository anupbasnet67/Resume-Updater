# Resume-Updater

A smart tool designed to help job seekers optimize their resumes by analyzing them against specific job descriptions using AI. This application streamlines the process of tailoring your application materials to maximize your chances of success.

## Features

### Current Functionality:
*   **Resume Upload & Extraction:** Upload your resume in `.docx` format. The system automatically extracts its content for analysis.
*   **GitHub Profile Summary:** Provide your GitHub profile link, and the application will generate a summary of your projects and contributions.
*   **Job Description Input:** Paste the full job description directly into the form.
*   **Additional Information:** Optionally upload a `.txt` file with any other relevant information.
*   **AI-Powered Analysis:** Utilizes LangChain and Google Gemini to perform a comprehensive analysis, providing:
    *   An estimated **ATS (Applicant Tracking System) compatibility score**.
    *   A list of **missing skills** identified from the job description.
    *   A brief **interview preparation guide** tailored to the role and company's tech stack.
*   **Structured Output:** AI analysis results are returned in a structured format (JSON-like) for reliable and consistent parsing.

### Planned Features:
*   **Document Generation:** Automatically update your resume content based on AI feedback.
*   **Google Docs Integration:** Seamlessly upload the updated resume to Google Docs for live editing and sharing.

## How It Works

1.  **Input Collection:** Users upload their `.docx` resume, provide a GitHub link, paste the job description, and can optionally include an "other info" text file.
2.  **Data Extraction:** The backend processes these inputs, extracting text from the resume, summarizing GitHub activity, and utilizing the provided job description and additional text.
3.  **AI Evaluation:** All collected data is fed into a LangChain-powered prompt using Google Gemini. The AI cross-references the candidate's profile with the job requirements.
4.  **Results Display:** The AI's structured analysis (ATS score, missing skills, interview prep) is presented to the user.
5.  **Resume Update (Future):** Based on the analysis, the system will generate an updated resume.
6.  **Google Docs Integration (Future):** The updated resume will be converted to a Google Doc, and a link will be provided for easy access and editing.

## Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

*   Python 3.9+
*   pip (Python package installer)
*   Git

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/Resume-Updater.git
    cd Resume-Updater
    ```
    *(Replace the URL with your actual repository URL)*

2.  **Create and activate a virtual environment:**
    *   On Windows:
        ```bash
        python -m venv .venv
        .\.venv\Scripts\Activate.ps1
        ```
    *   On macOS/Linux:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

3.  **Install Dependencies:**
    Create a `requirements.txt` file in the project root and add the necessary packages. Then, install them using pip:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables:**
    Create a file named `.env` in the root of the project directory to store your secret API keys.
    ```
    GOOGLE_API_KEY="your_google_api_key_here"
    GITHUB_TOKEN="your_github_personal_access_token_here"
    ```
    *   **`GOOGLE_API_KEY`**: Get your API key from Google AI Studio.
    *   **`GITHUB_TOKEN`**: Generate a personal access token from your GitHub account settings. A classic token with `public_repo` scope is sufficient.

### Running the Application

1.  **Start the Flask server:**
    With your virtual environment activated, run the following command:
    ```bash
    python app.py
    ```

2.  **Use the application:**
    Open your web browser and navigate to `http://127.0.0.1:5000`. Fill out the form and click "Submit" to see the AI-powered analysis.

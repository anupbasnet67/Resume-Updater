#compare resume, Github and job description
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from config import GOOGLE_API_KEY

def analyze_candidate_fit(resume_text, job_description_text, github_summary, other_info_text):
    """
    Uses LangChain and an LLM to analyze the candidate's materials against a job description.
    """
    if not GOOGLE_API_KEY:
        return "Error: GOOGLE_API_KEY not found. Please set it in your .env file."

    # Define the prompt template
    prompt_template = """
    You are an expert technical recruiter and career coach reviewing a candidate's profile for a job.
    Your task is to provide a detailed analysis based on the information provided.

    **Job Description:**
    {job_description}

    **Candidate's Resume:**
    {resume}

    **Candidate's GitHub Project Summary:**
    {github}

    **Additional Information from Candidate:**
    {other_info}

    ---

    Based on all the information above, please provide the following:

    1.  **ATS Score:** An estimated Applicant Tracking System (ATS) compatibility score from 0 to 100, representing how well the resume and skills align with the job description's keywords and requirements.
    2.  **Missing Skills:** A bulleted list of key skills or technologies mentioned in the job description that are missing or not clearly demonstrated in the candidate's profile.
    3.  **Interview Prep Guide:** A brief, actionable guide for the candidate to prepare for an interview. This should include:
        -   A list of 3-5 likely technical questions based on the company's tech stack and the job role.
        -   A suggestion for one project from their GitHub/resume they should be prepared to discuss in depth.
    """

    # Create a ChatPromptTemplate instance
    prompt = ChatPromptTemplate.from_template(prompt_template)

    # Initialize the language model
    model = ChatGoogleGenerativeAI(google_api_key=GOOGLE_API_KEY, model="gemini-3.5-flash")

    # Create the processing chain
    chain = prompt | model

    # Invoke the chain with the collected data
    response = chain.invoke({
        "job_description": job_description_text,
        "resume": resume_text,
        "github": github_summary,
        "other_info": other_info_text or "No additional information provided." # Handle case where it's empty
    })

    return response.content
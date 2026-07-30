#compare resume, Github and job description
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from config import GOOGLE_API_KEY
from pydantic import BaseModel, Field
from typing import List

# Define the Pydantic model for structured output
class CandidateAnalysis(BaseModel):
    """A structured analysis of a candidate's profile against a job description."""
    ats_score: str = Field(description="An estimated ATS compatibility score from 0 to 100.")
    missing_skills: List[str] = Field(description="A list of key skills from the job description that are missing from the candidate's profile.")
    interview_prep: str = Field(description="A brief, actionable interview prep guide with likely technical questions and a project to discuss.")

def analyze_candidate_fit(resume_text, job_description_text, github_summary, other_info_text) -> CandidateAnalysis | None:
    """
    Uses LangChain and an LLM to analyze the candidate's materials against a job description,
    returning a structured Pydantic object.
    """
    if not GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY not found. Please set it in your .env file.")
        return None

    # Define the prompt template. The instructions for the output format are now
    # handled by the structured output mechanism, so the prompt can be simpler.
    prompt_template = """
    You are an expert technical recruiter and career coach. Your task is to provide a detailed analysis of the candidate's profile against the job description.

    **Job Description:**
    {job_description}

    **Candidate's Resume:**
    {resume}

    **Candidate's GitHub Project Summary:**
    {github}

    **Additional Information from Candidate:**
    {other_info}

    ---

    Analyze the candidate's materials and provide:
    1. An estimated ATS compatibility score (0-100).
    2. A list of key skills from the job description missing in the candidate's profile.
    3. A brief interview prep guide, including 3-5 likely technical questions and a project to highlight.
    """

    # Create a ChatPromptTemplate instance
    prompt = ChatPromptTemplate.from_template(prompt_template)

    # Initialize the language model and bind it to the Pydantic structure
    model = ChatGoogleGenerativeAI(google_api_key=GOOGLE_API_KEY, model="gemini-3.6-flash")
    structured_llm = model.with_structured_output(CandidateAnalysis)

    # Create the processing chain
    chain = prompt | structured_llm

    try:
        # Invoke the chain with the collected data
        response = chain.invoke({
            "job_description": job_description_text,
            "resume": resume_text,
            "github": github_summary,
            "other_info": other_info_text or "No additional information provided." # Handle case where it's empty
        })
        return response
    except Exception as e:
        print(f"An error occurred during AI analysis: {e}")
        return None
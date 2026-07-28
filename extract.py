from firecrawl import Firecrawl
import docx # Import the python-docx library
import os

def process_resume(file_path):
    """
    Opens a .docx resume and extracts text using python-docx.
    """
    try:
        # Check if the file exists before processing
        if not os.path.exists(file_path):
            print(f"Error: File not found at {file_path}")
            return None
        
        # Open the .docx file with python-docx
        doc = docx.Document(file_path)
        
        print(f"Successfully opened '{os.path.basename(file_path)}'")
        
        # Extract text from all paragraphs in the document
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        
        return text
        
    except Exception as e:
        print(f"An error occurred while processing the .docx file: {e}")
        return None

from dotenv import load_dotenv #read key-value pairs from .env file
import os

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
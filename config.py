from dotenv import load_dotenv #read key-value pairs from .env file
import os

load_dotenv()

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
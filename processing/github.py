import requests
from config import GITHUB_TOKEN
from urllib.parse import urlparse

def _get_username_from_url(url):
    """Extracts username from a GitHub profile URL."""
    try:
        path = urlparse(url).path
        # Path will be like '/username' or '/username/'
        username = path.strip('/')
        return username
    except Exception:
        return None

def process_github_profile(github_url):
    """
    Analyzes a user's GitHub profile and summarizes their technical experience.
    """
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN not found. Please set it in your .env file.")
        return "Error: GitHub token not configured."

    username = _get_username_from_url(github_url)
    if not username:
        return "Error: Could not extract a valid username from the GitHub URL."

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    
    repos_url = f"https://api.github.com/users/{username}/repos?sort=pushed&per_page=10"
    
    try:
        response = requests.get(repos_url, headers=headers, timeout=10)
        response.raise_for_status()
        repos = response.json()

        if not repos:
            return "No public repositories found for this user."

        profile_summary = "GitHub Profile Summary:\n\n"

        for repo in repos:
            if repo.get("fork"):
                continue # Skip forked repositories

            repo_name = repo.get('name', 'N/A')
            description = repo.get('description', 'No description provided.')
            topics = repo.get('topics', [])
            
            # Fetch languages for the repository
            languages_response = requests.get(repo['languages_url'], headers=headers, timeout=5)
            languages = languages_response.json() if languages_response.status_code == 200 else {}
            
            profile_summary += f"### Project: {repo_name}\n"
            profile_summary += f"- **Description**: {description}\n"
            if languages:
                profile_summary += f"- **Technologies Used**: {', '.join(languages.keys())}\n"
            if topics:
                profile_summary += f"- **Topics**: {', '.join(topics)}\n"
            profile_summary += "\n"

        return profile_summary
    except requests.exceptions.RequestException as e:
        print(f"Error fetching GitHub data for {username}: {e}")
        return f"Error: Could not fetch data from GitHub. Status code: {e.response.status_code if e.response else 'N/A'}"
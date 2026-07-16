from ..config import API_URL

def get_repositories_url(owner: str) -> str:
    return f"{API_URL}/orgs/{owner}/repos?per_page=5&sort=updated"

def get_issues_url(owner: str, repo: str) -> str:
    return f"{API_URL}/repos/{owner}/{repo}/issues?state=all&per_page=100"

def get_commits_url(owner: str, repo: str) -> str:
    return f"{API_URL}/repos/{owner}/{repo}/commits"
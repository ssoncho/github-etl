import requests
from config import API_URL

def send_get_request(url: str) -> list[dict]:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

def get_repositories_url(owner: str) -> str:
    return f"{API_URL}/orgs/{owner}/repos"


def get_repositories(owner: str) -> list[dict]:
    url = get_repositories_url(owner)

    response = send_get_request(url)
    return response


def extract(owner: str) -> list[dict]:
    return get_repositories(owner)
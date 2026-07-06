import requests
from config import API_URL
from sqlalchemy import select
from db import engine
from models import languages

def get_language_map() -> dict[str, int]:
    with engine.begin() as connection:
        query = select(languages.c.id, languages.c.name)
        result = connection.execute(query)
        return {row.name: row.id for row in result}

def send_get_request(url: str) -> list[dict]:
    session = requests.Session()
    session.trust_env = False
    response = session.get(url, timeout=10)
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
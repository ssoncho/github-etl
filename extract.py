import json
import requests
from datetime import datetime
from pathlib import Path
from config import API_URL
from sqlalchemy import select
from db import engine
from models import languages

RAW_DIR = Path(__file__).parent / "raw"


def save_raw_json(data: list[dict], owner: str) -> None:
    """Сохраняет сырой JSON-ответ от GitHub API."""
    RAW_DIR.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{owner}_repos_{timestamp}.json"
    filepath = RAW_DIR / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


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
    repositories = get_repositories(owner)
    save_raw_json(repositories, owner)
    return repositories
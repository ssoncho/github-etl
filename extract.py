import json
from datetime import datetime, timezone
from pathlib import Path

import requests
from sqlalchemy import select

from config import API_URL, GITHUB_TOKEN
from db import engine
from models import etl_state, languages, owners

RAW_DIR = Path(__file__).parent / "raw"


def save_raw_json(data: list[dict], owner: str, data_type: str = "repos") -> None:
    """Сохраняет сырой JSON-ответ от GitHub API."""
    RAW_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{owner}_{data_type}_{timestamp}.json"
    filepath = RAW_DIR / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_language_map() -> dict[str, int]:
    with engine.begin() as connection:
        query = select(languages.c.id, languages.c.name)
        result = connection.execute(query)
        return {row.name: row.id for row in result}


def get_last_loaded_at(entity_name: str, owner: str) -> datetime | None:
    with engine.begin() as connection:
        owner_id = connection.execute(select(owners.c.id).where(owners.c.name == owner)) \
                    .scalar_one_or_none()
        if owner_id is None:
            return None
        query = select(etl_state.c.last_loaded_at) \
            .where(etl_state.c.entity == entity_name, etl_state.c.owner_id == owner_id)
        return connection.execute(query).scalar_one_or_none()


def format_github_since_param(timestamp: datetime) -> str:
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    return (
        timestamp.astimezone(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def filter_by_updated_at(items: list[dict], last_loaded_at: datetime | None) -> list[dict]:
    if last_loaded_at is None:
        return items

    if last_loaded_at.tzinfo is None:
        last_loaded_at = last_loaded_at.replace(tzinfo=timezone.utc)

    filtered_items = []
    for item in items:
        updated_at = item.get("updated_at")
        if not updated_at:
            filtered_items.append(item)
            continue

        try:
            updated_at_dt = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
        except ValueError:
            filtered_items.append(item)
            continue

        if updated_at_dt >= last_loaded_at:
            filtered_items.append(item)

    return filtered_items


def send_get_request(url: str, params: dict | None = None) -> list[dict]:
    session = requests.Session()
    session.trust_env = False
    session.headers.update({"Authorization": f"Bearer {GITHUB_TOKEN}"})
    response = session.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def get_repositories_url(owner: str) -> str:
    return f"{API_URL}/orgs/{owner}/repos?per_page=5&sort=updated"  # TODO: увеличить число репозиториев

def extract_repositories(owner: str) -> list[dict]:
    last_loaded_at = get_last_loaded_at("repositories", owner)
    url = get_repositories_url(owner)
    repositories = send_get_request(url)
    repositories = filter_by_updated_at(repositories, last_loaded_at)
    # save_raw_json(repositories, owner)
    return repositories


def get_issues_url(owner: str, repo: str) -> str:
    return f"{API_URL}/repos/{owner}/{repo}/issues?state=all&per_page=100"


def extract_issues(owner: str, repo: str) -> list[dict]:
    last_loaded_at = get_last_loaded_at("issues", owner)
    url = get_issues_url(owner, repo)
    params = None
    if last_loaded_at is not None:
        params = {"since": format_github_since_param(last_loaded_at)}

    issues = send_get_request(url, params=params)
    # save_raw_json(issues, owner, f"issues_{repo}")
    return issues


def get_commits_url(owner: str, repo: str) -> str:
    return f"{API_URL}/repos/{owner}/{repo}/commits"


def extract_commits(owner: str, repo: str) -> list[dict]:
    last_loaded_at = get_last_loaded_at("commits", owner)
    url = get_commits_url(owner, repo)
    params = None
    if last_loaded_at is not None:
        params = {"since": format_github_since_param(last_loaded_at)}

    commits = send_get_request(url, params=params)
    # save_raw_json(commits, owner, f"commits_{repo}")
    return commits

from datetime import datetime
from ..database.queries import get_last_loaded_at
from ..utils.dates import get_timestamp_with_zone
from .client import send_get_request
from .filters import filter_by_updated_at
from .urls import get_repositories_url, get_issues_url, get_commits_url

def build_since_params(
    last_loaded_at: datetime | None,
    is_new_repo: bool,
) -> dict | None:
    if last_loaded_at is None or is_new_repo:
        return None

    return {
        "since": get_timestamp_with_zone(last_loaded_at)
    }

def extract_marked_entity(
    entity: str,
    owner: str,
    url: str,
    is_new_repo: bool,
) -> list[dict]:
    last_loaded_at = get_last_loaded_at(entity, owner)

    params = None
    if last_loaded_at is not None and not is_new_repo:
        params = {"since": get_timestamp_with_zone(last_loaded_at)}

    return send_get_request(url, params)

def extract_repositories(owner: str) -> list[dict]:
    last_loaded_at = get_last_loaded_at("repositories", owner)
    url = get_repositories_url(owner)
    repositories = send_get_request(url)
    repositories = filter_by_updated_at(repositories, last_loaded_at)
    return repositories

def extract_issues(owner: str, repo: str, is_new_repo: bool) -> list[dict]:
    return extract_marked_entity(
        entity="issues",
        owner=owner,
        url=get_issues_url(owner, repo),
        is_new_repo=is_new_repo,
    )


def extract_commits(owner: str, repo: str, is_new_repo: bool) -> list[dict]:
    return extract_marked_entity(
        entity="commits",
        owner=owner,
        url=get_commits_url(owner, repo),
        is_new_repo=is_new_repo,
    )

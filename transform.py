from datetime import datetime, timezone

def transform_repository(repository: dict) -> dict:
    return {
        "id": repository["id"],
        "name": repository["name"],
        "language": repository["language"],
        "stars": repository["stargazers_count"],
        "forks": repository["forks_count"],
        "created_at": datetime.fromisoformat(
            repository["created_at"]
            .replace("Z", "+00:00")
        ).astimezone(timezone.utc),
        "updated_at": datetime.fromisoformat(
            repository["updated_at"].replace("Z", "+00:00")
        ).astimezone(timezone.utc),
    }


def transform_repositories(repositories: list[dict]) -> list[dict]:
    return [transform_repository(repository) for repository in repositories]
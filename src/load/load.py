from pandas import DataFrame

from .loaders import load_table, _load_entity, mark_entity_loaded
from ..database.models import commits, issues, languages, owners, repositories


def load_owners(df: DataFrame) -> None:
    _load_entity(
        owners,
        df,
        conflict_columns=["name"],
    )


def load_languages(df: DataFrame) -> None:
    _load_entity(
        languages,
        df,
        conflict_columns=["name"],
    )


def load_repositories(df: DataFrame, org_name: str) -> None:
    _load_entity(
        repositories,
        df,
        conflict_columns=["id"],
        entity_name="repositories",
        org_name=org_name,
    )


def load_issues(df: DataFrame, org_name: str) -> None:
    _load_entity(
        issues,
        df,
        conflict_columns=["id"],
        entity_name="issues",
        org_name=org_name,
    )


def load_commits(df: DataFrame, org_name: str) -> None:
    _load_entity(
        commits,
        df,
        conflict_columns=["sha", "repository_id"],
        entity_name="commits",
        org_name=org_name,
    )
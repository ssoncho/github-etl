from datetime import timezone

import pandas as pd

def transform_owners(repositories: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(repositories)

    owners_df = (
        pd.json_normalize(df["owner"])[["id", "login"]]
        .drop_duplicates(subset=["id"])
        .rename(
            columns={
                "login": "name",
            }
        )
    )

    return owners_df


def transform_languages(repositories: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(repositories)

    languages_df = (
        pd.DataFrame(
            {
                "name": df["language"].fillna("Unknown").unique()
            }
        )
        .sort_values("name")
        .reset_index(drop=True)
    )

    return languages_df


def transform_repositories(
    repositories: list[dict],
    language_map: dict[str, int],
) -> pd.DataFrame:
    df = pd.DataFrame(repositories)

    df = df[
        [
            "id",
            "name",
            "language",
            "stargazers_count",
            "forks_count",
            "created_at",
            "updated_at",
            "owner",
        ]
    ]

    df = df.rename(
        columns={
            "stargazers_count": "stars",
            "forks_count": "forks",
        }
    )

    df["language"] = df["language"].fillna("Unknown")

    df["created_at"] = pd.to_datetime(df["created_at"], utc=True)
    df["updated_at"] = pd.to_datetime(df["updated_at"], utc=True)
    now = pd.Timestamp.now(timezone.utc)

    df["last_activity_days"] = (
        now - df["updated_at"].fillna(df["created_at"])
    ).dt.days

    df["popularity"] = pd.cut(
        df["stars"],
        bins=[-1, 99, 999, float("inf")],
        labels=["Low", "Medium", "High"],
        ordered=True
    )

    df["owner_id"] = df["owner"].apply(
        lambda owner: owner["id"]
    )

    df["language_id"] = df["language"].map(language_map)
    df["updated_at"] = (
        df["updated_at"]
        .astype(object)
        .where(pd.notna(df["updated_at"]), None)
    )

    return df.drop(columns=["owner", "language"])


def transform_issues(issues: list[dict], repository_id: int) -> pd.DataFrame:
    final_columns = [
                "id",
                "repository_id",
                "author_id",
                "state",
                "created_at",
                "updated_at",
                "closed_at",
            ]
    if not issues:
        return pd.DataFrame(
            columns=final_columns
        )

    df = pd.DataFrame(issues)

    # Фильтруем pull requests (GitHub API возвращает их вместе с issues)
    if "pull_request" in df.columns:
        df = df[df["pull_request"].isna()]

    if df.empty:
        return pd.DataFrame(
            columns=final_columns
        )

    df = df[
        [
            "id",
            "state",
            "created_at",
            "updated_at",
            "closed_at",
            "user",
        ]
    ]

    df["author_id"] = df["user"].apply(lambda user: user["id"])
    df["repository_id"] = repository_id

    df["created_at"] = pd.to_datetime(df["created_at"], utc=True)
    df["updated_at"] = pd.to_datetime(df["updated_at"], utc=True)
    df["closed_at"] = (
        pd.to_datetime(df["closed_at"], utc=True)
        .astype(object)
        .where(pd.notna(df["closed_at"]), None)
    )

    return df.drop(columns=["user"])


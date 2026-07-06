from datetime import timezone

import pandas as pd


def get_popularity(stars: int) -> str:
    if stars >= 1000:
        return "High"
    if stars >= 100:
        return "Medium"
    return "Low"


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
        now - df["updated_at"]
    ).dt.days

    df["popularity"] = (
        df["stars"]
        .apply(get_popularity)
        .astype("category")
    )

    df["owner_id"] = df["owner"].apply(
        lambda owner: owner["id"]
    )

    df["language_id"] = df["language"].map(language_map)

    return df.drop(columns=["owner", "language"])
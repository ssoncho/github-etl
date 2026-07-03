from datetime import datetime, timezone
import pandas as pd

def get_popularity(stars: int) -> str:
    if stars >= 1000:
        return "High"
    if stars >= 100:
        return "Medium"
    return "Low"


def transform_repositories(repositories: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(repositories)
    columns_to_extract = ['id', 'name', 'language', 'stargazers_count', 'forks_count', 'created_at', 'updated_at']
    df = df[columns_to_extract]

    df = df.rename(
        columns={
            "stargazers_count": "stars",
            "forks_count": "forks"
        }
    )
    df["language"] = df["language"].fillna("Unknown")
    df["created_at"] = pd.to_datetime(df["created_at"], utc=True)
    df["updated_at"] = pd.to_datetime(df["updated_at"], utc=True)

    # вычисляемые поля
    now = pd.Timestamp.now(timezone.utc)
    df["last_activity_days"] = (now - df["updated_at"]).dt.days # сколько дней прошло с момента последней активности
    df["popularity"] = df["stars"].apply(get_popularity)
    df["popularity"] = df["popularity"].astype("category")

    return df
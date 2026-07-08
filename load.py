from pandas import DataFrame
from sqlalchemy import Table

from db import engine
from models import commits, issues, languages, owners, repositories


def load_table(table: Table, df: DataFrame) -> None:
    records = df.to_dict(orient="records")

    with engine.begin() as connection:
        connection.execute(table.delete())

        if records:
            connection.execute(table.insert(), records)


def load_owners(df: DataFrame) -> None:
    load_table(owners, df)


def load_languages(df: DataFrame) -> None:
    load_table(languages, df)


def load_repositories(df: DataFrame) -> None:
    load_table(repositories, df)


def load_issues(df: DataFrame) -> None:
    load_table(issues, df)


def load_commits(df: DataFrame) -> None:
    load_table(commits, df)
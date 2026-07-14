from datetime import datetime, timezone

from pandas import DataFrame
from sqlalchemy import Table, Connection
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select

from db import engine
from models import commits, etl_state, issues, languages, owners, repositories
        
def load_table(
    table: Table,
    df: DataFrame,
    conflict_columns: list[str],
    connection: Connection
) -> None:
    if df.empty:
        return

    records = df.to_dict(orient="records")

    statement = insert(table).values(records)

    update_columns = {
        column.name: statement.excluded[column.name]
        for column in table.columns
        if column.name not in conflict_columns
        and not column.primary_key
    }

    if update_columns:
        statement = statement.on_conflict_do_update(
            index_elements=conflict_columns,
            set_=update_columns,
        )
    else:
        statement = statement.on_conflict_do_nothing(
            index_elements=conflict_columns,
        )

    connection.execute(statement)


def mark_entity_loaded(entity_name: str, connection: Connection, org_name: str) -> None:
    loaded_at = datetime.now(timezone.utc)
    owner_id = connection.execute(select(owners.c.id).where(owners.c.name == org_name)) \
    .scalar_one_or_none()
    if owner_id is None:
        return
    statement = insert(etl_state).values(
        entity=entity_name,
        owner_id = owner_id,
        last_loaded_at=loaded_at,
    )
    upsert_statement = statement.on_conflict_do_update(
        index_elements=[etl_state.c.entity, etl_state.c.owner_id],
        set_={"last_loaded_at": loaded_at},
    )

    connection.execute(upsert_statement)


def load_owners(df: DataFrame) -> None:
    with engine.begin() as connection:
        load_table(
            owners,
            df,
            conflict_columns=["name"],
            connection=connection
        )


def load_languages(df: DataFrame) -> None:
    with engine.begin() as connection:
        load_table(
            languages,
            df,
            conflict_columns=["name"],
            connection=connection
        )


def load_repositories(df: DataFrame, org_name: str) -> None:
    with engine.begin() as connection:
        load_table(
            repositories,
            df,
            conflict_columns=["id"],
            connection=connection
        )
        mark_entity_loaded("repositories", connection, org_name)


def load_issues(df: DataFrame, org_name: str) -> None:
    with engine.begin() as connection:
        load_table(
            issues,
            df,
            conflict_columns=["id"],
            connection=connection
        )
        mark_entity_loaded("issues", connection, org_name)


def load_commits(df: DataFrame, org_name: str) -> None:
    with engine.begin() as connection:
        load_table(
            commits,
            df,
            conflict_columns=["sha", "repository_id"],
            connection=connection
        )
        mark_entity_loaded("commits", connection, org_name)
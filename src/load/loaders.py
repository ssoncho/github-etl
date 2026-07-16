from datetime import datetime, timezone

from pandas import DataFrame
from sqlalchemy import Table, Connection
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from ..database.models import etl_state, owners
from ..database.db import engine

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

def _load_entity(
    table: Table,
    df: DataFrame,
    conflict_columns: list[str],
    entity_name: str | None = None,
    org_name: str | None = None,
) -> None:
    with engine.begin() as connection:
        load_table(
            table,
            df,
            conflict_columns=conflict_columns,
            connection=connection,
        )

        if entity_name is not None:
            mark_entity_loaded(entity_name, connection, org_name)
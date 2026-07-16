from datetime import datetime, timezone
from sqlalchemy import select
from ..database.db import engine
from .models import etl_state, languages, owners, repositories

def get_language_map() -> dict[str, int]:
    with engine.begin() as connection:
        query = select(languages.c.id, languages.c.name)
        result = connection.execute(query)
        return {row.name: row.id for row in result}
    
def get_owner_id(owner: str) -> int | None:
    with engine.begin() as connection:
        owner_id = connection.execute(select(owners.c.id).where(owners.c.name == owner)) \
                    .scalar_one_or_none()
    return owner_id

def get_repository_ids(owner_id: int) -> set[int]:
    with engine.begin() as connection:
        result = connection.execute(
            select(repositories.c.id)
            .where(repositories.c.owner_id == owner_id)
        )
        return {row.id for row in result}


def get_last_loaded_at(entity_name: str, owner: str) -> datetime | None:
    with engine.begin() as connection:
        owner_id = connection.execute(select(owners.c.id).where(owners.c.name == owner)) \
                    .scalar_one_or_none()
        if owner_id is None:
            return None
        query = select(etl_state.c.last_loaded_at) \
            .where(etl_state.c.entity == entity_name, etl_state.c.owner_id == owner_id)
        return connection.execute(query).scalar_one_or_none()
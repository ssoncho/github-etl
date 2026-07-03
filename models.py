from sqlalchemy import (
    BigInteger,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    Column,
)

metadata = MetaData()

repositories = Table(
    "repositories",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("name", String(255), nullable=False),
    Column("language", String(100)),
    Column("stars", Integer, nullable=False),
    Column("forks", Integer, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
    Column("last_activity_days", Integer, nullable=False),
    Column("popularity", String(50), nullable=False)
)
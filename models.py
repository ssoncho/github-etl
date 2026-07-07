from sqlalchemy import (
    BigInteger,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    Column,
    ForeignKey,
)

metadata = MetaData()

repositories = Table(
    "repositories",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("name", String(255), nullable=False),
    Column("owner_id", Integer, ForeignKey("owners.id")),
    Column("language_id", Integer, ForeignKey("languages.id")),
    Column("stars", Integer, nullable=False),
    Column("forks", Integer, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
    Column("last_activity_days", Integer, nullable=False),
    Column("popularity", String(50), nullable=False),
)

owners = Table(
    "owners",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("name", String(255), nullable=False)
)

languages = Table(
    "languages",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False)
)

issues = Table(
    "issues",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("repository_id", BigInteger, ForeignKey("repositories.id"), nullable=False),
    Column("author_id", BigInteger, nullable=False),
    Column("state", String(50), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
    Column("closed_at", DateTime(timezone=True), nullable=True),
)
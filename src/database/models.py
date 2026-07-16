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
    Column("popularity", String(50), nullable=False),
)

owners = Table(
    "owners",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("name", String(255), nullable=False, unique=True)
)

languages = Table(
    "languages",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False, unique=True)
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

commits = Table(
    "commits",
    metadata,
    Column("sha", String(64), primary_key=True),
    Column("repository_id", BigInteger, ForeignKey("repositories.id"), primary_key=True),
    Column("committed_at", DateTime(timezone=True), nullable=False),
)

etl_state =  Table(
    "etl_state",
    metadata,
    Column("entity", String(100), primary_key=True),
    Column("owner_id", BigInteger, primary_key=True),
    Column("last_loaded_at", DateTime(timezone=True), nullable=False)
)
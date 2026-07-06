from sqlalchemy import create_engine
from models import metadata

from config import DATABASE_URL

engine = create_engine(DATABASE_URL)

def recreate_database() -> None:
    metadata.drop_all(engine)
    metadata.create_all(engine)
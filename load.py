from db import engine
from models import repositories

def load_repositories(repositories_data: list[dict]) -> None:
    with engine.begin() as connection:
        connection.execute(repositories.delete())
        connection.execute(repositories.insert(), repositories_data)
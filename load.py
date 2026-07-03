from db import engine
from models import repositories
from pandas import DataFrame 

def load_repositories(repositories_data: DataFrame) -> None:
    records = repositories_data.to_dict(orient="records")
    with engine.begin() as connection:
        connection.execute(repositories.delete())
        connection.execute(repositories.insert(), records)
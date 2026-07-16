from requests import Session
from ..config import GITHUB_TOKEN

session = Session()
session.trust_env = False
session.headers.update(
    {"Authorization": f"Bearer {GITHUB_TOKEN}"}
)

def send_get_request(url: str, params: dict | None = None) -> list[dict]:
    session = Session()
    session.trust_env = False
    session.headers.update({"Authorization": f"Bearer {GITHUB_TOKEN}"})
    response = session.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()
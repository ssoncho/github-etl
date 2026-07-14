import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
API_URL=os.environ["API_URL"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
ORGANIZATIONS = [
    org.strip()
    for org in os.getenv("ORGANIZATIONS", "").split(",")
    if org.strip()
]
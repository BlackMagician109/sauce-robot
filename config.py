import os

from dotenv import load_dotenv

load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")

REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")

REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")

REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")

REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

SAUCENAO_API_KEY = os.getenv("SAUCENAO_API_KEY")

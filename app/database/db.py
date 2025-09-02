from beanie import init_beanie
from pymongo import AsyncMongoClient
import os
from app.models.user import User
from app.core.constants import error_messages
from dotenv import load_dotenv

mongo_client = None

async def init_db():
    global mongo_client
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        raise ValueError(error_messages["database_url"])

    mongo_client = AsyncMongoClient(db_url)

    await init_beanie(
        database=mongo_client.get_default_database(),
        document_models=[User]
    )
from beanie import init_beanie
from pymongo import AsyncMongoClient
import os
from models.user import User
from ..utils import constants

mongo_client = None

async def init_db():
    global mongo_client
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        raise ValueError(constants.error_messages["database_url"])

    mongo_client = AsyncMongoClient(db_url)

    await init_beanie(
        database=mongo_client.get_default_database(),
        document_models=[User]
    )
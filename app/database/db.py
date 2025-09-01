from beanie import init_beanie
from pymongo import AsyncMongoClient
import os
from models.user import User

async def init_db():
    db_url = os.getenv("MONGO_URI")
    client = AsyncMongoClient(db_url)

    await init_beanie(
        database=client.get_default_database(),
        document_models=[User]
    )
    print("Database connection initialized...")
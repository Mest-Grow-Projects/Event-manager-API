from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.db import init_db
from utils.constants import messages
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    logger.info(messages["db_connection"])

    try:
        yield
    finally:
        logger.info(messages["shutdown"])

app = FastAPI(
    title=messages["app_title"],
    description=messages["app_description"],
    version=messages["app_version"],
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return messages["welcome"]

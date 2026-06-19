import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def connect_to_mongo():
    logger.info("Connecting to MongoDB...")
    db.client = AsyncIOMotorClient(
        settings.MONGO_URI,
        maxPoolSize=10,
        minPoolSize=1
    )
    logger.info("Successfully connected to MongoDB!")

async def close_mongo_connection():
    logger.info("Closing MongoDB connection...")
    if db.client:
        db.client.close()
        logger.info("Successfully closed MongoDB connection!")

def get_database():
    return db.client["task_verification_db"]

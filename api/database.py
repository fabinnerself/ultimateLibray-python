import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import logging
from .config import settings

logger = logging.getLogger(__name__)

class Database:
    client: Optional[AsyncIOMotorClient] = None
    database = None

db = Database()

async def get_database() -> AsyncIOMotorClient:
    return db.database

async def connect_to_mongo():
    """Create database connection"""
    try:
        mongodb_url = settings.mongodb_connect_uri
        if not mongodb_url:
            raise ValueError("MONGODB_CONNECT_URI environment variable is not set")
        
        db.client = motor.motor_asyncio.AsyncIOMotorClient(
            mongodb_url,
            maxPoolSize=10,
            minPoolSize=10,
            serverSelectionTimeoutMS=5000,
        )
        
        # Get database name from settings
        database_name = settings.database_name
        db.database = db.client[database_name]
        
        # Test the connection
        await db.client.admin.command('ping')
        logger.info("Connected to MongoDB successfully")
        
    except Exception as e:
        logger.error(f"Could not connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        logger.info("Disconnected from MongoDB")

# Collections
async def get_book_collection():
    database = await get_database()
    return database.books

async def get_user_collection():
    database = await get_database()
    return database.users

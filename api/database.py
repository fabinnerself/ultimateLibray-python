import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
import logging
from .config import settings

logger = logging.getLogger(__name__)

class Database:
    client: Optional[AsyncIOMotorClient] = None
    database: Optional[AsyncIOMotorDatabase] = None

db = Database()

async def get_database() -> AsyncIOMotorDatabase:
    """Get database connection with lazy initialization for Vercel"""
    if db.database is None:
        await connect_to_mongo()
    return db.database

async def connect_to_mongo():
    """Create database connection"""
    if db.client is not None:
        return  # Already connected
        
    try:
        mongodb_url = settings.mongodb_connect_uri
        if not mongodb_url:
            raise ValueError("MONGODB_CONNECT_URI environment variable is not set")
        
        # Optimized settings for serverless environment
        db.client = motor.motor_asyncio.AsyncIOMotorClient(
            mongodb_url,
            maxPoolSize=1,  # Reduced for serverless
            minPoolSize=0,  # Start with 0 connections
            maxIdleTimeMS=30000,  # Close idle connections faster
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
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
        db.client = None
        db.database = None
        logger.info("Disconnected from MongoDB")

# Collections with lazy loading
async def get_book_collection():
    database = await get_database()
    return database.books

async def get_user_collection():
    database = await get_database()
    return database.users

"""
MongoDB connection manager (Motor async driver).

Usage:
    from app.database import db
    await db.users.find_one({"email": email})
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config.settings import settings
import logging

logger = logging.getLogger("fin.database")


class MongoDatabase:
    """Thin wrapper that holds the Motor client/database singletons."""

    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect(self):
        logger.info("Connecting to MongoDB Atlas...")
        self.client = AsyncIOMotorClient(settings.MONGODB_URI)
        self.db = self.client[settings.MONGODB_DB_NAME]
        # Verify connection
        await self.client.admin.command("ping")
        logger.info(f"Connected to MongoDB database: {settings.MONGODB_DB_NAME}")
        await self._create_indexes()

    async def disconnect(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")

    async def _create_indexes(self):
        """Create indexes used across the app. Safe to call repeatedly."""
        await self.db.users.create_index("email", unique=True)
        await self.db.transactions.create_index("user_id")
        await self.db.transactions.create_index([("user_id", 1), ("date", -1)])
        await self.db.goals.create_index("user_id")
        await self.db.reminders.create_index("user_id")
        await self.db.reminders.create_index([("user_id", 1), ("due_date", 1)])
        await self.db.insights.create_index("user_id")
        await self.db.insights.create_index([("user_id", 1), ("created_at", -1)])


mongo = MongoDatabase()


def get_db() -> AsyncIOMotorDatabase:
    """FastAPI dependency-friendly accessor for the active database."""
    return mongo.db

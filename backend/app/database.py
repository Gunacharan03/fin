"""
MongoDB connection manager (Motor async driver).

Usage:
    from app.database import mongo, get_db
    await get_db().users.find_one({"email": email})
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config.settings import settings
import certifi
import logging

logger = logging.getLogger("fin.database")


class MongoDatabase:
    """MongoDB Atlas connection manager"""

    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect(self):
        try:
            logger.info("Connecting to MongoDB Atlas...")

            self.client = AsyncIOMotorClient(
                settings.MONGODB_URI,
                tls=True,
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=30000,
                connectTimeoutMS=30000,
                socketTimeoutMS=30000,
            )

            # Verify connection
            await self.client.admin.command("ping")

            self.db = self.client[settings.MONGODB_DB_NAME]

            logger.info(
                f"Connected successfully to database: {settings.MONGODB_DB_NAME}"
            )

            await self._create_indexes()

        except Exception as e:
            logger.error(f"MongoDB connection failed: {str(e)}")
            raise

    async def disconnect(self):
        try:
            if self.client:
                self.client.close()
                logger.info("MongoDB connection closed.")
        except Exception as e:
            logger.error(f"Error while closing MongoDB connection: {str(e)}")

    async def _create_indexes(self):
        """Create required indexes"""

        try:
            # Users
            await self.db.users.create_index(
                "email",
                unique=True
            )

            # Transactions
            await self.db.transactions.create_index(
                "user_id"
            )

            await self.db.transactions.create_index(
                [
                    ("user_id", 1),
                    ("date", -1)
                ]
            )

            # Goals
            await self.db.goals.create_index(
                "user_id"
            )

            # Reminders
            await self.db.reminders.create_index(
                "user_id"
            )

            await self.db.reminders.create_index(
                [
                    ("user_id", 1),
                    ("due_date", 1)
                ]
            )

            # Insights
            await self.db.insights.create_index(
                "user_id"
            )

            await self.db.insights.create_index(
                [
                    ("user_id", 1),
                    ("created_at", -1)
                ]
            )

            logger.info("Indexes created successfully")

        except Exception as e:
            logger.error(f"Index creation failed: {str(e)}")
            raise


mongo = MongoDatabase()


def get_db() -> AsyncIOMotorDatabase:
    """
    FastAPI dependency helper

    Usage:
        db = get_db()
    """
    return mongo.db
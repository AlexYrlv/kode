from config_fastapi import Config
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import date



class MongoDB:
    config = Config(section="mongodb")

    def __init__(self):
        self.client = AsyncIOMotorClient(self.config.uri)
        self.db = self.client[self.config.database]
        self.collection = self.db.schedules

    async def insert_schedule(self, doc: dict) -> str:
        result = await self.collection.insert_one(doc)
        return str(result.inserted_id)

    async def get_schedules_by_user(self, user_id: int) -> list[dict]:
        cursor = self.collection.find({"user_id": user_id})
        return [doc async for doc in cursor]

    async def get_schedule(self, user_id: int, schedule_id: str) -> dict | None:
        doc = await self.collection.find_one({"_id": ObjectId(schedule_id), "user_id": user_id})
        return doc

    async def get_active_schedules(self, user_id: int, today: date) -> list[dict]:
        cursor = self.collection.find({
            "user_id": user_id,
            "start_date": {"$lte": today.isoformat()},
            "$or": [
                {"end_date": None},
                {"end_date": {"$gte": today.isoformat()}}
            ]
        })
        return [doc async for doc in cursor]

from fastapi import HTTPException
from datetime import datetime, timedelta

from .constants import NEXT_PERIOD_HOURS, START_TIME, END_TIME
from .structures import Schedule, NextTaking
from .mongodb import MongoDB
import os


class ScheduleControl:
    def __init__(self):
        self.db = MongoDB()

    async def create_schedule(self, raw_data: dict) -> Schedule:
        schedule = Schedule.create(raw_data)
        inserted_id = await self.db.insert_schedule(schedule.to_mongo())
        schedule.schedule_id = inserted_id
        return schedule

    async def list_schedules(self, user_id: int) -> list[Schedule]:
        docs = await self.db.get_schedules_by_user(user_id)
        schedules = [Schedule.from_mongo(doc) for doc in docs]
        return schedules

    async def get_schedule(self, user_id: int, schedule_id: str) -> Schedule:
        doc = await self.db.get_schedule(user_id, schedule_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Schedule not found")
        schedule = Schedule.from_mongo(doc)
        return schedule

    async def get_next_takings(self, user_id: int) -> list[NextTaking]:
        now = datetime.now()

        if not START_TIME <= now.time() <= END_TIME:
            return []

        end_time = now + timedelta(hours=NEXT_PERIOD_HOURS)
        docs = await self.db.get_active_schedules(user_id, now.date())
        result = []

        for doc in docs:
            schedule = Schedule.from_mongo(doc)
            takings_today = schedule.get_takings_for_day(now.date())

            for time_str in takings_today:
                t = datetime.strptime(time_str, "%H:%M").replace(
                    year=now.year, month=now.month, day=now.day
                )
                if now <= t <= end_time:
                    result.append(NextTaking(
                        schedule_id=schedule.schedule_id,
                        medicine_name=schedule.medicine_name,
                        taking_time=time_str
                    ))

        return result

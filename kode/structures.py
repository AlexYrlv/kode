from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from .constants import START_TIME, END_TIME, ROUNDING_MINUTES



@dataclass
class Schedule:
    user_id: int
    medicine_name: str
    periodicity: float
    start_date: date
    end_date: date | None = None
    duration: int | None = None
    schedule_id: str | None = None

    @classmethod
    def create(cls, data: dict) -> Schedule:
        start_date = date.today()
        duration = data.get("duration")
        end_date = None
        if duration is not None:
            end_date = start_date + timedelta(days=duration - 1)
        return cls(
            user_id=data["user_id"],
            medicine_name=data["medicine_name"],
            periodicity=data["periodicity"],
            start_date=start_date,
            end_date=end_date,
            duration=duration
        )

    @classmethod
    def from_mongo(cls, doc: dict) -> Schedule:
        start_date = date.fromisoformat(doc["start_date"])
        end_date = date.fromisoformat(doc["end_date"]) if doc.get("end_date") else None
        return cls(
            user_id=doc["user_id"],
            medicine_name=doc["medicine_name"],
            periodicity=doc["periodicity"],
            start_date=start_date,
            end_date=end_date,
            duration=None,
            schedule_id=str(doc["_id"]) if "_id" in doc else None
        )

    def to_mongo(self) -> dict:
        return {
            "user_id": self.user_id,
            "medicine_name": self.medicine_name,
            "periodicity": self.periodicity,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if self.end_date else None,
        }

    def to_dict(self) -> dict:
        return {
            "schedule_id": self.schedule_id,
            "user_id": self.user_id,
            "medicine_name": self.medicine_name,
            "periodicity": self.periodicity,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if self.end_date else None
        }

    def get_takings_for_day(self, day: date) -> list[str]:
        start_dt = datetime.combine(day, START_TIME)
        end_dt = datetime.combine(day, END_TIME)
        current_dt = start_dt
        result = []

        seen = set()

        while current_dt <= end_dt:
            minutes = ((current_dt.minute + ROUNDING_MINUTES - 1) // ROUNDING_MINUTES) * ROUNDING_MINUTES
            rounded = current_dt.replace(minute=minutes % 60, second=0, microsecond=0)
            if minutes >= 60:
                rounded += timedelta(hours=1)

            time_str = rounded.strftime("%H:%M")

            if rounded <= end_dt and time_str not in seen:
                seen.add(time_str)
                result.append(time_str)

            current_dt += timedelta(minutes=int(self.periodicity * 60))

        return result

@dataclass
class NextTaking:
    schedule_id: str
    medicine_name: str
    taking_time: str

    def to_dict(self):
        return {
            "schedule_id": self.schedule_id,
            "medicine_name": self.medicine_name,
            "taking_time": self.taking_time,
        }

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from .baseclasses import BaseAPI, BaseResource
from .controls import ScheduleControl
from .constants import API_NAME, API_PREFIX


def init_api():
    api = BaseAPI(name=API_NAME, url_prefix=API_PREFIX)
    api.new_routes({
        "/schedule": ScheduleResource,
        "/schedules": SchedulesListResource,
        "/next_takings": NextTakingsResource,
    })
    return api.router


class ScheduleResource(BaseResource):
    def __init__(self):
        self.control = ScheduleControl()

    async def post(self, request: Request) -> JSONResponse:
        if not request.json:
            raise HTTPException(status_code=400, detail="Received empty request data")

        data = await request.json()
        schedule = await self.control.create_schedule(data)
        return JSONResponse(schedule.to_dict(), status_code=201)

    async def get(self, request: Request) -> JSONResponse:
        user_id = int(request.query_params["user_id"])
        schedule_id = request.query_params["schedule_id"]
        schedule = await self.control.get_schedule(user_id, schedule_id)
        return JSONResponse(schedule.to_dict())


class SchedulesListResource(BaseResource):
    def __init__(self):
        self.control = ScheduleControl()

    async def get(self, request: Request) -> JSONResponse:
        user_id = int(request.query_params["user_id"])
        schedules = await self.control.list_schedules(user_id)
        return JSONResponse({"schedules": [schedule.to_dict() for schedule in schedules]})


class NextTakingsResource(BaseResource):
    def __init__(self):
        self.control = ScheduleControl()

    async def get(self, request: Request) -> JSONResponse:
        user_id = int(request.query_params["user_id"])
        result = await self.control.get_next_takings(user_id)
        return JSONResponse([item.to_dict() for item in result])

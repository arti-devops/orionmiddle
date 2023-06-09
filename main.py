from typing import Union
from fastapi import FastAPI, Request, Header
from typing import Optional

from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from services.links import links_ns

from controllers.employee import get_employee_list_page_data
from controllers.employee import get_employee_details_page_data
from controllers.employee import get_dashboard_checkins_data

from controllers.task import get_task_list
from controllers.task import get_task_statistics
from controllers.task import get_employee_task_list
from controllers.task import get_filtered_task_list
from controllers.task import get_single_task_details
from controllers.logbook import get_employee_logbook
from controllers.course import get_employee_course_list
from controllers.evaluation import get_employee_evaluation_list

app = FastAPI()

# add CORS middleware to allow cross-origin requests
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
headers = {"Access-Control-Allow-Origin": "*"}

@app.get("/items")
async def read_items(user_agent: str = Header(None)):
    return {"User-Agent": user_agent}
    # return get_employee_list_page_data("2023-04-01","2023-04-30")

@app.get("/api/v1/e/list")
def read_emp_list():
    pass
    # return get_employee_list_page_data("2023-04-01","2023-04-30")

@app.get("/api/v1/employee/list")
async def get_users(q: Optional[str] = "", perPage: Optional[int] = 10, currentPage: Optional[int] = 1, x_filter: str = Header(None)):
    data = get_employee_list_page_data("2023-01-01","2023-01-31", q, perPage, currentPage, x_filter)
    print({"X-Custom-Header": x_filter})
    return JSONResponse(content=data, headers=headers)

@app.get("/api/v1/task/list/filter")
async def get_filter_task_list(q: Optional[str] = "", ptype: Optional[str] = "",  direction: Optional[str] = "", status: Optional[str] = "", perPage: Optional[int] = 10, currentPage: Optional[int] = 1, x_filter: str = Header(None)):
    data = get_filtered_task_list(q, ptype, direction, status, perPage, currentPage, x_filter)
    return JSONResponse(content=data, headers=headers)

@app.get("/api/v1/task/details/{tid}")
async def get_task_details(tid:str):
    return get_single_task_details(tid)


@app.get("/api/v1/employee/details/{p}")
async def get_employee(p:int):
    return get_employee_details_page_data(str(p), "2023-04-01","2023-04-30")

@app.get("/api/v1/dashboard/checkins/{date_string}") #Todo Add date range
async def get_dashboard_checkins(date_string:str, x_filter: str = Header(None)):
    return get_dashboard_checkins_data(date_string, x_filter)

@app.get("/api/v1/task/list/employee/{p}")
async def get_task_list_by_employee_id(p:str):
    return get_employee_task_list(p)

@app.get("/api/v1/task/stats/")
async def get_all_task_statistics():
    return get_task_statistics()

@app.get("/api/v1/task/list/")
async def get_all_tasks_list():
    return get_task_list()

@app.get("/api/v1/training/list/employee/{p}")
async def get_course_list_by_employee_id(p:str):
    return get_employee_course_list(p)

@app.get("/api/v1/evaluation/list/employee/{p}")
async def get_evaluation_list_by_employee_id(p:str):
    return get_employee_evaluation_list(p)

@app.get("/api/v1/logbook/employee/{p}/{date_string}")
async def get_logbook_by_employee_id(p:str, date_string:str):
    return get_employee_logbook(p, date_string)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
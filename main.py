from typing import Union
from fastapi import FastAPI
from typing import Optional

from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from services.links import links_ns

from controllers.employee import get_employee_list_page_data
from controllers.employee import get_employee_details_page_data
from controllers.employee import get_dashboard_checkins_data

from controllers.task import get_employee_task_list
from controllers.course import get_employee_course_list
from controllers.evaluation import get_employee_evaluation_list

app = FastAPI()

# add CORS middleware to allow cross-origin requests
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
headers = {"Access-Control-Allow-Origin": "*"}

@app.get("/")
def read_root():
    pass
    # return get_employee_list_page_data("2023-04-01","2023-04-30")

@app.get("/api/v1/e/list")
def read_emp_list():
    pass
    # return get_employee_list_page_data("2023-04-01","2023-04-30")

@app.get("/api/v1/employee/list")
async def get_users(q: Optional[str] = "", perPage: Optional[int] = 10, currentPage: Optional[int] = 1):
    data = get_employee_list_page_data("2023-01-01","2023-01-31", q, perPage, currentPage)
    return JSONResponse(content=data, headers=headers)

@app.get("/api/v1/employee/details/{p}")
async def get_employee(p:int):
    return get_employee_details_page_data(str(p), "2023-04-01","2023-04-30")

@app.get("/api/v1/dashboard/checkins/{date_string}") #Todo Add date range
async def get_dashboard_checkins(date_string:str):
    return get_dashboard_checkins_data(date_string)

@app.get("/api/v1/task/list/employee/{p}")
async def get_task_list_by_employee_id(p:str):
    return get_employee_task_list(p)

@app.get("/api/v1/training/list/employee/{p}")
async def get_course_list_by_employee_id(p:str):
    return get_employee_course_list(p)

@app.get("/api/v1/evaluation/list/employee/{p}")
async def get_evaluation_list_by_employee_id(p:str):
    return get_employee_evaluation_list(p)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
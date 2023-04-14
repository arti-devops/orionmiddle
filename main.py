from typing import Union
from fastapi import FastAPI
from typing import Optional

from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from services.links import links_ns

from controllers.employee import get_employee_list_page_data
from controllers.employee import get_employee_details_page_data

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

@app.get("/api/v1/emp/list")
async def get_users(q: Optional[str] = "", perPage: Optional[int] = 10, currentPage: Optional[int] = 1):
    data = get_employee_list_page_data("2023-04-01","2023-04-30", q, perPage, currentPage)
    return JSONResponse(content=data, headers=headers)

@app.get("/api/v1/employee/details/{p}")
async def get_employee(p:int):
    return get_employee_details_page_data(str(p), "2023-04-01","2023-04-30")


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
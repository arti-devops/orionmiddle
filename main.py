from typing import Union
from fastapi import FastAPI

from interfaces.employee import get_employee_list_bio_data
from interfaces.employee import get_employee_list_checkin_data

app = FastAPI()


@app.get("/")
def read_root():
    emp_data = get_employee_list_bio_data()
    return get_employee_list_checkin_data(emp_data, "2023-04-01","2023-04-30")


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
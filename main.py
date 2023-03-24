from typing import Union
from fastapi import FastAPI

from interfaces.employee import get_employee_list_bio_data

app = FastAPI()


@app.get("/")
def read_root():
    return get_employee_list_bio_data()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
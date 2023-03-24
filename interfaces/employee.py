import requests
from services.links import *
from services.processing import get_direction_name

def get_employee_list_bio_data():
    emp_data_list = list()
    positions = requests.get(base_link+links_ns.position.all_active).json()
    for p in positions:
        emp_data = dict()
        emp_data["position_id"] = p["positionId"]
        emp_data["employee_id"] = p["employee"]["employeeId"]
        emp_data["fullname"] = p["employee"]["lastName"] +" "+ p["employee"]["firstName"].strip() 
        emp_data["matricula"] = p["employee"]["matricule"]
        emp_data["rolename"] = p["role"]["name"]
        emp_data["direction"] = get_direction_name(p)
        emp_data_list.append(emp_data)
    return emp_data_list
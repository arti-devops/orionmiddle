import math

from interfaces.employee import get_employee_list_bio_data
from interfaces.employee import get_employee_list_checkin_data
from interfaces.employee import get_employee_list_task_data
from interfaces.employee import get_employee_bio_data

def get_employee_list_page_data(s_date:str, e_date:str, q, perPage, currentPage):
    data = None
    if currentPage == 0:
        currentPage = 1
    emp_data = get_employee_list_bio_data()
    check_data = get_employee_list_checkin_data(emp_data, s_date, e_date)[0]
    users = get_employee_list_task_data(check_data)[0]
    queryLower = q.lower()
    filteredUsers = [user for user in users if ((queryLower in user["fullname"].lower() or queryLower in user["matricula"].lower() or queryLower in user["direction"].lower() or queryLower in user["rolename"].lower()))][::-1]
    # Sort the data by name in ascending order
    sortedfilteredUsers = sorted(filteredUsers, key=lambda x: x['fullname'],reverse=False)
    totalPage = math.ceil(len(filteredUsers) / perPage) if perPage else 1
    totalUsers = len(filteredUsers)
    if perPage:
        firstIndex = (currentPage - 1) * perPage
        lastIndex = perPage * currentPage
        sortedfilteredUsers = sortedfilteredUsers[firstIndex:lastIndex]
        data = {"users": sortedfilteredUsers, "totalPage": totalPage, "totalUsers": totalUsers}
    return data

def get_employee_details_page_data(p:str):
    return {"bio":get_employee_bio_data(p)}
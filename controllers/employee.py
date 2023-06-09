import math

from services.date import get_first_and_last_date_of_month

from interfaces.employee import get_employee_list_bio_data
from interfaces.employee import get_employee_list_checkin_data
from interfaces.employee import get_employee_list_task_data
from interfaces.employee import get_employee_bio_data
from interfaces.employee import get_employee_absence_metadata
from interfaces.employee import get_employee_course_metadata
from interfaces.employee import get_employee_evaluation_metadata
from interfaces.employee import get_employee_task_metadata
from interfaces.employee import get_all_employees_ondate_checkins
from interfaces.employee import get_all_employees_late_occurence

from interfaces.filter import get_positionId_by_direction, filter_df_by_col_value

def get_employee_list_page_data(s_date:str, e_date:str, q, perPage, currentPage, filter="HOLLOW"):
    data = None
    if currentPage == 0:
        currentPage = 1
    emp_data = get_employee_list_bio_data()
    
    # Filter data
    emp_data = filter_df_by_col_value(emp_data, "direction", filter)
    
    emp_data = emp_data.to_dict(orient="records")
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

def get_employee_details_page_data(p:str, dr_s:str, dr_e:str):
    employee_metadata = {
        "absence":get_employee_absence_metadata(p, dr_s, dr_e),
        "evaluation":get_employee_evaluation_metadata(p),
        "task":get_employee_task_metadata(p),
        "training":get_employee_course_metadata(p)
    }
    return {
        "bio":get_employee_bio_data(p),
        "metadata": employee_metadata
    }

def get_dashboard_checkins_data(date_string, filter): 
    fdate, ldate = get_first_and_last_date_of_month(date_string)
    return {
        "checkins": {
            "log_date": date_string,
            "checkins": get_all_employees_ondate_checkins(date_string, date_string, filter),
            },
        "late": {
            "late_date": ldate,
            "late_occurence": get_all_employees_late_occurence(fdate, ldate, filter)
        }
    }
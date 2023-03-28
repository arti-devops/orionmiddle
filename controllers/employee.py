from interfaces.employee import get_employee_list_bio_data
from interfaces.employee import get_employee_list_checkin_data
from interfaces.employee import get_employee_list_task_data

def get_employee_list_page_data(s_date:str, e_date:str):
    emp_data = get_employee_list_bio_data()
    check_data = get_employee_list_checkin_data(emp_data, s_date, e_date)[0]
    return get_employee_list_task_data(check_data)[0]
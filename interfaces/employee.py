import requests
from services.date import *
from services.links import *
from services.processing import *

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
        emp_data["service"] = get_service_name(p)
        emp_data["direction"] = get_direction_name(p)
        emp_data["email"] = p["employee"]["email"]
        emp_data["contact"] = p["employee"]["contact"]
        emp_data["location"] = p["location"]
        emp_data_list.append(emp_data)
    return emp_data_list

def get_employee_list_checkin_data(emp_list:list, start_date:str, end_date:str):
    log_data_list = []
    for emp in emp_list:
        logd = dict()
        e = Namespace(emp)
        pid = e.position_id
        lc = generate_daterange_link(links_ns.logbook, pid, start_date, end_date)
        la = generate_daterange_link(links_ns.absence, pid, start_date, end_date)
        reqa = requests.get(la)
        reqc = requests.get(lc)
        loga = reqa.json()
        logc = reqc.json()
        #logd["position_id"] = pid
        logd["checkins"] = len(logc)
        logd["no_checkins"] = count_no_log_occurence(len(logc), start_date)
        logd["late_arrivals"] = count_late_occurence([compute_time_diff_in_minutes(c["checkinTime"]) for c in logc])
        logd["absences"] = len(loga)
        logd["abs_justified"] = len([1 for a in loga if a["justified"]=="yes"])
        log_data_list.append(logd)
        emp["logs"] = logd
    return emp_list, log_data_list

def get_employee_list_task_data(emp_list):
    task_data_list = []
    for emp in emp_list:
        taskd = dict()
        e = Namespace(emp)
        pid = e.position_id
        l = generate_position_req_link(links_ns.taskrole, pid)
        d = requests.get(l).json()
        if len(d) == 0:
            task_data = {"nb_task":0,"nb_finished":0,"progress":0}
        else:
            nb = len(d)
            finished = compute_nb_finished_tasks(d)
            progress = compute_progress(finished, nb)
            task_data = {"nb_task":nb, "nb_finished": finished, "progress":progress}
        task_data_list.append(task_data)
        emp["tasks"] = task_data
    return emp_list, task_data_list

def get_employee_bio_data(positionId:str):
    emp_data_list = list()
    positions = [requests.get(base_link+links_ns.position.single+positionId).json()]
    for p in positions:
        emp_data = dict()
        emp_data["position_id"] = p["positionId"]
        emp_data["employee_id"] = p["employee"]["employeeId"]
        emp_data["fullname"] = p["employee"]["lastName"] +" "+ p["employee"]["firstName"].strip() 
        emp_data["matricula"] = p["employee"]["matricule"]
        emp_data["rolename"] = p["role"]["name"]
        emp_data["service"] = get_service_name(p)
        emp_data["direction"] = get_direction_name(p)
        emp_data["email"] = p["employee"]["email"]
        emp_data["contact"] = p["employee"]["contact"]
        emp_data["location"] = p["location"]
        emp_data_list.append(emp_data)
    return emp_data_list[0]
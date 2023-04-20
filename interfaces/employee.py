import requests
import json
from pandas import json_normalize
from itertools import groupby
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

def get_employee_absence_metadata(p:str, s:str, e:str):
    req = requests.get(base_link+links_ns.absence.prange+p+'/'+s+'/'+e).json()
    nb = len(req)
    done = len([1 for x in req if x["justified"]=='yes'])
    return dict({"nb":nb, "done":done})

def get_employee_task_metadata(p:str):
    done = 0
    emp_task = requests.get(base_link+links_ns.taskrole.position+str(p)).json()
    nb = len(emp_task)
    if nb > 0:
        done = computer_finished_tasks(get_taskrole_status_list(emp_task))
    return dict({"nb":nb, "done":done})

def get_employee_evaluation_metadata(p:str):
    done = 0
    eval_data = requests.get(base_link+links_ns.evaluation.position+str(p)).json()
    nb = len(eval_data)
    return dict({"nb":5, "done":nb})

def get_employee_course_metadata(p:str):
    course_data = requests.get(base_link+links_ns.course.position+str(p)).json()
    nb = len(course_data)
    done = len([1 for x in course_data if x["status"] == "FINISHED"])
    return dict({"nb":nb, "done":done})

def get_all_employees_ondate_checkins(dr_s:str, dr_e:str):
    #TODO function is subject to change if daily data contains many records from a single employee
    log_data = requests.get(base_link+links_ns.logbook.range+dr_s+'/'+dr_e).json()
    if len(log_data)>0:
        checkin_data = log_data
        checkin_data = pd.json_normalize(checkin_data)
        checkin_data["isLate"] = checkin_data["checkinTime"].map(time_diff) < 0
        select_cols = ["logbookId","position.positionId","position.employee.employeeId","position.employee.lastName","position.employee.firstName","checkinTime","checkoutTime","isLate"]
        rename_cols = ["logbookId","positionId","employeeId","lastName","firstName","checkIn","checkOut","isLate"]
        df = checkin_data[select_cols]
        df.columns = rename_cols
        meta_data = {
            "late_count" : len([1 for x in df.isLate if x==True]),
            "log_count" : df.shape[0]
        }
        return {
            "metadata":meta_data,
            "checkins":json.loads(df.to_json(orient="records")),
            "debug":log_data
        }
    else: return list()

def get_all_employees_late_occurence(dr_s:str, dr_e:str): 
    #Todo Add date range from selected month name
    #Todo Add number of justified absences to monthLogCount
    log_data = requests.get(base_link+links_ns.logbook.range+dr_s+'/'+dr_e).json()
    if len(log_data)>0:
        df = json_normalize(log_data)
        df["isLate"] = df["checkinTime"].map(time_diff) < 0
        df_sn = df[["logbookId","isLate","position.positionId"]]
        df_sn = df_sn.groupby('position.positionId').agg({'isLate': 'sum', 'logbookId': 'count'}).reset_index()
        cols = ["position.positionId","position.employee.employeeId","position.employee.lastName","position.employee.firstName","isLate_x","logbookId_x"]
        late_occ = df_sn.merge(df, on='position.positionId', how="left")[cols].drop_duplicates()
        cols_new = ["positionId","employeeId","lastName","fisrtName","monthLateCount","monthLogCount"]
        late_occ.columns = cols_new
        late_occ_sorted = late_occ.sort_values(["monthLateCount","monthLogCount"], ascending=[False,True])
        late_occ_sorted = late_occ_sorted.to_json(orient="records")
        return json.loads(late_occ_sorted)
    else: return list()
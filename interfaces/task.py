import requests
import numpy as np
import pandas as pd
from services.links import *
from services.processing import compute_date_progression

def get_task_list_by_employee_id(p:str):
    link_to_emp_tasks = base_link+links_ns.taskrole.position+p
    emp_tasks = requests.get(link_to_emp_tasks).json()

    if len(emp_tasks)>0:
        df = pd.json_normalize(emp_tasks)
        select_cols = ["task.taskId","task.name","task.code","role","task.startDate","task.endDate","task.status"]
        df = df[select_cols]
        rename_cols = ["id","name","code","role","startDate","endDate","status"]
        df.columns = rename_cols
        df.sort_values(["startDate"], ascending=True, inplace=True)
        return df
    else:
        return pd.DataFrame(list())

def get_all_task_statistics() -> pd.DataFrame:
    link_to_all_tasks = base_link+links_ns.task.all
    all_tasks = requests.get(link_to_all_tasks).json()
    if len(all_tasks)>0:
        projects = pd.json_normalize(all_tasks)
        df = projects[["code","status"]].copy()
        # Getting the stats
        grouped = df.groupby("status").count()
        total_count = df.shape[0]
        grouped["percent"] = (grouped/total_count)*100
        grouped['percent'] = grouped['percent'].round(2)
        grouped.rename(columns={"code":"count"}, inplace=True)
        grouped.reset_index(inplace=True)
        # Add total line
        total = pd.DataFrame(index=[4],data={"status":"TOTAL","count":total_count,"percent":100})
        grouped = pd.concat([grouped,total])
        # Custome order
        custom_order = ["TOTAL",'IN_PROGRESS', 'FINISHED', 'SCHEDULED',"FAILED"]
        grouped = grouped.sort_values(by='status', key=lambda x: x.map({status: i for i, status in enumerate(custom_order)}))
        # Return
        return grouped
    
def get_all_tasks() -> pd.DataFrame:
    req = requests.get(base_link+links_ns.task.all).json() # Risk of empty list
    if len(req) > 0:
        task = pd.json_normalize(req)
        task = task[["taskId","code","name","comment","startDate","endDate","status"]].copy()
        task["progression"] = compute_date_progression(task)

        req = requests.get(base_link+links_ns.taskrole.all).json() # Risk of empty list
        projects = pd.json_normalize(req)
        select_cols = ["taskroleId","task.taskId"]
        rename_cols = ["taskroleId","taskId"]
        projects = projects[select_cols].copy()
        projects.columns = rename_cols

        # Groupe data on taskId to get number of people working on a project
        r_count = projects.groupby(by=["taskId"]).count()["taskroleId"].reset_index()
        r_count.rename(columns={"taskroleId":"resources"}, inplace=True)

        df = pd.merge(left=task, right=r_count, how='left')
        df["resources"] = df.resources.fillna(0).astype("int")
        df["startDate"] = df.startDate.astype("str")
        df["endDate"] = df.endDate.astype("str")
        return df
    else: return pd.DataFrame(list())

def get_task_details(id) -> dict:
    
    data = dict()
    data_task = dict()
    data_resources = dict()

    # Get task bio
    req = requests.get(base_link+links_ns.task.single+str(id)).json() # Risk of empty list or 404
    bio = pd.json_normalize(req)

    req = requests.get(base_link+links_ns.task.project+str(id))
    if req.status_code == 200 and len(req.json())>0:
        task = pd.json_normalize(req.json())
        data_task = task
        nb_task = task.shape[0] # First value
        # For each task compute number of employees involved
        nb_emp = list([])
        role_tmp = pd.DataFrame()
        for taskId in task.taskId:
            req = requests.get(base_link+links_ns.taskrole.task+str(taskId)).json() # Risk of empty list
            if len(req)>0:
                role = pd.json_normalize(req)
                role_tmp = pd.concat([role_tmp, role])
                nb_emp.append(role["position.positionId"].values)
        data_resources = role_tmp
        if len(nb_emp)>0:
            nb_emp = len(set(np.concatenate(nb_emp))) # Second value
        else: nb_emp=0
        # Project budget
        req = requests.get(base_link+links_ns.task.single+str(id)).json() # Risk of empty list
        task = pd.json_normalize(req)
        budget = task.budget.max()
        data = {"tasks":nb_task,"resources":nb_emp,"budget":budget}
        # print(nb_task, nb_emp, budget)
    else: # retuen empty dict
        data = {"tasks":0,"resources":0,"budget":0}
        data_task = {}
        data_resources = {}

    # Activities
    df = pd.DataFrame()
    if len(data_task)>0:
        tasks_df = data_task[["taskId","code","name","type","status","endDate"]]
        if len(data_resources)>0:
            resources_df = data_resources[["role","task.taskId","position.employee.firstName","position.employee.lastName"]]
            df = pd.merge(left=tasks_df, right=resources_df, left_on="taskId", right_on="task.taskId")
            df.drop(columns=["task.taskId"], inplace=True)
            rename_col = ["taskId","code","name","type","status","endDate","role","firstName","lastName"]
            df.columns = rename_col

    # Resources
    df_r = pd.DataFrame()
    if len(data_resources)>0:
        emp_task_list = data_resources[["task.taskId","position.employee.employeeId","position.employee.lastName","position.employee.firstName","role","task.name","task.status"]]
        rename_col = ["taskId","employeeId","lastName","firstName","role","taskName","status"]
        emp_task_list.columns = rename_col
        # compute total number of tasks per employee
        total_tasks = emp_task_list.groupby('employeeId')['taskId'].count()
        finished_tasks = emp_task_list[emp_task_list['status'] == 'FINISHED'].groupby('employeeId')['taskId'].count()
        ratio_finished = finished_tasks / total_tasks
        result = pd.concat([total_tasks, finished_tasks, ratio_finished], axis=1)
        result.columns = ['totalTasks', 'finishedTasks', 'ratioFinished']
        result.reset_index(inplace=True)
        df_r = pd.merge(left=result, right=emp_task_list.groupby("employeeId")[["lastName","firstName"]].first().reset_index(), how='left')
        print(df_r)
    return {
        "bio":bio,
        "stats": pd.DataFrame([data]),
        "tasks": df,
        "resources":df_r
    }
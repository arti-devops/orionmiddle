import requests
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
import requests
import pandas as pd
from services.links import *

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
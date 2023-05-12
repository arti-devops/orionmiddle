import json
from interfaces.task import *
from interfaces.filter import filter_df_by_col_value

#TODO : returning task list when position is active
def get_employee_task_list(p:str):
    tasks = get_task_list_by_employee_id(p) # type: DataFrame
    tasks = tasks.to_json(orient="records")
    tasks = json.loads(tasks)
    return {"tasks" : tasks}
    
#TODO : get all training from all positions of an employee
def get_employee_task_list_history(p:str): 
    pass

def get_task_statistics():
    stats = get_all_task_statistics()
    stats = stats.to_json(orient="records")
    stats = json.loads(stats)
    return {"stats": stats}

def get_task_list():
    tasks = get_all_tasks()
    tasks = tasks.to_json(orient="records")
    tasks = json.loads(tasks)
    return {"stats": tasks}

def get_filtered_task_list(q, ptype, direction, status, perPage, currentPage, filter):
    import math
    data = None
    if currentPage == 0:
        currentPage = 1
    tasks = get_all_tasks()
    
    #Filter data
    tasks = filter_df_by_col_value(tasks, "comment", filter, "taskId")
    
    tasks = tasks.to_dict(orient="records")
    queryLower = q.lower()
    direction = direction.lower()
    status = status.lower()
    ptype = ptype.lower()
    filteredUsers = [task for task in tasks if ((queryLower in task["name"].lower() or queryLower in task["code"].lower() or queryLower in task["comment"].lower() or queryLower in task["status"].lower()) and task['type'].lower() == (ptype or task['type'].lower()) and task['comment'].lower() == (direction or task['comment'].lower()) and task['status'].lower() == (status or task['status'].lower()))][::-1]
    # Sort the data by name in ascending order
    sortedfilteredUsers = sorted(filteredUsers, key=lambda x: x['code'],reverse=False)
    totalPage = math.ceil(len(filteredUsers) / perPage) if perPage else 1
    totalUsers = len(filteredUsers)
    if perPage:
        firstIndex = (currentPage - 1) * perPage
        lastIndex = perPage * currentPage
        sortedfilteredUsers = sortedfilteredUsers[firstIndex:lastIndex]
        data = {"tasks": sortedfilteredUsers, "totalPage": totalPage, "totalTasks": totalUsers}
    return data

def get_single_task_details(id) -> dict:
    task = get_task_details(id)
    bio = task["bio"].to_json(orient="records")
    stats = task["stats"].to_json(orient="records")
    tasks = task["tasks"].to_json(orient="records")
    resources = task["resources"].to_json(orient="records")
    bio = json.loads(bio)
    stats = json.loads(stats)
    tasks = json.loads(tasks)
    resources = json.loads(resources)
    return {"bio": bio, "stats":stats, "tasks":tasks, "resources":resources}
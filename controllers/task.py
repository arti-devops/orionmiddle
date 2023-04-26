import json
from interfaces.task import *

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

def get_filtered_task_list(q, perPage, currentPage):
    import math
    data = None
    if currentPage == 0:
        currentPage = 1
    tasks = get_all_tasks()
    tasks = tasks.to_dict(orient="records")
    queryLower = q.lower()
    filteredUsers = [task for task in tasks if ((queryLower in task["name"].lower() or queryLower in task["code"].lower() or queryLower in task["comment"].lower() or queryLower in task["status"].lower()))][::-1]
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
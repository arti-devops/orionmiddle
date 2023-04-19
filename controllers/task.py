
import json

#TODO : returning task list when position is active
def get_employee_task_list(p:str):
    from interfaces.task import get_task_list_by_employee_id
    tasks = get_task_list_by_employee_id(p) # type: DataFrame
    tasks = tasks.to_json(orient="records")
    tasks = json.loads(tasks)
    return {"tasks" : tasks}
    
#TODO : get all training from all positions of an employee
def get_employee_task_list_history(p:str): 
    pass
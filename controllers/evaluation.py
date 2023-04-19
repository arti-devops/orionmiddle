
import json

#TODO : returning evaluation list when position is active
def get_employee_evaluation_list(p:str) -> dict:
    from interfaces.evaluation import get_evaluation_list_by_employee_id
    evals = get_evaluation_list_by_employee_id(p)
    print(evals)
    evals = evals.to_json(orient="records")
    evals = json.loads(evals)
    return {"evaluations":evals}

    
#TODO : get all evaluations from all positions of an employee
def get_employee_evaluation_list_history(p:str): 
    pass
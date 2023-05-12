import json

#TODO : returning course list when position is active
def get_employee_course_list(p:str) -> dict:
    from interfaces.course import get_cours_list_by_employee_id
    courses = get_cours_list_by_employee_id(p)
    courses = courses.to_json(orient="records")
    courses = json.loads(courses)
    return {"courses": courses}

#TODO : get all training from all positions of an employee
def get_employee_course_list_history(p:str): 
    pass
import requests
import pandas as pd
from services.links import *

def get_cours_list_by_employee_id(p:str) -> pd.DataFrame:
    link_to_emp_courses = base_link+links_ns.course.position+p
    emp_courses = requests.get(link_to_emp_courses).json()
    if len(emp_courses)>0:
        df = pd.json_normalize(emp_courses)
        select_cols = ["courseId","training.name","training.school","startDate","training.duration","status"]
        df = df[select_cols]
        rename_cols = ["id","name","school","startDate","duration","status"]
        df.columns = rename_cols
        return df
    else: return pd.DataFrame(list())

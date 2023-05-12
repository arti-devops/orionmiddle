import requests
import pandas as pd
from services.links import *

def get_evaluation_list_by_employee_id(p:str) -> pd.DataFrame:
    link_to_emp_evals = base_link+links_ns.evaluation.position+p
    emp_evals = requests.get(link_to_emp_evals).json()
    if len(emp_evals)>0:
        return pd.json_normalize(emp_evals)
    else: return pd.DataFrame(list())
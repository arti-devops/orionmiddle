import requests
import pandas as pd
from services.links import *
from services.date import time_diff, generate_business_days_in_month

def get_daily_checkin_by_employee_id(p:str, s_d, e_d:str) -> pd.DataFrame :
    link_to_emp_logs = base_link+links_ns.logbook.prange+p+'/'+s_d+'/'+e_d
    print(link_to_emp_logs)
    emp_logs = requests.get(link_to_emp_logs).json()
    if len(emp_logs)>0:
        emp_logs = pd.json_normalize(emp_logs)
        select_cols = ["logbookId","logDate","checkinTime"]
        emp_logs = emp_logs[select_cols]

        bdays = pd.DataFrame(generate_business_days_in_month(s_d), columns=["bdays"])
        df = pd.merge(bdays, emp_logs, how="left", left_on="bdays", right_on="logDate")
        df = df[["bdays","logbookId","checkinTime"]]
        df.logbookId.fillna(0, inplace=True)
        df.checkinTime.fillna("23:59:59", inplace=True)

        df["isLate"] = df.checkinTime.map(time_diff) < 0
        df["isPresent"] = df.logbookId > 0
        df["isLate"] = df.isLate * df.isPresent
        df.rename(columns={"bdays":"logDate","checkinTime":"checkIn"}, inplace=True)
        emp_logs = df[["logDate","checkIn","isPresent","isLate"]]

    return pd.DataFrame(emp_logs)

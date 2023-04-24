import json
from services.date import get_first_and_last_date_of_month

#TODO returning active month logbook
def get_employee_logbook(p:str, date_string:str) -> dict:
    from interfaces.logbook import get_daily_checkin_by_employee_id
    # from interfaces.employee import get_employee_bio_data
    fdate, ldate = get_first_and_last_date_of_month(date_string)
    logbook = get_daily_checkin_by_employee_id(p, fdate, ldate)
    logbook = logbook.T.to_json(orient="split")
    logbook = json.loads(logbook)
    
    # emp = get_employee_bio_data(p)
    return {
        # "employee": emp,
        "logbook": logbook
        }
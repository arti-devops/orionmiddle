import pandas as pd
import datetime as dt
from datetime import datetime

#date_string = "2023-03-01" "%Y-%m-%d"

def extract_year_from_date(date_string:str):
    date_obj = datetime.strptime(date_string, "%Y-%m-%d")
    return date_obj.year

def extract_month_from_date(date_string:str):
    date_obj = datetime.strptime(date_string, "%Y-%m-%d")
    return date_obj.month

def extract_workdays_in_month(year, month):
    start_date = dt.date(year, month, 1)
    end_date = dt.date(year, month+1, 1) - dt.timedelta(days=1)
    return pd.bdate_range(start_date, end_date, freq='C').size

def compute_time_diff_in_minutes(checkin:str):
    time1 = '08:10:00'
    time2 = checkin
    dt1 = datetime.strptime(time1, '%H:%M:%S')
    dt2 = datetime.strptime(time2, '%H:%M:%S')
    time_diff = dt1 - dt2
    minutes_diff = time_diff.total_seconds() / 60.0
    return minutes_diff

def compute_word_days_in_month(date_string:str):
    year = extract_year_from_date(date_string)
    month = extract_month_from_date(date_string)
    return extract_workdays_in_month(year, month)
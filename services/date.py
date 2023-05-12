import pandas as pd
import datetime as dt
from datetime import datetime, timedelta

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

def time_diff(start_time_str, end_time_str="08:10:00"):
    start_time = datetime.strptime(start_time_str, '%H:%M:%S')
    end_time = datetime.strptime(end_time_str, '%H:%M:%S')
    time_delta = end_time - start_time
    time_diff_seconds = int(time_delta.total_seconds())
    return time_diff_seconds

def get_first_and_last_date_of_month(date_string):
    date = datetime.strptime(date_string, '%Y-%m-%d')
    first_date = datetime(date.year, date.month, 1)
    last_date = datetime(date.year, date.month, 1) + timedelta(days=31)
    last_date = last_date - timedelta(days=last_date.day)

    return first_date.strftime("%Y-%m-%d"), last_date.strftime("%Y-%m-%d")

def generate_business_days_in_month(date_str: str):
    from pandas.tseries.offsets import BDay
    from calendar import monthrange
    # Convert input date string to pandas datetime
    date = pd.to_datetime(date_str)
    # Extract year and month from the input date
    year = date.year
    month = date.month
    # Determine the last valid day of the month
    last_day = monthrange(year, month)[1]
    # Update the end date of the date range to the last valid day of the month
    date_range = pd.date_range(start=f"{year}-{month}-01", end=f"{year}-{month}-{last_day}", freq='B')
    # Filter the dates to get only business days
    business_days = date_range[date_range.isin(pd.date_range(date_range[0], date_range[-1], freq=BDay()))]
    # Convert the resulting pandas DatetimeIndex to a list of strings in YYYY-mm-dd format
    business_days_list = business_days.strftime('%Y-%m-%d').tolist()
    return business_days_list
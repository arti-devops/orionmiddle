import requests
import pandas as pd
from services.links import *

def get_positionId_by_direction() -> dict:
    req = requests.get(base_link+links_ns.position.all_active).json()
    position = pd.json_normalize(req)

    select_col = ["positionId","employee.employeeId","subdivision.code",'service.subdivision.code']
    rename_col = ["positionId","employeeId","codeA","codeB"]
    
    position_df = position[select_col].copy()
    position_df.columns = rename_col
    position_df["direction"] = position_df.codeA.fillna(position_df.codeB)
    position_df.drop(columns=["codeA","codeB"], inplace=True)
    position_df.direction = position_df.direction.map(lambda x: x.split("_")[1])

    df = position_df.copy()
    employee_ids_by_direction = {}
    # Loop through each unique direction in the DataFrame
    for direction in df['direction'].unique():
        direction_df = df[df['direction'] == direction]
        employee_ids = direction_df['employeeId'].tolist()
        employee_ids_by_direction[direction] = employee_ids
    #print(employee_ids_by_direction)
    return employee_ids_by_direction

def filter_df_by_col_value(df, col, value):
    matcher = get_positionId_by_direction()
    print(matcher)
    drn_df = df[df[col] == value]
    employee_ids = matcher[value]
    # Filter the "DRRN" DataFrame to only include rows with employee IDs in the list
    return drn_df[drn_df['positionId'].isin(employee_ids)]
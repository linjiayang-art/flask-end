
from ..models.usermodel import *
from sqlalchemy import Boolean, Integer, String, DateTime, VARCHAR, inspect
import pandas as pd
from pandas import DataFrame
import json
from flask import current_app
import os
import numpy as np
import datetime


def get_colums_type():
    data_structure_dict = {
        Integer: int,
        Boolean: bool,
        String: str,
        VARCHAR: VARCHAR,
        DateTime: datetime.datetime}

    target = User()
    type_result = {}
    columns = inspect(target.__class__).columns
    for column in columns:
        c_database_type = column.type
        c_column_name = column.name
        if type(c_database_type) in data_structure_dict.keys():
            data_type = data_structure_dict[type(c_database_type)]
            type_result[c_column_name] = data_type
        else:
            type_result[c_column_name] = str
    return type_result


def check_data_format(parms, data_type):
    if isinstance(parms, data_type):
        return {
            'status': True,
            'value': parms
        }
    else:
        return {
            'status': False,
            'value': 'erro'
        }


def get_data_dict(df: DataFrame, model_name: str) -> list:
    results = []
    type_result = get_colums_type()
    column_dict = get_data_dict(model_name=model_name)
    for index, row in df.iterrows():
        sql_dict = create_sql_dict(
            row=row, column_dict=column_dict, type_result=type_result)
        'row is dict '
        results.append(sql_dict)
    return results


def create_sql_dict(row: dict, column_dict: dict, type_result=dict) -> dict:
    sql_dict = {}
    for key, value in row.items():
        if pd.isna(value):
            continue
        if key in column_dict:
            sql_key = column_dict[key]
            # check value
            column_type = type_result[sql_key]
            check_r = check_data_format(value, column_type)
            # str not check
            if column_type == str:
                sql_dict[sql_key] = value
                continue
            if check_r['status'] == True:
                sql_dict[sql_key] = value
            else:
                # print(column_type,value)
                r = (str(column_type)+value)
                return {
                    'status': False,
                    'value': {
                        'sql_key': sql_key,
                        'value': value,
                        'colum': key,
                        'erro': r
                            }
                        }
    return {
        'status': True,
        'value': sql_dict
            }


def get_sheet_name(file):
    excel_data = pd.ExcelFile(file)
    # Get the sheet names
    sheet_name = excel_data.sheet_names[0]


def get_data_dict(model_name) -> dict:
    file_path = os.path.join(
        current_app.config['MODELFILE_DIR'], 'model_dict.json')
    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)
        load_data = data[model_name]
        return dict(load_data)

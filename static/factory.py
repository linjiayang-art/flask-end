
from datetime import datetime
from flask import current_app, g
from static.models.usermodel import User
from static.extensions import db
from pandas import ExcelWriter
import pandas as pd
#from openpyxl.utils import get_column_letter
import numpy as np



def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


""" def to_excel_auto_column_weight(df: pd.DataFrame, writer: ExcelWriter, sheet_name="Shee1"):
    "DataFrame保存为excel并自动设置列宽"
    # 数据 to 写入器，并指定sheet名称
    df.to_excel(writer, sheet_name=sheet_name, index=False, encoding="utf-8")
    #  计算每列表头的字符宽度
    column_widths = (
        df.columns.to_series().apply(lambda x: len(str(x).encode('utf8'))).values
    )
    #  计算每列的最大字符宽度
    max_widths = (
        df.astype(str).applymap(lambda x: len(
            str(x).encode('utf8'))).agg(max).values
    )
    # 取前两者中每列的最大宽度
    widths = np.max([column_widths, max_widths], axis=0)
    # 指定sheet，设置该sheet的每列列宽
    worksheet = writer.sheets[sheet_name]
    for i, width in enumerate(widths, 1):
        # openpyxl引擎设置字符宽度时会缩水0.5左右个字符，所以干脆+2使左右都空出一个字宽。
        worksheet.column_dimensions[get_column_letter(i)].width = width + 1
 """

def generate_norequery(model) -> list:
    resluts = []
    try:
        for r in model:
            r = to_dict(r)
            resluts.append(r)
        return resluts
    except:
        return False

def generate_date(input_dict:dict,**kwars)->dict:
    '''
    change result formart ,useing return result
    like this generate_date(mydict,datetype='%Y-%m-%d')
    '''
    datetype=kwars.get('datetype','%Y-%m-%d')
    datetime.strftime()
    for key,value in input_dict.items():
        if 'date' in key  or 'time' in key :
            try:
                input_dict[key]=value.strftime(datetype)
            except AttributeError:
                continue
    return input_dict

def generate_filenname():
    now = datetime.now()
    filename = f"{now.year}-{now.month}-{now.day}_{now.hour}-{now.minute}-{now.second}"+'.xlsx'
    return filename

def generate_filenname_log(filemodel):
    if not filemodel:
        filemodel = 'xlsx'
    now = datetime.now()
    filename = f"{now.year}-{now.month}-{now.day}"+'.%s' % filemodel
    return filename




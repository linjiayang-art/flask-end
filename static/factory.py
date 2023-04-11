import json
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from datetime import datetime, timedelta
from flask import current_app, g
from static.models import User
from static.extensions import db
from pandas import ExcelWriter
import pandas as pd
from openpyxl.utils import get_column_letter
import numpy as np
import re


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


def to_excel_auto_column_weight(df: pd.DataFrame, writer: ExcelWriter, sheet_name="Shee1"):
    """DataFrame保存为excel并自动设置列宽"""
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


def generate_norequery(model) -> list:
    resluts = []
    try:
        for r in model:
            r = to_dict(r)
            resluts.append(r)
        return resluts
    except:
        return False


def getassitesnumber(head: str) -> str:
    sql = 'SELECT it.Id AS Id, SequenceName,ItemSortNo,ItemType,ItemData,ItemLength FROM Sys_Sequence pa inner join Sys_SequenceItem it on pa.Id=it.ParentId'
    sql=sql +" where 1=1 and  SequenceName='%s'  order by SequenceName,ItemSortNo asc"%head
    result= db.session.execute(sql)
    dict_result=[]
    for row in result.fetchall():
        dict_result.append(dict(zip(result.keys(),row)))
    assitesNo=''
    for i in dict_result:
        if i['ItemType']=='SN':
            num=int(i['ItemData']) 
            if num <10:
                lenth= '00'.format(num)
            elif num >=10 or num <100:
                lenth= '0'.format(num)
            elif num >=100:
                 lenth=format(num)
            assitesNo=assitesNo+lenth
            num=num+1
            id=i['Id']
            sql="update Sys_SequenceItem set ItemData=%s where Id='%s'"%(num,id)
            db.session.execute(sql)
            db.session.commit()
        assitesNo=assitesNo+i['ItemData']
    return assitesNo


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


def generate_token(user):
    expiration = 3600
    s = Serializer(current_app.config['SECRET_KEY'])
    # 验证修改为字典传输
    data = {'id': user.userid}
    token = s.dumps(data)
    # token=s.dumps({'id':user.Userid}).decode('ascii')
    return (token, expiration)


def validate_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except (BadSignature, SignatureExpired):
        return False
    user = UserInfo.query.get(data['id'])
    if user is None:
        return False
    g.current_user = user  # 将用户对象储存到G上
    return True


def changeTimeType(*args, **kwargs):
    file = {}
    for key, value in kwargs.items():
        file[key] = value
    return file


def codePhase():
    # result=Phase.query.paginate(page=17, per_page=10000)
    result = []
    for r in result:
        # r.testdate
        oldtime = r.oldtestdate
        oldtime = re.sub('[\u4e00-\u9fa5]', '', oldtime)
        oldtime = pd.to_datetime(oldtime)
        r.testdate = oldtime
    db.session.commit()


def gettommerytime():
    """     time=datetime.now()
    limit_time=(time+ timedelta(days=1)).strftime('%Y-%m-%d')
    #print(pf[pf['StartTime']=='2021-03-01'])
    return limit_time """
    time = datetime.now()
    limit_time = (time + timedelta(days=1)).strftime('%Y-%m-%d')
    week = datetime.strptime(limit_time, "%Y-%m-%d").weekday() + 1  # 一定要加1
    if week == 6:
        time = datetime.now()
        limit_time = (time + timedelta(days=3)).strftime('%Y-%m-%d')
    # print(pf[pf['StartTime']=='2021-03-01'])
    return limit_time

from static.apis.v1 import api_v1
from flask import jsonify

@api_v1.route('/')
def index():

    return jsonify(code='200',msg="邮件发送成功", data= 'OK' )
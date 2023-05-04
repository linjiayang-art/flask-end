from static.apis.v1 import api_v1
from flask import jsonify,request,g,make_response,current_app
from static.apis.auth.auth import generate_token
from flask.views import MethodView
from static.extensions import csrf
from static.models import User
from flask_wtf.csrf import generate_csrf

class AuthTokenAPI(MethodView):
    decorators=[csrf.exempt]
    def post(self):
        #grant_type = request.form.get('grent_type')
        try:
            userno = request.form.get('userno')
            password = request.form.get('password')
            if userno is None or password is None:
                return  jsonify(code='201',msg='未获取到表单数据', data='未获取到表单数据')
        except:
            return  jsonify(code='201',msg='未获取到表单数据', data='未获取到表单数据')
        user =User.query.filter_by(userno=userno).first()
        if user is None or not user.validate_password(password):
            return  jsonify(code='B0001',msg='用户不存在或者密码错误', data='用户不存在或者密码错误')
        if user.isdeleted==True:
            return  jsonify(code='B0001',msg='用户失效,请联系管理员', data='用户失效,请联系管理员')
        token,expiration =generate_token(user)
        csrf_token = generate_csrf(secret_key=current_app.config['SECRET_KEY'])
        data= {
                'Authorization':token,
                'access_token':token,
                'statusText':expiration,
                'csrf_token':csrf_token
        }
        return jsonify(code='200', msg='一切OK',data=data)

api_v1.add_url_rule('/token',view_func=AuthTokenAPI.as_view('token'),methods=['POST'])
from static.apis.v1 import api_v1
from flask import jsonify, request, g, make_response, current_app
from static.apis.auth.auth import generate_token
from flask.views import MethodView
from static.extensions import csrf, db
from static.models import User
from flask_wtf.csrf import generate_csrf
import datetime
from static.forms import LoginFrom
from flask_login import logout_user

class AuthTokenAPI(MethodView):
    decorators = [csrf.exempt]
    def post(self):
        # print(request.get_json())
        form = LoginFrom()
        if form.validate_on_submit():
            userno = form.userno.data
            password=form.password.data
            user = User.query.filter_by(userno=userno).first()
            if user is None or not user.validate_password(password):
                return jsonify(code='B0001', msg='用户不存在或者密码错误', data='用户不存在或者密码错误')
            if user.isdeleted == True:
                return jsonify(code='B0001', msg='用户失效,请联系管理员', data='用户失效,请联系管理员')
            token, expiration = generate_token(user)
            csrf_token = generate_csrf(
                secret_key=current_app.config['SECRET_KEY'])
            username, userno = user.username, user.userno
            expires = datetime.datetime.now()
            expires += datetime.timedelta(minutes=30)
            data = {
                'Authorization': token,
                'accessToken': token,
                'access_token': token,
                'statusText': expiration,
                'csrf_token': csrf_token,
                'expires': expires.strftime('%Y-%m-%d %H:%M:%S'),
                'username': username,
                'userno': userno
            }
            return jsonify(code='200', msg='一切OK', data=data, success=True)
        else:
            return jsonify(code='201', msg='未获取到表单数据', data='未获取到表单数据')


class AuthTokenAPIv2(MethodView):
    decorators = [csrf.exempt]

    def post(self):
        try:
            formdata = request.get_json()
        except:
            formdata = {
                'userno': '123456',
                'password': '123456'
            }

        # grant_type = request.form.get('grent_type')
        if not formdata:
            return make_response(jsonify(code='201', msg='未获取到表单数据'), 200)
        userno = '123456'
        password = '123456'
        if userno is None or password is None:
            return jsonify(code='201', msg='未获取到表单数据', data='未获取到表单数据')
        user = User.query.filter_by(userno=userno).first()
        if user is None or not user.validate_password(password):
            return jsonify(code='B0001', msg='用户不存在或者密码错误', data='用户不存在或者密码错误')
        if user.isdeleted == True:
            return jsonify(code='B0001', msg='用户失效,请联系管理员', data='用户失效,请联系管理员')
        token, expiration = generate_token(user)
        csrf_token = generate_csrf(secret_key=current_app.config['SECRET_KEY'])
        expires = datetime.datetime.now()
        expires += datetime.timedelta(minutes=30)
        data = {
            'accessToken': token,
            'csrf_token': csrf_token,
            'tokenType': 'Bearer',
            'expires': expiration

        }
        return jsonify(code='200', msg='登录成功', data=data, success=True)

@api_v1.route('auth/logout',methods=['DELETE'])
def logout():
    logout_user()
    return make_response(jsonify(code="A230",msg="token无效或已过期") ,401) 


api_v1.add_url_rule(
    '/token', view_func=AuthTokenAPI.as_view('token'), methods=['POST'])

api_v1.add_url_rule(
    '/auth/login', view_func=AuthTokenAPIv2.as_view('auth_login'), methods=['POST'])

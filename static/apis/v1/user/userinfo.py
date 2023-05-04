from static.apis.v1 import api_v1
from flask import jsonify,g
from flask.views import MethodView
from static.apis.auth.auth import auth_required
from static.models import SysUserRole

class UserInfoApi(MethodView):
    decorators=[auth_required]
    def get(sefl):
        userinfo= g.current_user
        print(userinfo.username)
        data={
            'username':userinfo.username,
            'userno':userinfo.userno,
        }
        return  jsonify(code='200',msg='登录成功', data=data)
    
api_v1.add_url_rule('/userinfo',view_func=UserInfoApi.as_view('userinfoapi'),methods=['GET','POST'])
from static.apis.v1 import api_v1
from flask import jsonify,g,make_response
from flask.views import MethodView
from static.apis.auth.auth import auth_required
from static.models import SysUserRole,SYSRole

class UserInfoApi(MethodView):
    decorators=[auth_required]
    def get(sefl):
        userinfo= g.current_user
        
        perms=[ "sys:user:edit", 
                "sys:user:delete"] 
        if userinfo.perms=='y':
            perms.append("sys:user:add")
        roleresult=SysUserRole.query.filter_by(user_id=userinfo.id).all()
        roles=[]
        for i in roleresult:
            role=SYSRole.query.filter_by(id=i.role_id).first()
            roles.append(role.code)
        #roules=[userinfo.UserRole]
        if roles==[]:
            roles.append('USER')
        user={'roles':roles,
            'introduction':'I am a super administrator ',
            'avatar': userinfo.avatar,
            'nickname':userinfo.username,
            'perms':perms,
            'userId':userinfo.id,
           }
        return  jsonify(code='200',msg='登录成功', data=user)
    
api_v1.add_url_rule('/users/me',view_func=UserInfoApi.as_view('userinfoapi'),methods=['GET','POST'])
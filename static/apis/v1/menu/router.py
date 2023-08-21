from static.apis.v1 import api_v1
from flask import jsonify, g
from flask.views import MethodView
from static.apis.auth.auth import auth_required
from static.models.sysmodel import SysUserRole


class RouterInfoApi(MethodView):
    decorators = [auth_required]
    def get(self):
        userinfo = g.current_user
        data = _getmockdata()
        return jsonify(code='200', msg='登录成功', data=data)


def _getmockdata() -> list:

    router = [
    {
        "path": "/system/menu",
        "component": "Layout",
        "redirect": "/system/",
        "meta": {
            "title": "系统管理",
            "icon": "system",
            "hidden": False,
            "alwaysShow": True,
            "roles": ["ADMIN", "USER"],
            "keepAlive": True,
        },
        "children": [
            {
                "path": "menu",
                "component": "system/menu/index",
                "name": "menu",
                "meta": {
                    "title": "菜单管理",
                    "icon": "menu",
                    "hidden": False,
                    "alwaysShow": True,
                    "roles": ["ADMIN", "USER"],
                    "keepAlive": True,
                    'showParent': True
                },
            },
 {
                "path": "menu2",
                "component": "system/menu/index",
                "name": "menu2",
                "meta": {
                    "title": "菜单管理",
                    "icon": "menu",
                    "hidden": False,
                    "alwaysShow": True,
                    "roles": ["ADMIN", "USER"],
                    "keepAlive": True,
                    'showParent': True
                },
            },

        ]
    },
]

    return router

api_v1.add_url_rule('/menus/routes',view_func=RouterInfoApi.as_view('routes'),methods=['GET'])
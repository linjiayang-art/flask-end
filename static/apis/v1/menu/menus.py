from static.apis.v1 import api_v1
from flask import jsonify, g,request,make_response
from flask.views import MethodView
from static.apis.auth.auth import auth_required
from static.models import Menu
from static.factory import to_dict
from static.extensions import db
from static.forms import MenuForm

class MenusApi(MethodView):
    decorators=[auth_required]
    def get(self):
        data=[]
        menu=_generatallemenumodel(0,data)
        return jsonify(code='200',msg='获取目录成功',data=menu)
    def post(self):
        form=MenuForm()
        if form.validate_on_submit():
            try:
                menu=Menu(**form.data)
                db.session.add(menu)
                db.session.commit()
            except Exception as e:
                return jsonify(code='500',msg='数据新增失败',data=e.args)
            return jsonify(code='200',msg='新增目录成功',data='OK')
        else:
            return jsonify(code='201',msg='获取数据失败',data=form.errors)
    def put(self,menu_id):
        menu=Menu.query.get_or_404(menu_id)
        data=request.get_json()
        msg=' 更新成功,未成功修改数据项 :'
        for key,value in data.items():
            try:
                setattr(menu,key,value)
            except:
                msg+='%s :%s'%(key,value)
        db.session.commit()
        return jsonify(code='201',msg=msg,data='ok')
    

def _generatallemenumodel(parentid,mylist:list):
    result=Menu.query.filter_by(parent_id=parentid).order_by(Menu.menu_sort.asc()).all()
    for p in result:
        x1=[]
        model={}
        p=to_dict(p)
        for key,value in p.items():
            x1=[]
            if key=='id':
                nextkey=value
            model[key]=value
        model['children']=x1
        mylist.append(model)
        _generatallemenumodel(nextkey,x1)
    return mylist

def test_init_menu():
    menu1 = Menu(
                 parent_id=0,
                 menu_name='系统管理',
                 menu_type=2,
                 menu_path='/system',
                 component='Layout',
                 menu_visible=0,
                 menu_sort=1,
                 menu_icon='system',
                 redirect_url='/system/user'
                 )
    menu2 = Menu(
                 parent_id=1,
                 menu_name='菜单管理',
                 menu_type=1,
                 menu_path='menus',
                 component='system/menu/index',
                 menu_visible=0,
                 menu_sort=1,
                 menu_icon='menu',
                 )
    db.session.add(menu1)
    db.session.add(menu2)
    db.session.commit()

api_v1.add_url_rule('/menus/',view_func=MenusApi.as_view('menus'),methods=['GET','POST','PUT'])
api_v1.add_url_rule('/menus/<int:menu_id>',view_func=MenusApi.as_view('menu'),methods=['GET','POST','PUT'])

from static.tests.base import BaseAPITestCase
from flask import url_for
from static.models import User, Menu
from static.extensions import db


class MenuBaseData():
    '''provide for test model basedata'''
    menu1=Menu(id=1,  parent_id=0,menu_name='系统管理',menu_type='MENU',
                          menu_path='/system',component='Layout',
                          menu_visible=0,
                          menu_sort=1,
                          menu_icon='system',
                          redirect_url='/system/user'
                          )
    menu2=Menu(id=2,
                          parent_id=1,
                          menu_name='菜单管理',
                          menu_type='CATALOG',
                          menu_path='menus',
                          component='system/menu/index',
                          menu_visible=0,
                          menu_sort=1,
                          menu_icon='menu',
                          )
    addmenu = dict(
            id=3,
            parent_id=1,
            menu_name='/用户管理',
            menu_type='CATALOG',
            menu_path='/system',
            component='system/menu/user',
            menu_visible=True,
            menu_sort=3,
            menu_icon='user',
        )
    editmenu = dict(
            id=1,
            parent_id=1,
            menu_name='/用户管理修改',
            menu_type='CATALOG',
            menu_path='/system',
            component='system/menu/user/修改',
            menu_visible=True,
            menu_sort=3,
            menu_icon='user',
        )

    def __init__(self,menu1,menu2,addmenu,editment) :
        self.menu1 =menu1
        self.menu2 = menu2
        self.addmenu=addmenu
        self.editmenu=editment
      

class MenysTestCase(BaseAPITestCase,MenuBaseData):
    def test_init_menu(self):
        menu1 =self.menu1
        menu2 = self.menu2
        db.session.add(menu1)
        db.session.add(menu2)
        db.session.commit()
    def test_add_menu(self):

        token = self.get_oauth_token()
        response = self.client.post(url_for('api_v1.menus'), json=self.addmenu
                                    , headers=self.set_auth_headers(token))
        data = response.get_json()
        self.assertIn('code', data)
        self.assertIn('data', data)
        self.assertIn('200', data['code'])
        self.assertIn('成功', data['msg'])

    def test_get_menu(self):
        self.test_add_menu()
        self.test_init_menu()
        token = self.get_oauth_token()
        response = self.client.get(url_for('api_v1.menus'),
                                   headers=self.set_auth_headers(token))
        data = response.get_json()
        self.assertIn('code', data)
        self.assertIn('data', data)
        self.assertIn('data', data)
        self.assertIn(data['code'], '200')
        self.assertIn('成功', data['msg'])

    def test_update_menu(self):
        self.test_init_menu()
        token = self.get_oauth_token()
        response = self.client.put(url_for('api_v1.menu', menu_id=1), json=self.editmenu,
            headers=self.set_auth_headers(token=token))
        data = response.get_json()
        self.assertIn('code', data)

    def test_404_response(self):
        response = self.client.get('/api/foo')
        data = response.get_json()
        self.assertEqual(
            data['msg'], 'The requested URL was not found on the server.')

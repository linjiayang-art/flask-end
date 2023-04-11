from static.extensions import db
from static.models import UserInfo,SYS_Role,Menu

def fake_admin():
    admin=UserInfo(
        userno='555',
        username='lin yang',
    )
    admin.set_password('123456')
    db.session.add(admin)
    db.session.commit()


def fake_menu():
    menu=Menu(Parent_id=0,menu_name='系统管理',menu_type=0,menu_path='/sicore-system',
              component="Layout",menu_perm=None,menu_visible=True,menu_sort=1,
              redirect_url="/sicore-system/user", menu_icon='system')
    db.session.add(menu)
    db.session.commit()

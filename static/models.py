from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from static.extensions import db
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime,BigInteger
from sqlalchemy.orm import relationship,DeclarativeBase

class Base():
    createuser = Column(String(50))
    createdate = Column(DateTime, default=datetime.utcnow)
    isdeleted = Column(Boolean, default=False)


class User(db.Model, UserMixin,Base):
    __tablename__ = 'sys_user'
    id = Column(Integer, primary_key=True)
    userno = Column(Integer)
    password = Column(String(256))
    username = Column(String(50))
    perms = Column(String(128))
    department_id = Column(String(50))
    user_role = Column(String(50))
    avatar=Column(String(255),default='https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif')

    # consumableLog=relationship('ConsumableLog',lazy=False)
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)


class DePartMent(db.Model, Base):
    __tablename__ = 'sys_department'
    id = Column(Integer, primary_key=True)
    department_name = Column(String(50))
    department_no = Column(String(50))


#system
class Menu(db.Model, Base):
    __tablename__='sys_menu'
    id = Column(BigInteger, primary_key=True)
    parent_id = Column(BigInteger)
    menu_path = Column(String(80))
    component = Column(String(80))
    redirect_url = Column(String(80))
    menu_name = Column(String(80))  #title
    menu_icon = Column(String(80))
    menu_type = Column(String(80))
    menu_visible = Column(Boolean, default=True)
    menu_perm = Column(String(80))
    menu_sort = Column(BigInteger)


class SYSRole(db.Model, Base):
    __tablename__ = 'sys_role'
    id = Column(Integer, primary_key=True)
    rolename = Column(String(50))
    code = Column(String(50))
    sort = Column(String(50))
    rolestatus = Column(Boolean, default=True)


class SysRoleMenu(db.Model, Base):
    __tablename__='sys_role_menu'
    id=Column(BigInteger,primary_key=True)
    role_id=Column(BigInteger)
    menu_id=Column(BigInteger)
    #relationship
    #role_id=Column(BigInteger,ForeignKey('sys_role.id'))
    #menu_id=Column(BigInteger,ForeignKey('sys_menu.id'))
    #sys_role=relationship('SYSRole')
    #sys_menu=relationship('Menu')

class SysUserRole(db.Model, Base):
    __tablename__='sys_user_role'
    id=Column(BigInteger,primary_key=True)
    #relationship
    user_id=Column(BigInteger,)
    role_id=Column(BigInteger,)
    #user_id=Column(BigInteger,ForeignKey('sys_user.userid'))
    #role_id=Column(BigInteger,ForeignKey('sys_role.id'))
    #sys_user=relationship('User')
    #sys_role=relationship('SYSRole')


#dict
class DictType(db.Model, Base):
    __tablename__='sys_dict_type'
    id=Column(Integer,primary_key=True)
    name=Column(String(50))
    code=Column(String(50))
    status=Column(Boolean, default=True)
    remark=Column(String(50))


class DictItem(db.Model, Base):
    __tablename__='sys_dict_item'
    id=Column(Integer,primary_key=True)
    type_code=Column(String(50))
    type_id=Column(String(50))
    name=Column(String(50))
    value=Column(String(50))
    status=Column(Boolean, default=True)


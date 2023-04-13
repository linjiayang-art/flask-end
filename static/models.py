from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from static.extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'sys_user'
    userid = db.Column(db.Integer, primary_key=True)
    userno = db.Column(db.Integer)
    password = db.Column(db.String(256))
    username = db.Column(db.String(50))
    perms = db.Column(db.String(128))
    departMentId = db.Column(db.String(50))
    userRole = db.Column(db.String(50))
    isdeleted = db.Column(db.Boolean, default=False)
    # consumableLog=db.relationship('ConsumableLog',lazy=False)
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)


class DePartMent(db.Model):
    __tablename__ = 'sys_department'
    id = db.Column(db.Integer, primary_key=True)
    departmentName = db.Column(db.String(50))
    departmentNo = db.Column(db.String(50))
    createTime = db.Column(db.DateTime, default=datetime.utcnow)
    createUser = db.Column(db.String(50))
    isDeleted = db.Column(db.Boolean, default=False)

#system
class Menu(db.Model):
    __tablename__='sys_menu'
    id = db.Column(db.BigInteger, primary_key=True)
    parent_id = db.Column(db.BigInteger)
    menu_path = db.Column(db.String(80))
    component = db.Column(db.String(80))
    redirect_url = db.Column(db.String(80))
    menu_name = db.Column(db.String(80))  #title
    menu_icon = db.Column(db.String(80))
    menu_type = db.Column(db.String(80))
    menu_visible = db.Column(db.Boolean, default=True)
    menu_perm = db.Column(db.String(80))
    menu_sort = db.Column(db.BigInteger)
    isdeleted= db.Column(db.Boolean, default=False)

class SYSRole(db.Model):
    __tablename__ = 'sys_role'
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(50))
    code = db.Column(db.String(50))
    sort = db.Column(db.String(50))
    rolestatus = db.Column(db.Boolean, default=True)
    createTime = db.Column(db.DateTime, default=datetime.utcnow)
    createUser = db.Column(db.String(50))
    isDeleted = db.Column(db.Boolean, default=False)

class SysRoleMenu(db.Model):
    __tablename__='sys_role_menu'
    id=db.Column(db.BigInteger,primary_key=True)
    role_id=db.Column(db.BigInteger)
    menu_id=db.Column(db.BigInteger)
    #relationship
    #role_id=db.Column(db.BigInteger,db.ForeignKey('sys_role.id'))
    #menu_id=db.Column(db.BigInteger,db.ForeignKey('sys_menu.id'))
    #sys_role=db.relationship('SYSRole')
    #sys_menu=db.relationship('Menu')

class SysUserRole(db.Model):
    __tablename__='sys_user_role'
    id=db.Column(db.BigInteger,primary_key=True)
    #relationship
    user_id=db.Column(db.BigInteger,)
    role_id=db.Column(db.BigInteger,)
    #user_id=db.Column(db.BigInteger,db.ForeignKey('sys_user.userid'))
    #role_id=db.Column(db.BigInteger,db.ForeignKey('sys_role.id'))
    #sys_user=db.relationship('User')
    #sys_role=db.relationship('SYSRole')


#dict
class DictType(db.Model):
    __tablename__='sys_dict_type'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    code=db.Column(db.String(50))
    status=db.Column(db.Boolean, default=True)
    remark=db.Column(db.String(50))
    createtime=db.Column(db.DateTime, default=datetime.utcnow)

class DictItem(db.Model):
    __tablename__='sys_dict_item'
    id=db.Column(db.Integer,primary_key=True)
    type_code=db.Column(db.String(50))
    type_id=db.Column(db.String(50))
    name=db.Column(db.String(50))
    value=db.Column(db.String(50))
    status=db.Column(db.Boolean, default=True)
    createtime=db.Column(db.DateTime, default=datetime.utcnow)
    createuser=db.Column(db.String(50))


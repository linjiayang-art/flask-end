# -*- coding: utf-8 -*-
"""
    models.usermodule
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) YEAR by AUTHOR.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""

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

class User(db.Model, UserMixin, Base):

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
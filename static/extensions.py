from flask_sqlalchemy import SQLAlchemy
from jinja2.utils import markupsafe 
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_mail import Mail


db = SQLAlchemy()
moment = markupsafe.Markup()
login_manager = LoginManager()
csrf = CSRFProtect()
mail=Mail()

@login_manager.user_loader
def load_user(user_id):
    from static.models import UserInfo
    user = UserInfo.query.get(user_id)
    return user

""" @login_manager.user_loader
def load_user(user_id):
    from ITAM.models import UserInfo
    user = UserInfo.query.get(int(user_id))
    return user
 """
login_manager.login_view = 'auth.url_login'


from flask import Flask ,request,jsonify,g
import os
from flask_sqlalchemy import record_queries
#from flask_moment import Moment
from flask_cors import CORS
# 导入日志模块
import  logging
from logging import  FileHandler
from logging.handlers import SMTPHandler, RotatingFileHandler
from static.apis.v1 import api_v1
from flask_login import login_user
from static.factory import  generate_filenname_log
from flask_wtf.csrf import CSRFError
from static.settings import config
from static.extensions import db,login_manager,csrf,mail
from static.models import *
from static.blueprints.auth import auth_bp


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    #app config
    app = Flask('static')
    app.config.from_object(config[config_name])


    LOG_DIR=os.path.join(basedir, 'logs')
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    FILE_DIR=os.path.join(os.path.abspath(os.path.dirname(__file__)),'uploads')
    if not os.path.exists(FILE_DIR):
        os.makedirs(FILE_DIR)

    CORS(app,supports_credentials=True)
    register_logging(app)
    register_request_handlers(app)
    register_extensions(app)
    register_blueprints(app)
    register_errors(app)
    register_shell_context(app)
    app.ensure_ascii=True
    return app

def register_logging(app):
    class RequestFormmatter(logging.Formatter):
        def format(self,record):
            record.url=request.url
            record.remote_addr=request.remote_addr
            return super(RequestFormmatter,self).format(record)
    request_formatter=RequestFormmatter(
        '[%(asctime)s]%(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(messsage)s'
    )

    formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')


    filename =  generate_filenname_log('txt')
    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/%s'%filename),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    #waring
    '''filename =  generate_filenname_log('txt')
    waring_handler = RotatingFileHandler(os.path.join(basedir, 'errors/%s'%filename),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    waring_handler.setFormatter(formatter)
    waring_handler.setLevel(logging.WARN)
    app.logger.addHandler(waring_handler)'''
    app.logger.addHandler(file_handler)

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)

def register_request_handlers(app):
    @app.after_request
    def query_profiler(response):
        re=record_queries
        data=re.get_recorded_queries()
        for i in data:
            info='SQL  :'+i.statement + 'TIME  :'+str(i.duration)
            app.logger.info(info)
        return response

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)

def register_blueprints(app):
    app.register_blueprint(auth_bp,url_prefix= '/auth') #注册蓝图
    app.register_blueprint(api_v1,url_prefix='/api/v1')
    #app.register_blueprint(api_v2,url_prefix='/api/v2')
    #app.register_blueprint(api_v3,url_prefix='/api/v3')

def register_errors(app):
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return jsonify(code='A0230',msg='登录超时,请重新登录', data='超时'), 400

    @app.errorhandler(500)
    def internal_server_error(e):
        return ('errors/500.html'), 500
    
    @app.errorhandler(404)
    def internal_server_error(e):
        return jsonify(code='404',msg='The requested URL was not found on the server.', data='erro'), 404
    
    '''@app.errorhandler(Exception)
    def handle_csrf_error(e):
        app.logger.warning(e)
        return jsonify(code='201',msg='系统错误,请联系管理员', data='超时'), 400 '''

def forge():
        """Generate fake data."""
        from static.extensions import db,login_manager
        db.drop_all()
        db.create_all()






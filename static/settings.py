import os

basedir=os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    BACKEND_LOCALES=['en_US','zh_Hans_CN']
    BACKEND_ITEM_PER_PAGE=20

    SQLALCHEMY_DATABASE_URI="mssql+pymssql://sa:123456@127.0.0.1/web?charset=utf8"
    #SQLALCHEMY_DATABASE_URI="mssql+pymssql://sa:123456@172.16.3.158/sicoreWeb?charset=utf8"
    #SQLALCHEMY_BINDS={ 'sicore':'mysql://Sicore@2022:20220529@172.16.3.179/sicore',
                       #'assets':"mssql+pymssql://ITTest:it123456@172.16.2.8/Assets?charset=utf8"}
    SECRET_KEY = os.getenv('SECRET_KEY', 'a secret string')
    JSON_AS_ASCII = False

    #Mail
    #MAIL_SERVER=os.getenv('MAIL_SERVER','smtp.exmail.qq.com')
    MAIL_SERVER='smtp.exmail.qq.com'
    #MAIL_USE_SSL=True
    #MAIL_USE_SSL=True
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME='it-auto@sicoresemi.com'
    MAIL_PASSWORD='8pAgCkfJ2L3hzQWh'
    MAIL_DEFAULT_SENDER=('ITAUTO','it-auto@sicoresemi.com')
    #MAIL_USERNAME=os.getenv('MAIL_USERNAME','it-auto@sicoresemi.com')
    #MAIL_PASSWORLD=os.getenv('MAIL_PASSWORD','zeA5q7aSn8DuZ8iY')
    #MAIL_DEFAULT_SENDER=('lin yang',os.getenv('MAIL_USERNAME','jlin@sicoresemi.com'))
    #WTF LIMT TIME
    WTF_CSRF_TIME_LIMIT=None
    
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #record sql 
    #SQLALCHEMY_RECORD_QUERIES=True
    SQLALCHEMY_RECORD_QUERIES=False
    MAX_CONTENT_LENGTH= 16 * 1000 * 1000

    UPLOAD_FOLDER=os.getenv('UPLOAD_FOLDER',os.path.join(basedir,'uploads') )
    
class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    SQLALCHEMY_RECORD_QUERIES=True
    pass

class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

""" 
config={
    "DEBUG":"True",
    "SECRET_KEY":"This i key",
    "SQLALCHEMY_TRACK_MODIFICATIONS" :"True",
    "SQLALCHEMY_DATABASE_URI":"mssql+pymssql://ITTest:it123456@172.16.2.8/sicoreWeb?charset=utf8",
    "JSON_AS_ASCII" : "False"
  } """
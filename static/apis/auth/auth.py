from flask import g,current_app,request
from functools import wraps

from itsdangerous import  BadSignature, SignatureExpired
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from static.models import User
 
from  static.apis.auth.errors import api_abort, invalid_token, token_missing

#创建token
def generate_token(user):
    expiration=3600
    s=Serializer(current_app.config['SECRET_KEY'])
    #验证修改为字典传输
    data={'id':user.userid}
    token=s.dumps(data)
    #token=s.dumps({'id':user.Userid}).decode('ascii')
    return(token,expiration)

#验证
def validate_token(token):
    s=Serializer(current_app.config['SECRET_KEY'])
    try:
        data=s.loads(token)
    except (BadSignature,SignatureExpired):
        return False
    user=User.query.get(data['id'])
    if user is None:
        return False
    g.current_user =user #将用户对象储存到G上
    return True

#get token
def get_token():
    if 'Authorization' in request.headers:
        try:
            token=request.headers.get('Authorization')
        except ValueError:
             token_type = token = None
    else:
        token=None
    return token
def auth_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token =get_token()
        if request.method != 'OPTIONS':
            #if token_type is None or token_type.lower() != 'bearer':
                #return api_abort(400, 'The token type must be bearer.')
            if token is None:
                return token_missing()
            if not validate_token(token):
                return invalid_token()
        return f(*args, **kwargs)
    return decorated
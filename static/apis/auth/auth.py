from flask import g,current_app,request
from functools import wraps
from itsdangerous import  BadSignature, SignatureExpired
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from static.models import User
from static.extensions import db
from static.apis.auth.errors import api_abort, invalid_token, token_missing



#创建token
def generate_token(user):
    expiration=3600
    s=Serializer(current_app.config['SECRET_KEY'])
    #验证修改为字典传输
    data={'id':user.id}
    token=s.dumps(data)
    #token=s.dumps({'id':user.Userid}).decode('ascii')
    return(token,expiration)

#验证
def validate_token(token):
    s=Serializer(current_app.config['SECRET_KEY'])
    try:
        data=s.loads(token,max_age=3600)
    except (BadSignature,SignatureExpired):
        return False
    user=db.session.get(User,data['id'])
    #user=User.query.get(data['id'])
    if user is None:
        return False
    g.current_user =user #将用户对象储存到G上
    return True

#get token
""" def get_token():
    if 'Authorization' in request.headers:
        try:
            token=request.headers.get('Authorization')
        except ValueError:
             token_type = token = None
    else:
        token=None
    return token """


def get_token():
    # Flask/Werkzeug do not recognize any authentication types
    # other than Basic or Digest, so here we parse the header by hand.
    if 'Authorization' in request.headers:
        try:
            token_type, token = request.headers['Authorization'].split(None, 1)
        except ValueError:
            # The Authorization header is either empty or has no token
            token_type = token = None
    else:
        token_type = token = None

    return token_type, token

""" def auth_required(f):
    
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

 """
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_type, token = get_token()

        # Flask normally handles OPTIONS requests on its own, but in the
        # case it is configured to forward those to the application, we
        # need to ignore authentication headers and let the request through
        # to avoid unwanted interactions with CORS.
        if request.method != 'OPTIONS':
            if token_type is None or token_type.lower() != 'bearer':
                return api_abort(400, 'The token type must be bearer.')
            if token is None:
                return token_missing()
            if not validate_token(token):
                return invalid_token()
        return f(*args, **kwargs)

    return decorated
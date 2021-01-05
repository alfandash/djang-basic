from functools import wraps
from todoproject.jwt import JWTAuth
from todoproject.response import Response

def jwtRequired(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            
            data = decode(args[0].META['HTTP_AUTHORIZATION'])
            args[0].META['DATA'] = data
            
        except Exception as e:
            return Response.unauthorized()
        
        return fn(*args, **kwargs)
    return wrapper

def decode(token):
    token = str(token).split(' ')
    return JWTAuth().decode(token[1])
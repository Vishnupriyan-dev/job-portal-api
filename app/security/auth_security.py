import bcrypt
import jwt
import os
from datetime import datetime,timedelta,timezone
from app.exceptions.exception import NoneKeyError,AuthenticationError,NoneAlgorithm,AuthorizationError
from jwt import ExpiredSignatureError,InvalidTokenError

def hash_password(password:str):
    salt=bcrypt.gensalt()
    hashed_pw=bcrypt.hashpw(password.encode(),salt)
    return hashed_pw.decode()
def verify_password(password,hashed_password):
    return bcrypt.checkpw(password.encode(),hashed_password.encode())

def create_access_token(user_id:int,user_role:str):
    secret_key=os.getenv("SECRET_KEY")
    algo=os.getenv("ALGO")
    if not secret_key:
        raise NoneKeyError("Key is None")
    if not algo:
        raise NoneAlgorithm("Key is None")
    payload={
        "sub":str(user_id),
        "iat":datetime.now(timezone.utc),
        "exp":datetime.now(timezone.utc)+timedelta(minutes=600),
        "role":user_role
    }
    return jwt.encode(payload,secret_key,algo)

def verify_access_token(token:str):
    secret_key=os.getenv("SECRET_KEY")
    algo=os.getenv("ALGO")
    if not secret_key:
        raise NoneKeyError("Key is None")
    if not algo:
        raise NoneAlgorithm("Key is None")
    try:
        payload=jwt.decode(
            token,
            secret_key,
            algorithms=[algo]
                           )
    except ExpiredSignatureError:
        raise AuthenticationError()
    except InvalidTokenError:
        raise AuthenticationError()
    
    if "sub"not in payload or "role"not in payload:
        raise AuthenticationError()
    if not isinstance(payload["sub"], str):
        raise AuthenticationError()
    return {
        "sub":int(payload["sub"]),
        "role":payload["role"]
    }
    




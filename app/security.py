from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from .db import SessionDep,Session
from .models import User
import dotenv
import os

dotenv.load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRES_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRES_MINUTES') or 30)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")
pwd_context = CryptContext(schemes=['pbkdf2_sha256'],deprecated='auto')


def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRES_MINUTES))
    to_encode.update(
        {'exp':expire}
    )
    return jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        return None
    

def authenticate(email:str,password:str,db:SessionDep):
    #first we query the user
    user = db.query(User).filter(User.email==email).first()
    if not user:
        return False

    try:
        is_valid = pwd_context.verify(password,user.password)
    except ValueError:
        return False

    if not is_valid:
        return False
    return user   #the user is legitimate to login




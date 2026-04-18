from passlib.context import CryptContext
from jwt import encode
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
    
ALGORITHM = os.getenv('ALGORITHM')

TOKEN_EXPIRE_TIME = 15

pwd_context = CryptContext(schemes=['bcrypt'])

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)

def create_access_token(user_data: dict):
    payload = user_data.copy()
    
    exp = datetime.now(timezone.utc) + timedelta(minutes = TOKEN_EXPIRE_TIME)
    
    payload.update({'exp': exp.timestamp()})
    
    token = encode(payload, SECRET_KEY, algorithm = ALGORITHM)
    
    return token
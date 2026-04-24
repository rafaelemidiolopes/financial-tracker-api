from passlib.context import CryptContext
from jwt import encode, decode, ExpiredSignatureError, InvalidSignatureError, DecodeError
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from models.users import User
from fastapi import security, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db

load_dotenv()

oauth2 = security.OAuth2PasswordBearer(tokenUrl='/user')

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

def get_current_user(db: Session = Depends(get_db), token = Depends(oauth2)):
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user = db.query(User).filter_by(id = int(payload['sub'])).first()

        if not user:
            raise HTTPException(status_code=404, detail='User not found! ')
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='token has expired', headers={'WWW-Authenticate': 'Bearer'})
    
    except InvalidSignatureError:
        raise HTTPException(status_code=401, detail='invalid signature token', headers={'WWW-Authenticate': 'Bearer'})
    
    except DecodeError:
        raise HTTPException(status_code=401, detail='invalid decode error', headers={'WWW-Authenticate': 'Bearer'})
    
    return user
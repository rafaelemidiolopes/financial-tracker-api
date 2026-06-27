from pwdlib import PasswordHash
from jwt import encode
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from core.config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_TIME

oauth2 = OAuth2PasswordBearer(tokenUrl='/user')

password_hasher = PasswordHash.recommended()

def hash_password(password: str):
    return password_hasher.hash(password)

def verify_password(password: str, hashed_password: str):
    return password_hasher.verify(password, hashed_password)

def create_access_token(user_data: dict):
    payload = user_data.copy()
    
    exp = datetime.now(timezone.utc) + timedelta(minutes = TOKEN_EXPIRE_TIME)
    
    payload.update({'exp': exp.timestamp()})
    
    token = encode(payload, SECRET_KEY, algorithm = ALGORITHM)
    
    return token
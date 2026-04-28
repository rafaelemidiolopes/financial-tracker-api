from passlib.context import CryptContext
from jwt import encode
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from core.config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_TIME

load_dotenv()

oauth2 = OAuth2PasswordBearer(tokenUrl='/user')

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
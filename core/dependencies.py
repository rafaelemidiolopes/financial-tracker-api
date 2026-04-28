from database import SessionLocal
from models.users import User
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from jwt import decode, ExpiredSignatureError, InvalidSignatureError, DecodeError
from core.security import oauth2
from core.config import SECRET_KEY, ALGORITHM

def get_db():
    db = SessionLocal()
    
    try:
        yield db
        
    finally:
        db.close()
        
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
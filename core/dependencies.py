from database import SessionLocal
from models.users import User
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from jwt import decode, ExpiredSignatureError, InvalidSignatureError, DecodeError
from core.security import oauth2
from core.config import SECRET_KEY, ALGORITHM
from loguru import logger

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
            logger.warning(f'Error when getting current user. User {payload["sub"]} not found')
            
            raise HTTPException(status_code=404, detail='User not found! ')
    
    except ExpiredSignatureError:
        logger.warning(f'Token has expired')
        
        raise HTTPException(status_code=401, detail='token has expired', headers={'WWW-Authenticate': 'Bearer'})
    
    except InvalidSignatureError:
        logger.warning(f'Invalid signature error')
        
        raise HTTPException(status_code=401, detail='invalid signature token', headers={'WWW-Authenticate': 'Bearer'})
    
    except DecodeError:
        logger.warning(f'Invalid decode error')
        
        raise HTTPException(status_code=401, detail='invalid decode error', headers={'WWW-Authenticate': 'Bearer'})
    
    logger.info(f'User {user.id} authenticated successfully')
    
    return user
from sqlalchemy.orm import Session
from schemas.users import UserCreate, UserLogin, TokenResponse, UpdateUser, UpdatePassword
from models.users import User
from core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException
from loguru import logger

def create_user(user: UserCreate, db: Session):
    password_hashed = hash_password(user.password)
    
    email_exists = db.query(User).filter_by(email = user.email).first()
    
    if email_exists:
        logger.bind(email = user.email).warning(f'Creating user failed. Email already exists')
        
        raise HTTPException(status_code=409, detail='Email already exists')
    
    new_user = User(email = user.email, password_hash = password_hashed)
    
    try:
        db.add(new_user)
        
        db.commit()
        
        db.refresh(new_user)
        
    except Exception:
        db.rollback()
        
        logger.exception('Creating user failed')
        
        raise
    
    logger.bind(user_id = new_user.id).info(f'User created')
    
    return new_user

def login_user(user_data: UserLogin, db: Session):
    user = db.query(User).filter_by(email = user_data.email).first()
    
    if not user:
        logger.bind(email = user_data.email).warning(f'Login failed. Invalid credentials')
        
        raise HTTPException(status_code=401, detail='Invalid credentials') 
    
    if not verify_password(user_data.password, user.password_hash):
        logger.bind(user_id = user.id).warning(f'Login failed. Invalid credentials')
        
        raise HTTPException(status_code=401, detail='Invalid credentials! ')
    
    access_token = create_access_token({'sub': str(user.id)})
    
    logger.bind(user_id = user.id).info('Access token created')
    
    return TokenResponse(access_token=access_token, token_type='bearer')

def update_me(new_data: UpdateUser, user: User, db: Session):
    if new_data.email:
        new_email_exists = db.query(User).filter_by(email = new_data.email).first()
    
        if new_email_exists and new_email_exists.id != user.id:
            logger.bind(email = new_data.email).warning(f'Update user failed. Email already used')
            
            raise HTTPException(status_code=409, detail='Email already exists')
        
    new_data_dict = new_data.model_dump(exclude_unset=True)
    
    for key, value in new_data_dict.items():
        setattr(user, key, value)
        
    try:  
        db.commit()
        
        db.refresh(user)
        
    except Exception:
        db.rollback()
        
        logger.bind(user_id = user.id).exception(f'Update user failed')
        
        raise
    
    logger.bind(user_id = user.id).info(f'User updated')
    
    return user

def update_password(new_password: UpdatePassword, user: User, db: Session):
    user.password_hash = hash_password(new_password.password)
    
    try:
        db.commit()
        
        db.refresh(user)
        
    except Exception:
        db.rollback()
        
        logger.bind(user_id = user.id).exception(f'Update password failed')
        
        raise
    
    logger.bind(user_id = user.id).info(f'Password updated')
    
    return user
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
        logger.warning(f'Creating user failed. email {user.email} already exists')
        
        raise HTTPException(status_code=409, detail='Email already exists')
    
    new_user = User(email = user.email, password_hash = password_hashed)
    
    try:
        db.add(new_user)
        
        db.commit()
        
        db.refresh(new_user)
        
    except Exception:
        db.rollback()
        
        logger.exception('Creating user failed.')
        
        raise
    
    logger.info(f'User created. Id user: {new_user.id}')
    
    return new_user

def login_user(user_data: UserLogin, db: Session):
    user = db.query(User).filter_by(email = user_data.email).first()
    
    if not user:
        logger.warning(f'Login failed. Email {user_data.email} not found.')
        
        raise HTTPException(status_code=404, detail='Invalid credentials') 
    
    if not verify_password(user_data.password, user.password_hash):
        logger.warning(f'Login failed. Invalid credentials for user {user.id}')
        
        raise HTTPException(status_code=401, detail='Invalid credentials! ')
    
    access_token = create_access_token({'sub': str(user.id)})
    
    logger.info(f'Access token created for {user.id}')
    
    return TokenResponse(access_token=access_token, token_type='bearer')

def update_me(new_data: UpdateUser, user: User, db: Session):
    if new_data.email:
        new_email_exists = db.query(User).filter_by(email = new_data.email).first()
    
        if new_email_exists and new_email_exists.id != user.id:
            logger.warning(f'Update user failed. Email {new_data.email} already used')
            
            raise HTTPException(status_code=409, detail='Email already exists')
        
    new_data_dict = new_data.model_dump(exclude_unset=True)
    
    for key, value in new_data_dict.items():
        setattr(user, key, value)
        
    try:  
        db.commit()
        
        db.refresh(user)
        
    except Exception:
        db.rollback()
        
        logger.exception(f'Update user failed. User id: {user.id}')
        
        raise
    
    logger.info(f'User {user.id} updated')
    
    return user

def update_password(new_password: UpdatePassword, user: User, db: Session):
    user.password_hash = hash_password(new_password.password)
    
    try:
        db.commit()
        
        db.refresh(user)
        
    except Exception:
        db.rollback()
        
        logger.exception(f'Update password failed. User id: {user.id}')
        
        raise
    
    logger.info(f'Password updated by user {user.id}')
    
    return user
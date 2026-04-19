from sqlalchemy.orm import Session
from schemas.users import UserCreate, UserLogin, TokenResponse, UpdateUser, UpdatePassword
from models.users import User
from core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException

def create_user(user: UserCreate, db: Session):
    password_hashed = hash_password(user.password)
    
    new_user = User(email = user.email, password_hash = password_hashed)
    
    db.add(new_user)
    
    db.commit()
    
    db.refresh(new_user)
    
    return new_user

def login_user(user_data: UserLogin, db: Session):
    user = db.query(User).filter_by(email = user_data.email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail='User not exists! ') 
    
    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail='Invalid credentials! ')
    
    access_token = create_access_token({'sub': str(user.id)})
    
    return TokenResponse(access_token=access_token, token_type='bearer')

def update_me(new_data: UpdateUser, user: User, db: Session):
    new_data_dict = new_data.model_dump(exclude_unset=True)
    
    for key, value in new_data_dict.items():
        setattr(user, key, value)
        
    db.commit()
    
    db.refresh(user)
    
    return user

def update_password(new_password: UpdatePassword, user: User, db: Session):
    user.password_hash = hash_password(new_password.password)
    
    db.commit()
    
    db.refresh(user)
    
    return user
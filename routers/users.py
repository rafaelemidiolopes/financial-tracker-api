from fastapi import APIRouter, Depends
from schemas.users import UserCreate, UserResponse, TokenResponse, UserLogin, UpdateUser, UpdatePassword
from database import get_db
from sqlalchemy.orm import Session
from services import users
from core.security import get_current_user

router = APIRouter()

@router.post('/users', response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return users.create_user(user, db)

@router.post('/user', response_model=TokenResponse)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    return users.login_user(user_data, db)

@router.get('/me', response_model=UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return current_user

@router.patch('/me', response_model=UserResponse)
def update_me(new_data: UpdateUser, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return users.update_me(new_data, current_user, db)

@router.patch('/me/password', response_model=UserResponse)
def update_password(new_password: UpdatePassword, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return users.update_password(new_password, current_user, db)
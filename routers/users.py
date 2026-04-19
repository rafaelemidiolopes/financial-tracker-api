from fastapi import APIRouter, Depends
from schemas.users import UserCreate, UserResponse, TokenResponse, UserLogin
from database import get_db
from sqlalchemy.orm import Session
from services.users import create_user as create_user_service
from services import users
from core.security import get_current_user

router = APIRouter()

@router.post('/users', response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(user, db)

@router.post('/user', response_model=TokenResponse)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    return users.login_user(user_data, db)

@router.get('/me', response_model=UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return current_user
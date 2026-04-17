from fastapi import APIRouter, Depends
from schemas.users import UserCreate, UserResponse
from database import get_db
from sqlalchemy.orm import Session
from services.users import create_user as create_user_service

router = APIRouter()

@router.post('/users', response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(user, db)
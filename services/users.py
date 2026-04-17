from sqlalchemy.orm import Session
from schemas.users import UserCreate
from models.users import User
from core.security import hash_password

def create_user(user: UserCreate, db: Session):
    password_hashed = hash_password(user.password)
    
    new_user = User(email = user.email, password_hash = password_hashed)
    
    db.add(new_user)
    
    db.commit()
    
    db.refresh(new_user)
    
    return new_user
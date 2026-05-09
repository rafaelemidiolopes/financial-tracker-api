from services.users import create_user, login_user
from unittest.mock import MagicMock, patch
from schemas.users import UserCreate, UserLogin
from fastapi import HTTPException
import pytest
from models.users import User
from models.transactions import Transaction

def test_email_dont_exists():
    fake_db = MagicMock()
    
    fake_db.query.return_value.filter_by.return_value.first.return_value = None
    
    user = UserCreate(email = 'email@test.com', password = 'abc')
    
    result = create_user(user, fake_db)
    
    assert result is not None
    
def test_email_exists():
    fake_db = MagicMock()
    
    fake_db.query.return_value.filter_by.return_value.first.return_value = MagicMock()
    
    user = UserCreate(email = 'email@test.com', password = 'abc')
    
    with pytest.raises(HTTPException):
        create_user(user, fake_db)
        
def test_user_dont_exists():
    fake_db = MagicMock()
    
    fake_db.query.return_value.filter_by.return_value.first.return_value = None
    
    user = UserLogin(email = 'email@test.com', password = 'abc')
    
    with pytest.raises(HTTPException):
        login_user(user, fake_db)
        
@patch('services.users.verify_password')
def test_login_wrong_password(mock_password):
    fake_db = MagicMock()
    
    fake_db.query.return_value.filter_by.return_value.first.return_value = MagicMock()
    
    mock_password.return_value = False
    
    user = UserLogin(email = 'email@test.com', password = 'abc')
    
    with pytest.raises(HTTPException):
        login_user(user, fake_db)
from services.users import create_user, login_user, update_me
from unittest.mock import MagicMock, patch
from schemas.users import UserCreate, UserLogin, UpdateUser
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
        
@patch('services.users.verify_password')
def test_login_success(mock_password):
    fake_db = MagicMock()
    
    fake_db.query.return_value.filter_by.return_value.first.return_value = MagicMock()
    
    user = UserLogin(email='abc@test.com', password='123')
    
    mock_password.return_value = True 
    
    assert login_user(user, fake_db) is not None
    
def test_update_user_with_email_from_another_user():
    fake_db = MagicMock() 
    
    fake_user = MagicMock()
    
    fake_user_email = MagicMock()
    
    fake_user_email.id = 2
    
    fake_db.query.return_value.filter_by.return_value.first.return_value = fake_user_email
    
    fake_user.id = 1
    
    user_new_data = UpdateUser(email = 'abc@test.com')
    
    with pytest.raises(HTTPException):
        update_me(user_new_data, fake_user, fake_db)
           
def test_update_me_success():
    fake_db = MagicMock()
    
    fake_user = User(id = 1, email = 'old_email@test.com')
    
    fake_new_data = UpdateUser(email = 'new_email@test.com')
    
    fake_db.query.return_value.filter_by.return_value.first.return_value = None
    
    result = update_me(fake_new_data, fake_user, fake_db)
    
    assert result.email == 'new_email@test.com'  
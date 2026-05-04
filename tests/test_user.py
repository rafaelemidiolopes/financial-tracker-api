from services.users import create_user
from unittest.mock import MagicMock
from schemas.users import UserCreate
from models.users import User
from models.transactions import Transaction

def test_email_dont_exists():
    fake_db = MagicMock()
    
    fake_db.query.return_value.filter_by.return_value.first.return_value = None
    
    user = UserCreate(email = 'email@test.com', password = 'abc')
    
    result = create_user(user, fake_db)
    
    assert result is not None
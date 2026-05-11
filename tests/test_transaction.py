from unittest.mock import MagicMock
from services.transactions import create_transaction
from schemas.transactions import TransactionCreate

def test_success_create_transaction_case():
    fake_db = MagicMock()
    
    fake_user = MagicMock()
    fake_user.id = 1
    
    fake_data = TransactionCreate(type = 'income', amount = 99999, category = 'fake_category', description = 'fake description')
    
    result = create_transaction(fake_user, fake_data, fake_db)
    
    assert result.user_id == 1
    assert result.amount == 99999
    
    fake_db.add.assert_called_once()
    fake_db.commit.assert_called_once()
    fake_db.refresh.assert_called_once()
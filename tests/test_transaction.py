from unittest.mock import MagicMock
from services.transactions import create_transaction, get_transactions
from schemas.transactions import TransactionCreate, TransactionFilters

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
    
def test_get_transactions_success_case():
    fake_db = MagicMock()
    
    fake_query = MagicMock()
    
    fake_query.filter_by.return_value = fake_query
    fake_query.filter.return_value = fake_query
    fake_query.all.return_value = ['fake_transaction']
    
    fake_db.query.return_value = fake_query
    
    fake_user = MagicMock()
    fake_user.id = 1
    
    fake_filters = TransactionFilters(type = 'income', category = 'fake_category')
    
    result = get_transactions(fake_filters, fake_user, fake_db)
    
    assert result[0] == 'fake_transaction'
    
def test_get_transations_without_filters_success_case():
    fake_db = MagicMock()
    
    fake_filters = TransactionFilters()
    
    fake_user = MagicMock()
    fake_user.id = 1
    
    fake_db.query.return_value.filter_by.return_value.all.return_value = ['fake transaction']
    
    result = get_transactions(fake_filters, fake_user, fake_db)
    
    assert result[0] == 'fake transaction'
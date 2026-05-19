from fastapi.testclient import TestClient
from main import app
from tests.integration.test_user import create_user_with_fake_email, get_access_token

client = TestClient(app)

def test_create_transaction_success_case():
    email = create_user_with_fake_email()
    
    access_token = get_access_token(email, '123')
    
    response = client.post('/transaction', json = {"type": "income", "amount": 500, "category": "fake category", "description": "fake description"}, headers = {"Authorization": f'Bearer {access_token}'})
    
    assert response.status_code == 200
    assert response.json()['type'] == 'income'
    assert response.json()['amount'] == 500
    assert response.json()['category'] == 'fake category'
    assert response.json()['description'] == 'fake description'
    
def test_get_transaction_success_case():
    email = create_user_with_fake_email()
    
    access_token = get_access_token(email, '123')
    
    client.post('/transaction', json = {"type": "income", "amount": 500, "category": "fake category", "description": "fake description"}, headers = {"Authorization": f'Bearer {access_token}'})
    
    response = client.get('/transaction', params = {"type": "income"}, headers = {"Authorization": f'Bearer {access_token}'})
    
    assert response.status_code == 200
    assert response.json()[-1]['type'] == 'income'
    assert response.json()[-1]['amount'] == 500
    assert response.json()[-1]['category'] == 'fake category'
    assert response.json()[-1]['description'] == 'fake description'
    
def test_get_transactions_without_transactions_case():
    email = create_user_with_fake_email()
    
    access_token = get_access_token(email, '123')
    
    response = client.get('/transaction', headers = {"Authorization": f"Bearer {access_token}"})
    
    assert response.status_code == 200
    assert response.json() == []
    
def test_update_transaction_success_case():
    email = create_user_with_fake_email()
    
    access_token = get_access_token(email, '123')
    
    response_post_transaction = client.post('/transaction', json = {"type": "income", "amount": 500, "category": "fake category", "description": "fake description"}, headers = {"Authorization": f'Bearer {access_token}'})
    
    response_update_transaction = client.patch(f'/transaction/{response_post_transaction.json()["id"]}', json = {"amount": 999, "category": "new fake category"}, headers = {"Authorization": f"Bearer {access_token}"})
    
    assert response_update_transaction.json()["amount"] == 999
    assert response_update_transaction.json()["category"] == "new fake category"
    assert response_update_transaction.status_code == 200
    
def test_update_inexistent_transaction_case():
    email = create_user_with_fake_email()
    
    access_token = get_access_token(email, '123')
    
    response = client.patch('/transaction/999999999999', json = {"amount": 600}, headers = {"Authorization": f"Bearer {access_token}"})
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Transaction not found! "
    
def test_delete_transaction_success_case():
    email = create_user_with_fake_email()
    
    access_token = get_access_token(email, '123')
    
    response_create_transaction = client.post('/transaction', json = {"type": "income", "amount": 499, "category": "fake category"}, headers = {"Authorization": f"Bearer {access_token}"})
    
    response_delete_transaction = client.delete(f'/transaction/{response_create_transaction.json()["id"]}', headers = {"Authorization": f"Bearer {access_token}"})
    
    assert response_delete_transaction.status_code == 204
    
def test_delete_inexistent_transaction_case():
    email = create_user_with_fake_email()
    
    access_token = get_access_token(email, '123')
    
    response = client.delete('/transaction/9999999999999', headers = {"Authorization": f"Bearer {access_token}"})
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Transaction not found! "
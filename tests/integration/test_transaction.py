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
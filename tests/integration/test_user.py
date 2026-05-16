from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user_success_case():
    response = client.post('/user', json = {"email": "test_email@test.com", "password": "123"})
    
    assert response.status_code == 200
    assert response.json()["email"] == "test_email@test.com"
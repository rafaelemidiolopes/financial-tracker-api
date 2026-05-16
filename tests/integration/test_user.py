from fastapi.testclient import TestClient
from main import app
from core.dependencies import get_db
from tests.integration.test_database import override_get_db

client = TestClient(app)

app.dependency_overrides[get_db] = override_get_db

def test_create_user_success_case():
    response = client.post('/user', json = {"email": "test_email@test.com", "password": "123"})
    
    assert response.status_code == 200
    assert response.json()["email"] == "test_email@test.com"
    
def test_create_user_with_email_existing_case():
    client.post('/user', json = {"email": "email_user_test@test.com", "password": "123"})
    
    response = client.post('/user', json = {"email": "email_user_test@test.com", "password": "123"})
    
    assert response.status_code == 409
    assert response.json()["detail"] == 'Email already exists'
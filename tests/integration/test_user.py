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
    
def test_login_user_success_case():
    response = client.post('/login', json = {"email": "test_email@test.com", "password": "123"})
    
    assert response.status_code == 200
    assert response.json()['token_type'] == 'bearer'
    
def test_login_with_inexistent_email_case():
    response = client.post('/login', json = {"email": "inexistent_email@test.com", "password": "321"})
    
    assert response.status_code == 404
    assert response.json()['detail'] == 'User not exists! '
    
def test_login_with_wrong_password():
    response = client.post('/login', json = {"email": "test_email@test.com", "password": "12345"})
    
    assert response.status_code == 401
    assert response.json()['detail'] == 'Invalid credentials! '
    
def test_update_me_success_case():
    response_login = client.post('/login', json = {"email": "test_email@test.com", "password": "123"})
    
    access_token = response_login.json()["access_token"]
    
    response_update_me = client.patch('/me', json = {"email": "new_email@test.com"}, headers = {"Authorization": f'Bearer {access_token}'})
    
    assert response_update_me.status_code == 200
    assert response_update_me.json()["email"] == "new_email@test.com"
    
def test_update_me_email_already_existing_case():
    response_login = client.post('/login', json = {"email": "new_email@test.com", "password": "123"})
    
    access_token = response_login.json()["access_token"]
    
    response_update_me = client.patch('/me', json = {"email": "email_user_test@test.com"}, headers = {"Authorization": f'Bearer {access_token}'})
    
    assert response_update_me.status_code == 409
    assert response_update_me.json()['detail'] == 'Email already exists'
     
def test_update_password_success_case():
    response_login = client.post('/login', json = {"email": "new_email@test.com", "password": "123"})
    
    access_token = response_login.json()["access_token"]
    
    response_update_password = client.patch('/me/password', json = {"password": "543210"}, headers = {"Authorization": f'Bearer {access_token}'})
    
    assert response_update_password.status_code == 200
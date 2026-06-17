from fastapi.testclient import TestClient
from main import app
from core.dependencies import get_db
from tests.integration.test_database import override_get_db
from faker import Faker

faker = Faker()

client = TestClient(app)

app.dependency_overrides[get_db] = override_get_db

def test_create_user_success_case():
    fake_email = faker.email()
    
    response = client.post('/user', json = {"email": fake_email, "password": "123"})
    
    assert response.status_code == 200
    assert response.json()["email"] == fake_email
    
def test_create_user_with_email_existing_case():
    client.post('/user', json = {"email": "email_user_test@test.com", "password": "123"})
    
    response = client.post('/user', json = {"email": "email_user_test@test.com", "password": "123"})
    
    assert response.status_code == 409
    assert response.json()["detail"] == 'Email already exists'
    
def test_login_user_success_case():
    fake_email = create_user_with_fake_email()
    
    response = client.post('/login', json = {"email": fake_email, "password": "123"})
    
    assert response.status_code == 200
    assert response.json()['token_type'] == 'bearer'
    
def test_login_with_inexistent_email_case():
    response = client.post('/login', json = {"email": "inexistent_email@test.com", "password": "321"})
    
    assert response.status_code == 401
    assert response.json()['detail'] == 'Invalid credentials'
    
def test_login_with_wrong_password():
    email = create_user_with_fake_email()
    
    response = client.post('/login', json = {"email": email, "password": "12345"})
    
    assert response.status_code == 401
    assert response.json()['detail'] == 'Invalid credentials! '
    
def test_update_me_success_case():
    email = create_user_with_fake_email()
    
    access_token = get_access_token(email, "123")
    
    new_fake_email = faker.email()
    
    response = client.patch('/me', json = {"email": new_fake_email}, headers = {"Authorization": f'Bearer {access_token}'})
    
    assert response.status_code == 200
    assert response.json()["email"] == new_fake_email
    
def test_create_user_email_already_exists():   
    email = create_user_with_fake_email()
    
    access_token = get_access_token(email, "123")
    
    response = client.patch('/me', json = {"email": "email_user_test@test.com"}, headers = {"Authorization": f'Bearer {access_token}'})
    
    assert response.status_code == 409
    assert response.json()['detail'] == 'Email already exists'
     
def test_update_password_success_case():
    email = create_user_with_fake_email()
    
    access_token = get_access_token(email, "123")
    
    response = client.patch('/me/password', json = {"password": "543210"}, headers = {"Authorization": f'Bearer {access_token}'})
    
    assert response.status_code == 200

def get_access_token(email, password):
    response = client.post('/login', json = {"email": email, "password": password})
                               
    return response.json()["access_token"]

def create_user_with_fake_email():
    fake_email = faker.email()
    
    client.post('/user', json = {"email": fake_email, "password": "123"})
    
    return fake_email
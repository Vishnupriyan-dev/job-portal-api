from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)


def test_read_root_endpont():
    response=client.get("/user")
    assert response.json() == {"message":"Job Portal API Running"}

def test_user_duplicate_email():
    payload={
         "name":"kiri",
         "number":"8778216378",
         "email":"vishnupriyan@gmail.com",
         "password":"Kiri@u1"
    }
    response=client.post("user/signup",json=payload)
    assert response.status_code==409
    assert response.json()["detail"]=="EMAIL_ALREADY_EXISTS"

def test_user_signup():
    payload={
        "name":"kanimozhi",
         "number":"6345678110",
         "email":"kaniparvendhan@gmail.com",
         "password":"Kani@2000"
    }
    response=client.post("/user/signup",json=payload)
    print(response.json())
    assert response.status_code==200
    data=response.json()
    assert "access" in data
    assert "token_type" in data

    assert data["access"].count(".")==2
    

def test_duplicate_number():
    payload={
        "name":"albert",
         "number":"6345678110",
         "email":"albert@gmail.com",
         "password":"Albert@2000"
    }
    response=client.post("user/signup",json=payload)
    print(response.status_code)
    print(response.json())
    assert response.status_code==409
    assert response.json()["detail"]=="EMAIL_ALREADY_EXISTS"



def test_signup_invalid_password():
    payload = {
        "name": "test",
        "number": "9876543210",
        "email": "test@gmail.com",
        "password": "test123"
    }

    response = client.post("/user/signup", json=payload)
    assert response.status_code == 422


def test_signup_invalid_email():
    payload = {
        "name": "test",
        "number": "9876543211",
        "email": "invalid-email",
        "password": "Test@123"
    }

    response = client.post("/user/signup", json=payload)
    assert response.status_code == 422


def test_signup_missing_name():
    payload = {
        "number": "9876543212",
        "email": "test2@gmail.com",
        "password": "Test@123"
    }

    response = client.post("/user/signup", json=payload)
    assert response.status_code == 422


def test_signup_empty_payload():
    response = client.post("/user/signup", json={})
    assert response.status_code == 422


def test_login_wrong_password():
    payload = {
        "email": "vishnupriyan@gmail.com",
        "password": "Wrong@123"
    }

    response = client.post("/user/login", json=payload)
    assert response.status_code == 401


def test_login_invalid_email():
    payload = {
        "email": "notfound@gmail.com",
        "password": "Test@123"
    }

    response = client.post("/user/login", json=payload)
    assert response.status_code == 404
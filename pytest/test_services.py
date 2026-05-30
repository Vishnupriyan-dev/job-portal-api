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
    

    
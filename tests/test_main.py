
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_user_registration_success():
    res = client.post("/users", json={
        "username": "john123",
        "password": "Password1",
        "email": "john@example.com",
        "dob": "2000-01-01",
        "credit_card": "1234567812345678"
    })
    print("✅ test_user_registration_success:", res.status_code)
    assert res.status_code == 201

def test_user_underage():
    res = client.post("/users", json={
        "username": "kid123",
        "password": "Password1",
        "email": "kid@example.com",
        "dob": "2010-01-01"
    })
    print("✅ test_user_underage:", res.status_code)
    assert res.status_code == 403

def test_duplicate_user():
    client.post("/users", json={
        "username": "dupuser",
        "password": "Password1",
        "email": "dup@example.com",
        "dob": "2000-01-01"
    })
    res = client.post("/users", json={
        "username": "dupuser",
        "password": "Password1",
        "email": "dup@example.com",
        "dob": "2000-01-01"
    })
    print("✅ test_duplicate_user:", res.status_code)
    assert res.status_code == 409

def test_payment_success():
    client.post("/users", json={
        "username": "payuser",
        "password": "Password1",
        "email": "pay@example.com",
        "dob": "1990-01-01",
        "credit_card": "9999888877776666"
    })
    res = client.post("/payments", json={
        "credit_card": "9999888877776666",
        "amount": 120
    })
    print("✅ test_payment_success:", res.status_code)
    assert res.status_code == 201

def test_registration_missing_fields():
    res = client.post("/users", json={
        "username": "noemail",
        "password": "Password1",
        "dob": "2000-01-01"
    })
    print("✅ test_registration_missing_fields:", res.status_code)
    assert res.status_code == 400

def test_invalid_credit_card():
    res = client.post("/users", json={
        "username": "badcard",
        "password": "Password1",
        "email": "bad@example.com",
        "dob": "2000-01-01",
        "credit_card": "1234"
    })
    print("✅ test_invalid_credit_card:", res.status_code)
    assert res.status_code == 400

def test_get_users_with_credit_card_filter():
    client.post("/users", json={
        "username": "filteryes",
        "password": "Password1",
        "email": "yes@example.com",
        "dob": "1990-01-01",
        "credit_card": "1111222233334444"
    })
    client.post("/users", json={
        "username": "filterno",
        "password": "Password1",
        "email": "no@example.com",
        "dob": "1990-01-01"
    })

    res_yes = client.get("/users", params={"creditCard": "Yes"})
    res_no = client.get("/users", params={"creditCard": "No"})

    print("✅ test_get_users_with_credit_card_filter - Yes:", res_yes.status_code, res_yes.json())
    print("✅ test_get_users_with_credit_card_filter - No:", res_no.status_code, res_no.json())

    assert res_yes.status_code == 200
    assert all(u["credit_card"] for u in res_yes.json())

    assert res_no.status_code == 200
    assert all(not u["credit_card"] for u in res_no.json())

def test_invalid_payment():
    res = client.post("/payments", json={
        "credit_card": "0000000000000000",
        "amount": 50
    })
    print("✅ test_invalid_payment:", res.status_code)
    assert res.status_code == 404

def test_password_validation():
    res = client.post("/users", json={
        "username": "weakpass",
        "password": "weakpass",
        "email": "weak@example.com",
        "dob": "1995-01-01"
    })
    print("✅ test_password_validation:", res.status_code)
    assert res.status_code == 400
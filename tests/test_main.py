from fastapi.testclient import TestClient
from main import app
from services.data_store import user_store, payment_store

client = TestClient(app)

def clear_stores():
    user_store.clear()
    payment_store.clear()

# 1. User Registration

# Test registering a valid user
def test_user_registration_success():
    clear_stores()
    res = client.post("/users", json={
        "username": "john121",
        "password": "Password1",
        "email": "john@example.com",
        "dob": "2000-01-01",
        "credit_card": "1234567812345678"
    })
    assert res.status_code == 201

# Test registering a user under 18 years old
def test_user_underage():
    clear_stores()
    res = client.post("/users", json={
        "username": "kid123",
        "password": "Password1",
        "email": "kid@example.com",
        "dob": "2010-01-01"
    })
    assert res.status_code == 403

# Test registering a user with a duplicate username
def test_duplicate_user():
    clear_stores()
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
    assert res.status_code == 409

# 2. Payment Processing

# Test processing a payment with valid card and amount
def test_payment_success():
    clear_stores()
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
    assert res.status_code == 201

# 3. Registration validation

# Test missing required fields (email)
def test_registration_missing_fields():
    clear_stores()
    res = client.post("/users", json={
        "username": "noemail",
        "password": "Password1",
        "dob": "2000-01-01"
    })
    assert res.status_code == 400

# Test with invalid credit card
def test_invalid_credit_card():
    clear_stores()
    res = client.post("/users", json={
        "username": "badcard",
        "password": "Password1",
        "email": "bad@example.com",
        "dob": "2000-01-01",
        "credit_card": "1234"
    })
    assert res.status_code == 400

# Test with missing username
def test_registration_missing_username():
    clear_stores()
    res = client.post("/users", json={
        "password": "Password1",
        "email": "user@example.com",
        "dob": "2000-01-01"
    })
    assert res.status_code == 400

# Test with missing password
def test_registration_missing_password():
    clear_stores()
    res = client.post("/users", json={
        "username": "nopass",
        "email": "user@example.com",
        "dob": "2000-01-01"
    })
    assert res.status_code == 400

# Test with missing dob
def test_registration_missing_dob():
    clear_stores()
    res = client.post("/users", json={
        "username": "nodob",
        "password": "Password1",
        "email": "user@example.com"
    })
    assert res.status_code == 400

# Test with with invalid dob format
def test_registration_invalid_dob():
    clear_stores()
    res = client.post("/users", json={
        "username": "baddob",
        "password": "Password1",
        "email": "user@example.com",
        "dob": "2000/01/01"
    })
    assert res.status_code == 400

# 4. User Retrieval

# Test filtering users with and without credit card
def test_get_users_with_credit_card_filter():
    clear_stores()
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

    assert res_yes.status_code == 200
    assert all(u["credit_card"] for u in res_yes.json())

    assert res_no.status_code == 200
    assert all(not u["credit_card"] for u in res_no.json())

# 5. Payment edge cases

# Test payment with a credit card not registered to any user
def test_invalid_payment():
    clear_stores()
    res = client.post("/payments", json={
        "credit_card": "0000000000000000",
        "amount": 150
    })
    assert res.status_code == 404

# Test payment with invalid amount (not 3 digits)
def test_invalid_payment_amount():
    clear_stores()
    client.post("/users", json={
        "username": "amtuser",
        "password": "Password1",
        "email": "amt@example.com",
        "dob": "1990-01-01",
        "credit_card": "1111222233334444"
    })
    res = client.post("/payments", json={
        "credit_card": "1111222233334444",
        "amount": 9  
    })
    assert res.status_code == 400

# 6. Password validation

# Test registering with an invalid password (too weak)
def test_password_validation():
    clear_stores()
    res = client.post("/users", json={
        "username": "weakpass",
        "password": "weakpass",
        "email": "weak@example.com",
        "dob": "1995-01-01"
    })
    assert res.status_code == 400

# 7. Email validation

# Test registering with invalid email format
def test_invalid_email():
    clear_stores()
    res = client.post("/users", json={
        "username": "bademail",
        "password": "Password1",
        "email": "bademail",
        "dob": "1995-01-01"
    })
    assert res.status_code == 400

# 8. User Retrieval fallback

# Test creditCard query with invalid value (should return all users)
def test_get_users_credit_card_fallback():
    clear_stores()
    client.post("/users", json={
        "username": "userwithcard",
        "password": "Password1",
        "email": "userwithcard@example.com",
        "dob": "1990-01-01",
        "credit_card": "1111222233334444"
    })
    client.post("/users", json={
        "username": "usernocard",
        "password": "Password1",
        "email": "usernocard@example.com",
        "dob": "1990-01-01"
    })

    res = client.get("/users", params={"creditCard": "Maybe"})
    assert res.status_code == 200
    assert len(res.json()) == 2
# User Subscription API

A FastAPI-based RESTful API for managing user registrations and processing payments.

## Features

- User registration with input validation
- Filter users by credit card availability
- Process payments for registered users
- Custom validation error handling
- Unit tests included using pytest

## Requirements

- Python 3.10+
- FastAPI
- Uvicorn
- Pydantic v2 (with email validation support)
- pytest

## Installation

To install dependencies:

`pip install -r requirements.txt`

## Running the Application

To start the development server:

`python -m uvicorn main:app --reload`

Then open your browser at:

`http://127.0.0.1:8000/docs`

## API Endpoints

### POST `/users`

Register a new user.

Request Body Example:

```json
{
  "username": "john123",
  "password": "Password1",
  "email": "john@example.com",
  "dob": "2000-01-01",
  "credit_card": "1234567812345678"
}
```

`credit_card` is optional.

Response Codes:

- `201 Created`: User registered successfully
- `400 Bad Request`: Invalid input data
- `403 Forbidden`: User must be at least 18 years old
- `409 Conflict`: Username already exists

---

### GET `/users`

Retrieve users, optionally filtered by credit card availability.

- No filter: returns all users
- `creditCard=Yes`: users with a credit card
- `creditCard=No`: users without a credit card

---

### POST `/payments`

Process a payment for a registered user.

Request Body Example:

```json
{
  "credit_card": "1234567812345678",
  "amount": 100
}
```

Response Codes:

- `201 Created`: Payment processed successfully
- `400 Bad Request`: Invalid card or amount
- `404 Not Found`: Credit card not found

## Running Tests

Unit tests are provided using `pytest`. Run all tests using:

`python -m pytest`

Tests cover:

- User Registration
  - Successful registration
  - Underage user rejection
  - Duplicate username
  - Missing or invalid fields (username, password, email, date of birth, credit card)

- User Retrieval
  - Fetch all users
  - Filter by credit card (present or not present)
  - Fallback behavior for unknown `creditCard` filter values

- Payment Processing
  - Successful payment with valid card and amount
  - Payment with unregistered or invalid credit card
  - Invalid payment amounts (not three digits)

## Notes

- This application uses in-memory storage (no database).
- Designed for demonstration and evaluation purposes.

from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
import re

class User(BaseModel):
    username: str
    password: str
    email: EmailStr
    dob: date
    credit_card: str | None = None

    @field_validator('username')
    @classmethod
    def username_valid(cls, v):
        if not re.match("^[a-zA-Z0-9]+$", v):
            raise ValueError("Username must be alphanumeric")
        return v

    @field_validator('password')
    @classmethod
    def password_valid(cls, v):
        if len(v) < 8 or not re.search(r'[A-Z]', v) or not re.search(r'[0-9]', v):
            raise ValueError("Password must be at least 8 chars, one uppercase, one number")
        return v

    @field_validator('credit_card')
    @classmethod
    def credit_card_valid(cls, v):
        if v in (None, ""):
            return None
        if not re.fullmatch(r'\d{16}', v):
            raise ValueError("Credit Card must be 16 digits")
        return v
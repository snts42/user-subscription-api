from models import User
from datetime import datetime
from fastapi import HTTPException
import re

user_store = []
payment_store = []

def register_user(user: User):
    if any(u['username'] == user.username for u in user_store):
        raise HTTPException(status_code=409, detail="Username already taken")
    
    age = (datetime.now().date() - user.dob).days // 365
    if age < 18:
        raise HTTPException(status_code=403, detail="User must be 18+")
    
    user_store.append(user.model_dump()) 
    return user

def get_users(credit_card_filter=None):
    if credit_card_filter == "Yes":
        return [u for u in user_store if u['credit_card']]
    elif credit_card_filter == "No":
        return [u for u in user_store if not u['credit_card']]
    return user_store

def process_payment(card_number: str, amount: int):
    if not re.fullmatch(r'\d{16}', card_number) or not (0 < amount < 1000):
        raise HTTPException(status_code=400, detail="Invalid payment data")
    
    if not any(u['credit_card'] == card_number for u in user_store):
        raise HTTPException(status_code=404, detail="Credit card not found")
    
    payment_store.append({"card_number": card_number, "amount": amount})
    return {"status": "success"}
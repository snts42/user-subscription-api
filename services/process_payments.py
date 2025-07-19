from services.data_store import user_store, payment_store
from fastapi import HTTPException
import re

def process_payment(card_number: str, amount: int):
    if not re.fullmatch(r'\d{16}', card_number):
        raise HTTPException(status_code=400, detail="Invalid credit card")
    
    if not (isinstance(amount, int) and 100 <= amount <= 999):
        raise HTTPException(status_code=400, detail="Amount must be a 3-digit number")
    
    if not any(u['credit_card'] == card_number for u in user_store):
        raise HTTPException(status_code=404, detail="Credit card not found")
    
    payment_store.append({"card_number": card_number, "amount": amount})
    return {"status": "success"}
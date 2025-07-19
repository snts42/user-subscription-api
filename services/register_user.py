from models.user import User
from datetime import datetime
from fastapi import HTTPException
from services.data_store import user_store

def register_user(user: User):
    if any(u['username'] == user.username for u in user_store):
        raise HTTPException(status_code=409, detail="Username already taken")
    
    age = (datetime.now().date() - user.dob).days // 365
    if age < 18:
        raise HTTPException(status_code=403, detail="User must be 18+")
    
    user_store.append(user.model_dump())
    return user
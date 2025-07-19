from fastapi import APIRouter, Query
from services import register_user, get_users, process_payment
from models import User
from pydantic import BaseModel

user_router = APIRouter()
payment_router = APIRouter()

@user_router.post("", status_code=201)
def create_user(user: User):
    return register_user(user)

@user_router.get("")
def read_users(creditCard: str = Query(default=None)):
    return get_users(creditCard)

class PaymentRequest(BaseModel):
    credit_card: str
    amount: int

@payment_router.post("", status_code=201)
def make_payment(payment: PaymentRequest):
    return process_payment(payment.credit_card, payment.amount)
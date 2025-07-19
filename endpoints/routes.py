from fastapi import APIRouter, Query
from models.user import User
from services.register_user import register_user
from services.get_users import get_users
from services.process_payments import process_payment
from pydantic import BaseModel

user_router = APIRouter()
payment_router = APIRouter()

@user_router.post("", status_code=201)
def create_user(user: User):
    return register_user(user)

@user_router.get("")
def read_users(creditCard: str = Query(default=None, alias="creditCard")):
    return get_users(creditCard)

class PaymentRequest(BaseModel):
    credit_card: str
    amount: int

@payment_router.post("", status_code=201)
def make_payment(payment: PaymentRequest):
    return process_payment(payment.credit_card, payment.amount)
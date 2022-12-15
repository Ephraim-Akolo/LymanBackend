from pydantic import BaseModel
from datetime import date
# from typing import Optional


class Authenticate(BaseModel):
    email: str
    password: str


class Customer(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    confirm_password: str


class Artistan(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    email: str
    qualification: str
    password: str
    confirm_password: str

class Orders(BaseModel):
    customer_id: int
    product_quantity_ids: dict[int, int]
    
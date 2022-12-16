from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class Authenticate(BaseModel):
    email: EmailStr
    password: str


class Customer(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    confirm_password: str


class Artistan(Customer):
    birth_date: date
    qualification: str


class Orders(BaseModel):
    product_quantity_ids: dict[int, int]


class CustomerResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    class Config:
        orm_mode = True


class ArtistanResponse(CustomerResponse):
    birth_date: date
    qualification: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    type: Optional[str] = None
    
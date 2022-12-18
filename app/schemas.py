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


class ProductsResponse(BaseModel):
    id:int
    name:str
    price:float
    image:str
    category:str
    discription:str
    instock:bool
    class Config:
        orm_mode = True


class PurchaseResponse(BaseModel):
    order_id:int
    created_at:date
    artistan_id:Optional[int] = None
    rating:Optional[int] = None
    class Config:
        orm_mode = True


class OrderResponse(BaseModel):
    order_id:int
    product:ProductsResponse
    quantity:int
    shipped:bool
    delivered:bool
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    type: Optional[str] = None
    
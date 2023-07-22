from pydantic import BaseModel
from typing import List
class CreateUser(BaseModel):
    username: str 
    email: str 
    password: str 
    full_name: str

class LoginUser(BaseModel):
    username: str 
    password: str

class ProfileResponse(BaseModel):
    username: str 
    email: str
    full_name: str

class CreateFlower(BaseModel):
    name: str 
    count: int 
    cost: int

class GetFlowerResponse(BaseModel):
    name: str
    count: int 
    cost: int

class UpdateFlower(BaseModel):
    name: str 
    count: int
    cost: int

class CartResponse(BaseModel):
    name: str 
    count: int
    cost: int


class ListCartResponse(BaseModel):
    carts: List[CartResponse]

class PurchaseResponse(BaseModel):
    name: str 
    sum: int
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserLogin(BaseModel):
    email:str
    password:str

class UserRegister(UserLogin):
    name:Optional[str]| None = None
    phone:Optional[str]| None = None

class UserOut(BaseModel):
    id:str
    email:str
    name:Optional[str]| None = None
    role:Optional[str]| None = None

class Product(BaseModel):
    name: str
    description:Optional[str]| None = None
    price:float
    quantity:int
    category:str

class ProductIn(Product):
    image:Optional[bytes]| None = None

class ProductOut(Product):
    id:str
    imageUrl:str
    reviews:Optional[list] | []
    orderItems:Optional[list] | []
    cartItems:Optional[list] | []
    createdAt:datetime
    updatedAt:datetime
    availableQuantity:int

class CreateOrderRequest(BaseModel):
    userId: str
    productId: str
    quantity: int
    totalPrice: float
    addressId:Optional[str]| None = None

class PaymentResponse(BaseModel):
    success: bool
    message: str
    order_id: str = None
from pydantic import BaseModel
from typing_extensions import Optional


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
    categoryId:str
    image:Optional[bytes]| None = None
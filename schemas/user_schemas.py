from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    pin: int = 1234 
    is_admin: Optional[bool] = False  

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    pin: Optional[int] = None
    is_admin: Optional[bool] = None

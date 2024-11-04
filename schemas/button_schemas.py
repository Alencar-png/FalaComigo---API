from pydantic import BaseModel
from typing import Optional

class ButtonCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ButtonUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ButtonResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    image_path: str
    user_id: int

    class Config:
        orm_mode = True

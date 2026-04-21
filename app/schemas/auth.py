from typing import Literal
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str
    email: str
    password: str = Field(..., min_length=6)
    role: Literal["user", "admin"] # Role must be user or admin

class UserLogin(BaseModel):
    email: str
    password: str
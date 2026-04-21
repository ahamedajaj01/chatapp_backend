from typing import Literal
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str
    email: str
    password: str = Field(..., min_length=6)
    role: Literal["user", "admin"] = "user" # Defaults to user if not provided

class UserLogin(BaseModel):
    email: str
    password: str
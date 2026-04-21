from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    room_id: int

class MessageOut(MessageBase):
    id: int
    timestamp: datetime
    user_id: int
    username: str
    room_id: int

    class Config:
        from_attributes = True

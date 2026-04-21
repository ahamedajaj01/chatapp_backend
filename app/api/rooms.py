from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.api import deps
from app.models.room import Room
from app.services.chat_service import get_messages
from app.schemas.room import RoomCreate, RoomOut
from app.schemas.message import MessageOut

# Router for room management
router = APIRouter(prefix="/rooms", tags=["rooms"])

# Create a new chat room
@router.post("/", response_model=RoomOut)
def create_room(
    room_data: RoomCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(deps.get_current_user)
):
    db_room = Room(name=room_data.name, description=room_data.description)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

# Get message history for a room with cursor pagination
@router.get("/{room_id}/messages", response_model=List[MessageOut])
def read_messages(
    room_id: int,
    limit: int = Query(50, ge=1, le=100),
    cursor: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(deps.get_current_user)
):
    # Check if the room actually exists
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
        
    # Fetch messages using the cursor service
    messages = get_messages(db, room_id, limit, cursor)
    
    # Map messages to our output schema
    return [
        {
            "id": m.id,
            "content": m.content,
            "timestamp": m.timestamp,
            "user_id": m.user_id,
            "username": m.user.username,
            "room_id": m.room_id
        } for m in messages
    ]

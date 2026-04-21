from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.message import Message

# Save a message to the database
def save_message(db: Session, content: str, user_id: int, room_id: int):
    new_message = Message(content=content, user_id=user_id, room_id=room_id)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

# Fetch messages for a specific room using cursor-based pagination
def get_messages(db: Session, room_id: int, limit: int = 50, cursor: int = None):
    # Base query for messages in this room
    query = db.query(Message).filter(Message.room_id == room_id)
    
    # If a cursor is provided, only get messages older than the cursor id
    if cursor:
        query = query.filter(Message.id < cursor)
    
    # Sort by id descending newest first and limit results
    messages = query.order_by(desc(Message.id)).limit(limit).all()
    
    # Reverse the list to get chronological order for the client
    return messages[::-1]

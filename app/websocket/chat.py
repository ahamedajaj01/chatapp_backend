from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from jose import jwt, JWTError # For decoding JWT tokens

from app.db.session import get_db
from app.core.config import SECRET_KEY, ALGORITHM
from app.websocket.manager import manager
from app.services.chat_service import save_message, get_messages
from app.models.user import User

router = APIRouter()

# check token and return user if valid
async def get_token_user(db: Session, token: str):
    try:
        # decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            return None
        # get user from db
        user = db.query(User).filter(User.id == user_id).first()
        return user
    except JWTError:
        return None

# websocket endpoint for chat
@router.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    room_id: int, 
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    # check if user is valid
    user = await get_token_user(db, token)
    if not user:
        await websocket.close(code=4003)
        return

    # check if room exists
    from app.models.room import Room
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        await websocket.close(code=4004)
        return

    # just print for debug
    print(f"User {user.username} (ID: {user.id}) joining room {room_id}")

    # connect user to room
    await manager.connect(websocket, room_id)
    
    # send last messages when user joins
    initial_messages = get_messages(db, room_id, limit=50)
    for msg in initial_messages:
        await websocket.send_json({
            "id": msg.id,
            "content": msg.content,
            "username": msg.user.username,
            "timestamp": msg.timestamp.isoformat()
        })

    try:
        while True:
            # wait for message from client
            data = await websocket.receive_text()
            
            # save message in db
            db_msg = save_message(db, content=data, user_id=user.id, room_id=room_id)
            
            # send message to everyone in room
            await manager.broadcast({
                "id": db_msg.id,
                "content": db_msg.content,
                "username": user.username,
                "timestamp": db_msg.timestamp.isoformat()
            }, room_id)
            
    except WebSocketDisconnect:
        # remove user when disconnected
        manager.disconnect(websocket, room_id)
        print(f"User {user.username} left room {room_id}")
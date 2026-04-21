from fastapi import FastAPI, Depends
from app.db.session import engine
from app.db.base import Base
from app.api import auth, deps, rooms
from app.websocket import chat

# This creates all tables in the database automatically
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI(title="Chat Application")

# Include all the different routes
app.include_router(auth.router)
app.include_router(rooms.router)
app.include_router(chat.router)

# Simple health check endpoint
@app.get("/")
def read_root():
    return {"message": "Chat Application Backend is running"}

# A route only admins can see, to test RBAC
@app.get("/admin/protected", dependencies=[Depends(deps.require_role("admin"))])
def admin_only():
    return {"message": "Welcome, admin! You have access to this protected route."}
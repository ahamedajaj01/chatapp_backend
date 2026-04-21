from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin
from app.services.auth_service import create_user, authenticate_user, login_user

# Create router for auth endpoints
router = APIRouter(prefix="/auth", tags=["auth"])

# Endpoint to register a new user
@router.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        # Save user to DB using the auth service
        user = create_user(
            db,
            user_data.username,
            user_data.email,
            user_data.password,
            user_data.role
        )
        return {"id": user.id, "username": user.username, "email": user.email, "role": user.role, "message": "User created successfully"}

    except IntegrityError:
        # Rollback if email or username already exists
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="User with this email or username already exists"
        )

# Endpoint to log in and get a token
@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # Check if credentials are correct
    user = authenticate_user(db, user_data.email, user_data.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate and return a JWT token
    token = login_user(user)
    
    return {"access_token": token}
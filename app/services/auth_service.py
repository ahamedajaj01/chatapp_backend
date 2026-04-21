from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

# Function to create a new user record
def create_user(db: Session, username, email, password, role):
    # hash the password before saving
    hashed_pw = hash_password(password)
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_pw,
        role=role
    )
    db.add(user)
    db.commit() # Save the new user to the database
    db.refresh(user)
    return user

# Function to check if email and password match
def authenticate_user(db: Session, email, password):
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        return None
    
    # Compare plain password with stored hash
    if not verify_password(password, user.hashed_password):
        return None
    
    return user

# Generate a JWT token for the user session
def login_user(user):
    # We include user ID and role in the token payload
    token = create_access_token({
        "user_id": user.id,
        "role": user.role
    })
    return token
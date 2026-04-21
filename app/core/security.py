from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# Set up bcrypt for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Use this to hash plain passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Check if a plain password matches a hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Create a JWT token with an expiry time
def create_access_token(data: dict):
    to_encode = data.copy()
    # Token expires after the set amount of minutes
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Sign the token using our secret key and algorithm (HS256)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship # For defining relationships between tables
from app.db.base_class import Base

# DB Model for users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False) # Store hashed passwords
    role = Column(String, nullable=False)  # Role can be 'user' or 'admin'

    # Link to all messages sent by this user
    messages = relationship("Message", back_populates="user") 
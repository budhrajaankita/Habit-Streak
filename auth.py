from datetime import datetime, timedelta
import os
import hashlib
import secrets
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from typing import Optional
from database import Base, engine, get_db

# Define the User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    salt = Column(String)
    created_date = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)
    session_token = Column(String, nullable=True)
    token_expiry = Column(DateTime, nullable=True)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def hash_password(password: str, salt: str = None) -> tuple:
    """Hash a password with a salt for secure storage"""
    if not salt:
        salt = secrets.token_hex(16)
    
    # Create a hash with the password and salt
    password_hash = hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
    return password_hash, salt

def verify_password(plain_password: str, hashed_password: str, salt: str) -> bool:
    """Verify a password against a hash"""
    calculated_hash, _ = hash_password(plain_password, salt)
    return calculated_hash == hashed_password

def create_user(db: Session, username: str, email: str, password: str) -> Optional[User]:
    """Create a new user in the database"""
    # Check if user already exists
    user_exists = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()
    
    if user_exists:
        return None
    
    # Hash the password
    hashed_password, salt = hash_password(password)
    
    # Create new user
    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        salt=salt
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Authenticate a user with username and password"""
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password, user.salt):
        return None
    
    return user

def create_session_token(db: Session, user: User) -> str:
    """Create a session token for authenticated user"""
    # Generate a random token
    token = secrets.token_hex(32)
    
    # Set token expiry (24 hours)
    expiry = datetime.now() + timedelta(hours=24)
    
    # Update user record
    user.session_token = token
    user.token_expiry = expiry
    db.commit()
    
    return token

def validate_session(db: Session, token: str) -> Optional[User]:
    """Validate a session token and return the user if valid"""
    user = db.query(User).filter(User.session_token == token).first()
    
    if not user:
        return None
    
    # Check if token has expired
    if user.token_expiry < datetime.now():
        # Clear expired token
        user.session_token = None
        user.token_expiry = None
        db.commit()
        return None
    
    return user

def logout_user(db: Session, user: User) -> None:
    """Log out a user by clearing their session token"""
    user.session_token = None
    user.token_expiry = None
    db.commit()